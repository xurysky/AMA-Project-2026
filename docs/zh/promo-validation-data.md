# 零售促销验证数据复用说明

## 为什么要复用 Hybrid AI 数据结构

原 AMA demo 最大弱点是数据过于 mock：价格、库存、销量、折扣和 ROI 之间没有可解释关系。retail promotion validation 的核心模式正好补这个洞：

> Data Layer（历史 SKU / 折扣 / measured lift）→ ML / Econometric Validator（预测 uplift、incremental profit、ROI）→ LLM Business Reasoning（生成候选促销）→ Human Approval。

因此本项目新增 `data/promo_validation/apparel_promo_history.csv`，作为 Pricing Agent 的促销验证数据源。

## 数据来源与定位

当前文件是 **retail promotion planning pattern 的服装 SKU 映射版 demo 数据**：

- 保留 促销验证数据结构：历史 SKU、折扣、销量 uplift、促销投入、incremental profit、profit ROI、stockout risk。
- 将超市/CPG 语义映射到服装零售：
  - `12-pack Soft Drinks` → `HEATTECH Crew Neck Innerwear 2-Pack`
  - `24-pack Soft Drinks` → `HEATTECH Kids Innerwear Set`
  - `Family Size Chips` → `Fleece Full-Zip Jacket`
  - `Granola Snack Bars` → `HEATTECH Scarf`
  - `Organic Eggs` → `Ultra Light Down Jacket`
  - `Premium Milk 1L` → `Warm Lined Pants`
- 这不是Contoso 服装店真实销售数据，不声称真实 ROI；它用于演示 Hybrid AI 的决策验证方法。

## 为什么这种映射是合理的

我们不是把“可乐改名成衣服”来伪装真实数据，而是复用数据结构和行为模式：

- 饮料促销峰值 → 保暖内衣在寒潮下的需求峰值
- 零食组合促销 → 围巾/抓绒等搭配型商品
- 生鲜短保质期风险 → 季节性外套/冬装窗口期风险
- 折扣 → measured lift → ROI → 审批，这条逻辑在零售服装也成立

## 代码接入点

- 数据：`data/promo_validation/apparel_promo_history.csv`
- Validator：`src/simulators/promotion_validator.py`
- 接入 Agent：`src/scenario_engine.py` 的 `Pricing Agent`

Pricing Agent 现在会：

1. 根据库存风险和竞品价格给出最终定价动作。
2. 用 Hybrid AI validator 验证最终动作。
3. 同时评估 LLM 可能生成的 5%、10%、15% 折扣候选方案。
4. 如果 ROI 为负、折扣过深、或高库存风险下折扣会放大断货，则打 risk flag。
5. 风险动作进入 human approval。

## 汇报时的诚实说法

建议说：

> We reused the Hybrid AI retail promotion planning data pattern and mapped it into apparel SKUs, so the prototype can demonstrate discount validation, predicted uplift, incremental profit, and ROI guardrails. This is simulation data for architecture validation, not claimed real Contoso Fashion performance data.

不要说：

> 这是Contoso 服装店真实数据。
> 这个 ROI 已经真实验证。
