#!/usr/bin/env python3
"""Generate Project 46 review-story decks.

This version is optimized for panel logic:
what the assignment asks -> my solution thesis -> one scenario -> three proof
chains -> demo -> Azure landing -> measurement.
"""

from pathlib import Path

from gen_project46_revised_ppt import (
    ARCH_EN,
    ARCH_ZH,
    architecture_slide,
    grid_slide,
    new_prs,
    process_slide,
    two_col_slide,
)
from gen_project46_solution_demo_ppt import cover, statement_slide


ROOT = Path(__file__).resolve().parent
OUT_ZH = ROOT / "AMA-项目46-评审故事线-中文.pptx"
OUT_EN = ROOT / "AMA-Project46-Review-Story-English.pptx"
SCRIPT = ROOT / "AMA-项目46-评审故事线讲稿-中英双语.md"
STATIC = ROOT / "src" / "static"


ZH = [
    ("thesis", "1. 46 号课题的问题与我的解法", "开场先回答三个核心问题。", "课题问题：如何整合客户数据，并跨渠道自主交付个性化体验？", [
        "我的判断：难点不在“推荐一个商品”，而在客户、库存、价格、授权和履约同时成立。",
        "我的解法：用 Customer 360 统一客户上下文，用 Retail Decision Case 承接经营异常，用五个 Agent 形成可审批的决策包。",
        "最终价值：把个性化从营销内容，升级为可执行、可审计、可复盘的零售经营动作。",
    ]),
    ("grid", "2. 我的解决方案蓝图", "把 Project 46 从“会推荐”升级为“能闭环经营”。", [
        ("Customer 360", "整合会员、App、门店、POS、订单和授权，形成同一客户上下文。", "green"),
        ("Retail Case", "把异常需求、SKU、门店、库存和 SLA 变成一张可处理的经营 Case。", "blue"),
        ("五 Agent 协同", "围绕同一事实快照判断客户、个性化、库存、价格和营销动作。", "amber"),
        ("人工审批", "高风险补货、价格、促销和触达必须进入授权角色审批。", "purple"),
        ("受控执行", "审批后才写 ERP、WMS、OMS、CRM，并保留回执和补偿路径。", "red"),
        ("Azure 落地", "用云原生运行时、AI 编排、数据存储、集成和监控支撑扩展。", "green"),
    ]),
    ("two", "3. 为什么传统零售系统做不好这件事", "问题来自跨系统割裂，而不是缺少单点智能。", ("业务割裂", [
        "客户行为在 App、门店、POS、平台和会员系统里分散。",
        "库存、价格、营销和履约各自优化，彼此不共享约束。",
        "结果是推荐看起来个性化，但可能没货、亏毛利或无法触达。",
    ], "red"), ("Project 46 改变什么", [
        "先统一客户和经营事实，再让 Agent 推理。",
        "把 AI 输出变成企业可处理的 Case。",
        "用人工审批和规则护栏控制生产动作。",
    ], "green")),
    ("two", "4. 主演示 Case：AIRism 黑色 M/L 断码风险", "演示主线在“待我审批”里，热浪只是触发信号。", ("业务事件", [
        "上海淮海路旗舰店 AIRism 黑色 M/L 进入断码风险。",
        "证据显示：连续三天高温后，M/L 动销提升到 46 件/天。",
        "当前可售 ATP 只有 29 件，但未来可承接供货为 449 件。",
        "周边门店可调拨，华东仓可补货。",
    ], "amber"), ("系统承接", [
        "区域经理在“待我审批”看到这个 Case。",
        "AI 决策助手展示 7 天预测、供货能力、备选方案和护栏。",
        "四季沙盘只用于说明类似天气/季节信号如何做规划，不是主审批入口。",
        "审批前不写 ERP / WMS / OMS / CRM。",
    ], "blue")),
    ("process", "5. 我的系统解法：从信号到经营动作", "五步不是功能导航，而是方案主线。", [
        ("整合客户", "Customer 360 建立身份、意图、授权和渠道偏好。", "green"),
        ("形成 Case", "把 SKU、门店、库存、信号和 SLA 变成经营对象。", "blue"),
        ("Agent 推理", "五个 Agent 围绕同一事实快照形成方案。", "amber"),
        ("人工审批", "高风险补货、价格、促销和触达由授权角色批准。", "purple"),
        ("执行复盘", "写入下游系统，记录回执，衡量预测与实际。", "red"),
    ]),
    ("two", "6. 门店店长故事线：把现场事实变成可信输入", "店长不做商业审批，只负责把门店事实核准。", ("业务处境", [
        "AIRism 白色 M/L 的系统库存与 RFID / 门店信号不一致。",
        "库存可信度低，继续推荐或调拨可能造成超卖。",
        "门店是最接近商品实物的一线事实源。",
        "店长需要完成盘点、收货确认和异常反馈。",
    ], "green"), ("系统结果", [
        "低可信库存会自动暂停商业动作。",
        "Case 保留盘点任务、时间、责任人和证据来源。",
        "实物确认后，系统才允许重新评估或流转到区域审批。",
    ], "blue")),
    ("two", "7. 区域经理故事线：从异常到可审批方案", "区域经理把热浪需求转化为受控补货和调拨决策。", ("业务处境", [
        "上海热浪推高 AIRism 黑色 M/L 需求。",
        "核心门店出现断码风险，周边门店和 DC 仍有可承接供货。",
        "客户触达、门店履约、库存调拨和毛利保护必须同时成立。",
        "区域经理需要在 SLA 内决定是否批准方案。",
    ], "blue"), ("系统结果", [
        "同一 Case 汇总 7 天预测、ATP、补货调拨和业务护栏。",
        "Decision Packet 提供推荐方案、备选方案和阻断理由。",
        "审批通过前不写 ERP / WMS / OMS / CRM。",
    ], "amber")),
    ("two", "8. 跨国经营管理层故事线：看市场组合和重大例外", "管理层关注跨市场资源、预算和政策例外，不处理门店小任务。", ("业务处境", [
        "中国、日本、韩国和东南亚市场的季节节奏和需求信号不同。",
        "当前真实 Case 来自中国市场，其他市场作为区域规划上下文。",
        "重大促销、价格例外、预算和跨区域资源需要管理层治理。",
    ], "purple"), ("系统结果", [
        "门店盘点和区域调拨不会越级打扰管理层。",
        "四季沙盘只生成规划信号，不直接写生产动作。",
        "经核验的市场风险可以升级为 Case、预算决策或区域资源调整。",
    ], "green")),
    ("two", "9. 证明链一：个性化为什么可信", "不是“更会推荐”，而是“推荐能够被履约”。", ("Customer 360 提供", [
        "客户是谁、近期意图是什么。",
        "是否授权当前渠道触达。",
        "偏好语言、渠道和服务方式。",
    ], "green"), ("经营信号约束", [
        "SKU / 门店 / 尺码 / 颜色的可售库存。",
        "补货和调拨能力。",
        "价格、毛利和会员触达规则。",
    ], "blue")),
    ("two", "10. 证明链二：Agent 输出如何进入企业流程", "关键是 Retail Decision Case，而不是 Agent 聊天。", ("Case 把什么放在一起", [
        "业务事实：门店、商品、SKU、库存、需求信号。",
        "AI 方案：预测、备选、风险和推荐动作。",
        "治理信息：审批角色、政策版本、审计和执行回执。",
    ], "blue"), ("企业流程结果", [
        "AI 建议不是停留在文本里。",
        "区域经理可以基于同一个 Case 审核。",
        "系统可以追踪谁批准、执行了什么、结果如何。",
    ], "purple")),
    ("two", "11. 证明链三：自主决策如何不失控", "自主是生成方案，控制是决定能否执行。", ("规则护栏", [
        "未授权客户不能触达。",
        "低可信库存不能推荐。",
        "低于毛利底线的折扣被阻断。",
        "审批前不写 ERP / WMS / OMS / CRM。",
    ], "red"), ("组织责任", [
        "店长确认门店事实。",
        "区域经理审批调拨和补货。",
        "管理层审批重大促销、价格例外和预算。",
        "AI 负责推荐、解释、草拟和监控。",
    ], "green")),
    ("process", "12. 一张 Decision Packet 如何生成", "五个 Agent 不是五个功能按钮，而是共同生成一个可审批方案。", [
        ("客户识别", "确认目标会员、近期意图、语言偏好和触达授权。", "green"),
        ("体验生成", "选择适合的 SKU、渠道、内容和服务方式。", "blue"),
        ("履约校验", "检查门店、仓库、尺码、颜色和库存可信度。", "amber"),
        ("价格约束", "校验折扣、毛利底线和价格例外。", "purple"),
        ("触达与审批", "生成会员触达或经营动作，并标记审批角色与风险。", "red"),
    ]),
    ("two", "13. 区域经理看到的不是 AI，而是下一步经营决策", "演示从一个真实异常开始，到批准一个可执行方案结束。", ("进入 Case", [
        "上海热浪导致 AIRism 黑色 M/L 断码风险。",
        "系统汇总线上搜索、门店试穿、POS 转化和库存可信度。",
        "区域经理看到的是业务影响、到期时间和建议动作。",
    ], "blue"), ("做出决策", [
        "查看 7 天预测和可承接供货。",
        "比较补货、调拨、限购、会员券等备选方案。",
        "确认库存、毛利、授权和审批要求。",
        "审批后才进入下游执行和复盘。",
    ], "amber")),
    ("two", "14. 从单个热浪 Case 扩展到四季经营规划", "四季沙盘证明系统不只处理今天的异常，也能提前发现未来风险。", ("规划视角", [
        "春夏秋冬带来不同的商品组合、天气、节假日和库存压力。",
        "沙盘用于模拟需求变化、断码风险和门店履约能力。",
        "它帮助管理层提前准备 SKU、补货和区域资源。",
    ], "purple"), ("治理边界", [
        "沙盘结果只是规划信号，不能直接写生产系统。",
        "只有经过真实数据核验，才会形成 Retail Decision Case。",
        "进入 Case 后仍然经过规则护栏、人工审批和审计。",
    ], "green")),
    ("two", "15. 沙盒演示故事线：从天气信号到季节经营规划", "沙盒不是审批入口，而是把当前 Case 的热浪信号扩展成规划推演。", ("沙盒输入", [
        "夏季高温、App 搜索、POS 动销、RFID 试穿和仓库可用量形成规划信号。",
        "夏季页显示气温 36°C、需求信号 1.35× 和 14 天预测窗口。",
        "SKU 组合覆盖 AIRism、速干、防晒等夏季商品，以及反季清仓池。",
    ], "purple"), ("沙盒输出", [
        "五个 Agent 只做情景推演：需求、库存、价格、客群和营销触达。",
        "沙盒不直接写生产系统，也不直接生成审批。",
        "只有被真实销售、库存和门店信号核验后，才会变成 Retail Decision Case。",
    ], "green")),
    ("architecture", "16. Azure 架构：为什么方案能落地", "架构页承接“企业可落地”，不是技术炫技。"),
    ("grid", "17. Azure 服务栈如何支撑故事", "把每个服务和解决方案环节绑定。", [
        ("Container Apps", "承载 Agent Runtime，支持 revision、弹性和灰度。", "green"),
        ("Azure OpenAI / AI Foundry", "负责五 Agent 推理、编排、评估和安全治理。", "blue"),
        ("Cosmos DB", "保存 Customer 360、Case、审批状态和审计日志。", "amber"),
        ("AI Search", "检索商品、政策、FAQ 和历史案例。", "purple"),
        ("APIM + MCP", "让 Agent 安全调用企业工具和 API。", "red"),
        ("Service Bus / Event Grid", "处理异步执行、回执、重试和补偿。", "green"),
        ("Key Vault / Managed Identity", "密钥和权限治理。", "blue"),
        ("App Insights / Log Analytics", "监控 Agent、API、错误、延迟和业务事件。", "amber"),
        ("Fabric / Power BI", "承接 test/control 试点与经营看板。", "purple"),
    ]),
    ("two", "18. 当前原型证明了什么", "不要声称已经实现业务增长，要证明系统形态成立。", ("已经可证明", [
        "角色工作台、Case 流转、AI 决策详情、审批和审计可点击。",
        "中英文演示和手机端关键路径可用。",
        "生产部署在 Azure Container Apps，支持 revision 和健康验证。",
    ], "green"), ("仍需试点证明", [
        "+40% 同店销售。",
        "-50% 库存浪费。",
        "85% 满意度。",
        "+60% LTV。",
    ], "red")),
    ("process", "19. 业务效果怎么验证", "把课题指标落到实验设计。", [
        ("Baseline", "选择同类门店、SKU 和会员 cohort。", "green"),
        ("Pilot", "试点门店使用 Agent 建议，但保留人工审批。", "blue"),
        ("Control", "对照组沿用当前流程。", "amber"),
        ("Measure", "衡量销售、库存、满意度、LTV 和治理指标。", "purple"),
        ("Scale", "只有护栏、执行和 KPI 稳定后才扩大。", "red"),
    ]),
    ("thesis", "20. 结论：一句话总结", "最后回到 46 号课题本身。", "Project 46 不是功能集合，而是一套让 AI 进入零售经营决策的系统方案。", [
        "它用 Customer 360 回答客户数据整合。",
        "它用五个 Agent 回答全渠道个性化和库存/价格/营销协同。",
        "它用 Case、审批、审计和 Azure 架构回答企业落地可信度。",
    ]),
]


