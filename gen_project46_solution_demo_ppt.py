#!/usr/bin/env python3
"""Generate Project 46 solution-demo decks and bilingual speaker script.

This deck is intentionally not a Q&A appendix. It is a solution presentation:
prompt -> retail problem -> scenario -> system design -> demo -> Azure landing.
"""

from pathlib import Path

from gen_project46_revised_ppt import (
    ARCH_EN,
    ARCH_ZH,
    COLORS,
    add_text,
    architecture_slide,
    closing_slide,
    grid_slide,
    new_prs,
    process_slide,
    set_bg,
    two_col_slide,
)
from pptx.enum.text import PP_ALIGN


ROOT = Path(__file__).resolve().parent
OUT_ZH = ROOT / "AMA-项目46-解决方案演示-中文.pptx"
OUT_EN = ROOT / "AMA-Project46-Solution-Demo-English.pptx"
SCRIPT = ROOT / "AMA-项目46-解决方案演示讲稿-中英双语.md"
STATIC = ROOT / "src" / "static"


def cover(prs, lang, n):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, COLORS["deep"])
    if lang == "zh":
        title = "Project 46\n自主零售智能 Agent 平台"
        subtitle = "把客户数据、全渠道个性化和五 Agent 落到一个可审批、可执行、可审计的零售经营闭环"
        meta = "王缘 · AMA Capstone"
    else:
        title = "Project 46\nAutonomous Retail Intelligence Agent Platform"
        subtitle = "Turning customer data, omni-channel personalization and five Agents into an approvable, executable and auditable retail operating loop"
        meta = "Yuan Wang · AMA Capstone"
    add_text(slide, 0.9, 0.78, 11.5, 1.55, title, 36, "white", True, PP_ALIGN.CENTER)
    add_text(slide, 1.15, 3.05, 10.9, 0.68, subtitle, 18, "soft_green", align=PP_ALIGN.CENTER)
    add_text(slide, 1.1, 6.35, 5.6, 0.28, meta, 12, "soft_green")
    add_text(slide, 11.95, 7.05, 0.8, 0.22, str(n), 8.5, "soft_green", align=PP_ALIGN.RIGHT)


def statement_slide(prs, lang, n, title, subtitle, main, bullets, accent="deep"):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    from gen_project46_revised_ppt import add_shape, header, add_bullets
    header(slide, title, subtitle, n, lang)
    add_shape(slide, 0.95, 1.72, 11.45, 1.55, accent, None)
    add_text(slide, 1.35, 2.12, 10.65, 0.48, main, 23, "white", True, PP_ALIGN.CENTER)
    add_bullets(slide, 1.15, 4.0, 10.95, 2.3, bullets, 14.5, "ink")


