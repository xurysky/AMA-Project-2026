# 46 号项目真实零售场景深度研究与查缺补漏

## 1. 研究结论

当前 46 号项目最大的问题不是技术栈，而是业务重心偏高：它把“全渠道个性化、动态定价、Customer 360、区域合规、多 Agent 协同”都放进来了，但真实零售企业最先愿意落地的通常不是一个全能 AI 大脑，而是一个能解决具体经营痛点的系统。

更合理的课题设计应该是：

**面向服装零售门店的商品经营异常决策系统**

也可以用更产品化的名字：

**Retail Merchandise Operations Copilot**

核心不是“AI 自动卖货”，而是：

- 发现门店/SKU/尺码/颜色级别的异常。
- 解释异常背后的库存、销售、天气、活动、渠道和履约原因。
- 给商品、运营、供应链、CRM 和门店团队生成可审批的动作包。
- 把审批后的动作写入 ERP/WMS/OMS/CRM/门店任务系统。
- 记录每一步证据、审批和执行回执。

## 2. 外部研究依据

### 2.1 UNIQLO/RFID 的启发

UNIQLO 的真实价值点不是“AI 自动营销”，而是把 RFID 贯穿制造、仓储、配送、门店、结账和退货，提升库存可见性和门店运营效率。

可借鉴点：

- 商品必须精确到 style / color / size，而不是只有大类 SKU。
- 库存准确性是全渠道、补货、门店履约和自助结账的基础。
- 门店员工需要的是“这件货在哪里、能不能卖、什么时候补到”，不是抽象的 AI 建议。
- 线上下单门店取货、门店发货、跨店调拨都依赖可信库存。

来源：

- Impinj, “How Uniqlo Tracks Style and Savings with RAIN RFID”

### 2.2 Microsoft Intelligent Order Management 的启发

Microsoft Dynamics 365 Intelligent Order Management 强调的是复杂供应链环境下的订单编排、库存可见性、履约优化、Provider 集成和 Power BI 洞察。

可借鉴点：

- 系统应作为业务系统之上的编排层，而不是替代现有 ERP/CRM/WMS。
- 订单、库存、履约、物流伙伴、渠道平台之间要通过 provider/API 连接。
- 业务团队需要可以配置流程和规则，而不是每次依赖 IT 改代码。
- 实时库存可见性和履约优化是零售系统的核心能力之一。

来源：

- Microsoft Learn, “Intelligent Order Management overview”

### 2.3 Microsoft Fabric 架构的启发

Microsoft Fabric 的现代数据平台架构强调多源数据接入、OneLake、Lakehouse/Warehouse、Eventstream、Real-Time Intelligence、Power BI、Purview、Entra ID、Key Vault 和 CI/CD。

可借鉴点：

- 真实零售系统会同时处理结构化、半结构化、流式和历史数据。
- POS、库存、CRM、天气、活动、订单、退货等数据不能只靠一个 mock JSON。
- Demo 可以用 Cosmos DB 做运行状态，但生产架构应把 Fabric 作为经营分析和 KPI 回流中心。
- Purview、Entra、Key Vault 和监控是企业可信架构的一部分。

来源：

- Microsoft Learn, “Analytics End-to-End with Microsoft Fabric”

### 2.4 国内时尚零售商品经营方案的启发

国内时尚零售方案普遍把核心链路描述为：

- 商品企划
- 预算采买 / OTB
- 销售预测
- 铺货 / 补货 / 调拨
- 清货 / 折扣
- 经营复盘

这说明服装零售的核心不是单点营销，而是“商品计划到门店执行”的连续闭环。

可借鉴点：

- 需要支持门店、区域、渠道、商品、尺码、颜色、波段和生命周期。
- 补货不是“销一补一”，而是重新分配销售机会。
- 清货不是“直接打折”，而是毛利、库存、门店、渠道和生命周期的联合判断。
- 系统应从一个关键场景试点，再扩展到企划、预测、铺补调闭环。

来源：

- 览众数据，“时尚零售智能商品决策解决方案”
- 第七在线行业文章目录：补货、调拨、全渠道配货、门店差异

### 2.5 Odoo 服装 ERP 场景的启发

服装零售不同于通用零售，因为一个款式会拆成颜色、尺码、版型、批次等变体。门店、电商、社媒下单、第三方平台必须共享一致库存，否则就会出现超卖、误导推荐、匆忙调拨和毛利失真。

可借鉴点：

- 产品主数据必须有 style-color-size 变体。
- 门店经理应能发起调拨、追踪收货和质检。
- 退货、换货、二次销售、奥莱转价会影响真实毛利。
- CRM 应保存偏好、尺码、面料敏感、营销授权等信息，但不能绕过授权触达。
- 用户验收测试应使用真实小票、退货单、网单和调拨单演练，而不是只测页面。

来源：

- Dasolo, “Odoo Clothing Store: Fashion Retail POS, Inventory & eCommerce”

### 2.6 Centric 补货策略的启发

时尚鞋服补货难点包括需求波动、仓储空间、调拨成本、交货周期、最小订购量、包装要求、新品初始配货和可持续库存压力。

可借鉴点：

- 补货必须考虑 lead time、门店容量、配送中心库存、销售窗口、毛利和调拨成本。
- 需求预测不能只看历史销售，还要考虑天气、活动、促销、突发事件和外部市场因素。
- 库存优化的目标是同时降低缺货和过剩，而不是单纯提高销售。
- AI 建议必须透明可解释，否则商品和供应链团队不会信任。

来源：

- Centric Software China，“一文详解时尚鞋服零售商的库存补货策略”

### 2.7 Bain GenAI 零售落地观点的启发

Bain 强调零售企业已经从 GenAI 试点进入规模化阶段，但规模化的关键不是孤立 demo，而是围绕 use case family、变革管理、员工赋能和可复用能力建设。

可借鉴点：

- GenAI 不应该只是一个聊天窗口，而要嵌入员工工作流。
- “Supercharged employees” 比“完全无人自治”更适合当前企业落地。
- 营销内容生成可以保留，但应作为具体业务动作的一部分。
- 评审中应说明如何从单场景扩展到用例族，而不是一开始就声称覆盖所有场景。

来源：

- Bain & Company, “Retail and Gen AI: Now Scale Those Terrific Early Returns”

## 3. 对现有项目的判断

### 应该保留

- Azure Container Apps + Cosmos DB + Azure OpenAI 的原型部署方式。
- 有状态 run、work order、approval、audit log 的设计。
- 多 Agent 作为能力模块的设计，但要弱化“人格化 Agent”。
- PIPL/PDPA/APPI/PIPA 的合规意识，但不要让区域合规喧宾夺主。
- GPT 实时生成能力，但用途要改成业务摘要、审批说明和任务说明。

### 应该弱化

- “全渠道个性化大脑”的叙事。
- “动态定价自动化”的表达。
- “销售 +40%、LTV +60%”这种像结果承诺的数字。
- Customer 360 的中心地位。
- “Agent 自动执行营销活动”的感觉。
- 过于复杂的跨国区域治理展示。

### 必须补强

- 门店和 SKU 颗粒度。
- 尺码、颜色、版型、生命周期、波段等服装变体逻辑。
- 补货、调拨、清货、保价、会员券的真实经营动作。
- 仓库库存、门店库存、在途库存、可售库存、锁定库存的区别。
- lead time、门店容量、调拨成本、配送可行性。
- 人工审批权限和阈值。
- 退货/换货/不可售库存对毛利和可售库存的影响。
- 下游系统边界：ERP、WMS、OMS、CRM、CDP、POS、门店任务系统。
- KPI 从业务大数改成过程指标和 test/control 验证指标。

## 4. 推荐的新课题设计

### 4.1 课题名称

建议从：

**Autonomous Retail Intelligence Agent Platform**

改成：

**AI-Powered Retail Merchandise Operations Copilot**

