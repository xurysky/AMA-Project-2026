# Hybrid AI Retail Promotion Data Reuse

## Why reuse the Hybrid AI data pattern

The original AMA demo was too mock-heavy: price, inventory, sales, discount, and ROI were not connected by an explainable decision model. Hybrid AI provides the missing pattern:

> Data Layer (historical SKUs / discounts / measured lift) → ML / Econometric Validator (uplift, incremental profit, ROI) → LLM Business Reasoning (promotion candidates) → Human Approval.

This project adds `data/promo_validation/apparel_promo_history.csv` as the data source for Pricing Agent promotion validation.

## Data positioning

The file is an **apparel-mapped demo dataset based on the retail promotion planning pattern**:

- It preserves the Hybrid AI structure: historical SKU, discount, measured lift, promo investment, incremental profit, profit ROI, and stockout risk.
- It semantically maps grocery/CPG items to apparel retail SKUs:
  - `12-pack Soft Drinks` → `HEATTECH Crew Neck Innerwear 2-Pack`
  - `24-pack Soft Drinks` → `HEATTECH Kids Innerwear Set`
  - `Family Size Chips` → `Fleece Full-Zip Jacket`
  - `Granola Snack Bars` → `HEATTECH Scarf`
  - `Organic Eggs` → `Ultra Light Down Jacket`
  - `Premium Milk 1L` → `Warm Lined Pants`
- It is not real Contoso Fashion sales data and does not claim validated production ROI.

## Why the mapping is defensible

The goal is not to disguise grocery data as apparel data. The goal is to reuse the decision structure and behavioral pattern:

- Soft drink promotion spike → HEATTECH cold-snap demand spike
- Snack bundle promotion → scarf/fleece outfit bundle
- Fresh product margin/window risk → seasonal apparel demand window risk
- Discount → measured lift → ROI → approval is reusable across retail categories

## Code integration

- Data: `data/promo_validation/apparel_promo_history.csv`
- Validator: `src/simulators/promotion_validator.py`
- Agent integration: `Pricing Agent` in `src/scenario_engine.py`

The Pricing Agent now:

1. Produces final price actions based on inventory risk and competitor price.
2. Validates the final action using the Hybrid AI validator.
3. Evaluates LLM-generated promotion candidates at 5%, 10%, and 15% discount levels.
4. Flags negative ROI, deep discounts, and discounts that amplify stockout risk.
5. Routes risky actions to human approval.

## Honest presentation wording

Recommended wording:

> We reused the Hybrid AI retail promotion planning data pattern and mapped it into apparel SKUs, so the prototype can demonstrate discount validation, predicted uplift, incremental profit, and ROI guardrails. This is simulation data for architecture validation, not claimed real Contoso Fashion performance data.

Avoid saying:

> This is real Contoso Fashion data.
> This ROI has been validated in production.