ZH = [
    ("agenda", "今天的演示逻辑", "不是回答补充问题，而是展示 46 号课题的一套解决方案。", [
        ("1. 课题目标", "客户数据整合、全渠道个性化、五 Agent、自主但可治理。", "green"),
        ("2. 业务场景", "上海夏季热浪下，会员需求上升但门店库存不均。", "red"),
        ("3. 系统方案", "Customer 360 + Retail Decision Case + 五 Agent 协同。", "blue"),
        ("4. 经营闭环", "预测、方案、审批、执行、审计和复盘。", "amber"),
        ("5. Azure 落地", "云原生运行时、AI 编排、数据与治理服务栈。", "purple"),
        ("6. 试点衡量", "用 test/control 验证销售、库存、满意度和 LTV。", "green"),
    ]),
    ("statement", "1. Project 46 要解决什么", "课题不是做一个 AI 菜单，而是让零售企业能跨渠道自主交付个性化体验。", "核心命题：个性化只有同时理解客户、库存、价格、授权和履约，才可能真正落地。", [
        "客户在线上浏览、移动端加购、门店试穿、POS 成交，数据天然分散。",
        "如果推荐不看库存，会承诺无法履约的商品；如果营销不看授权，会触碰合规风险。",
        "Project 46 的方案是把五个 Agent 放进一个可治理的零售决策系统。",
    ]),
    ("two", "2. 业务场景：上海夏季热浪", "用一个具体经营事件承载整套解决方案。", ("触发事件", [
        "天气预报显示未来 7 天持续高温。",
        "App / 小程序搜索 AIRism、防晒、速干商品上升。",
        "门店试穿和 POS 转化升高，但黑色 M/L 出现断码风险。",
        "部分奥莱门店库存偏高，存在调拨和会员券机会。",
    ], "red"), ("系统需要回答", [
        "哪些客户值得触达？",
        "哪些 SKU 可以推荐，哪些不能推荐？",
        "哪些门店需要补货或调拨？",
        "价格、会员券和营销动作是否被允许？",
    ], "green")),
    ("process", "3. 解决方案总览", "一个业务事件如何变成可执行的个性化动作。", [
        ("Customer 360", "统一会员、App、门店、POS 和服务信号。", "green"),
        ("Decision Case", "把商品、门店、SKU、信号和 SLA 固化为一个经营对象。", "blue"),
        ("Five Agents", "客户、个性化、库存、定价、营销围绕同一 Case 协作。", "amber"),
        ("Human Approval", "区域经理或管理层审批高风险动作。", "purple"),
        ("Execution & Learn", "写入下游系统，保留回执并复盘业务效果。", "red"),
    ]),
    ("grid", "4. 客户数据整合：Customer 360", "先建立连续上下文，个性化才有基础。", [
        ("身份", "会员 ID、App ID、门店 POS、平台账号在授权范围内对齐。", "green"),
        ("行为", "浏览、搜索、加购、试穿、购买、退货、投诉。", "blue"),
        ("意图", "通勤防晒、儿童运动、防闷汗、价格敏感、服务恢复。", "amber"),
        ("授权", "按国家/渠道记录 consent，未授权客户不触达。", "red"),
        ("渠道偏好", "App、小程序、邮件、门店、平台和自提偏好。", "purple"),
        ("价值", "LTV、留存风险、会员等级和服务敏感度。", "green"),
    ]),
    ("process", "5. 全渠道个性化旅程", "同一个客户上下文贯穿线上、移动端和门店。", [
        ("Browse", "客户在 App / 天猫看到夏季商品。", "green"),
        ("Personalize", "系统只推荐有库存且可履约的商品。", "blue"),
        ("Check Store", "客户查看附近门店可售库存和自提选项。", "amber"),
        ("Visit", "门店试穿与 POS 反馈更新画像。", "purple"),
        ("Retain", "售后、复购和下一次推荐继续使用同一上下文。", "red"),
    ]),
    ("two", "6. Retail Decision Case：系统的业务对象", "Agent 输出必须变成业务可处理对象，而不是一段聊天文本。", ("Case 里有什么", [
        "门店、商品、SKU 组合、库存快照、需求信号、SLA。",
        "候选方案、备选方案、风险、护栏、审批角色。",
        "执行动作、回执、审计日志和复盘指标。",
    ], "blue"), ("为什么关键", [
        "评委看到的不只是 AI 能说，而是企业能处理。",
        "区域经理可以审批，系统可以执行，审计可以追踪。",
        "这也是五个 Agent 共享同一事实状态的载体。",
    ], "green")),
    ("grid", "7. 五个 Agent 的分工", "五个 Agent 是业务能力域，不是五个孤立 chatbot。", [
        ("Customer Understanding", "识别客户、意图、授权、偏好和生命周期。", "green"),
        ("Personalization", "生成可履约的商品、内容、渠道和下一步动作。", "blue"),
        ("Inventory", "预测 SKU / 门店 / 渠道需求，建议补货或调拨。", "amber"),
        ("Pricing", "结合需求、竞争、库存和毛利护栏给出价格建议。", "purple"),
        ("Marketing", "选择已授权高意向人群，生成活动草稿和预算。", "red"),
        ("Orchestration", "共享 Case 状态，控制顺序、跳过、阻断和审计。", "green"),
    ]),
    ("process", "8. Agent 如何协作形成决策包", "每个 Agent 只回答自己领域的问题。", [
        ("Who", "Customer Agent 判断客户是谁、是否授权、是否有意图。", "green"),
        ("What", "Personalization Agent 选择商品与体验。", "blue"),
        ("Can fulfill", "Inventory Agent 校验 ATP、调拨和补货能力。", "amber"),
        ("Is safe", "Pricing Agent 校验价格、毛利和竞品压力。", "purple"),
        ("How activate", "Marketing Agent 形成受控触达方案。", "red"),
    ]),
    ("two", "9. AI 决策智能：业务用户真正看到什么", "页面展示经营方案，不展示内部模型流水线。", ("区域经理看到", [
        "未来 7 天需求预测。",
        "不行动、调拨、调拨 + 会员券、全渠道降价等方案比较。",
        "门店当前可售、跨店调拨、配送中心补货和销售限制。",
    ], "blue"), ("审计详情保留", [
        "五 Agent 协作轨迹。",
        "会员授权、库存可信度、毛利底线和生产写入护栏。",
        "执行后预测与实际对比。",
    ], "purple")),
    ("two", "10. 业务规则与人工审批", "自主不等于失控，规则让 AI 能进入企业流程。", ("确定性护栏", [
        "未授权客户不能触达。",
        "低可信库存不能推荐。",
        "低于毛利底线的折扣被阻断。",
        "审批前不写 ERP / WMS / OMS / CRM。",
    ], "red"), ("角色边界", [
        "店长确认门店事实。",
        "区域经理审批补货和调拨。",
        "管理层审批重大促销、价格例外和预算。",
        "AI 推荐、解释、草拟和监控。",
    ], "green")),
    ("two", "11. 四季沙盘如何服务主线", "它不是另一套系统，而是风险发现入口。", ("沙盘做什么", [
        "模拟春夏秋冬、节假日、天气和商品生命周期变化。",
        "提前发现可能的断码、滞销、履约和促销风险。",
        "帮助管理层理解未来经营压力。",
    ], "amber"), ("它不做什么", [
        "不直接生成生产动作。",
        "不把模拟数字伪装成已发生销售。",
        "必须经过数据核验，才可能形成 Retail Decision Case。",
    ], "red")),
    ("grid", "12. 现场系统演示路径", "演示按业务故事走，不按功能菜单走。", [
        ("首页", "一句话说明课题、客户数据、全渠道和五 Agent。", "green"),
        ("区域经理", "进入上海 Case，看 SKU、库存、信号和下一步。", "blue"),
        ("AI 决策助手", "展示预测、方案比较、供货限制和护栏。", "amber"),
        ("审批", "说明 AI 不直接写生产，需授权角色批准。", "purple"),
        ("复盘审计", "展示执行回执、政策阻断和后续学习。", "red"),
        ("四季沙盘", "补充说明它是规划风险发现，不是生产执行入口。", "green"),
    ]),
    ("architecture", "13. Azure 云原生架构", "从演示应用到企业生产架构的落地路径。"),
    ("grid", "14. Azure 服务栈", "服务清单不是堆名字，而是支撑解决方案的各层能力。", [
        ("Azure Container Apps", "承载 FastAPI Agent Runtime，支持 revision、健康探针和流量切换。", "green"),
        ("Azure OpenAI / AI Foundry", "五 Agent 推理、编排、评估和安全测试。", "blue"),
        ("Cosmos DB", "保存 Customer 360、Case、Agent 状态、审批和审计日志。", "amber"),
        ("Azure AI Search", "检索商品、政策、FAQ、历史案例和知识库。", "purple"),
        ("API Management + MCP", "作为企业 API 和工具调用网关。", "red"),
        ("Service Bus / Event Grid", "驱动异步 Agent 任务、执行回执和补偿流程。", "green"),
        ("Managed Identity / Key Vault", "管理身份、密钥和最小权限访问。", "blue"),
        ("App Insights / Log Analytics", "监控 API、Agent 调用、错误、延迟和业务事件。", "amber"),
        ("Fabric / Power BI", "承接经营指标、test/control 试点和管理看板。", "purple"),
    ]),
    ("two", "15. 为什么这些 Azure 服务是先进且必要的", "每个先进服务都对应一个企业级问题。", ("AI 原生能力", [
        "AI Foundry 负责 Agent 编排、评估和安全治理。",
        "Azure OpenAI 负责推理、生成和结构化决策解释。",
        "AI Search 让 Agent 能基于商品、政策和历史知识回答。",
    ], "blue"), ("生产级能力", [
        "Container Apps 支持弹性、revision 和灰度。",
        "Cosmos DB 支持低延迟状态与全球分布。",
        "APIM、Managed Identity、Key Vault 和可观测性让系统可治理。",
    ], "green")),
    ("grid", "16. 当前实现证据", "原型已经证明系统形态，而不是声称业务指标已实现。", [
        ("生产应用", "已部署 Azure Container Apps，支持公开演示入口。", "green"),
        ("Case API", "提供 Retail Decision Case 列表、详情、审批和执行接口。", "blue"),
        ("Decision Intelligence", "每个 Case 有只读 AI 决策智能接口和详情页。", "amber"),
        ("角色工作台", "店长、区域经理、管理层看到不同任务与权限。", "purple"),
        ("审计与护栏", "政策阻断、执行回执和 Agent 结果可追踪。", "red"),
        ("中英演示", "中文业务界面和英文答辩路径均可点击。", "green"),
    ]),
    ("two", "17. 成功指标如何验证", "课题里的数字是试点目标，不是 demo 已经实现的结果。", ("试点目标", [
        "+40% 同店销售：看 test/control 门店转化、客单价和复购。",
        "-50% 库存浪费：看滞销、缺货、markdown loss 和调拨效率。",
        "85% 满意度：看调查、投诉、退货原因和服务恢复。",
        "+60% LTV：看会员 cohort 留存和复购。",
    ], "green"), ("验证设计", [
        "先选 baseline，再选试点门店和对照组。",
        "Agent 建议仍需人工审批。",
        "只有护栏、执行和 KPI 稳定后才扩大规模。",
    ], "blue")),
    ("statement", "18. 最终结论", "用一句话收束整套解决方案。", "Project 46 不是展示五个 Agent，而是展示 AI 如何进入零售企业的经营系统。", [
        "它回答课题要求：客户数据整合、全渠道个性化、五 Agent 和亚洲区域挑战。",
        "它证明企业可落地：审批、执行、审计、复盘和 Azure 云原生架构。",
        "它把个性化从“推荐内容”升级为“受控经营决策”。",
    ]),
]