中文可以叫：

**AI 驱动的零售商品经营协同决策系统**

这个名字更稳，因为它没有承诺完全自治，也更贴近真实企业会购买的系统。

### 4.2 核心业务问题

不要问：

> 如何用 AI 实现全渠道个性化和自动化零售经营？

应该问：

> 当区域门店出现热销断码、库存错配、反季积压和会员触达机会时，AI 如何帮助商品、运营、供应链、CRM 和门店团队更快生成可执行、可审批、可追溯的经营动作？

### 4.3 主场景

**上海夏季热浪 AIRism 断码风险处理**

示例业务事实：

- 上海区域 38 家门店。
- 12 家核心门店 AIRism M/L 尺码库存覆盖低于 2 天。
- 华东仓有可用库存，但到店需要 36 小时。
- 3 家低动销门店库存充足，可做跨店调拨。
- 春季薄外套库存周转下降，但毛利不允许大范围折扣。
- CRM 可触达用户只限已授权会员。
- 门店店长需要确认陈列、试衣间反馈和实际断码。

这个场景足够具体，也能覆盖 46 号题目要求的 Agent、数据、Azure 架构、合规、业务价值。

### 4.4 扩展场景

主场景做好后，可以扩展三个相邻场景：

- 新品首配复盘：新品上市后 7 天，哪些门店补、哪些门店停、哪些尺码需要重分配。
- 反季清货：过季 SKU 如何在毛利护栏下做门店级、会员级、渠道级清货。
- 退货异常：某 SKU 退货率异常升高，是否是尺码、面料、质量或渠道描述问题。

## 5. 新系统模块

### 5.1 Exception Queue

第一屏展示经营异常，而不是战略概览。

异常类型：

- 缺货风险
- 断色断码
- 慢动销
- 库存错配
- 高退货率
- 不可履约推荐
- 毛利风险
- 未授权触达风险

每条异常必须有：

- 影响门店
- 影响 SKU / 颜色 / 尺码
- 销售机会
- 风险级别
- 推荐动作
- 审批状态

### 5.2 Decision Packet

每个异常生成一个决策包。

决策包包含：

- 业务摘要
- 触发原因
- 数据证据
- 可选动作
- 预计影响
- 风险和限制
- 推荐审批人
- 下游执行系统

### 5.3 Merchandise Agent Group

Agent 应按真实业务能力重组：

- Exception Detection Agent：识别异常。
- Inventory Position Agent：计算可售、在途、锁定、门店和仓库库存。
- Fulfillment Feasibility Agent：判断补货、调拨、门店发货和 ETA。
- Pricing & Margin Guardrail Agent：给折扣边界，不直接改价。
- Customer Eligibility Agent：筛选已授权会员和渠道。
- Store Ops Agent：生成店长任务。
- Decision Packet Agent：生成业务可读的决策包。
- Compliance & Audit Agent：门禁、权限、审计。

### 5.4 Human Approval Workflow

审批不应只是一个按钮，而是按动作风险分级：

- 自动通过：低风险信息查询、店长确认任务、库存盘点任务。
- 店长审批：本店陈列调整、本店货架补货。
- 区域运营审批：跨店调拨、门店优先级调整。
- 商品经理审批：SKU 生命周期、清货策略、主推商品保价。
- 财务/品类审批：超过阈值的折扣、毛利影响动作。
- CRM/合规审批：会员触达、人群包、优惠券预算。

### 5.5 Execution Connectors

Demo 可以 mock，但架构必须说明真实连接：

- ERP：调拨申请、采购建议、库存主账。
- WMS：仓库可用库存、拣货、出库、到店 ETA。
- OMS：订单、门店履约、BOPIS、ship-from-store。
- POS：门店销售、退货、换货、小票。
- CRM/CDP：会员授权、分群、活动草稿。
- Store Task App：店长确认、陈列调整、盘点任务。
- BI/Fabric：复盘指标和 test/control 实验。

## 6. 数据模型查缺补漏

现有 Demo 如果要变真实，至少需要这些对象：

### Product Variant

- style_id
- color
- size
- fit
- lifecycle_status
- season
- launch_date
- margin_floor
- markdown_stage

### Store

- store_id
- city
- district
- tier
- format
- floor_capacity
- replenishment_window
- transfer_group

### Inventory Position

- on_hand
- sellable
- reserved
- in_transit
- warehouse_available
- safety_stock
- days_of_cover

### Sales Signal

- sales_7d
- sales_14d
- sell_through_rate
- lost_sales_estimate
- return_rate
- fitting_room_signal
- app_view
- cart_add

### Work Order

- action_type
- target_system
- owner_role
- approval_threshold
- risk_level
- execution_status
- external_reference_id

### Consent-Aware Customer Segment

- segment_id
- eligible_count
- excluded_count
- exclusion_reasons
- allowed_channels
- coupon_budget

## 7. 真实 KPI 设计

不要把目标写成“Demo 已经证明销售 +40%”。应该分三层：

### 原型验证 KPI

- 系统能否生成完整决策包。
- 每个决策包是否包含证据、风险、审批人和执行目标系统。
- 审批和工单状态是否可追溯。
- GPT 输出是否能被业务字段约束。

### 试点运营 KPI

- 异常发现到决策包生成时间。
- 业务负责人平均判断时间。
- 高风险动作人工审批覆盖率。
- 不可触达人群剔除率。
- 不可履约推荐拦截率。

### 业务结果 KPI

这些必须通过 test/control 门店验证：

- 缺货率下降。
- 断码恢复时间缩短。
- 调拨成功率提升。
- 毛利损失下降。
- 慢动销库存周转改善。
- 会员触达转化率提升。

## 8. 评审叙事建议

### 开场

真实零售企业的问题不是缺少 Dashboard，而是经营动作分散在 ERP、WMS、POS、CRM、Excel、邮件和人工会议里。门店缺货、库存积压、折扣失控和会员触达经常互相影响，但决策过程缺少统一证据链。

### 价值主张

本项目设计一个 AI 驱动的商品经营协同决策系统。它从门店和商品异常开始，调用多个 Agent 形成可解释的决策包，再通过人工审批和系统连接把动作落到补货、调拨、清货、会员触达和门店任务中。

### 技术亮点

- Azure Container Apps 承载 Agent Runtime。
- Cosmos DB 保存运行状态、工单和审计。
- Azure OpenAI 生成业务摘要、审批说明和任务草稿。
- Fabric 作为经营分析、特征计算和 KPI 回流中心。
- Event Hubs / Fabric Real-Time Intelligence 接入实时 POS、库存和事件。
- APIM / Logic Apps / Functions 连接 ERP、WMS、OMS、CRM、POS。
- AI Search 检索商品政策、促销规则、SOP 和合规条款。

### 审慎表达

这不是一个完全自动经营系统，而是一个“人机协同的经营决策系统”。AI 负责发现异常、准备证据、提出建议和生成执行草稿；人负责高风险审批；业务系统负责最终执行；BI 负责结果回流。

## 9. 下一步改造建议

建议分三步改：

### 第一步：改业务叙事和文档

- 把 46 号 ADD 从“全渠道个性化平台”改成“商品经营协同决策系统”。
- 重写成功指标、系统边界、业务角色和主场景。
- 保留 Azure 架构，但调整服务映射。

### 第二步：改 Demo 数据和 API

- 新增 style-color-size 变体数据。
- 新增 store、inventory_position、sales_signal、customer_segment。
- run 不再代表“宏大季节活动”，而是代表一个具体异常处理单。
- GPT 生成从营销文案改成业务摘要、审批理由和门店任务说明。

### 第三步：改前端

- 默认页改成 Exception Queue。
- 详情页改成 Decision Packet。
- 审批页按角色和阈值展示。
- 执行页展示 mock ERP/WMS/CRM/Store Task 回执。
- KPI 页展示试点指标，而不是理想化大目标。