EN = [
    ("thesis", "1. The Project 46 Question and My Answer", "Start with three core questions.", "Question: how can a retailer integrate customer data and autonomously deliver personalized experiences across channels?", [
        "My view: the hard part is not recommending a product. The hard part is making customer, inventory, price, consent and fulfillment true at the same time.",
        "My answer: Customer 360 unifies customer context, Retail Decision Case carries operating exceptions, and five Agents create approvable decision packets.",
        "Value: personalization becomes executable, auditable and measurable retail action.",
    ]),
    ("grid", "2. My Solution Blueprint", "Upgrade Project 46 from recommendation to closed-loop retail operation.", [
        ("Customer 360", "Unify member, app, store, POS, order and consent data into one customer context.", "green"),
        ("Retail Case", "Turn demand exception, SKU, store, inventory and SLA into one operating Case.", "blue"),
        ("Five Agents", "Reason over customer, personalization, inventory, pricing and marketing on the same facts.", "amber"),
        ("Human Approval", "Risky supply, price, campaign and outreach actions require authorized approval.", "purple"),
        ("Controlled Execution", "Only approved actions write to ERP, WMS, OMS and CRM, with receipts and compensation.", "red"),
        ("Azure Landing", "Cloud-native runtime, AI orchestration, data, integration and monitoring support scale.", "green"),
    ]),
    ("two", "3. Why Traditional Retail Systems Fail Here", "The problem is cross-system fragmentation, not lack of point intelligence.", ("Fragmentation", [
        "Customer behavior is split across app, store, POS, marketplace and membership systems.",
        "Inventory, pricing, marketing and fulfillment optimize separately.",
        "Recommendations may look personalized but be unavailable, unprofitable or non-compliant.",
    ], "red"), ("What Project 46 Changes", [
        "Unify customer and operating facts before Agent reasoning.",
        "Turn AI output into an enterprise-processable Case.",
        "Use human approval and guardrails to control production actions.",
    ], "green")),
    ("two", "4. Main Demo Case: AIRism Black M/L Stockout Risk", "The demo storyline lives in My approvals. Heatwave is a trigger signal.", ("Business Event", [
        "Shanghai Huaihai Road Flagship faces AIRism black M/L broken-size risk.",
        "Evidence shows M/L sell-through accelerated to 46 units/day after three heatwave days.",
        "Current sellable ATP is only 29 units, while future fulfillable supply is 449 units.",
        "Nearby stores can transfer stock and East China DC can replenish.",
    ], "amber"), ("System Flow", [
        "The regional manager sees this Case in My approvals.",
        "AI decision support shows 7-day forecast, fulfillable supply, alternatives and guardrails.",
        "The seasonal sandbox only explains how weather / season signals support planning; it is not the main approval entry.",
        "No ERP / WMS / OMS / CRM write happens before approval.",
    ], "blue")),
    ("process", "5. My Solution: From Signals To Retail Action", "These five steps are the solution storyline.", [
        ("Unify customer", "Customer 360 captures identity, intent, consent and channel preference.", "green"),
        ("Create Case", "SKU, store, inventory, signals and SLA become an operating object.", "blue"),
        ("Agent reasoning", "Five Agents reason over the same fact snapshot.", "amber"),
        ("Human approval", "Risky inventory, price, campaign and outreach actions require authorization.", "purple"),
        ("Execute & learn", "Downstream writes keep receipts and compare forecast with actuals.", "red"),
    ]),
    ("two", "6. Store Manager Storyline: Turn Store Facts Into Trusted Input", "Store managers do not approve commercial actions. They certify store facts.", ("Business Situation", [
        "AIRism white M/L system stock conflicts with RFID and store signals.",
        "Low inventory confidence can create oversell if the system keeps recommending or transferring.",
        "The store is the closest source of physical product truth.",
        "The manager completes count, receiving confirmation and exception feedback.",
    ], "green"), ("System Outcome", [
        "Low-confidence inventory automatically pauses commercial action.",
        "The Case keeps task, time, owner and evidence source.",
        "Only verified facts allow reassessment or regional approval.",
    ], "blue")),
    ("two", "7. Regional Manager Storyline: From Exception To Approvable Plan", "The regional manager turns heatwave demand into controlled replenishment and transfer decisions.", ("Business Situation", [
        "Shanghai heatwave raises AIRism black M/L demand.",
        "Core stores face stockout risk while nearby stores and DC can still supply.",
        "Customer activation, store fulfillment, inventory transfer and margin protection must all hold.",
        "The manager must decide within the SLA.",
    ], "blue"), ("System Outcome", [
        "One Case combines 7-day forecast, ATP, supply plan and guardrails.",
        "The Decision Packet provides recommendation, alternatives and blockers.",
        "No ERP / WMS / OMS / CRM write happens before approval.",
    ], "amber")),
    ("two", "8. International Management Storyline: Market Portfolio And Major Exceptions", "Executives focus on cross-market resources, budget and policy exceptions, not store tasks.", ("Business Situation", [
        "China, Japan, Korea and Southeast Asia have different seasons and demand signals.",
        "Current real Cases come from China; other markets remain planning context.",
        "Major campaign, price exception, budget and cross-region resources require executive governance.",
    ], "purple"), ("System Outcome", [
        "Store count and regional transfer tasks do not escalate to executives.",
        "Seasonal sandbox creates planning signals, not production writes.",
        "Verified market risk can become a Case, budget decision or regional resource adjustment.",
    ], "green")),
    ("two", "9. Proof Chain 1: Why Personalization Is Credible", "It is not just better recommendation. It is fulfillable recommendation.", ("Customer 360 Provides", [
        "Who the customer is and what intent they show.",
        "Whether the current channel is consented.",
        "Preferred language, channel and service pattern.",
    ], "green"), ("Operating Signals Constrain", [
        "Sellable stock by SKU, store, size and color.",
        "Replenishment and transfer capability.",
        "Price, margin and outreach rules.",
    ], "blue")),
    ("two", "10. Proof Chain 2: How Agent Output Enters Enterprise Workflow", "Retail Decision Case is the key, not Agent chat.", ("Case Combines", [
        "Facts: store, product, SKU, inventory and demand signals.",
        "AI options: forecast, alternatives, risks and recommended actions.",
        "Governance: approver, policy version, audit and execution receipts.",
    ], "blue"), ("Workflow Outcome", [
        "AI suggestions do not remain as text.",
        "A regional manager can review one shared Case.",
        "The system can trace who approved, what executed and what happened.",
    ], "purple")),
    ("two", "11. Proof Chain 3: How Autonomy Stays Controlled", "Autonomy creates options; controls decide execution.", ("Guardrails", [
        "No outreach without consent.",
        "No recommendation on low-confidence inventory.",
        "Discount below margin floor is blocked.",
        "No ERP / WMS / OMS / CRM write before approval.",
    ], "red"), ("Accountability", [
        "Store manager confirms store facts.",
        "Regional manager approves transfer and replenishment.",
        "Executives approve major campaigns, price exceptions and budget.",
        "AI recommends, explains, drafts and monitors.",
    ], "green")),
    ("process", "12. How One Decision Packet Is Generated", "The five Agents are not five buttons. They jointly create one approvable plan.", [
        ("Identify customer", "Confirm target members, recent intent, language preference and consent.", "green"),
        ("Generate experience", "Choose SKU, channel, content and service pattern.", "blue"),
        ("Check fulfillment", "Validate store, warehouse, size, color and inventory confidence.", "amber"),
        ("Constrain price", "Check discount, margin floor and price exception.", "purple"),
        ("Activate & approve", "Create outreach or operating action, with approver and risk flags.", "red"),
    ]),
    ("two", "13. A Regional Manager Sees The Next Retail Decision, Not The AI Internals", "The demo starts with an exception and ends with an executable approved plan.", ("Open The Case", [
        "Shanghai heatwave creates AIRism black M/L stockout risk.",
        "The system combines online search, store try-on, POS conversion and inventory confidence.",
        "The regional manager sees business impact, due time and recommended action.",
    ], "blue"), ("Make The Decision", [
        "Review the 7-day forecast and fulfillable supply.",
        "Compare replenishment, transfer, purchase limit and member coupon options.",
        "Check inventory, margin, consent and approval requirements.",
        "Execution and learning start only after approval.",
    ], "amber")),
    ("two", "14. From One Heatwave Case To Seasonal Retail Planning", "The seasonal sandbox proves the system can detect future risk, not only today’s exception.", ("Planning View", [
        "Spring, summer, autumn and winter change assortment, weather, holidays and inventory pressure.",
        "The sandbox simulates demand shift, size risk and store fulfillment capacity.",
        "Management can prepare SKU, replenishment and regional resources earlier.",
    ], "purple"), ("Governance Boundary", [
        "Sandbox output is a planning signal, not a production write.",
        "Only verified real data can become a Retail Decision Case.",
        "Every Case still goes through guardrails, human approval and audit.",
    ], "green")),
    ("two", "15. Sandbox Demo Storyline: From Weather Signal To Seasonal Planning", "The sandbox is not an approval entry. It turns the heatwave signal behind the current Case into planning simulation.", ("Sandbox Inputs", [
        "Summer heat, app search, POS sell-through, RFID try-ons and warehouse availability become planning signals.",
        "The summer view shows 36°C temperature, 1.35× demand signal and a 14-day forecast window.",
        "The SKU mix covers AIRism, quick-dry and UV-protection summer products, plus off-season clearance.",
    ], "purple"), ("Sandbox Outputs", [
        "Five Agents run scenario simulation for demand, inventory, price, audience and outreach.",
        "The sandbox does not write to production systems or directly create approvals.",
        "Only signals verified by real sales, inventory and store facts can become a Retail Decision Case.",
    ], "green")),
    ("architecture", "16. Azure Architecture: Why It Can Land", "Architecture supports enterprise readiness, not technical showmanship."),
    ("grid", "17. Azure Services Mapped To The Story", "Bind every service to a solution step.", [
        ("Container Apps", "Agent Runtime, revisions, elasticity and rollout.", "green"),
        ("Azure OpenAI / AI Foundry", "Agent reasoning, orchestration, evaluation and safety governance.", "blue"),
        ("Cosmos DB", "Customer 360, Cases, approval state and audit logs.", "amber"),
        ("AI Search", "Product, policy, FAQ and historical case retrieval.", "purple"),
        ("APIM + MCP", "Safe enterprise tool and API gateway.", "red"),
        ("Service Bus / Event Grid", "Async execution, receipts, retry and compensation.", "green"),
        ("Key Vault / Managed Identity", "Secrets and access governance.", "blue"),
        ("App Insights / Log Analytics", "Agent, API, error, latency and business event monitoring.", "amber"),
        ("Fabric / Power BI", "Test/control pilot and business dashboard.", "purple"),
    ]),
    ("two", "18. What The Prototype Proves", "Do not claim business lift yet; prove system shape.", ("Proven Now", [
        "Role workspace, Case flow, AI decision detail, approval and audit are clickable.",
        "Chinese/English demo and mobile critical path work.",
        "Production deployment on Azure Container Apps supports revisions and health checks.",
    ], "green"), ("Needs Pilot", [
        "+40% same-store sales.",
        "-50% inventory waste.",
        "85% satisfaction.",
        "+60% LTV.",
    ], "red")),
    ("process", "19. How Business Impact Will Be Proven", "Turn assignment metrics into experiment design.", [
        ("Baseline", "Choose comparable stores, SKUs and member cohorts.", "green"),
        ("Pilot", "Pilot stores use Agent recommendations with human approval.", "blue"),
        ("Control", "Control group stays on current process.", "amber"),
        ("Measure", "Track sales, inventory, satisfaction, LTV and governance metrics.", "purple"),
        ("Scale", "Expand only when guardrails, execution and KPIs are stable.", "red"),
    ]),
    ("thesis", "20. Closing: One Sentence For The Panel", "Return to the Project 46 assignment.", "Project 46 is not a collection of features. It is a system design for bringing AI into retail operating decisions.", [
        "Customer 360 answers customer data integration.",
        "Five Agents answer omni-channel personalization and inventory / price / marketing coordination.",
        "Case, approval, audit and Azure architecture answer enterprise trust and production readiness.",
    ]),
]


