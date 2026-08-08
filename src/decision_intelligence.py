"""Read-only decision intelligence for retail cases.

This module turns case facts and deterministic simulation outputs into a
business-facing forecast, option comparison, channel supply plan, and agent
collaboration trace. It never creates or executes production actions.
"""

from __future__ import annotations

from typing import Any, Dict, List

from src.simulators.promotion_validator import PromotionScenario, PromotionValidator


def _forecast_curve(total: int, horizon: int = 7) -> List[Dict[str, int]]:
    weights = [1.00, 1.04, 1.08, 1.10, 1.06, 1.02, 0.98][:horizon]
    raw = [total * weight / sum(weights) for weight in weights]
    values = [round(value) for value in raw]
    values[-1] += total - sum(values)
    return [
        {
            "day": index + 1,
            "p50": value,
            "p10": max(0, round(value * 0.82)),
            "p90": round(value * 1.18),
        }
        for index, value in enumerate(values)
    ]


def _scenario(
    key: str,
    name: str,
    discount_pct: int,
    transfer_qty: int,
    validation: Dict[str, Any],
    atp: int,
    status: str,
    reason: str,
) -> Dict[str, Any]:
    predicted = int(validation["predicted_units"])
    return {
        "key": key,
        "name": name,
        "discount_pct": discount_pct,
        "transfer_qty": transfer_qty,
        "predicted_units": predicted,
        "predicted_lift_pct": validation["predicted_lift_pct"],
        "promo_price_cny": validation["promo_price"],
        "incremental_profit_cny": validation["incremental_profit"],
        "promo_investment_cny": validation["promo_investment"],
        "profit_roi": validation["profit_roi"],
        "ending_atp": max(0, atp - predicted - transfer_qty),
        "status": status,
        "reason": reason,
        "risk_flags": validation["risk_flags"],
    }


def _agent_trace(case: Dict[str, Any]) -> List[Dict[str, Any]]:
    stages = {
        "Inventory Agent": "forecast_and_supply",
        "Pricing Agent": "promotion_simulation",
        "Customer Understanding Agent": "audience_eligibility",
        "Personalization Agent": "next_best_action",
        "Marketing Agent": "channel_orchestration",
    }
    return [
        {
            "agent": decision["agent"],
            "stage": stages.get(decision["agent"], "domain_assessment"),
            "role": decision["role"],
            "status": decision["status"],
            "output": decision["recommendation"],
            "confidence": decision["confidence"],
            "evidence_refs": decision["evidence_refs"],
        }
        for decision in case["agent_decisions"]
    ]