## 10. 最终判断

这个课题可以做得更深，但必须把深度放在真实业务闭环上，而不是放在更多 Agent 名称上。

最强的一版应该是：

> 用 AI Agent 把服装零售中“门店异常、商品判断、库存履约、折扣毛利、会员触达、人工审批、执行留痕”这一条真实经营链路做成可运行的 Azure 原型。

这样既能满足 46 号题目对 AI Agent 和 Azure 架构的要求，又不会显得像脱离现实的万能零售大脑。

## 11. 第二轮行业方案补充研究

继续对照 RELEX、Blue Yonder、Oracle Retail、SAP Retail、o9 等成熟行业方案后，可以看到真实零售解决方案的能力地图非常稳定：

- Merchandise Financial Planning / OTB：商品财务计划和采买预算。
- Assortment Planning：商品组合、店群、季节、价格带、颜色尺码。
- Allocation：新品和稀缺库存的初始配货。
- Replenishment：基于需求和库存水位的持续补货。
- Markdown Optimization：生命周期、毛利和清货目标下的降价策略。
- Space / Planogram：陈列空间、货架容量和视觉陈列。
- Store Execution：门店任务、收货、盘点、上架、陈列检查。
- Workforce / Workload：门店员工工时和任务负载。
- S&OP / S&OE：销售运营计划和短周期执行协调。

这说明 46 号项目如果要更像真实零售系统，不能只讲 Agent 和推荐，还要把这些经营约束放进设计。

补充来源：

- RELEX：端到端计划、预测、补货、空间、价格促销、门店执行。
- Blue Yonder：Allocation & Replenishment，Push/Pull 库存执行逻辑，短生命周期时尚商品配货。
- Oracle Retail：Assortment Planning，门店集群、季节性目标、空间和地理差异。
- SAP Retail：Forecasting & Replenishment，DIF 需求影响因子、异常处理、多级补货、鲜品损耗。
- o9：Markdown Optimization，生命周期、价格弹性、分层降价、what-if 场景。

## 12. 新发现的关键查缺补漏

### 12.1 OTB 和预算约束

现有设计主要关注“建议做什么”，但真实商品经营一定受预算限制。

需要补：

- 本季 OTB 剩余额度。
- 补货动作是否占用采购预算或调拨预算。
- 清货动作是否影响既定毛利目标。
- 活动优惠券是否占用 CRM campaign budget。

如果没有预算约束，系统建议容易显得“拍脑袋”。

### 12.2 长生命周期和短生命周期商品要分开

成熟方案会区分 basics / carryover / seasonal / fashion / limited items。

需要补：

- AIRism、HEATTECH 这种核心基础款可以持续补货。
- 联名款、流行色、短季节商品更适合分配和清货，而不是无限补货。
- 过季商品应进入 markdown lifecycle，而不是继续按常规补货。

Demo 里每个 SKU 要有 lifecycle_type：

- basic_replenishable
- seasonal_core
- fashion_short_lifecycle
- limited_drop
- clearance

### 12.3 Allocation 和 Replenishment 不是一回事

真实零售里：

- Allocation 是“推”：新品、首配、稀缺货量，决定先给谁。
- Replenishment 是“拉”：根据销售和库存水位持续补。

现有设计把补货、调拨、首配混在一起了。

需要在 Agent 里分开：

- Allocation Agent：新货或稀缺货的门店分配。
- Replenishment Agent：持续补货和安全库存。
- Transfer Agent：跨店调拨和库存再平衡。

### 12.4 门店集群和尺码曲线

服装零售不能只看门店总销量。不同门店有不同尺码曲线、客群和空间。

需要补：

- store_cluster：旗舰店、社区店、商场店、郊区店、奥莱店。
- size_curve：S/M/L/XL 或儿童年龄段分布。
- broken_size_risk：断码导致可售库存看起来有货但实际不可卖。
- true_rate_of_sale：剔除断货天数、异常折扣和清货噪音后的真实销售速度。

这会让 Demo 立刻更像服装行业，而不是通用库存系统。

### 12.5 空间和陈列约束

成熟零售方案一定会考虑 space / planogram。

需要补：

- 门店货架/陈列容量。
- 是否有主推陈列位。
- 补货后是否有地方上架。
- 清货是否释放陈列空间给新品。
- 店长是否完成陈列调整任务。

如果只建议“补 2,600 件”但不考虑门店放不放得下，就不真实。

### 12.6 门店任务负载和人员约束

真实门店执行失败，经常不是因为总部不知道该做什么，而是门店没时间做。

需要补：

- 当日门店任务量。
- 收货、上架、盘点、拣货、陈列调整所需工时。
- 高峰客流时段不能安排重任务。
- 店长确认任务要有 SLA。

Store Ops Agent 不应该只是审批角色，而要生成可执行任务和工时估算。

### 12.7 Phantom Inventory 和库存可信度

行业里经常出现 phantom inventory：系统显示有货，但实物不存在、损坏、丢失、放错位置或不可售。

需要补：

- inventory_confidence_score。
- last_cycle_count_time。
- shrink_risk。
- damaged_or_unsellable_qty。
- location_unknown_qty。
- RFID / manual count evidence。

如果库存可信度低，Agent 不应直接建议营销触达，而应先派发盘点或找货任务。

### 12.8 退货和换货

服装零售退货率高，退货会影响库存、毛利、可售性和商品判断。

需要补：

- return_rate。
- return_reason。
- resellable_return_qty。
- damaged_return_qty。
- channel_return_mismatch：线上买、门店退、库存归属变化。

某 SKU 如果高退货，不应该只看销量好就补货，可能是尺码、面料、图片描述或质量问题。

### 12.9 促销和 markdown 要分开

促销是临时刺激，markdown 是生命周期降价。两者不能混用。

需要补：

- promotion_discount：短期活动、券、会员专享。
- markdown_stage：季末/生命周期降价。
- clearance_goal：清完库存、保护毛利、释放空间。
- price_elasticity：降价是否真的能带来需求。
- markdown_ladder：分层降价节奏。

AI 不应该说“打 20% 折”，而要说明这是 promotion 还是 markdown，目标是拉动需求、清库存还是保护毛利。

### 12.10 Fresh / Grocery 不适合作为主线，但可作为扩展

如果做商超/鲜品，会多出保质期、损耗、临期折扣、日内补货、报损和废弃物管理。这个方向也真实，但会把课题复杂度拉高。

建议：

- 主线继续用服装零售，因为与你之前的优衣库/时尚零售叙事一致。
- 文档里可以提一句系统可扩展到 fresh retail，但 Demo 不切换主赛道。

## 13. 第二轮后更新的目标架构判断

推荐把系统拆成四层，而不是只讲 5 个 Agent：

### 13.1 Planning Context Layer

回答“业务目标和约束是什么”。

- Merchandise financial plan
- OTB / budget
- assortment plan
- store cluster
- product lifecycle
- price and margin policy

### 13.2 Operational Signal Layer

回答“现在发生了什么”。

- POS sales
- inventory position
- returns
- RFID / cycle count
- weather
- promotions
- web/app demand signal
- store task status

### 13.3 Agent Decision Layer

回答“应该建议什么动作”。

- Exception Detection
- Allocation
- Replenishment
- Transfer
- Markdown
- Customer Eligibility
- Store Execution
- Compliance & Audit

### 13.4 Execution & Feedback Layer

回答“动作有没有执行、有没有效果”。

- ERP / WMS / OMS / CRM / POS connectors
- store task app
- approval workflow
- execution receipt
- Fabric / Power BI KPI feedback

## 14. 对 Demo 的新增改造要求

下一版 Demo 至少要能展示这些点：