EN = [
    ("agenda", "Today’s Solution Story", "This is a Project 46 solution demo, not a list of answers to follow-up questions.", [
        ("1. Assignment Goal", "Customer data integration, omni-channel personalization, five Agents, autonomous but governed.", "green"),
        ("2. Business Scenario", "A Shanghai heatwave creates demand surge and uneven store inventory.", "red"),
        ("3. System Design", "Customer 360 + Retail Decision Case + five-Agent collaboration.", "blue"),
        ("4. Operating Loop", "Forecast, options, approval, execution, audit and learning.", "amber"),
        ("5. Azure Landing", "Cloud-native runtime, AI orchestration, data and governance stack.", "purple"),
        ("6. Pilot Measurement", "Use test/control to prove sales, waste, satisfaction and LTV impact.", "green"),
    ]),
    ("statement", "1. What Project 46 Solves", "The assignment is not to build an AI menu. It asks for autonomous omni-channel personalization through customer data integration.", "Personalization only works when it understands customer, inventory, price, consent and fulfillment at the same time.", [
        "A customer browses online, adds to cart on mobile, tries in store and buys through POS.",
        "Recommendations fail if inventory is unavailable; campaigns create risk if consent is missing.",
        "Project 46 puts the five Agents inside a governable retail decision system.",
    ]),
    ("two", "2. Business Scenario: Shanghai Heatwave", "One concrete operating event carries the whole solution.", ("Trigger", [
        "The next 7 days are forecast to be very hot.",
        "Searches for AIRism, UV protection and quick-dry products rise.",
        "Store try-on and POS conversion increase, but black M/L sizes face stockout risk.",
        "Some outlet stores have excess stock, creating transfer and member offer opportunities.",
    ], "red"), ("System Questions", [
        "Which customers should be reached?",
        "Which SKUs can be recommended, and which cannot?",
        "Which stores need replenishment or transfer?",
        "Are price, coupon and marketing actions allowed?",
    ], "green")),
    ("process", "3. Solution Overview", "How one business event becomes executable personalized actions.", [
        ("Customer 360", "Unify member, app, store, POS and service signals.", "green"),
        ("Decision Case", "Turn product, store, SKU, signals and SLA into one operating object.", "blue"),
        ("Five Agents", "Customer, personalization, inventory, pricing and marketing collaborate on one Case.", "amber"),
        ("Human Approval", "Regional or executive roles approve high-risk actions.", "purple"),
        ("Execution & Learn", "Write approved actions downstream, keep receipts and learn from outcome.", "red"),
    ]),
    ("grid", "4. Customer Data Integration: Customer 360", "Continuous context is the foundation of personalization.", [
        ("Identity", "Align loyalty ID, app ID, store POS and marketplace account where consent allows.", "green"),
        ("Behavior", "Browse, search, cart, try-on, purchase, return and complaint.", "blue"),
        ("Intent", "Commute cooling, kids sports, anti-sweat, price sensitivity, service recovery.", "amber"),
        ("Consent", "Record channel and market consent; no outreach without permission.", "red"),
        ("Channel Preference", "App, mini-program, email, store, marketplace and pickup preference.", "purple"),
        ("Value", "LTV, retention risk, tier and service sensitivity.", "green"),
    ]),
    ("process", "5. Omni-channel Personalization Journey", "One customer context moves across online, mobile and store.", [
        ("Browse", "Customer sees summer products in app or marketplace.", "green"),
        ("Personalize", "The system recommends only products that can be fulfilled.", "blue"),
        ("Check Store", "Customer sees nearby sellable stock and pickup options.", "amber"),
        ("Visit", "Store try-on and POS feedback update the profile.", "purple"),
        ("Retain", "Service, repeat purchase and next recommendation reuse the same context.", "red"),
    ]),
    ("two", "6. Retail Decision Case: The Business Object", "Agent output must become something the enterprise can process.", ("What The Case Contains", [
        "Store, product, SKU combination, inventory snapshot, demand signals and SLA.",
        "Candidate options, alternatives, risks, guardrails and approver roles.",
        "Execution actions, receipts, audit log and learning metrics.",
    ], "blue"), ("Why It Matters", [
        "The panel sees an operating system, not just AI talking.",
        "A regional manager can approve, systems can execute and audit can trace.",
        "It is the shared state for all five Agents.",
    ], "green")),
    ("grid", "7. Five-Agent Operating Model", "The five Agents are business domains, not isolated chatbots.", [
        ("Customer Understanding", "Identity, intent, consent, preference and lifecycle.", "green"),
        ("Personalization", "Fulfillable product, content, channel and next best action.", "blue"),
        ("Inventory", "Demand forecast, ATP confidence, replenishment and transfer.", "amber"),
        ("Pricing", "Demand, competition, inventory and margin guardrails.", "purple"),
        ("Marketing", "Consented high-intent audience, draft campaign and budget.", "red"),
        ("Orchestration", "Shared Case state, sequence, skip, block and audit.", "green"),
    ]),
    ("process", "8. How Agents Create A Decision Packet", "Each Agent answers one domain question.", [
        ("Who", "Customer Agent checks identity, consent and intent.", "green"),
        ("What", "Personalization Agent chooses product and experience.", "blue"),
        ("Can fulfill", "Inventory Agent checks ATP, transfer and replenishment.", "amber"),
        ("Is safe", "Pricing Agent checks price, margin and competition.", "purple"),
        ("How activate", "Marketing Agent creates a governed outreach plan.", "red"),
    ]),
    ("two", "9. What Business Users Actually See", "The screen shows operating decisions, not internal model pipelines.", ("Regional Manager View", [
        "7-day demand forecast.",
        "No action, transfer, transfer plus member coupon, and broad markdown options.",
        "Store sellable stock, cross-store transfer, DC replenishment and selling limits.",
    ], "blue"), ("Audit Detail Keeps", [
        "Five-Agent collaboration trace.",
        "Consent, inventory confidence, margin floor and production-write guardrails.",
        "Forecast versus actual after execution.",
    ], "purple")),
    ("two", "10. Business Rules and Human Approval", "Autonomous does not mean uncontrolled.", ("Deterministic Guardrails", [
        "No outreach without consent.",
        "No recommendation on low-confidence inventory.",
        "Discount below margin floor is blocked.",
        "No ERP / WMS / OMS / CRM write before approval.",
    ], "red"), ("Role Boundaries", [
        "Store manager confirms store facts.",
        "Regional manager approves transfer and replenishment.",
        "Executives approve major promotion, price exception and budget.",
        "AI recommends, explains, drafts and monitors.",
    ], "green")),
    ("two", "11. How The Seasonal Sandbox Fits", "It is the risk-discovery entry point, not another production system.", ("What It Does", [
        "Simulates seasons, holidays, weather and product lifecycle changes.",
        "Detects possible stockout, overstock, fulfillment and campaign risk.",
        "Helps leadership understand future operating pressure.",
    ], "amber"), ("What It Does Not Do", [
        "It does not trigger production actions.",
        "It does not present simulated numbers as actual sales.",
        "Only verified signals can become a Retail Decision Case.",
    ], "red")),
    ("grid", "12. Live System Demo Path", "The demo follows the business story, not the menu.", [
        ("Home", "State assignment fit: customer data, omni-channel, five Agents.", "green"),
        ("Regional Manager", "Open the Shanghai Case and show SKU, inventory, signals and next step.", "blue"),
        ("Decision Support", "Show forecast, option comparison, supply limit and guardrails.", "amber"),
        ("Approval", "Explain that AI does not write production without authorization.", "purple"),
        ("Audit", "Show receipts, policy blocks and learning loop.", "red"),
        ("Seasonal Sandbox", "Explain it as planning risk discovery, not production execution.", "green"),
    ]),
    ("architecture", "13. Azure Cloud-Native Architecture", "The landing path from demo app to enterprise production architecture."),
    ("grid", "14. Azure Service Stack", "The services support layers of the solution, not a name-dropping list.", [
        ("Azure Container Apps", "FastAPI Agent Runtime, revisions, health probes and traffic shifting.", "green"),
        ("Azure OpenAI / AI Foundry", "Agent reasoning, orchestration, evaluation and safety testing.", "blue"),
        ("Cosmos DB", "Customer 360, Cases, Agent state, approval and audit logs.", "amber"),
        ("Azure AI Search", "Product, policy, FAQ, historical case and knowledge retrieval.", "purple"),
        ("API Management + MCP", "Enterprise API and tool gateway.", "red"),
        ("Service Bus / Event Grid", "Async Agent tasks, execution receipts and compensation workflows.", "green"),
        ("Managed Identity / Key Vault", "Identity, secrets and least-privilege access.", "blue"),
        ("App Insights / Log Analytics", "API, Agent calls, errors, latency and business events.", "amber"),
        ("Fabric / Power BI", "Business metrics, test/control pilot and executive dashboard.", "purple"),
    ]),
    ("two", "15. Why These Azure Services Are Advanced and Necessary", "Every advanced service maps to an enterprise problem.", ("AI-native Capabilities", [
        "AI Foundry for Agent orchestration, evaluation and safety governance.",
        "Azure OpenAI for reasoning, generation and structured decision explanations.",
        "AI Search grounds Agents in product, policy and historical knowledge.",
    ], "blue"), ("Production-grade Capabilities", [
        "Container Apps provides elasticity, revisions and rollout control.",
        "Cosmos DB provides low-latency state and global distribution path.",
        "APIM, Managed Identity, Key Vault and observability make the system governable.",
    ], "green")),
    ("grid", "16. Current Implementation Evidence", "The prototype proves system shape, not claimed business lift.", [
        ("Production App", "Deployed on Azure Container Apps with public demo endpoint.", "green"),
        ("Case API", "Retail Decision Case list, detail, approval and execution APIs.", "blue"),
        ("Decision Intelligence", "Read-only AI decision API and detail view per Case.", "amber"),
        ("Role Workspaces", "Store, regional and executive users see different tasks and permissions.", "purple"),
        ("Audit and Guardrails", "Policy blocks, execution receipts and Agent outputs are traceable.", "red"),
        ("Bilingual Demo", "Chinese business flow and English defense path are clickable.", "green"),
    ]),
    ("two", "17. How Success Will Be Measured", "The assignment numbers are pilot targets, not demo achievements.", ("Pilot Targets", [
        "+40% same-store sales: conversion, basket size and repeat purchase in test/control stores.",
        "-50% waste: aging stock, stockout, markdown loss and transfer efficiency.",
        "85% satisfaction: survey, complaint, return reason and service recovery.",
        "+60% LTV: member cohort retention and repeat purchase.",
    ], "green"), ("Experiment Design", [
        "Choose baseline, pilot stores and control stores.",
        "Agent recommendations still go through human approval.",
        "Scale only when guardrails, execution and KPIs are stable.",
    ], "blue")),
    ("statement", "18. Closing Message", "One sentence to close the solution.", "Project 46 is not a demo of five Agents. It shows how AI enters the retail operating system.", [
        "It matches the prompt: customer data integration, omni-channel personalization, five Agents and Asia-specific challenges.",
        "It proves enterprise readiness: approval, execution, audit, learning and Azure cloud-native architecture.",
        "It upgrades personalization from recommendation content into governed retail decisions.",
    ]),
]