def _overstock_intelligence(case: Dict[str, Any]) -> Dict[str, Any]:
    inv = case["inventory"]
    variant = case["variant"]
    baseline_units = round(inv["demand_units_per_day"] * 7)
    validator = PromotionValidator()

    validations = {}
    for discount in (0, 10, 15, 20, 30):
        validations[discount] = validator.validate(
            PromotionScenario(
                sku_id=variant["variant_id"],
                product_name=variant["product_name"],
                category=variant["category"],
                current_price=variant["current_price_cny"],
                unit_cost=variant["unit_cost_cny"],
                discount_pct=discount,
                baseline_units=baseline_units,
                stock_risk="medium",
            )
        )

    scenarios = [
        _scenario(
            "no_action",
            "Take no action",
            0,
            0,
            validations[0],
            inv["sellable_atp"],
            "NOT_RECOMMENDED",
            "Aging stock and backroom pressure remain unresolved.",
        ),
        _scenario(
            "transfer_only",
            "Transfer only",
            0,
            320,
            validations[0],
            inv["sellable_atp"],
            "SAFE_ALTERNATIVE",
            "Relieves store capacity but leaves demand generation unchanged.",
        ),
        _scenario(
            "transfer_member_15",
            "Transfer + 15% member offer",
            15,
            320,
            validations[15],
            inv["sellable_atp"],
            "RECOMMENDED",
            "Balances sell-through, contribution profit, consent, and available supply.",
        ),
        _scenario(
            "broad_markdown_30",
            "30% broad markdown",
            30,
            0,
            validations[30],
            inv["sellable_atp"],
            "POLICY_BLOCKED",
            "The approved margin policy blocks a chain-wide deep markdown.",
        ),
    ]
    recommended = next(item for item in scenarios if item["status"] == "RECOMMENDED")
    confidence = min(item["confidence"] for item in case["agent_decisions"] if item["status"] not in {"SKIPPED", "NOT_INVOKED"})

    return {
        "case_id": case["case_id"],
        "mode": "READ_ONLY_DECISION_SUPPORT",
        "data_boundary": "Scenario forecast based on the current Case snapshot and apparel-mapped demo promotion history; not observed sales.",
        "generated_from_as_of": case["as_of_time"],
        "brief": {
            "headline": "A targeted member offer plus outlet transfer is the best balanced option.",
            "summary": "AI compared five discount bands, supply feasibility, member eligibility, and margin policy before recommending a 15% member offer with a 320-unit transfer.",
            "recommended_scenario": recommended["key"],
            "confidence": round(confidence, 2),
            "horizon_days": 7,
            "baseline_units": baseline_units,
            "recommended_units": recommended["predicted_units"],
            "recommended_incremental_profit_cny": recommended["incremental_profit_cny"],
            "blocked_action": "30% chain-wide markdown",
        },
        "forecast": {
            "baseline": _forecast_curve(baseline_units),
            "recommended": _forecast_curve(recommended["predicted_units"]),
            "method": "Econometric comparable-promotion validation + current POS rate of sale",
            "confidence": round(confidence, 2),
        },
        "scenarios": scenarios,
        "discount_sensitivity": [
            {
                "discount_pct": discount,
                "predicted_units": validations[discount]["predicted_units"],
                "predicted_lift_pct": validations[discount]["predicted_lift_pct"],
                "incremental_profit_cny": validations[discount]["incremental_profit"],
                "profit_roi": validations[discount]["profit_roi"],
                "decision": (
                    "RECOMMENDED"
                    if discount == 15
                    else "POLICY_BLOCKED"
                    if discount == 30
                    else "COMPARED"
                ),
            }
            for discount in (0, 10, 15, 20, 30)
        ],
        "channel_supply_plan": [
            {
                "channel": "Store POS",
                "purpose": "Base store demand",
                "forecast_units": 360,
                "supply_cap": 360,
                "status": "COVERED",
            },
            {
                "channel": "WeChat member offer",
                "purpose": "Consented high-intent audience",
                "forecast_units": 160,
                "supply_cap": 160,
                "status": "DRAFT_UNTIL_APPROVED",
            },
            {
                "channel": "Outlet store network",
                "purpose": "Inventory rebalance",
                "forecast_units": 320,
                "supply_cap": 320,
                "status": "TRANSFER_PENDING_APPROVAL",
            },
            {
                "channel": "Tmall / JD broad campaign",
                "purpose": "Mass-market activation",
                "forecast_units": 0,
                "supply_cap": 0,
                "status": "NOT_ACTIVATED",
            },
        ],
        "agent_trace": _agent_trace(case),
        "guardrails": [
            {"name": "Inventory availability", "status": "PASS", "detail": "Recommended demand and transfer fit within sellable ATP."},
            {"name": "Member consent", "status": "PASS_WITH_FILTER", "detail": "Only consented members with recent category intent are eligible."},
            {"name": "Margin policy", "status": "BLOCK", "detail": "The 30% chain-wide markdown remains blocked."},
            {"name": "Production write", "status": "WAITING_FOR_APPROVAL", "detail": "The simulation cannot write WMS, CRM, or pricing systems."},
        ],
        "learning_plan": {
            "measurement": "Test/control member cohort",
            "checkpoints": ["24-hour audience response", "7-day sell-through", "14-day incremental profit"],
            "success_metrics": ["incremental units", "incremental profit", "stockout rate", "voucher redemption"],
        },
    }