- 一个 AIRism 主推款分成颜色和尺码，而不是一个 SKU。
- 同一个商品在不同门店有不同尺码需求和库存覆盖。
- 系统能识别“总库存够，但 M/L 断码”的异常。
- 系统能区分“补货、调拨、清货、会员券、盘点任务”。
- 系统能因库存可信度低而先派发盘点任务。
- 系统能因门店任务负载过高而调整到货/上架 SLA。
- 系统能说明折扣是促销还是 markdown。
- 系统能显示预算和毛利护栏。
- 系统能生成下游系统回执：ERP transfer request、WMS pick ticket、CRM audience draft、Store task。

## 15. 评委可能追问的问题

### 问：这个系统和 ERP/WMS/CRM 的边界是什么？

答：本系统不是交易主账，不替代 ERP/WMS/CRM。它是决策编排和协同层，读取业务系统数据，生成建议和审批工单，审批后通过 API / Logic Apps / APIM 写回下游系统。

### 问：为什么不用完全自动化？

答：库存查询、低风险盘点任务可以自动化；调拨、折扣、会员触达涉及毛利、预算、门店执行和合规，需要 human-in-the-loop。系统先提高判断速度和一致性，再逐步提高自动化比例。

### 问：为什么主线不是 Customer 360？

答：Customer 360 重要，但零售履约的前提是“货准、货在、货能履约”。如果库存、尺码、门店和调拨不可信，个性化推荐会制造更差体验。因此主线从商品经营异常开始，CRM 触达是审批后的动作之一。

### 问：Agent 的价值在哪里？

答：Agent 的价值不是替代规划系统，而是把分散在商品、供应链、门店、CRM 和合规团队之间的判断组织成一个可解释、可审批、可追溯的决策包，并能调用下游工具执行。

### 问：怎么证明效果？

答：先用原型验证流程完整性，再用 test/control 门店验证缺货率、断码恢复时间、调拨成功率、清货毛利、任务完成 SLA 和会员触达转化。

## 16. 回到课题 46：五个 Agent 和四层架构如何结合

课题 46 原本要求的是一个由五个 AI Agent 驱动的智能零售平台：

- Customer Understanding Agent
- Personalization Agent
- Inventory Agent
- Pricing Agent
- Marketing Agent

第二轮研究提出的四层架构不是替代这五个 Agent，而是给这五个 Agent 加上真实企业落地所需的上下文、数据、执行和反馈边界。

一句话：

> 四层架构是系统落地骨架，五个 Agent 是贯穿四层的业务决策能力；Agent 的推理和编排核心集中在 Agent Decision Layer，但每个 Agent 都必须读取上层约束、消费事实信号、输出执行动作并接收反馈。

### 16.1 四层架构的职责

四层架构回答四个企业真实问题：

1. Planning Context Layer：业务目标和约束是什么？
2. Operational Signal Layer：现在门店和商品发生了什么？
3. Agent Decision Layer：五个 Agent 如何生成建议？
4. Execution & Feedback Layer：建议如何审批、执行、回流？

所以，四层架构不是新增四个模块来取代 Agent，而是让 Agent 不再“凭空智能”，而是在真实业务约束中工作。

### 16.2 五个 Agent 与四层的正确关系

更准确的模型不是“把五个 Agent 单独放在第三层”，也不是“每一层各塞五个 Agent 副本”。

最合适的模型是：

> Agent Runtime / Orchestration 位于第三层；Agent Capability 生命周期贯穿四层。

也就是说：

- Planning Context Layer：给每个 Agent 提供业务约束。
- Operational Signal Layer：给每个 Agent 提供实时和历史事实。
- Agent Decision Layer：五个 Agent 在这里完成推理、协作、冲突处理和决策包生成。
- Execution & Feedback Layer：每个 Agent 的建议通过工单和 connector 落地，并把结果反馈给下一轮判断。

所以，从部署架构看，Agent 在第三层；从业务能力看，Agent 贯穿四层。

这个表达最准确，也最容易向评委解释。

#### Planning Context Layer

这一层主要给 Agent 提供约束，不是 Agent 自己的舞台。

输入包括：

- OTB / 预算
- 商品生命周期
- 店群策略
- 尺码曲线
- 毛利底线
- 陈列空间
- 促销日历
- 区域政策和合规规则

对应到五个 Agent：

- Inventory Agent 读取安全库存、门店容量、补货窗口。
- Pricing Agent 读取毛利底线、markdown 阶段、折扣审批阈值。
- Marketing Agent 读取 campaign budget、渠道日历、会员券预算。
- Personalization Agent 读取可推荐商品范围和不可履约约束。
- Customer Understanding Agent 读取授权规则、客户分群口径和隐私边界。

#### Operational Signal Layer

这一层给 Agent 提供事实。

输入包括：

- POS 销售
- RFID / 盘点
- 门店库存
- 仓库库存
- 在途库存
- 退货/换货
- App 浏览、收藏、加购
- 试衣间信号
- 天气和活动
- 门店任务完成情况

对应到五个 Agent：

- Inventory Agent 消费最多的事实数据：库存、销售、在途、退货、盘点。
- Customer Understanding Agent 消费会员行为、购买历史、授权状态。
- Personalization Agent 消费 App 行为、试穿、库存可用性。
- Pricing Agent 消费销售速度、库存压力、退货率、竞品价格。
- Marketing Agent 消费人群规模、活动表现、渠道触达状态。

#### Agent Decision Layer

这是五个 Agent 真正工作的层。

五个 Agent 不需要换掉，但职责要从“理想化全能”调整为“真实业务约束下的决策专家”。

##### Inventory Agent

从“自动补货 Agent”升级为：

**Inventory / Allocation / Replenishment Agent**

核心问题：

- 哪些门店和尺码有断货风险？
- 是补仓、跨店调拨，还是先盘点？
- 这件商品是基础款、季节款、短生命周期款，还是清货款？
- 当前库存可信度够不够？
- 到店 ETA 和门店收货能力是否支持？

输出：

- stockout risk
- broken size risk
- replenishment proposal
- transfer proposal
- cycle count task
- inventory confidence score

##### Pricing Agent

从“动态定价 Agent”调整为：

**Pricing / Margin / Markdown Guardrail Agent**

核心问题：

- 这个动作是促销还是 markdown？
- 是否低于毛利底线？
- 当前生命周期是否允许清货？
- 应该保价、轻促销、阶梯 markdown，还是禁止折扣？
- 需要谁审批？

输出：

- margin guardrail
- promotion boundary
- markdown ladder
- approval level
- price risk explanation

##### Customer Understanding Agent

从“Customer 360 大而全”调整为：

**Consent-aware Customer & Demand Signal Agent**

核心问题：

- 哪些会员真实有购买意图？
- 哪些用户可以被合法触达？
- 哪些用户要排除？
- 行为信号是否能支持营销动作？
- 高退货或投诉是否说明商品问题？

输出：

- eligible audience
- excluded audience and reasons
- intent segment
- consent status
- return / complaint signal

##### Personalization Agent

从“千人千面推荐 Agent”调整为：

**Fulfillable Personalization Agent**

核心问题：

- 推荐的商品当前能不能履约？
- 是否存在断码、不可售、库存可信度低？
- 是否应该推荐替代尺码、替代颜色、附近门店或线上发货？
- 是否应该先阻断推荐，避免制造差体验？

输出：

- next best product
- substitute recommendation
- pickup / ship-from-store option
- recommendation blocked reason
- customer-facing rationale

##### Marketing Agent

从“自主营销 Agent”调整为：

**Campaign Draft & Store Activation Agent**

核心问题：

- 这次是否应该触达会员，还是只做门店动作？
- 触达渠道是 App Push、短信、企微、邮件，还是门店导购任务？
- 是否有足够库存承接活动？
- campaign budget 是否够？
- 是否需要 CRM/合规审批？

输出：

- campaign draft
- channel plan
- store activation task
- coupon budget impact
- A/B test proposal

#### Execution & Feedback Layer

这一层保证 Agent 建议不是停留在页面上。

