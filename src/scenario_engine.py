"""Scenario engine for the AMA Retail Agent demo.

This module intentionally uses a single Retail State object so the demo is
business-credible: each agent consumes prior outputs instead of running as an
isolated hard-coded function.
"""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from src.simulators.promotion_validator import PromotionScenario, PromotionValidator


FIXTURE_PATH = Path(__file__).resolve().parent.parent / "data" / "fixtures" / "cold_snap.json"
SUPPORTED_SEASONS = ["spring", "summer", "autumn", "winter"]


@dataclass
class AgentDecision:
    agent: str
    method_sources: List[str]
    input_summary: Dict[str, Any]
    decision: Dict[str, Any]
    evidence: List[str]
    confidence: float
    human_approval_required: bool = False
    business_impact: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "agent": self.agent,
            "method_sources": self.method_sources,
            "input_summary": self.input_summary,
            "decision": self.decision,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "human_approval_required": self.human_approval_required,
            "business_impact": self.business_impact,
        }


class RetailScenarioEngine:
    """Scenario-driven multi-agent decision loop."""

    def __init__(self, fixture_path: Path = FIXTURE_PATH):
        self.fixture_path = fixture_path

    def load_state(self) -> Dict[str, Any]:
        with open(self.fixture_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run_cold_snap(self) -> Dict[str, Any]:
        return self.run_season("winter")

    def run_season(self, season: str) -> Dict[str, Any]:
        """Run a business-decision scenario for one seasonal operating cycle."""
        normalized = season.lower()
        if normalized not in SUPPORTED_SEASONS:
            normalized = "winter"
        state = self._seasonal_state(normalized)
        return self._run_state(state)

    def run_custom_launch(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Run a user-provided SKU launch scenario.

        This keeps the same agent loop but lets a business user enter SKU,
        stock, cost, CTR and launch assumptions from the UI.
        """
        season = str(payload.get("season") or "summer").lower()
        if season not in SUPPORTED_SEASONS:
            season = "summer"
        state = self._seasonal_state(season)
        sku_id = str(payload.get("sku_id") or "CUSTOM-SKU-001")
        name = str(payload.get("name") or "Custom AI Launch Product")
        category = str(payload.get("category") or "contoso_air")
        price = int(float(payload.get("current_price") or 129))
        cost = int(float(payload.get("cost") or max(1, price * 0.42)))
        stock = int(float(payload.get("current_stock") or 120))
        safety = int(float(payload.get("safety_stock") or 220))
        warehouse = int(float(payload.get("warehouse_available") or 1000))
        baseline_daily_sales = int(float(payload.get("baseline_daily_sales") or 80))
        views = int(float(payload.get("app_views_24h") or 30000))
        cart_adds = int(float(payload.get("cart_adds_24h") or max(1, views * 0.08)))
        tryons = int(float(payload.get("rfid_tryons_24h") or max(1, views * 0.015)))
        demand_multiplier = float(payload.get("demand_multiplier") or state["event"].get("demand_signal_multiplier", 1.35))
        state["event"]["demand_signal_multiplier"] = demand_multiplier
        state["event"]["type"] = str(payload.get("trigger") or "custom_ai_launch")
        state["event"]["severity"] = "high" if demand_multiplier >= 1.3 or stock < safety else "medium"
        state["scenario_id"] = f"custom_launch_{sku_id.lower().replace(' ', '_')}"
        state["scenario_name"] = f"15-Day AI Launch — {name}"
        state["description"] = str(payload.get("description") or f"业务用户输入 {sku_id}/{name}，系统按真实 SKU 数字模拟 15 天上新闭环。")
        custom_product = self._product(
            sku_id, name, category, stock, safety, warehouse,
            int(float(payload.get("lead_time_days") or 2)), price, cost,
            float(payload.get("gross_margin_floor") or 0.35), baseline_daily_sales,
            [max(1, round(baseline_daily_sales * x)) for x in [0.82, 0.91, 1.0, 1.08, 1.18, 1.32, demand_multiplier]],
            views, cart_adds, tryons,
            {"zara": int(price * 1.2), "hm": int(price * 0.95), "local_brand": int(price * 0.8)},
            "summer_in_season" if season == "summer" else f"{season}_in_season",
            int(float(payload.get("clearance_discount_candidate_pct") or 0)),
        )
        # Put the user SKU first so it becomes hero SKU for launch story.
        state["products"] = [custom_product] + [p for p in state.get("products", []) if p.get("sku_id") != sku_id]
        state["custom_inputs"] = payload
        return self._run_state(state)

    def list_seasons(self) -> List[Dict[str, str]]:
        return [
            {"id": "spring", "name": "Spring", "decision_theme": "new-season launch + light outerwear stock watch"},
            {"id": "summer", "name": "Summer", "decision_theme": "Contoso Air demand spike + off-season winter clearance"},
            {"id": "autumn", "name": "Autumn", "decision_theme": "layering transition + summer markdown exit"},
            {"id": "winter", "name": "Winter", "decision_theme": "HEATTECH/down stockout prevention + limited discounting"},
        ]

    def _run_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        decisions: List[AgentDecision] = []

        inventory = self._inventory_agent(state)
        decisions.append(inventory)
        state["inventory_decision"] = inventory.decision

        pricing = self._pricing_agent(state)
        decisions.append(pricing)
        state["pricing_decision"] = pricing.decision

        customer = self._customer_understanding_agent(state)
        decisions.append(customer)
        state["customer_decision"] = customer.decision

        personalization = self._personalization_agent(state)
        decisions.append(personalization)
        state["personalization_decision"] = personalization.decision

        marketing = self._marketing_agent(state)
        decisions.append(marketing)
        state["marketing_decision"] = marketing.decision

        approvals = [
            {
                "agent": d.agent,
                "decision": d.decision.get("action") or d.decision.get("strategy") or d.decision.get("campaign_name"),
                "reason": "High-risk business action requires human approval",
            }
            for d in decisions
            if d.human_approval_required
        ]

        return {
            "scenario": state["scenario_id"],
            "scenario_name": state["scenario_name"],
            "description": state["description"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "season": state.get("season"),
            "season_label": state.get("season_label"),
            "trigger": state["event"],
            "store": state["store"],
            "products": state.get("products", []),
            "business_calendar": state.get("business_calendar", {}),
            "decision_loop": [d.as_dict() for d in decisions],
            "human_approval_queue": approvals,
            "customers": state.get("customers", []),
            "method_mapping": state["method_mapping"],
            "data_sources": self._data_sources(),
            "executive_summary": self._executive_summary(state, decisions, approvals),
            "architecture_note": {
                "implemented_now": "FastAPI + scenario-driven Retail State + 5 agent decision loop + Azure OpenAI-ready reasoning layer",
                "target_azure_native": "Azure Container Apps, Azure AI Foundry, Event Hubs, Cosmos DB/Fabric, Azure ML, APIM/MCP Gateway, Application Insights",
                "honest_positioning": "Prototype demonstrates the decision logic required for the target outcomes; it does not claim validated production ROI."
            }
        }

    def _seasonal_state(self, season: str) -> Dict[str, Any]:
        """Create a realistic seasonal retail state for a decision-maker demo.

        The goal is to show internal operating decisions across the retail calendar:
        in-season demand capture, out-of-season promotion, replenishment alerts,
        pricing guardrails, customer targeting, and human approval.
        """
        base = self.load_state()
        common = {
            "store": {
                "store_id": "SH-001",
                "name": "Contoso Fashion Shanghai Flagship Store",
                "city": "Shanghai",
                "tier": "tier_1_city",
                "traffic_index": 1.25,
                "format": "flagship",
                "fulfillment_options": ["store_pickup", "ship_from_store", "nearby_store_transfer"],
            },
            "channel_metrics": base["channel_metrics"],
            "business_constraints": base["business_constraints"],
            "method_mapping": base["method_mapping"],
        }
        scenarios: Dict[str, Dict[str, Any]] = {
            "spring": {
                "season": "spring",
                "season_label": "春季",
                "scenario_id": "seasonal_spring_shanghai_001",
                "scenario_name": "Spring New Season Launch & Rainy-Day Stock Watch",
                "description": "春季换季上新，轻外套和防晒/防雨单品需求抬升；冬季 HEATTECH 进入反季清仓，但不能牺牲毛利。",
                "event": {"type": "seasonal_transition", "season": "spring", "city": "Shanghai", "temperature_current_c": 18, "temperature_normal_c": 16, "temperature_drop_c": 4, "demand_signal_multiplier": 1.18, "forecast_days": 14, "severity": "medium", "source": "Seasonal calendar + Weather + POS / Event Hubs"},
                "business_calendar": {"in_season_focus": ["light_outerwear", "uv_protection", "linen"], "off_season_clearance": ["thermal_innerwear"], "decision_window_days": 14},
                "products": [
                    self._product("JKT-SP-001", "BlockTech Light Parka", "outerwear", 96, 180, 620, 2, 399, 188, 0.38, 26, [20,22,24,31,41,56,63], 11200, 870, 260, {"zara":499,"hm":349,"gap":429}, "spring_in_season"),
                    self._product("UV-001", "UV Protection Pocketable Parka", "uv_protection", 78, 160, 740, 2, 299, 126, 0.40, 22, [18,21,24,29,45,58,64], 14800, 920, 310, {"zara":359,"hm":249,"local_brand":219}, "spring_in_season"),
                    self._product("LINEN-001", "Premium Linen Shirt", "linen", 320, 160, 880, 3, 199, 72, 0.42, 38, [34,36,39,43,48,54,59], 9300, 680, 160, {"zara":249,"hm":179,"gap":229}, "spring_new_arrival"),
                    self._product("HT-001", "HEATTECH Thermal Innerwear", "thermal_innerwear", 880, 220, 1600, 1, 199, 82, 0.42, 18, [40,34,28,22,18,15,12], 3200, 180, 25, {"zara":199,"hm":149,"local_brand":129}, "off_season_clearance", 15),
                ],
                "customers": self._seasonal_customers("spring", ["BlockTech Light Parka", "UV Protection Pocketable Parka"]),
            },
            "summer": {
                "season": "summer",
                "season_label": "夏季",
                "scenario_id": "seasonal_summer_shanghai_001",
                "scenario_name": "Summer Heatwave Contoso Air Demand & Winter Clearance",
                "description": "高温推动 Contoso Air、速干、短裤需求上涨；羽绒/抓绒进入反季促销池，系统需要判断哪些可打折、哪些要补货。",
                "event": {"type": "heatwave", "season": "summer", "city": "Shanghai", "temperature_current_c": 36, "temperature_normal_c": 29, "temperature_drop_c": 7, "demand_signal_multiplier": 1.35, "forecast_days": 14, "severity": "high", "source": "Weather alert + App search + POS / Event Hubs"},
                "business_calendar": {"in_season_focus": ["contoso_air", "shorts", "dry_ex"], "off_season_clearance": ["outerwear", "fleece"], "decision_window_days": 14},
                "products": [
                    self._product("CAIR-001", "Contoso Air Cotton Oversized T-Shirt", "contoso_air", 140, 360, 1400, 1, 99, 36, 0.45, 92, [76,82,95,118,154,190,221], 28600, 2400, 520, {"zara":129,"hm":99,"local_brand":79}, "summer_in_season"),
                    self._product("DRY-001", "DRY-EX Polo Shirt", "dry_ex", 210, 260, 920, 2, 149, 58, 0.42, 58, [49,56,62,75,91,105,122], 17200, 1380, 330, {"zara":199,"hm":129,"gap":169}, "summer_in_season"),
                    self._product("SHORT-001", "Ultra Stretch Active Shorts", "shorts", 92, 190, 760, 2, 149, 54, 0.42, 44, [39,43,50,68,84,98,117], 15300, 1120, 280, {"zara":179,"hm":139,"local_brand":119}, "summer_in_season"),
                    self._product("DOWN-004", "Ultra Light Down Jacket", "outerwear", 540, 140, 360, 3, 499, 299, 0.35, 8, [11,9,8,7,6,5,4], 1800, 65, 12, {"zara":499,"hm":399,"gap":429}, "off_season_clearance", 20),
                ],
                "customers": self._seasonal_customers("summer", ["Contoso Air Cotton Oversized T-Shirt", "DRY-EX Polo Shirt"]),
            },
            "autumn": {
                "season": "autumn",
                "season_label": "秋季",
                "scenario_id": "seasonal_autumn_shanghai_001",
                "scenario_name": "Autumn Layering Transition & Summer Markdown Exit",
                "description": "秋季温差变大，针织、衬衫、轻羽绒开始预热；夏季 Contoso Air 尾货需要分层促销，避免库存跨季积压。",
                "event": {"type": "layering_transition", "season": "autumn", "city": "Shanghai", "temperature_current_c": 15, "temperature_normal_c": 21, "temperature_drop_c": 6, "demand_signal_multiplier": 1.22, "forecast_days": 14, "severity": "medium", "source": "Seasonal calendar + Weather + POS / Event Hubs"},
                "business_calendar": {"in_season_focus": ["knitwear", "shirt", "light_down"], "off_season_clearance": ["contoso_air", "shorts"], "decision_window_days": 14},
                "products": [
                    self._product("KNIT-001", "Souffle Yarn Crew Neck Sweater", "knitwear", 84, 170, 680, 2, 299, 126, 0.40, 28, [21,24,27,36,49,64,73], 13800, 980, 290, {"zara":399,"hm":249,"gap":329}, "autumn_in_season"),
                    self._product("SHIRT-002", "Flannel Checked Shirt", "shirt", 128, 160, 720, 2, 199, 78, 0.42, 34, [30,32,36,44,51,60,68], 10200, 840, 240, {"zara":249,"hm":179,"gap":229}, "autumn_in_season"),
                    self._product("DOWN-VEST-001", "Ultra Light Down Vest", "outerwear", 62, 130, 420, 3, 399, 226, 0.35, 18, [14,17,20,29,38,51,59], 11800, 750, 230, {"zara":459,"hm":359,"gap":429}, "autumn_preheat"),
                    self._product("CAIR-001", "Contoso Air Cotton Oversized T-Shirt", "contoso_air", 760, 260, 1200, 1, 99, 36, 0.45, 31, [54,49,43,37,30,24,21], 5100, 280, 60, {"zara":99,"hm":79,"local_brand":69}, "off_season_clearance", 15),
                ],
                "customers": self._seasonal_customers("autumn", ["Souffle Yarn Crew Neck Sweater", "Flannel Checked Shirt"]),
            },
            "winter": {
                "season": "winter",
                "season_label": "冬季",
                "scenario_id": "seasonal_winter_shanghai_001",
                "scenario_name": "Winter Cold Snap HEATTECH Stockout Prevention",
                "description": "冬季寒潮导致 HEATTECH 和轻羽绒需求暴涨；系统优先做补货和价格保护，夏季尾货只做定向反季促销。",
                "event": {**base["event"], "season": "winter", "demand_signal_multiplier": 1.42},
                "business_calendar": {"in_season_focus": ["thermal_innerwear", "outerwear", "fleece"], "off_season_clearance": ["contoso_air", "linen"], "decision_window_days": 7},
                "products": [*base["products"], self._product("CAIR-001", "Contoso Air Cotton Oversized T-Shirt", "contoso_air", 620, 260, 1200, 1, 99, 36, 0.45, 12, [18,16,14,13,11,9,8], 1300, 70, 8, {"zara":99,"hm":79,"local_brand":69}, "off_season_clearance", 20)],
                "customers": base["customers"],
            },
        }
        state = deepcopy(common)
        state.update(scenarios[season])
        return state

    def _product(self, sku_id: str, name: str, category: str, current_stock: int, safety_stock: int, warehouse_available: int, lead_time_days: int, current_price: int, cost: int, gross_margin_floor: float, baseline_daily_sales: int, last_7_days_sales: List[int], app_views_24h: int, cart_adds_24h: int, rfid_tryons_24h: int, competitor_prices: Dict[str, int], lifecycle: str, clearance_discount_candidate_pct: int = 0) -> Dict[str, Any]:
        return {
            "sku_id": sku_id,
            "name": name,
            "category": category,
            "current_stock": current_stock,
            "safety_stock": safety_stock,
            "warehouse_available": warehouse_available,
            "lead_time_days": lead_time_days,
            "current_price": current_price,
            "cost": cost,
            "gross_margin_floor": gross_margin_floor,
            "baseline_daily_sales": baseline_daily_sales,
            "last_7_days_sales": last_7_days_sales,
            "app_views_24h": app_views_24h,
            "cart_adds_24h": cart_adds_24h,
            "rfid_tryons_24h": rfid_tryons_24h,
            "competitor_prices": competitor_prices,
            "lifecycle": lifecycle,
            "clearance_discount_candidate_pct": clearance_discount_candidate_pct,
        }

    def _seasonal_customers(self, season: str, recent_views: List[str]) -> List[Dict[str, Any]]:
        return [
            {
                "customer_id": f"CONTOSO_2026_{season.upper()}_001",
                "segment": "young_professional_commuter",
                "city": "Shanghai",
                "membership_tier": "gold",
                "lifetime_value": 12500,
                "recent_views": recent_views,
                "cart_items": [],
                "purchase_history": ["Stretch Jeans", "Oxford Shirt"],
                "price_sensitivity": "medium",
                "preferred_channel": "app_push",
                "language": "zh-CN",
                "consent": {"personalization": True, "marketing_push": True},
            },
            {
                "customer_id": f"CONTOSO_2026_{season.upper()}_002",
                "segment": "family_value_shopper",
                "city": "Shanghai",
                "membership_tier": "silver",
                "lifetime_value": 6800,
                "recent_views": [recent_views[0], "Kids basics"],
                "cart_items": [recent_views[0]],
                "purchase_history": ["Kids Innerwear", "Fleece Jacket"],
                "price_sensitivity": "high",
                "preferred_channel": "wechat_mini",
                "language": "zh-CN",
                "consent": {"personalization": True, "marketing_push": True},
            },
        ]

    def _inventory_agent(self, state: Dict[str, Any]) -> AgentDecision:
        event = state["event"]
        products = state["products"]
        results = []
        total_replenishment = 0
        high_risk_count = 0

        for p in products:
            recent_avg = sum(p["last_7_days_sales"][-3:]) / 3
            behavior_signal = min(0.45, (p["app_views_24h"] / 20000) * 0.25 + (p["cart_adds_24h"] / 1500) * 0.20)
            seasonal_multiplier = event.get("demand_signal_multiplier")
            weather_multiplier = seasonal_multiplier or (1 + min(0.9, abs(event.get("temperature_drop_c", 0)) / 20))
            demand_multiplier = round(weather_multiplier + behavior_signal, 2)
            predicted_daily = round(max(p["baseline_daily_sales"], recent_avg) * demand_multiplier)
            seven_day_demand = predicted_daily * event["forecast_days"]
            stock_gap = max(0, seven_day_demand + p["safety_stock"] - p["current_stock"])
            stock_risk = "high" if stock_gap > p["safety_stock"] else "medium" if stock_gap > 0 else "low"
            if stock_risk == "high":
                high_risk_count += 1
            replenishment = min(stock_gap, p["warehouse_available"])
            total_replenishment += replenishment
            results.append({
                "sku_id": p["sku_id"],
                "name": p["name"],
                "baseline_daily_sales": p["baseline_daily_sales"],
                "recent_avg_sales": round(recent_avg, 1),
                "demand_multiplier": demand_multiplier,
                "predicted_daily_sales": predicted_daily,
                "seven_day_demand": seven_day_demand,
                "current_stock": p["current_stock"],
                "safety_stock": p["safety_stock"],
                "stock_gap": stock_gap,
                "stock_risk": stock_risk,
                "recommended_replenishment": replenishment,
                "lead_time_days": p["lead_time_days"],
                "lifecycle": p.get("lifecycle", "in_season"),
                "clearance_discount_candidate_pct": p.get("clearance_discount_candidate_pct", 0),
            })

        return AgentDecision(
            agent="Inventory Agent",
            method_sources=["Hybrid AI", "Agentic AI data-to-decision pattern"],
            input_summary={
                "event": f"{event['city']} {event.get('season', 'seasonal')} demand signal: {event['type']}",
                "products_evaluated": len(products),
                "signals": ["seasonal calendar", "weather", "recent_sales", "app_views", "cart_adds", "RFID try-ons", "warehouse availability"],
            },
            decision={
                "action": "urgent_replenishment" if high_risk_count else "monitor",
                "products": results,
                "total_replenishment_units": int(total_replenishment),
                "handoff_to": "Pricing Agent",
            },
            evidence=[
                "Seasonal calendar and weather are combined with actual demand signals, not treated as a static campaign plan.",
                "Recent 3-day sales exceed baseline, showing demand acceleration before marketing push.",
                "App views, cart adds, and RFID try-ons are leading indicators before POS sales catch up.",
            ],
            confidence=0.86,
            human_approval_required=total_replenishment > 500,
            business_impact={
                "risk_reduced": "stockout risk",
                "estimated_lost_sales_prevented_units": int(total_replenishment * 0.65),
            },
        )

    def _pricing_agent(self, state: Dict[str, Any]) -> AgentDecision:
        constraints = state["business_constraints"]
        inventory_products = state["inventory_decision"]["products"]
        product_by_id = {p["sku_id"]: p for p in state["products"]}
        pricing_actions = []
        promo_validator = PromotionValidator()

        for inv in inventory_products:
            p = product_by_id[inv["sku_id"]]
            avg_competitor = sum(p["competitor_prices"].values()) / len(p["competitor_prices"])
            margin = (p["current_price"] - p["cost"]) / p["current_price"]
            if inv.get("lifecycle") == "off_season_clearance" and inv["stock_risk"] != "high":
                candidate_discount = p.get("clearance_discount_candidate_pct", 10) or 10
                recommended_price = round(max(p["cost"] / (1 - p["gross_margin_floor"]), p["current_price"] * (1 - candidate_discount / 100)))
                strategy = "off_season_clearance_promotion"
                reason = "Product is out of season with sufficient stock; use controlled markdown to release working capital."
            elif inv["stock_risk"] == "high" and constraints["do_not_discount_when_stock_risk_high"]:
                strategy = "hold_price_protect_margin"
                recommended_price = p["current_price"]
                reason = "Demand is rising and stock risk is high; discounting would worsen stockout risk."
            elif avg_competitor < p["current_price"] * 0.9 and inv["stock_risk"] != "high":
                strategy = "selective_match_competition"
                recommended_price = round(max(p["cost"] / (1 - p["gross_margin_floor"]), avg_competitor * 0.98))
                reason = "Competitor price gap is material and inventory risk is manageable."
            else:
                strategy = "maintain_price"
                recommended_price = p["current_price"]
                reason = "Current price balances margin, competition, and demand."

            price_change_pct = (recommended_price - p["current_price"]) / p["current_price"]
            approval = abs(price_change_pct) > constraints["human_approval_price_change_pct"]
            candidate_discount_pct = round(max(0, (p["current_price"] - recommended_price) / p["current_price"] * 100), 2)
            validation = promo_validator.validate(PromotionScenario(
                sku_id=p["sku_id"],
                product_name=p["name"],
                category=p["category"],
                current_price=p["current_price"],
                unit_cost=p["cost"],
                discount_pct=candidate_discount_pct,
                baseline_units=inv["baseline_daily_sales"] * state["event"]["forecast_days"],
                stock_risk=inv["stock_risk"],
            ))
            llm_generated_candidates = []
            for discount in [5, 10, 15]:
                llm_generated_candidates.append(promo_validator.validate(PromotionScenario(
                    sku_id=p["sku_id"],
                    product_name=p["name"],
                    category=p["category"],
                    current_price=p["current_price"],
                    unit_cost=p["cost"],
                    discount_pct=discount,
                    baseline_units=inv["baseline_daily_sales"] * state["event"]["forecast_days"],
                    stock_risk=inv["stock_risk"],
                )))
            pricing_actions.append({
                "sku_id": p["sku_id"],
                "name": p["name"],
                "current_price": p["current_price"],
                "recommended_price": recommended_price,
                "price_change_pct": round(price_change_pct, 3),
                "strategy": strategy,
                "reason": reason,
                "gross_margin": round(margin, 3),
                "avg_competitor_price": round(avg_competitor, 2),
                "promotion_validation": validation,
                "llm_generated_promotion_candidates": llm_generated_candidates,
                "requires_approval": approval or bool(validation["risk_flags"]),
            })

        return AgentDecision(
            agent="Pricing Agent",
            method_sources=["Data -> ML Validator -> LLM Reasoning", "Responsible AI guardrails"],
            input_summary={
                "received_from": "Inventory Agent",
                "pricing_constraints": constraints,
                "products_priced": len(pricing_actions),
            },
            decision={
                "strategy": "guardrailed_dynamic_pricing",
                "pricing_actions": pricing_actions,
                "handoff_to": "Customer Understanding Agent and Personalization Agent",
            },
            evidence=[
                "Pricing uses inventory risk instead of optimizing price in isolation.",
                "Hybrid AI promo history validates discount candidates with predicted lift, incremental profit, and ROI.",
                "High stockout risk blocks broad discounting even when demand is high.",
                "Price changes beyond threshold or negative ROI require human approval and audit log.",
            ],
            confidence=0.82,
            human_approval_required=any(a["requires_approval"] for a in pricing_actions),
            business_impact={"risk_reduced": "margin erosion and AI-driven price mistakes"},
        )

    def _customer_understanding_agent(self, state: Dict[str, Any]) -> AgentDecision:
        qualified = []
        focus_categories = set(state.get("business_calendar", {}).get("in_season_focus", []))
        product_keywords = [p["name"] for p in state["products"] if p.get("category") in focus_categories or p.get("lifecycle", "").endswith("in_season")]
        for c in state["customers"]:
            intent_score = 0.25
            intent_score += 0.25 if any(any(k.lower() in x.lower() or x.lower() in k.lower() for k in product_keywords) for x in c["recent_views"]) else 0
            intent_score += 0.20 if c["cart_items"] else 0
            intent_score += 0.15 if c["city"] == state["event"]["city"] else 0
            intent_score += 0.10 if c["consent"].get("personalization") else 0
            intent_score = min(0.95, round(intent_score, 2))
            qualified.append({
                "customer_id": c["customer_id"],
                "segment": c["segment"],
                "purchase_intent": "high" if intent_score >= 0.75 else "medium",
                "intent_score": intent_score,
                "price_sensitivity": c["price_sensitivity"],
                "preferred_channel": c["preferred_channel"],
                "language": c["language"],
                "marketing_consent": c["consent"].get("marketing_push", False),
            })

        return AgentDecision(
            agent="Customer Understanding Agent",
            method_sources=["Synthetic Persona", "Understand pillar", "Personal memory"],
            input_summary={
                "customers_evaluated": len(state["customers"]),
                "signals": ["recent views", "cart", "purchase history", "location", "consent", "channel preference"],
            },
            decision={
                "target_customers": qualified,
                "primary_segment": "high_intent_winter_buyer",
                "handoff_to": "Personalization Agent and Marketing Agent",
            },
            evidence=[
                "Customer intent combines behavioral signals and local context, not demographics alone.",
                "Consent and channel preference are part of the profile to support privacy-aware personalization.",
                "Synthetic persona patterns can fill cold-start gaps without exposing real PII in demos.",
            ],
            confidence=0.84,
            business_impact={"risk_reduced": "irrelevant targeting and privacy-insensitive outreach"},
        )

    def _personalization_agent(self, state: Dict[str, Any]) -> AgentDecision:
        stock_by_id = {p["sku_id"]: p for p in state["inventory_decision"]["products"]}
        price_by_id = {a["sku_id"]: a for a in state["pricing_decision"]["pricing_actions"]}
        catalog = {p["sku_id"]: p for p in state["products"]}
        recommendations = []

        for customer in state["customer_decision"]["target_customers"]:
            customer_recs = []
            for sku_id, p in catalog.items():
                inv = stock_by_id[sku_id]
                price = price_by_id[sku_id]
                if inv["stock_risk"] == "high" and customer["intent_score"] < 0.75:
                    continue
                customer_recs.append({
                    "sku_id": sku_id,
                    "name": p["name"],
                    "recommended_price": price["recommended_price"],
                    "reason": self._recommendation_reason(customer, p, inv, price),
                    "priority": 1 if customer["intent_score"] >= 0.75 and inv["stock_risk"] == "high" else 2,
                    "inventory_guardrail": f"stock_risk={inv['stock_risk']}; avoid broad promotion",
                })
            recommendations.append({
                "customer_id": customer["customer_id"],
                "channel": customer["preferred_channel"],
                "language": customer["language"],
                "recommendations": sorted(customer_recs, key=lambda x: x["priority"]),
            })

        return AgentDecision(
            agent="Personalization Agent",
            method_sources=["Understand -> Act -> Learn", "memory-aware personalization"],
            input_summary={
                "received_from": ["Customer Understanding Agent", "Inventory Agent", "Pricing Agent"],
                "customers_personalized": len(recommendations),
            },
            decision={
                "personalized_recommendations": recommendations,
                "handoff_to": "Marketing Agent",
            },
            evidence=[
                "Recommendations are constrained by stock risk and price strategy.",
                "High-intent customers are prioritized when inventory is scarce.",
                "The next-best-action is channel-aware and language-aware for Asia markets.",
            ],
            confidence=0.88,
            business_impact={"expected_effect": "higher conversion with lower customer fatigue"},
        )

    def _marketing_agent(self, state: Dict[str, Any]) -> AgentDecision:
        channel_metrics = state["channel_metrics"]
        customers = state["customer_decision"]["target_customers"]
        personalization = state["personalization_decision"]["personalized_recommendations"]
        high_stock_risk = any(p["stock_risk"] == "high" for p in state["inventory_decision"]["products"])
        budget = 5000
        channel_plan: Dict[str, Dict[str, Any]] = {}

        eligible_customers = [c for c in customers if c["marketing_consent"]]
        for c in eligible_customers:
            ch = c["preferred_channel"]
            metric = channel_metrics[ch]
            channel_plan.setdefault(ch, {"customers": 0, "budget": 0, "expected_conversions": 0})
            channel_plan[ch]["customers"] += 1
            channel_plan[ch]["budget"] += 1000 if c["purchase_intent"] == "high" else 500
            channel_plan[ch]["expected_conversions"] += round(metric["conversion_rate"] * (1.25 if c["purchase_intent"] == "high" else 1), 3)

        allocated = sum(v["budget"] for v in channel_plan.values()) or 1
        for v in channel_plan.values():
            v["budget"] = round(min(budget, v["budget"] / allocated * budget), 2)

        requires_approval = high_stock_risk and len(eligible_customers) > 1
        campaign_scope = "precision_targeting" if high_stock_risk else "broad_campaign"

        return AgentDecision(
            agent="Marketing Agent",
            method_sources=["Act/Learn loop", "Hybrid AI constrained optimization", "Responsible AI"],
            input_summary={
                "received_from": ["Customer Understanding Agent", "Personalization Agent", "Inventory Agent"],
                "eligible_customers": len(eligible_customers),
                "stock_risk": "high" if high_stock_risk else "normal",
            },
            decision={
                "campaign_name": "Shanghai Cold Snap Warmth Campaign",
                "campaign_scope": campaign_scope,
            "message": self._seasonal_message(state),
                "channel_plan": channel_plan,
                "ab_test": {
                    "variant_a": "weather urgency: 上海降温提醒",
                    "variant_b": "comfort benefit: 通勤更暖更轻松",
                    "success_metric": "conversion_rate and stockout-safe revenue",
                },
                "uses_recommendations": personalization,
            },
            evidence=[
                "Marketing scope is narrowed when inventory risk is high.",
                "Budget allocation uses channel conversion and customer intent instead of equal split.",
                "Customer consent and frequency guardrails prevent over-targeting.",
            ],
            confidence=0.8,
            human_approval_required=requires_approval,
            business_impact={
                "expected_outcome": "convert high-intent customers without triggering broad stockout",
                "budget": budget,
            },
        )

    def _recommendation_reason(self, customer: Dict[str, Any], product: Dict[str, Any], inventory: Dict[str, Any], price: Dict[str, Any]) -> str:
        return (
            f"{customer['segment']} in Shanghai showed {customer['purchase_intent']} seasonal intent; "
            f"{product['name']} matches the cold snap context. Pricing strategy is {price['strategy']} "
            f"and inventory risk is {inventory['stock_risk']}."
        )

    def _seasonal_message(self, state: Dict[str, Any]) -> str:
        messages = {
            "spring": "春季换装已开始，为你准备了轻外套、防晒和通勤穿搭建议。",
            "summer": "上海高温预警，为你准备了 Contoso Air、速干和清爽通勤搭配。",
            "autumn": "早晚温差变大，为你准备了针织、衬衫和轻量叠穿建议。",
            "winter": "上海降温，为你准备了 HEATTECH 和轻羽绒保暖穿搭。",
        }
        return messages.get(state.get("season"), "为你准备了适合当前季节的穿搭建议。")

    def _data_sources(self) -> List[Dict[str, str]]:
        return [
            {"source": "Weather API", "signals": "temperature drop, 7-day forecast", "azure_service": "Event Hubs"},
            {"source": "POS / RFID", "signals": "sales, try-ons, shelf movement", "azure_service": "Fabric / Event Hubs"},
            {"source": "App / WeChat Mini Program", "signals": "views, cart adds, searches", "azure_service": "Event Hubs / Cosmos DB"},
            {"source": "CRM / Membership", "signals": "tier, consent, lifetime value", "azure_service": "Cosmos DB"},
            {"source": "Competitor Monitoring", "signals": "Zara/H&M/GAP prices", "azure_service": "MCP tools via APIM"},
            {"source": "Apparel-Mapped Promo History", "signals": "discount, measured lift, incremental profit, promo ROI", "azure_service": "Fabric / Azure ML"},
            {"source": "Agent Memory", "signals": "prior campaign outcomes, customer preferences", "azure_service": "Cosmos DB vector search / Foundry Memory"},
        ]

    def _executive_summary(self, state: Dict[str, Any], decisions: List[AgentDecision], approvals: List[Dict[str, Any]]) -> Dict[str, Any]:
        inventory = state["inventory_decision"]
        pricing = state["pricing_decision"]
        marketing = state["marketing_decision"]
        season_label = state.get("season_label", "季节")
        off_season = state.get("business_calendar", {}).get("off_season_clearance", [])
        return {
            "what_happened": f"{season_label}经营周期触发：系统同时处理当季需求、反季促销和缺货补货提醒。",
            "what_the_agents_decided": [
                "Inventory Agent flags stockout risk and creates replenishment work orders for high-risk SKUs.",
                "Pricing Agent separates in-season price protection from off-season clearance promotion.",
                "Customer Understanding Agent identifies high-intent winter buyers with consent.",
                "Personalization Agent recommends available cold-weather products under inventory guardrails.",
                "Marketing Agent runs precision targeting instead of broad discounting."
            ],
            "business_result": {
                "replenishment_units": inventory["total_replenishment_units"],
                "pricing_strategy": pricing["strategy"],
                "campaign_scope": marketing["campaign_scope"],
                "approval_items": len(approvals),
                "off_season_clearance_categories": off_season,
            },
            "target_outcomes_positioning": "Sales +40%, waste -50%, satisfaction 85%, CLV +60% are target business hypotheses, not claimed validated results from this prototype."
        }