SCRIPT_ZH = [
    "各位老师好，我的项目是 Project 46，自主零售智能 Agent 平台。今天我不按功能菜单讲，而是按一个真实零售经营事件讲：系统如何整合客户数据，跨渠道做个性化，并让五个 Agent 形成可审批、可执行、可审计的经营动作。",
    "今天的逻辑是完整解决方案。先讲课题目标，再进入上海夏季热浪场景，然后讲 Customer 360、Retail Decision Case、五个 Agent、人工审批和 Azure 架构，最后说明如何验证业务指标。",
    "Project 46 的核心不是做一个 AI 菜单。它要解决的是：个性化必须同时理解客户、库存、价格、授权和履约，否则推荐会不可执行，营销会有合规风险。",
    "我用上海热浪作为演示场景。高温带来需求上升，App 搜索和门店转化都变强，但黑色 M/L 出现断码风险，同时部分门店有可调拨库存。",
    "解决方案从 Customer 360 开始，把客户、门店和渠道信号合到一起。然后形成 Retail Decision Case，再由五个 Agent 生成方案，最后由人审批并执行。",
    "Customer 360 是个性化的基础。它不是把所有数据随便拼起来，而是在授权范围内统一身份、行为、意图、渠道偏好和客户价值。",
    "全渠道体验的关键是上下文连续。客户从 App 到门店再到售后，系统始终知道这个人看过什么、是否授权、附近门店有没有货，以及下一步适合做什么。",
    "Retail Decision Case 是系统里的业务对象。它把门店、商品、SKU、库存、信号、SLA、方案、审批和审计放在一起，让 Agent 输出可以被企业处理。",
    "五个 Agent 是五个业务能力域。Customer 理解客户，Personalization 做体验，Inventory 判断履约，Pricing 保护毛利，Marketing 负责受控触达。",
    "Agent 协作不是五个机器人聊天，而是围绕同一个 Case 逐步回答：对谁、给什么、能不能履约、价格是否安全、怎么触达。",
    "业务用户看到的是经营方案，不是内部模型流水线。区域经理主要看预测、供货限制、方案比较和护栏；详细轨迹放在审计里。",
    "业务规则和人工审批让自主 Agent 可控。未授权客户不能触达，低可信库存不能推荐，低于毛利底线的折扣被阻断，审批前不写生产系统。",
    "四季沙盘是风险发现入口。它帮助提前发现季节性风险，但不直接发起生产动作；只有经过数据核验，才可能变成 Retail Decision Case。",
    "现场演示我会按业务故事走：首页说明课题贴合，区域经理打开上海 Case，进入决策助手，看预测和方案，再看审批、审计和四季沙盘。",
    "Azure 架构分层很清楚：体验层、入口和 API、Agent Runtime、AI 编排、数据知识层、安全和运维层。",
    "Azure 服务栈不是堆名字。Container Apps 负责运行时，Azure OpenAI 和 AI Foundry 负责 Agent，Cosmos DB 保存状态，AI Search 做知识检索，APIM 和 Service Bus 做集成，Key Vault 和可观测性做治理。",
    "这些先进服务对应企业级问题：AI Foundry 让 Agent 可编排和可评估，Container Apps 支持灰度和弹性，Cosmos DB 支持低延迟状态，APIM、身份和监控让系统可治理。",
    "当前原型已经证明系统形态：有生产应用、Case API、AI 决策智能、角色工作台、审计护栏和中英可点击演示。",
    "最后，课题里的 +40%、-50%、85% 和 +60% 是试点目标，不是 demo 已经实现。后续要用 test/control 门店和 cohort 来验证。",
    "我的结论是：Project 46 不是展示五个 Agent，而是展示 AI 如何进入零售企业经营系统，把个性化从推荐内容升级为受控经营决策。",
]