输出到下游系统：

- ERP：调拨申请、采购建议、库存主账引用。
- WMS：拣货单、出库单、到店 ETA。
- OMS：BOPIS、门店发货、订单履约状态。
- CRM/CDP：人群包、活动草稿、触达排除名单。
- Store Task App：店长盘点、陈列调整、收货上架任务。
- Fabric / Power BI：结果复盘和 test/control KPI。

五个 Agent 输出的是领域决策，不应各自创建重复工单。只有经过 Orchestrator 聚合、规则校验和人工审批后的动作，才转换成一个或多个下游 work order，并统一接收执行回执。

### 16.3 五个 Agent 的协同流程

推荐 Demo 流程如下：

1. Operational Signal Layer 发现上海 12 家门店 AIRism M/L 码库存覆盖低于 2 天。
2. Inventory Agent 判断是断码风险，不是简单总库存不足；同时发现两家门店库存可信度低。
3. Inventory Agent 先生成两个动作：一是跨店调拨，二是盘点确认。
4. Pricing Agent 判断 AIRism 是 in-season core，不允许 markdown，只允许保价；春季薄外套进入 clearance，可给 15% 会员券。
5. Customer Understanding Agent 筛出已授权、近 14 天有浏览/加购/试穿行为的会员，同时剔除未授权和不可履约区域用户。
6. Personalization Agent 只推荐有库存、可到店取货或可调拨履约的颜色和尺码。
7. Marketing Agent 生成活动草稿，但不直接发送；同时生成门店导购任务。
8. 平台控制面中的 Policy Engine 和 Orchestrator 检查权限、预算、合规、PII 脱敏、数据时效和审批路径；它们是跨领域平台能力，不计入五个业务 Agent。
9. 业务负责人审批后，系统写入 ERP/WMS/CRM/Store Task mock 回执。
10. Fabric / Power BI 回流缺货率、调拨成功率、任务 SLA、转化率和毛利影响。

### 16.4 课题 46 里的五个 Agent 不建议改名，但建议改解释

为了贴合课题，公开文档和评审里仍然保留五个 Agent 名称。

但解释方式要变：

- Customer Understanding Agent：不是泛泛 Customer 360，而是 consent-aware demand and eligibility。
- Personalization Agent：不是无限推荐，而是 fulfillment-aware personalization。
- Inventory Agent：不是只做预测，而是 allocation / replenishment / transfer / inventory confidence。
- Pricing Agent：不是自动改价，而是 pricing, margin and markdown guardrail。
- Marketing Agent：不是自动投放，而是 campaign draft, store activation and budget approval。

这样既保留课题 46 的多 Agent 要求，又把逻辑落回真实零售经营。

### 16.5 最终建议表达

评审时可以这样讲：

> Project 46 is still a five-agent retail intelligence platform. The redesign does not remove the five agents. Instead, it gives each agent a full decision lifecycle across a four-layer enterprise architecture: planning context, operational signals, agent decisions, and execution feedback. The agent runtime and orchestration are concentrated in the decision layer, while each agent reads constraints from planning, consumes facts from operations, produces decision packets, and receives execution feedback.

中文表达：

> 这仍然是五个 Agent 驱动的智能零售平台。四层架构不是替代五个 Agent，而是给每个 Agent 一个完整的企业决策生命周期：先读取商品计划、预算、门店策略和合规约束，再消费 POS、库存、RFID、退货和会员行为信号，然后在 Agent Decision Layer 完成协同推理和决策包生成，最后通过审批、ERP/WMS/CRM/门店任务系统执行并回流 KPI。

### 16.6 五个 Agent 贯穿四层的矩阵

| Agent | Planning Context 读取什么 | Operational Signal 消费什么 | Decision Layer 生成什么 | Execution & Feedback 落地什么 |
| --- | --- | --- | --- | --- |
| Customer Understanding Agent | 授权规则、会员分群口径、隐私边界 | 购买、浏览、加购、退货、投诉、渠道偏好 | 可触达人群、高意向分群、排除原因 | CRM/CDP 人群包、触达排除名单、转化/投诉回流 |
| Personalization Agent | 可推荐商品范围、履约规则、门店策略 | 可售库存、断码、门店履约、App/试穿行为 | 可履约推荐、替代尺码/颜色、阻断理由 | App/小程序推荐草稿、门店导购建议、推荐效果回流 |
| Inventory Agent | 安全库存、店群、尺码曲线、门店容量、补货窗口、OTB/补货预算 | POS、RFID、仓库库存、在途、退货、盘点 | 补货、调拨、盘点、断码风险、库存可信度 | ERP 调拨申请、WMS 拣货单、门店盘点/收货任务、缺货率回流 |
| Pricing Agent | 毛利底线、商品生命周期、markdown/促销预算与策略 | 销售速度、库存压力、竞价、退货、折扣表现 | 保价、促销、markdown 阶梯、审批级别 | 价格/促销草稿、财务/品类审批、毛利和清货结果回流 |
| Marketing Agent | 活动预算、渠道日历、触达频控、合规规则 | 可触达人群、库存承接能力、渠道表现、门店任务状态 | 活动草稿、渠道组合、券预算、A/B test | CRM 活动草稿、App Push/短信审批、门店激活任务、转化率回流 |

这个矩阵是最适合写进 ADD 和答辩材料的版本，因为它同时回答了两个问题：

- 课题 46 的五个 Agent 没有丢。
- 五个 Agent 不再漂浮在架构图里，而是被真实零售业务的计划、信号、执行和反馈闭环约束住。

## 17. 最终推荐：以经营 Case 为核心的五 Agent × 四层集成架构

### 17.1 架构判断

五个 Agent 与四层架构的最佳结合方式，不是把五个 Agent 在每一层各部署一遍，也不是让五个 Agent 只在第三层串行调用，而是：

> 四层承载一个经营 Case 的完整生命周期，五个 Agent 作为领域决策能力按 Case 类型动态参与；Orchestrator、Policy Engine、Case Store 和 Human Approval 作为共享控制面贯穿全流程。

这里有三个不同概念：

- 四层是企业系统的职责边界，回答数据、决策和动作分别在哪里发生。
- 五个 Agent 是业务决策域，回答谁负责库存、价格、客户、推荐和营销判断。
- Retail Decision Case 是两者的集成单位，回答多个 Agent 如何围绕同一个门店问题协同，而不是各自产生互相冲突的动作。

因此，架构图应表现为“四个横向层 + 五条领域能力纵向贯穿 + 一个共享 Case 控制面”，而不是简单的 5 × 4 方格。

### 17.2 四层的重新定义与明确边界

#### Layer 1: Planning Context & Policy

这一层保存已经由业务负责人确定的约束，不做实时 Agent 推理。

- 商品：品类、颜色尺码、生命周期、首配/补货属性、季节、成本和毛利底线。
- 门店：店群、容量、陈列位、收货窗口、服务能力和人员负载上限。
- 计划：MFP、OTB、促销日历、补货预算、物流能力和渠道预算。
- 治理：PIPL、会员授权、频控、审批矩阵、价格权限和审计保留策略。

系统原则：Agent 可以解释和引用这些约束，但不能自行改写预算、毛利底线、会员授权或审批权限。

#### Layer 2: Operational Signals & Case Formation

这一层把来源不同、时效不同的数据标准化成可判断的经营事实，并创建 Case。

- 输入：POS、RFID/盘点、ERP/WMS/OMS、退货、App 行为、天气、活动、门店任务状态。
- 数据处理：时间对齐、门店/SKU/颜色/尺码主数据映射、去重、质量评分和 freshness 检查。
- 异常检测：断码、缺货风险、库存积压、库存不可信、退货异常、履约能力不足。
- Case 形成：固定 `as_of_time`、影响对象、证据快照、严重度、SLA 和主责 Agent。