SCRIPT_ZH = [
    "我会先用这一页把 46 号课题说清楚：题目问的是如何整合客户数据，并跨渠道自主交付个性化体验。我的解法不是单点推荐，而是 Customer 360、Retail Decision Case 和五个 Agent 组成的经营决策系统。",
    "这一页是我的解决方案蓝图：Customer 360 负责客户上下文，Retail Case 承接经营异常，五个 Agent 生成方案，人工审批控制风险，执行系统留下回执，Azure 支撑规模化落地。",
    "传统零售系统的问题是割裂。客户、库存、价格、营销和履约分散优化，所以推荐可能没货，折扣可能亏毛利，触达可能没有授权。",
    "这一页我会把主线收回到系统里真实可点的 Case：AIRism 黑色 M/L 断码风险。上海热浪不是一个独立功能页，而是 Case 里的需求触发信号；主演示入口是区域经理的待我审批。",
    "系统主线是五步：整合客户，形成 Case，Agent 推理，人工审批，执行复盘。这五步就是演示逻辑，不是菜单导航。",
    "第一条角色故事线是门店店长。店长不负责审批，他负责让系统相信门店事实：库存不可信时先做实物盘点，确认后 Case 才能继续流转。",
    "第二条角色故事线是区域经理，这是现场演示主线。区域经理打开待审批 Case，看到预测、供货能力、业务护栏和建议方案，然后决定是否批准。",
    "第三条角色故事线是跨国经营管理层。管理层不处理门店小任务，而是看国家组合、重大促销、价格例外、预算和跨区域资源配置。",
    "第一条证明链是个性化可信。Customer 360 解决客户是谁和是否授权，经营信号解决 SKU、门店、库存、补货、价格和毛利约束。",
    "第二条证明链是 Agent 输出能进入企业流程。Retail Decision Case 把事实、方案、审批、政策、执行和审计放在一起，让 AI 建议可处理。",
    "第三条证明链是自主不失控。AI 可以生成方案，但未授权、低可信库存、毛利底线和生产写入都由规则和人工审批控制。",
    "这一页讲一张 Decision Packet 是怎么生成的。五个 Agent 不是五个功能按钮，而是围绕同一个上海热浪 Case 共同确认客户、体验、履约、价格和触达审批。",
    "这一页把演示视角切到区域经理。区域经理不需要看 AI 内部编排，他需要看到断码风险、七天预测、可承接供货、备选方案和审批后才能执行的动作。",
    "这一页讲四季沙盘的业务价值。它让系统从今天的热浪 Case 扩展到春夏秋冬的经营规划，但沙盘只是规划信号，必须核验后才能形成 Case 并进入审批。",
    "这一页把沙盒演示放进故事线。它承接上海热浪信号，但不是审批入口；它展示天气、搜索、动销、试穿和仓库可用量如何先形成季节规划推演，只有被真实销售、库存和门店事实核验后，才进入 Retail Decision Case。",
    "Azure 架构页回答的是企业可落地。分层包括体验、API、Agent Runtime、AI 编排、数据知识、安全运维。",
    "Azure 服务栈要绑定故事：Container Apps 跑运行时，Azure OpenAI 和 AI Foundry 跑 Agent，Cosmos DB 存 Case 和审计，AI Search 做知识检索，APIM 和 Service Bus 做集成，Fabric 和 Power BI 做指标。",
    "当前原型证明的是系统形态：角色工作台、Case 流转、AI 决策、审批审计、中英文和移动端关键路径。业务增长指标还需要试点。",
    "业务效果用实验验证：baseline、pilot、control、measure、scale。这样课题里的指标不是口号，而是可衡量的试点目标。",
    "最后一句话：Project 46 不是功能集合，而是一套让 AI 进入零售经营决策的系统方案。",
]