SCRIPT_EN = [
    "Hello everyone. My project is Project 46, the Autonomous Retail Intelligence Agent Platform. I will not present it as a feature menu. I will use one retail operating event to show how the system integrates customer data, delivers omni-channel personalization, and turns five Agents into approvable, executable and auditable business actions.",
    "The logic today is a complete solution story. I start with the assignment goal, then the Shanghai heatwave scenario, then Customer 360, Retail Decision Case, five Agents, human approval and Azure architecture, and finally business measurement.",
    "The core of Project 46 is not an AI menu. Personalization must understand customer, inventory, price, consent and fulfillment at the same time. Otherwise, recommendations cannot be executed and campaigns create compliance risk.",
    "I use a Shanghai heatwave as the demo scenario. Hot weather increases demand. App search and store conversion rise, but black M/L sizes face stockout risk, while some stores still have transferable inventory.",
    "The solution starts with Customer 360, combines customer, store and channel signals, creates a Retail Decision Case, lets five Agents produce options, and then routes high-risk actions to human approval and execution.",
    "Customer 360 is the foundation of personalization. It does not freely combine all data. It aligns identity, behavior, intent, channel preference and customer value only within consent boundaries.",
    "The key to omni-channel experience is context continuity. From app to store to service, the system knows what the customer viewed, whether consent exists, whether nearby inventory exists, and what next action is suitable.",
    "Retail Decision Case is the business object of the system. It keeps store, product, SKU, inventory, signals, SLA, options, approval and audit together, so Agent output becomes enterprise-processable.",
    "The five Agents are business domains. Customer understands the customer, Personalization designs the experience, Inventory checks fulfillment, Pricing protects margin, and Marketing handles governed outreach.",
    "Agent collaboration is not five chatbots talking. It answers step by step: who, what experience, can we fulfill, is the price safe, and how should we activate.",
    "Business users see operating decisions, not internal model pipelines. The regional manager sees forecast, supply limits, option comparison and guardrails. The detailed trace stays in audit.",
    "Business rules and human approval make autonomy controllable. No outreach without consent, no recommendation on low-confidence inventory, discounts below margin floor are blocked, and no production write happens before approval.",
    "The seasonal sandbox is a risk discovery entry point. It detects seasonal risks early, but it does not trigger production actions. Only verified signals can become a Retail Decision Case.",
    "The live demo follows the business story: home page for prompt fit, regional manager opens the Shanghai Case, decision support shows forecast and options, then approval, audit and seasonal sandbox.",
    "The Azure architecture is layered: experience, ingress and API, Agent Runtime, AI orchestration, data and knowledge, security and operations.",
    "The Azure service stack is not name-dropping. Container Apps runs the runtime. Azure OpenAI and AI Foundry power Agents. Cosmos DB stores state. AI Search retrieves knowledge. APIM and Service Bus handle integration. Key Vault and observability provide governance.",
    "These advanced services map to enterprise problems. AI Foundry enables orchestration and evaluation. Container Apps supports rollout and elasticity. Cosmos DB supports low-latency state. APIM, identity and monitoring make the system governable.",
    "The current prototype proves the system shape: production app, Case API, AI decision intelligence, role workspaces, audit guardrails and bilingual clickable demo.",
    "Finally, +40%, -50%, 85% and +60% are pilot targets from the assignment, not demo achievements. They should be validated by test/control stores and customer cohorts.",
    "My conclusion is: Project 46 is not a demo of five Agents. It shows how AI enters the retail operating system and upgrades personalization from recommendation content to governed retail decisions.",
]