关键现实约束：系统不能把昨晚的库存、当前的订单和明天的天气混成一个“实时事实”。每个 Case 必须显示数据时间和库存可信度；低可信度库存先生成盘点任务，不直接触发调拨或营销。

#### Layer 3: Multi-Agent Decision & Orchestration

这一层部署五个 Agent 的 runtime，但协作不是固定全量串行，而是由 Case 类型决定参与者和依赖关系。

- Orchestrator 根据 Case 类型选择 lead Agent 和 supporting Agents。
- 每个 Agent 读取同一个不可变 Case Snapshot，输出结构化 Domain Decision。
- Policy Engine 用确定性规则检查预算、库存、毛利、授权、权限和动作冲突。
- Orchestrator 将多个 Domain Decision 合并为一个 Decision Packet。
- 人工可以批准、驳回、修改数量或要求补充证据，但修改必须留痕。

LLM 适合生成解释、归纳证据和处理非结构化 SOP；库存数量、毛利、授权、预算和审批级别必须由规则、SQL 或优化模型计算，不能由 LLM 猜测。

#### Layer 4: Controlled Execution, Store Operations & Learning

这一层只执行已批准动作，并验证现实世界是否真正完成。

- ERP/WMS/OMS：调拨申请、拣货、出库、ETA、到店和履约状态。
- Pricing/Promotion System：价格或会员券草稿、有效期和审批结果。
- CRM/CDP：已授权人群包、排除名单、活动草稿和触达回执。
- Store Task App：盘点、收货、上架、陈列、导购跟进任务。
- Fabric/Power BI：缺货率、调拨成功率、任务 SLA、毛利、退货和 test/control 结果。

动作必须使用 `case_id + action_id` 作为幂等键。失败动作进入重试或人工处理队列，不能因为 Agent 重跑而重复发券、重复调拨或重复触达。

### 17.3 五个 Agent 如何真实融入四层

#### Inventory Agent：商品可得性与履约主责

- Context 接口：读取安全库存、店群、尺码曲线、陈列容量、补货窗口、OTB/补货预算和供应链能力。
- Signal 订阅：POS、RFID、可用库存、在途、退货、盘点差异和订单占用。
- Decision 职责：判断 stockout、broken-size、overstock、phantom inventory；比较仓补、店间调拨、延迟补货和不动作方案。
- Action 合同：只生成调拨/补货/盘点建议，不直接修改库存主账。
- Feedback：调拨接受率、到货准时率、缺货率、库存准确率和售罄率。

它通常是缺货和积压 Case 的 lead Agent，也是 Personalization、Pricing 和 Marketing 的库存事实提供者。

#### Pricing Agent：价格、促销与毛利护栏主责

- Context 接口：读取成本、毛利底线、生命周期、价格带、markdown/促销预算和审批权限。
- Signal 订阅：库存压力、售速、退货、历史折扣效果、竞品价格和活动冲突。
- Decision 职责：区分保价、短期 promotion 和生命周期 markdown；给出折扣范围、财务影响和审批级别。
- Action 合同：只生成价格/促销草稿；超过阈值必须由品类或财务审批。
- Feedback：实际毛利、清货率、折扣渗透率、价格投诉和促销增量。

它不能因为高温和需求暴增自动涨价，也不能为了清库存绕过品牌价格策略。

#### Customer Understanding Agent：授权需求与客户风险主责

- Context 接口：读取授权用途、分群口径、数据驻留、频控和敏感属性禁用规则。
- Signal 订阅：购买、浏览、加购、试穿、退货、投诉和渠道偏好。
- Decision 职责：输出高意向人群、可触达状态、排除原因和需求证据；识别高退货/投诉是否提示商品问题。
- Action 合同：只输出 audience eligibility，不输出最终商品或营销内容。
- Feedback：授权命中率、投诉率、退订率、转化和分群漂移。

Customer 360 在这里是受用途约束的数据视图，不是无限收集的统一画像。

#### Personalization Agent：供需交集与下一最佳商品主责

- Context 接口：读取可推荐商品范围、替代规则、门店服务和履约策略。
- Signal 订阅：Customer Understanding 的 eligible audience、Inventory 的 fulfillment envelope、Pricing 的 commercial envelope，以及实时会话行为。
- Decision 职责：计算“这个客户在这个渠道现在能看到什么”，输出可履约商品、替代颜色/尺码/门店和阻断理由。
- Action 合同：输出 recommendation set 或导购建议，不直接触达客户。
- Feedback：曝光、点击、加购、履约成功、取消、退货和推荐阻断率。

它是三个决策集合的交集：`eligible customer ∩ fulfillable SKU ∩ allowed price`。

#### Marketing Agent：渠道动作与门店激活主责

- Context 接口：读取渠道预算、活动日历、频控、品牌模板、门店任务能力和审批规则。
- Signal 订阅：eligible audience、recommendation set、可承接库存、价格方案和门店执行状态。
- Decision 职责：判断是否需要营销；若需要，生成渠道、节奏、预算、A/B test 和门店激活方案。
- Action 合同：输出 CRM campaign draft、券申请或 Store Task，不直接发送。
- Feedback：送达、转化、增量、券核销、频控投诉、库存承接和门店完成率。

Marketing Agent 是链路末端的可选参与者。库存不足、无合格人群或门店无执行能力时，应输出 `NO_CAMPAIGN`，而不是强行生成文案。

### 17.4 真实业务中的 Agent 依赖关系

以上海 AIRism M/L 码断码 Case 为例，推荐依赖图如下：

```text
POS / RFID / OMS / Weather
            |
            v
Case Formation: SH-AIRISM-BROKEN-SIZE
            |
            v
Inventory Agent (lead)
  |-- inventory confidence low --> Store cycle-count task --> wait for result
  |-- inventory confirmed -------> fulfillment envelope
                                      |               |
                                      v               v
                              Pricing Agent    Customer Understanding Agent
                              commercial       eligible audience
                              envelope         envelope
                                      \               /
                                       v             v
                                     Personalization Agent
                                     recommendation set
                                              |
                                              v
                                      Marketing Agent (optional)
                                      campaign/store task draft
                                              |
                                              v
                             Policy check -> Human approval -> Execution
                                              |
                                              v
                                     Receipt and KPI feedback
```

这个流程包含三个真实分支：

1. 库存可信度不足：先盘点，Case 进入 `WAITING_FOR_STORE_CONFIRMATION`，暂停营销。
2. 仓库可补但 36 小时后才到：Personalization 只能推荐当前可履约门店或替代款，不能把未来库存当现货。
3. 没有足够库存承接活动：Marketing Agent 输出 `NO_CAMPAIGN`，系统只执行补货/调拨和门店任务。

### 17.5 Case 与 Agent 的结构化契约

每个 Agent 不通过自由文本互相“聊天”，而是围绕共享 Case State 交换版本化对象。

Case 最少包含：

- `case_id`, `case_type`, `status`, `severity`, `sla_due_at`
- `as_of_time`, `region`, `store_cluster`, `sku_color_size_scope`
- `evidence_refs`, `data_freshness`, `inventory_confidence`
- `planning_policy_version`, `consent_policy_version`
- `lead_agent`, `required_agents`, `optional_agents`

Domain Decision 最少包含：

- `agent_name`, `decision_version`, `recommendation`, `alternatives`
- `evidence_refs`, `rules_applied`, `model_version`, `confidence`
- `constraints_checked`, `blockers`, `expires_at`
- `proposed_actions`, `required_approval_role`

最终 Decision Packet 最少包含：

- 业务问题和影响门店/SKU。
- 推荐动作、备选动作和“不动作”方案。
- 库存、毛利、预算、授权和门店负载证据。
- 哪些判断由规则/模型产生，哪些文字由 LLM 解释。
- 审批人、动作有效期、下游系统和回滚/补偿方式。

### 17.6 Orchestrator 不是第六个业务 Agent

