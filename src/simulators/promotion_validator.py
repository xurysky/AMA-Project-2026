"""Hybrid AI promotion validator for the AMA Retail Agent demo.

The data file is a cleaned, apparel-mapped version of the Hybrid AI retail promotion
planning pattern: historical SKU, discount, measured lift, incremental profit,
and ROI. It is demo/simulation data, not real Contoso Fashion sales.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "promo_validation" / "apparel_promo_history.csv"


@dataclass
class PromotionScenario:
    sku_id: str
    product_name: str
    category: str
    current_price: float
    unit_cost: float
    discount_pct: float
    baseline_units: int
    stock_risk: str


class PromotionValidator:
    """Small econometric-style validator for demo promotion candidates."""

    def __init__(self, data_path: Path = DATA_PATH):
        self.data_path = data_path
        self.rows = self._load_rows()

    def _load_rows(self) -> List[Dict[str, Any]]:
        with self.data_path.open("r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            for k in [
                "week", "base_price", "unit_cost", "discount_pct", "baseline_units",
                "measured_units", "measured_lift_pct", "promo_revenue", "gross_profit",
                "incremental_profit", "promo_investment", "profit_roi",
            ]:
                r[k] = float(r[k])
        return rows

    def validate(self, scenario: PromotionScenario) -> Dict[str, Any]:
        comparable = [r for r in self.rows if r["mapped_apparel_category"] == scenario.category]
        if not comparable:
            comparable = self.rows

        # Use nearest discount band as the validator sample, similar to scenario simulation.
        nearest = min({r["discount_pct"] for r in comparable}, key=lambda d: abs(d - scenario.discount_pct))
        sample = [r for r in comparable if r["discount_pct"] == nearest]
        if not sample:
            sample = comparable

        avg_lift_pct = mean(r["measured_lift_pct"] for r in sample)
        avg_roi = mean(r["profit_roi"] for r in sample)
        promo_price = round(scenario.current_price * (1 - scenario.discount_pct / 100), 2)
        baseline_profit = scenario.baseline_units * (scenario.current_price - scenario.unit_cost)

        if scenario.discount_pct <= 0:
            predicted_units = scenario.baseline_units
            avg_lift_pct = 0
            incremental_profit = 0
            promo_investment = 0
            profit_roi = 0
        else:
            predicted_units = round(scenario.baseline_units * (1 + avg_lift_pct / 100))
            predicted_profit = predicted_units * (promo_price - scenario.unit_cost)
            incremental_profit = round(predicted_profit - baseline_profit, 2)
            promo_investment = round(max(1, scenario.baseline_units * scenario.current_price * (scenario.discount_pct / 100) * 0.52), 2)
            profit_roi = round(incremental_profit / promo_investment, 2) if promo_investment else 0

        risk_flags = []
        if scenario.stock_risk == "high" and scenario.discount_pct > 0:
            risk_flags.append("stockout_risk_amplified_by_discount")
        if profit_roi < 0:
            risk_flags.append("negative_profit_roi")
        if scenario.discount_pct > 15:
            risk_flags.append("deep_discount_requires_business_approval")
        if avg_roi < 0 and scenario.discount_pct > 0:
            risk_flags.append("historical_comparable_promos_underperformed")

        pass_validator = profit_roi > 0 and not (
            scenario.stock_risk == "high" and scenario.discount_pct > 0
        )

        return {
            "validator": "econometric_promotion_validator",
            "data_source": str(self.data_path.relative_to(Path(__file__).resolve().parents[2])),
            "source_positioning": "Apparel-mapped Hybrid AI retail promo pattern; demo simulation, not real Contoso Fashion sales.",
            "candidate_discount_pct": scenario.discount_pct,
            "comparable_category": scenario.category,
            "nearest_historical_discount_pct": nearest,
            "comparable_records": len(sample),
            "baseline_units": scenario.baseline_units,
            "predicted_units": predicted_units,
            "predicted_lift_pct": round(avg_lift_pct, 2),
            "promo_price": promo_price,
            "incremental_profit": incremental_profit,
            "promo_investment": promo_investment,
            "profit_roi": profit_roi,
            "historical_avg_profit_roi": round(avg_roi, 2),
            "risk_flags": risk_flags,
            "pass_validator": pass_validator,
        }