def build(data, lang):
    prs = new_prs()
    cover(prs, lang, 1)
    slide_no = 2
    for entry in data:
        kind = entry[0]
        if kind == "agenda" or kind == "grid":
            _, title, subtitle, items = entry
            grid_slide(prs, lang, slide_no, title, subtitle, items, cols=3)
        elif kind == "two":
            _, title, subtitle, left, right = entry
            two_col_slide(prs, lang, slide_no, title, subtitle, left, right)
        elif kind == "process":
            _, title, subtitle, steps = entry
            process_slide(prs, lang, slide_no, title, subtitle, steps)
        elif kind == "architecture":
            _, title, subtitle = entry
            architecture_slide(prs, lang, slide_no, title, subtitle, ARCH_ZH if lang == "zh" else ARCH_EN)
        elif kind == "statement":
            _, title, subtitle, main, bullets = entry
            statement_slide(prs, lang, slide_no, title, subtitle, main, bullets)
        slide_no += 1
    closing_slide(prs, lang, slide_no)
    return prs


def write_script():
    titles_zh = ["封面"] + [x[1] for x in ZH] + ["收尾"]
    titles_en = ["Cover"] + [x[1] for x in EN] + ["Closing"]
    zh_lines = SCRIPT_ZH + [SCRIPT_ZH[-1]]
    en_lines = SCRIPT_EN + [SCRIPT_EN[-1]]
    lines = [
        "# Project 46 解决方案演示讲稿 / Solution Demo Speaker Script",
        "",
        "定位：这版是解决方案演示稿，不是问题答复稿。问题点会自然嵌入故事，而不是单独答疑。",
        "",
    ]
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