def _stockout_intelligence(case: Dict[str, Any]) -> Dict[str, Any]:
    inv = case["inventory"]
    baseline_units = round(inv["demand_units_per_day"] * 7)
    transfer_qty = sum(action.get("quantity") or 0 for action in case["actions"] if "TRANSFER" in action["action_type"])
    replenish_qty = sum(action.get("quantity") or 0 for action in case["actions"] if "REPLENISH" in action["action_type"])
    count_required = any("CYCLE_COUNT" in action["action_type"] for action in case["actions"])
    future_supply = inv["sellable_atp"] + transfer_qty + replenish_qty
    confidence = max((item["confidence"] for item in case["agent_decisions"] if item["agent"] == "Inventory Agent"), default=inv["inventory_confidence"])
    recommended_scenario = "verify_inventory" if count_required and transfer_qty == 0 and replenish_qty == 0 else "restore_supply"
    recommended_summary = (
        f"Inventory confidence is {round(inv['inventory_confidence'] * 100)}%, so the store must complete a physical count before transfer, replenishment, or campaign decisions."
        if recommended_scenario == "verify_inventory"
        else f"AI expects about {baseline_units} units of seven-day demand versus {inv['sellable_atp']} sellable units now, and recommends transfer/replenishment before any campaign."
    )
    return {
        "case_id": case["case_id"],
        "mode": "READ_ONLY_DECISION_SUPPORT",
        "data_boundary": "Demand range is a scenario forecast from the current Case snapshot; it is not observed future sales.",
        "generated_from_as_of": case["as_of_time"],
        "brief": {
            "headline": "Protect availability; do not promote a constrained SKU.",
            "summary": recommended_summary,
            "recommended_scenario": recommended_scenario,
            "confidence": round(confidence, 2),
            "horizon_days": 7,
            "baseline_units": baseline_units,
            "recommended_units": baseline_units,
            "recommended_incremental_profit_cny": None,
            "blocked_action": "Broad promotion while stock is constrained",
        },
        "forecast": {
            "baseline": _forecast_curve(baseline_units),
            "recommended": _forecast_curve(baseline_units),
            "method": "Current POS rate of sale + inventory availability check",
            "confidence": round(confidence, 2),
        },
        "scenarios": [
            {"key": "no_action", "name": "Take no action", "discount_pct": 0, "transfer_qty": 0, "predicted_units": baseline_units, "ending_atp": max(0, inv["sellable_atp"] - baseline_units), "status": "HIGH_STOCKOUT_RISK", "reason": "Current ATP cannot cover forecast demand."},
            *(
                [{"key": "verify_inventory", "name": "Verify physical stock", "discount_pct": 0, "transfer_qty": 0, "predicted_units": baseline_units, "ending_atp": max(0, inv["sellable_atp"] - baseline_units), "status": "RECOMMENDED", "reason": "Inventory variance must be resolved before supply or promotion decisions."}]
                if recommended_scenario == "verify_inventory"
                else [{"key": "restore_supply", "name": "Transfer + replenish", "discount_pct": 0, "transfer_qty": transfer_qty + replenish_qty, "predicted_units": baseline_units, "ending_atp": max(0, future_supply - baseline_units), "status": "RECOMMENDED", "reason": "Restores availability without creating avoidable promotional demand."}]
            ),
        ],
        "discount_sensitivity": [],
        "channel_supply_plan": [
            {"channel": "Store sellable stock", "purpose": "Current store availability", "forecast_units": baseline_units, "supply_cap": inv["sellable_atp"], "status": "SUPPLY_GAP"},
            *(
                [{"channel": "Store cycle count", "purpose": "Verify physical stock before supply decision", "forecast_units": 0, "supply_cap": inv["physical_on_hand"], "status": "STORE_COUNT_REQUIRED"}]
                if count_required and transfer_qty == 0 and replenish_qty == 0
                else []
            ),
            *(
                [{"channel": "Inter-store transfer", "purpose": "Approved transfer quantity", "forecast_units": transfer_qty, "supply_cap": transfer_qty, "status": "TRANSFER_PENDING_APPROVAL"}]
                if transfer_qty > 0
                else []
            ),
            *(
                [{"channel": "DC replenishment", "purpose": "Approved replenishment quantity", "forecast_units": replenish_qty, "supply_cap": replenish_qty, "status": "REPLENISHMENT_PENDING_APPROVAL"}]
                if replenish_qty > 0
                else []
            ),
        ],
        "agent_trace": _agent_trace(case),
        "guardrails": [
            {"name": "Inventory availability", "status": "BLOCK", "detail": "Promotion remains disabled until supply is restored."},
            {"name": "Production write", "status": "WAITING_FOR_APPROVAL", "detail": "Transfer and replenishment require the authorized role."},
        ],
        "learning_plan": {"measurement": "Forecast versus fulfilled demand", "checkpoints": ["24-hour ATP", "7-day fill rate"], "success_metrics": ["in-stock rate", "lost sales avoided", "forecast error"]},
    }


def build_decision_intelligence(case: Dict[str, Any]) -> Dict[str, Any]:
    if case["case_type"] == "SEASONAL_OVERSTOCK":
        return _overstock_intelligence(case)
    return _stockout_intelligence(case)