SCRIPT_EN = [
    "I start by making the Project 46 question clear. The assignment asks how to integrate customer data and autonomously deliver personalized experiences across channels. My answer is not point recommendation. It is Customer 360, Retail Decision Case and five Agents as a retail decision system.",
    "This slide is my solution blueprint: Customer 360 provides customer context, Retail Case carries operating exceptions, five Agents create a plan, human approval controls risk, execution systems keep receipts, and Azure supports scale.",
    "Traditional retail systems fail because they are fragmented. Customer, inventory, price, marketing and fulfillment optimize separately, so a recommendation may be unavailable, unprofitable or non-compliant.",
    "This slide brings the story back to the real clickable Case: AIRism black M/L stockout risk. Shanghai heatwave is not a standalone feature page. It is the demand trigger inside the Case, and the main demo entry is the regional manager’s My approvals.",
    "The system storyline has five steps: unify customer, create Case, Agent reasoning, human approval, execute and learn. These steps are the demo logic, not menu navigation.",
    "The first role storyline is the store manager. The store manager does not approve commercial decisions. They make store facts trusted: when inventory confidence is low, the system asks for a physical count before the Case moves on.",
    "The second role storyline is the regional manager, which is the main live demo. The manager opens an approval Case, reviews forecast, fulfillable supply, guardrails and the recommended plan, then decides whether to approve.",
    "The third role storyline is international management. Executives do not handle store-level tasks. They review market portfolio, major campaigns, price exceptions, budget and cross-region resources.",
    "The first proof chain is credible personalization. Customer 360 handles who the customer is and whether consent exists. Operating signals constrain SKU, store, inventory, replenishment, price and margin.",
    "The second proof chain is enterprise workflow. Retail Decision Case keeps facts, options, approval, policy, execution and audit together, so AI suggestions become processable.",
    "The third proof chain is controlled autonomy. AI creates options, but consent, inventory confidence, margin floor and production writes are controlled by rules and human approval.",
    "This slide explains how one Decision Packet is generated. The five Agents are not five feature buttons. They jointly confirm customer, experience, fulfillment, price, activation and approval around the same Shanghai heatwave Case.",
    "This slide shifts the demo to the regional manager. The manager does not need to see internal AI orchestration. They need stockout risk, seven-day forecast, fulfillable supply, alternative actions and approval before execution.",
    "This slide explains the business value of the seasonal sandbox. It expands the system from today’s heatwave Case to seasonal retail planning, but sandbox output is only a planning signal and must be verified before becoming a Case.",
    "This slide places the sandbox demo into the storyline. It extends the Shanghai heatwave signal, but it is not the approval entry. It shows how weather, search, sell-through, try-ons and warehouse availability first become seasonal planning simulation. Only signals verified by real sales, inventory and store facts enter a Retail Decision Case.",
    "The Azure architecture answers enterprise landing. The layers are experience, API, Agent Runtime, AI orchestration, data and knowledge, security and operations.",
    "The Azure service stack must bind to the story: Container Apps runs runtime, Azure OpenAI and AI Foundry run Agents, Cosmos DB stores Cases and audit, AI Search retrieves knowledge, APIM and Service Bus integrate systems, and Fabric / Power BI measure outcomes.",
    "The prototype proves system shape: role workspace, Case flow, AI decision, approval, audit, bilingual demo and mobile critical path. Business lift still needs pilot validation.",
    "Business impact is proven through experiment design: baseline, pilot, control, measure and scale. This turns assignment metrics into measurable pilot targets.",
    "Final sentence: Project 46 is not a collection of features. It is a system design for bringing AI into retail operating decisions.",
]