Orchestrator 属于平台控制面，职责是：

- 根据 Case 类型加载 workflow template。
- 选择 lead/supporting Agents 并管理依赖、超时和重试。
- 固定 Case Snapshot，防止不同 Agent 使用不同时点的数据。
- 检测冲突，例如 Marketing 想扩大触达但 Inventory 无法承接。
- 聚合 Domain Decision，生成唯一 Decision Packet。
- 维护 `NEW -> ANALYZING -> WAITING_FOR_CONFIRMATION -> WAITING_FOR_APPROVAL -> EXECUTING -> COMPLETED/FAILED` 状态机。

Policy Engine、审批流、审计和可观测性同样是共享平台能力，不应为了让架构看起来更“Agentic”而继续增加 Agent 数量。

### 17.7 不同 Case 不应强制调用全部五个 Agent

- 断码/缺货：Inventory 为 lead；Pricing、Personalization 参与；只有满足库存承接条件时才调用 Customer Understanding 和 Marketing。
- 反季积压：Inventory 为 lead；Pricing 必须参与；Customer Understanding、Personalization、Marketing 根据清货策略参与。
- 高退货异常：Customer Understanding 与 Inventory 联合 lead；先检查商品质量、尺码描述和库存批次，默认不启动营销。
- 会员触达机会：Customer Understanding 为 lead；Inventory、Pricing、Personalization 是前置门禁；Marketing 负责渠道动作。
- 库存不可信：Inventory 单独处理，生成盘点任务；确认前不调用下游营销链路。

这种按需编排比“五个 Agent 每次都跑一遍”更节省成本，也更符合真实组织分工和故障隔离要求。

### 17.8 决策权与人工审批边界

- 自动执行：只读查询、异常创建、低风险盘点任务、解释生成、KPI 回流。
- 业务审批：跨店调拨、补货数量变更、门店陈列任务、活动人群和渠道方案。
- 品类/财务审批：价格变化、markdown、券预算、超过阈值的营销投入。
- 合规门禁：未授权触达、敏感属性使用、跨区域数据访问直接阻断，不能由业务审批覆盖。
- 系统禁止：Agent 直接改库存主账、直接修改生产价格、直接群发消息、删除审计记录。

### 17.9 Azure 落地映射

- Layer 1：Fabric OneLake / Warehouse 保存计划与历史；Azure AI Search 保存 SOP 和政策；主数据仍以 ERP/商品系统为准。
- Layer 2：Event Hubs 接收事件；Fabric Real-Time Intelligence / Data Factory 做标准化；Azure Functions 或规则作业创建 Case。
- Layer 3：Azure AI Foundry Agent Service 承载五个 Agent 和 tracing；Container Apps 承载 Orchestrator/API；Cosmos DB 保存 Case State；Azure ML 承载预测和优化模型。
- Layer 4：APIM + Logic Apps / Functions 连接 ERP、WMS、OMS、CRM 和 Store Task；Power BI 复盘 KPI；Application Insights 追踪 Agent、规则和执行链路。
- Cross-cutting：Managed Identity、Key Vault、Private Link、Purview、RBAC、PII masking 和 immutable audit log。

原型不需要假装已经接入所有生产系统。Demo 可以使用结构真实的 synthetic snapshot 和 mock connector，但必须展示 Case Snapshot、决策依赖、审批、幂等动作和执行回执。

### 17.10 最终架构表述

建议最终命名为：

**Retail Decision Case Platform: Five-Agent Decision Lifecycle on a Four-Layer Enterprise Architecture**

中文：

**零售经营决策 Case 平台：基于四层企业架构的五 Agent 协同闭环**

最终的一句话叙事是：

> 系统不是让五个 Agent 分别经营零售，而是把真实门店异常固化成一个有数据快照、业务约束、责任人和 SLA 的经营 Case；五个 Agent 在统一 Case 上分别完成库存、价格、客户、推荐和营销判断，平台通过规则门禁、人工审批和下游回执把建议变成可审计、可执行、可复盘的业务动作。

## 18. 系统改造前的最终查缺补漏

### 18.1 本轮研究结论

继续对照 GS1、SAP Retail、Dynamics 365 Inventory Visibility、RELEX、Manhattan Active、NIST AI RMF、Microsoft Fabric 和 Azure Architecture Center 后，业务范围不需要继续扩大。服装零售主线、五个 Agent 和四层 Case 架构已经足够完整。

最后的缺口主要不在“还缺哪个 Agent”，而在系统能否正确处理真实零售运行中的数据状态、并发占用、门店执行和失败恢复。这些问题必须在修改系统时进入数据模型和状态机，不能只写在架构文档里。

### 18.2 必须进入第一轮系统改造的缺口

#### 1. 商品与门店主数据必须成为独立上下文

现在 Demo 里的 SKU 主要是名称和简单库存字段，不足以支撑服装零售判断。

必须增加：

- `style_id`, `color_id`, `size_id`, `variant_id`, `gtin`
- 商品层级：department / category / class / subclass
- 商品生命周期：basic / seasonal / short-lifecycle / limited / clearance
- `site_id`, `store_cluster`, `assortment_status`, `effective_from`, `effective_to`
- 商品、门店、政策的 `master_data_version`

GS1 对不同颜色和尺码变体使用独立标识；SAP Retail 也区分 generic article/style 与可实际销售的 variant。Case 必须落到可售变体，而不是只落到模糊商品名称。

#### 2. 库存必须从 on-hand 升级为 sellable ATP

真实可推荐库存不是“系统显示有几件”，而是：

```text
sellable_atp
= physical_on_hand
- soft_reserved
- safety_stock
- blocked_or_quarantined
- pending_transfer_out
+ eligible_confirmed_inbound
```

必须区分：

- physical on-hand
- available-to-reserve
- soft reserved
- safety stock
- in-transit
- returned-pending-inspection
- quarantined / damaged
- channel allocation
- current ATP 与 future ATP date

Dynamics 365 Inventory Visibility 明确把 soft reservation、ATP、inventory allocation 和不同库存状态作为防止超卖与兑现承诺的核心能力。Personalization 和 Marketing 只能消费 ATP，不得直接消费 physical on-hand。

#### 3. 退货不能直接回到可售库存

服装退货必须经过 disposition：

- `RETURN_INITIATED`
- `RETURN_RECEIVED`
- `PENDING_INSPECTION`
- `SELLABLE`
- `REPACK_REQUIRED`
- `DEFECTIVE`
- `QUARANTINED`
- `RETURN_TO_VENDOR`
- `DISPOSED`

退货原因也要结构化：尺码不合、颜色偏差、商品描述不符、质量、改变主意、疑似滥用。高退货率可能说明尺码/商品问题，不能被 Inventory Agent 当作新增供给，也不能被 Marketing Agent 当作再次促销机会。

#### 4. Case 必须支持去重、合并、过期和重新评估

同一门店、同一变体可能每小时重复触发缺货告警。系统必须提供：

- `dedupe_key = case_type + site + variant + time_window`
- 相同异常合并证据，不重复创建 Case。
- 新库存、盘点或订单事件到达后，标记 Case `REASSESS_REQUIRED`。
- Decision Packet 必须有 `expires_at`；超过有效期不能继续审批。
- Case 关闭后再次恶化，应创建关联 Case，而不是静默重开旧记录。

#### 5. 门店执行必须包含接受、拒绝和完成证据

“生成门店任务”不等于任务完成。任务对象至少要包含：

- owner、门店、任务类型、数量、截止时间、预计工时
- 门店当前任务负载和收货/盘点时间窗
- `ACCEPTED`, `REJECTED`, `IN_PROGRESS`, `COMPLETED`, `FAILED`
- 拒绝原因：无人员、无空间、库存不符、商品损坏、到货延迟
- 完成证据：盘点数量、RFID 扫描、收货回执或陈列确认