def build(data, lang):
    prs = new_prs()
    cover(prs, lang, 1)
    slide_no = 2
    for entry in data:
        kind = entry[0]
        if kind == "thesis":
            _, title, subtitle, main, bullets = entry
            statement_slide(prs, lang, slide_no, title, subtitle, main, bullets)
        elif kind == "grid":
            _, title, subtitle, items = entry
            grid_slide(prs, lang, slide_no, title, subtitle, items)
        elif kind == "two":
            _, title, subtitle, left, right = entry
            two_col_slide(prs, lang, slide_no, title, subtitle, left, right)
        elif kind == "process":
            _, title, subtitle, steps = entry
            process_slide(prs, lang, slide_no, title, subtitle, steps)
        elif kind == "architecture":
            _, title, subtitle = entry
            architecture_slide(prs, lang, slide_no, title, subtitle, ARCH_ZH if lang == "zh" else ARCH_EN)
        slide_no += 1
    return prs


def write_script():
    titles_zh = ["封面"] + [x[1] for x in ZH]
    titles_en = ["Cover"] + [x[1] for x in EN]
    lines = [
        "# Project 46 评审故事线讲稿 / Review Story Speaker Script",
        "",
        "定位：这版以评审逻辑为核心，开头先讲 46 号课题的问题和解法，中段只保留支撑主线的证明链。",
        "",
    ]
    zh_lines = ["各位老师好，我的项目是 Project 46，自主零售智能 Agent 平台。我先用一页讲清楚课题问题和我的解法，然后用一个上海热浪场景证明这套方案如何落地。"] + SCRIPT_ZH
    en_lines = ["Hello everyone. My project is Project 46, the Autonomous Retail Intelligence Agent Platform. I will first clarify the assignment question and my solution, then use a Shanghai heatwave scenario to prove how the solution works."] + SCRIPT_EN
    for i, (tz, te, z, e) in enumerate(zip(titles_zh, titles_en, zh_lines, en_lines), 1):
        lines.extend([f"## Slide {i}: {tz} / {te}", "", "中文：", z, "", "English:", e, ""])
    SCRIPT.write_text("\n".join(lines), encoding="utf-8")


def main():
    zh = build(ZH, "zh")
    en = build(EN, "en")
    zh.save(OUT_ZH)
    en.save(OUT_EN)
    write_script()
    STATIC.mkdir(parents=True, exist_ok=True)
    for path in [OUT_ZH, OUT_EN, SCRIPT]:
        (STATIC / path.name).write_bytes(path.read_bytes())
    print(OUT_ZH)
    print(OUT_EN)
    print(SCRIPT)


if __name__ == "__main__":
    main()