RELEX 等成熟方案把本地化陈列、补货节奏和门店执行连接起来。Project 46 不需要实现完整 planogram 优化，但必须把门店容量与执行确认作为动作门禁。

#### 6. 下游执行需要 Saga、幂等和补偿动作

一次 Decision Packet 可能同时创建调拨、WMS 拣货、门店收货和 CRM 草稿。任何一步都可能失败。

必须增加：

- `action_id` 与 idempotency key
- 每一步的 request、response、attempt、error code
- retryable / non-retryable 区分
- dead-letter / manual intervention 状态
- compensation action，例如取消预留、撤销未执行调拨、停用未发送活动
- 部分成功状态 `PARTIALLY_EXECUTED`

Azure Architecture Center 的 Saga 和 Compensating Transaction 模式强调：跨系统事务必须记录每一步进度，重试命令需要幂等，无法自动恢复时需要人工介入。Demo 至少要模拟一次执行失败和补偿过程。

#### 7. KPI 必须区分过程指标、业务结果和因果增量

当前 UI 中 `+40% Same Store Sales`、`+60% LTV` 等目标不能继续作为“执行后结果”展示。

第一轮应展示可由 Demo 证明的过程指标：

- Case 创建到 Decision Packet 的时间
- stale/low-confidence 数据阻断率
- 人工审批时间与 override rate
- 门店任务接受率和 SLA 完成率
- 调拨成功率、到货准时率、ATP 履约率
- 未授权用户剔除率、不可履约推荐阻断率
- 动作失败、重试和补偿成功率

业务指标只能标记为 hypothesis 或 pilot measurement：

- stockout rate、full-price sell-through、markdown rate、gross margin return
- return rate、cancellation rate、conversion uplift

增量效果必须来自 test/control 门店或用户组。Microsoft Fabric 的 uplift modeling 示例同样要求 treatment/control 指示和实际 outcome，不能把所有自然销量变化归因于 Agent。

### 18.3 必须增加的 AI 运行治理

NIST AI RMF 与 GenAI Profile 强调持续监控、数据来源、模型版本、人类监督、事件响应和长期审计。对应到本系统，第一轮至少需要：

- 每个 Domain Decision 保存 `model_version`, `prompt_version`, `rule_version`, `policy_version`。
- 保存输入证据引用，不在 trace 中保存明文 PII。
- 规则结果与 LLM 解释分栏展示，防止把自然语言解释误认为计算事实。
- Agent 超时或模型不可用时，返回规则基线或 `MANUAL_REVIEW_REQUIRED`。
- 支持人工 override，并保存原建议、修改值、修改人和理由。
- Agent 决策异常进入 incident log，可按模型/规则版本追踪影响 Case。

### 18.4 可以后置到第二阶段的能力

以下能力真实存在，但不应进入第一轮 Demo，以免重新复杂化：

- 完整 MFP/OTB 财务规划引擎。
- 自动 planogram 生成与计算机视觉验收。
- 门店 workforce scheduling 优化。
- 全网运输路线和成本优化。
- 大规模实时推荐模型和完整 Customer 360 平台。
- 亚洲多国家生产级数据驻留部署。
- 自主动态定价和自动营销投放。
- 生产级 ERP/WMS/OMS/CRM 双向集成。

第一轮只需要结构真实的 synthetic data、mock connector 和可验证状态变化。

### 18.5 明确不做的内容

- 不切换商超鲜品。
- 不增加新的业务 Agent。
- 不把 Orchestrator、Policy Engine、Compliance、Store Ops 包装成额外 Agent。
- 不让所有 Case 强制运行五个 Agent。
- 不用营销文案生成作为核心价值证明。
- 不把行业案例 KPI 或模拟值写成本项目已实现收益。
- 不宣称原型已经接入真实优衣库内部系统。

### 18.6 当前代码与目标架构的主要差距

对当前 `src/api.py`、`src/scenario_engine.py` 和 `src/static/index.html` 的检查显示：

- 现有后端按固定 `decision_loop` 读取五个 Agent，尚未以 Case 类型动态编排。
- `build_work_orders()` 直接从各 Agent 输出创建工单，缺少统一 Decision Packet。
- 库存主要使用 current stock / replenishment，缺少 reservation、ATP 和库存 disposition。
- 前端仍保留 Fashion Launch、AIGC Visual、Digital Human、Customer 360、Dynamic Pricing 等偏离主线的模块。
- UI 多处继续展示 `+40% Same Store Sales` 和 `+60% LTV`。
- Compliance 仍以 Agent 形式出现在部分 runtime trace 中。
- 当前执行状态有审批和完成，但缺少 Case 去重、过期、重新评估、部分成功、补偿和 execution receipt 细节。

因此下一步不是在现有页面上继续叠加模块，而是重构核心对象和主导航。

### 18.7 第一轮系统改造范围

后端核心对象：

- `RetailCase`
- `CaseSnapshot`
- `DomainDecision`
- `DecisionPacket`
- `ProposedAction`
- `ApprovalRecord`
- `ExecutionReceipt`
- `AuditEvent`

优先实现两个 workflow template：

1. `BROKEN_SIZE_STOCKOUT`
   - 包含 inventory confidence 低时先盘点的暂停分支。
   - 包含 ATP、soft reservation 和门店/仓库履约判断。
   - 库存不足时 Marketing 返回 `NO_CAMPAIGN`。

2. `SEASONAL_OVERSTOCK`
   - 区分 transfer、promotion、markdown 和 no-action。
   - 受生命周期、毛利、退货、门店空间和审批权限约束。

前端主导航：

- Exception Queue
- Case Detail
- Decision Packet
- Approval Queue
- Execution & Receipts
- Audit & KPI

Agent Runtime、架构说明和 GPT 文案生成降为 Case Detail 内的辅助信息，不再成为主导航。

### 18.8 开始修改系统的验收门槛

第一轮改造完成后，Demo 应满足：

1. 第一屏是门店异常队列，不是 Control Tower 或营销大屏。
2. 每个 Case 明确到门店、style-color-size variant、时间快照和 SLA。
3. 低可信库存会暂停决策并创建盘点任务。
4. Personalization 使用 ATP，而不是 physical on-hand。
5. 不同 Case 动态选择 Agent，不强制五个全部运行。
6. 一个 Case 只生成一个聚合 Decision Packet。
7. 风险动作必须审批，过期 Packet 不能执行。
8. 下游动作有幂等键、失败、重试、补偿和回执。
9. 门店可以接受或拒绝任务，并填写现实原因。
10. 未授权客户、不可履约商品和低毛利动作可以明确显示为 BLOCKED。
11. KPI 清楚区分 demo-observed、simulation hypothesis 和 pilot-measured。
12. 页面不再把 `+40%`、`+60%` 显示为系统已实现结果。

满足以上十二项，就可以认为系统从“理想化 Agent 展示”转成“可解释的零售经营决策原型”。

### 18.9 本轮主要来源

- GS1 General Specifications: https://ref.gs1.org/standards/genspecs/
- SAP Learning, Creating Products for Retail: https://learning.sap.com/courses/exploring-sap-s-4hana-cloud-public-edition-retail/creating-products-for-retail-3i1-
- Microsoft Learn, Inventory Visibility: https://learn.microsoft.com/en-us/dynamics365/supply-chain/inventory/inventory-visibility
- RELEX Planogram Software: https://www.relexsolutions.com/solutions/planogram-software/
- Manhattan, Reverse Logistics Guide: https://www.manh.com/our-insights/resources/articles/reverse-logistics-ultimate-guide
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- Microsoft Learn, Saga Pattern: https://learn.microsoft.com/en-us/azure/architecture/patterns/saga
- Microsoft Learn, Compensating Transaction Pattern: https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction
- Microsoft Fabric Uplift Modeling: https://learn.microsoft.com/en-us/fabric/data-science/uplift-modeling

检索和复核日期：2026-08-01。
