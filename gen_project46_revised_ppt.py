#!/usr/bin/env python3
"""Generate revised Project 46 Chinese and English decks plus speaker script."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parent
OUT_ZH = ROOT / "AMA-项目46-答辩故事线-中文.pptx"
OUT_EN = ROOT / "AMA-Project46-Defense-Storyline-English.pptx"
SCRIPT = ROOT / "AMA-项目46-逐页口述脚本-中英双语.md"
STATIC = ROOT / "src" / "static"


COLORS = {
    "bg": RGBColor(247, 247, 244),
    "ink": RGBColor(32, 36, 34),
    "muted": RGBColor(91, 99, 95),
    "line": RGBColor(214, 219, 214),
    "surface": RGBColor(255, 255, 255),
    "deep": RGBColor(18, 65, 60),
    "green": RGBColor(28, 131, 111),
    "blue": RGBColor(30, 93, 142),
    "amber": RGBColor(169, 101, 15),
    "red": RGBColor(194, 54, 43),
    "purple": RGBColor(104, 78, 145),
    "soft_green": RGBColor(228, 245, 239),
    "soft_blue": RGBColor(232, 241, 248),
    "white": RGBColor(255, 255, 255),
}

ACCENTS = ["green", "blue", "amber", "purple", "red"]


def new_prs():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def set_bg(slide, color=None):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color or COLORS["bg"]


def add_shape(slide, x, y, w, h, fill="surface", line="line", rounded=True):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = COLORS[fill] if isinstance(fill, str) else fill
    if line:
        s.line.color.rgb = COLORS[line] if isinstance(line, str) else line
        s.line.width = Pt(1)
    else:
        s.line.fill.background()
    return s


def add_text(slide, x, y, w, h, value, size=15, color="ink", bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    p = tf.paragraphs[0]
    p.text = value
    p.font.name = "Microsoft YaHei"
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = COLORS[color] if isinstance(color, str) else color
    p.alignment = align
    return box


def add_bullets(slide, x, y, w, h, items, size=13, color="ink"):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item if item.startswith(("•", "-", "1.", "2.", "3.", "4.", "5.")) else f"• {item}"
        p.font.name = "Microsoft YaHei"
        p.font.size = Pt(size)
        p.font.color.rgb = COLORS[color] if isinstance(color, str) else color
        p.space_after = Pt(6)
    return box


def header(slide, title, subtitle, n, lang):
    add_text(slide, 0.55, 0.32, 11.7, 0.45, title, 21, "ink", True)
    if subtitle:
        add_text(slide, 0.57, 0.82, 11.4, 0.28, subtitle, 10.5, "muted")
    add_shape(slide, 0.55, 1.20, 12.2, 0.02, "line", None, False)
    footer(slide, n, lang)


def footer(slide, n, lang):
    label = "AMA Project 46 · Autonomous Retail Intelligence Agent Platform"
    if lang == "zh":
        label = "AMA 项目 46 · 自主零售智能 Agent 平台"
    add_text(slide, 0.58, 7.08, 7.2, 0.22, label, 8.5, "muted")
    add_text(slide, 12.1, 7.08, 0.65, 0.22, str(n), 8.5, "muted", align=PP_ALIGN.RIGHT)


def cover(prs, lang, n):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, COLORS["deep"])
    add_shape(slide, 0, 0, 13.333, 0.10, "red", None, False)
    if lang == "zh":
        title = "自主零售智能\nAgent 平台"
        sub = "从客户数据整合到可审批、可执行、可审计的零售决策闭环"
        presenter = "王缘 · AMA Capstone · Project 46"
    else:
        title = "Autonomous Retail\nIntelligence Agent Platform"
        sub = "From customer data integration to approvable, executable and auditable retail decisions"
        presenter = "Yuan Wang · AMA Capstone · Project 46"
    add_text(slide, 0.78, 1.18, 11.8, 1.5, title, 39, "white", True)
    add_text(slide, 0.82, 3.08, 11.6, 0.45, sub, 18, "soft_green")
    add_shape(slide, 0.82, 4.05, 11.7, 1.35, "surface", None)
    claim = (
        "五个 Agent 不是五个聊天机器人，而是一套把“发现 → 核验 → 决策 → 执行 → 复盘”跑通的经营系统。"
        if lang == "zh"
        else "The five Agents are not five chatbots. They form an operating system for discover, verify, decide, execute and learn."
    )
    add_text(slide, 1.15, 4.34, 11.0, 0.58, claim, 20, "deep", True, PP_ALIGN.CENTER)
    add_text(slide, 0.82, 6.35, 6.2, 0.3, presenter, 12, "soft_green")
    footer(slide, n, lang)


def card(slide, x, y, w, h, title, body, accent="green"):
    add_shape(slide, x, y, w, h, "surface", "line")
    add_shape(slide, x, y, 0.07, h, accent, None, False)
    add_text(slide, x + 0.18, y + 0.15, w - 0.32, 0.28, title, 12.5, "ink", True)
    if isinstance(body, list):
        add_bullets(slide, x + 0.18, y + 0.55, w - 0.35, h - 0.65, body, 10.2, "muted")
    else:
        add_text(slide, x + 0.18, y + 0.55, w - 0.35, h - 0.65, body, 10.2, "muted")


def grid_slide(prs, lang, n, title, subtitle, items, cols=3):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    header(slide, title, subtitle, n, lang)
    rows = (len(items) + cols - 1) // cols
    w = 11.8 / cols
    h = 4.9 / rows
    for i, (head, body, accent) in enumerate(items):
        x = 0.72 + (i % cols) * (w + 0.12)
        y = 1.52 + (i // cols) * (h + 0.18)
        card(slide, x, y, w - 0.12, h, head, body, accent)


def two_col_slide(prs, lang, n, title, subtitle, left, right):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    header(slide, title, subtitle, n, lang)
    card(slide, 0.75, 1.55, 5.85, 4.95, left[0], left[1], left[2])
    card(slide, 6.95, 1.55, 5.65, 4.95, right[0], right[1], right[2])


def process_slide(prs, lang, n, title, subtitle, steps):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    header(slide, title, subtitle, n, lang)
    for i, (head, body, accent) in enumerate(steps):
        x = 0.68 + i * 2.48
        add_shape(slide, x, 1.85, 2.14, 3.55, "surface", "line")
        add_shape(slide, x + 0.73, 1.48, 0.68, 0.68, accent, None)
        add_text(slide, x + 0.93, 1.66, 0.26, 0.18, str(i + 1), 10, "white", True, PP_ALIGN.CENTER)
        add_text(slide, x + 0.18, 2.25, 1.78, 0.42, head, 12.7, "ink", True, PP_ALIGN.CENTER)
        add_text(slide, x + 0.18, 2.94, 1.78, 1.45, body, 10.0, "muted", align=PP_ALIGN.CENTER)


def architecture_slide(prs, lang, n, title, subtitle, layers):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide)
    header(slide, title, subtitle, n, lang)
    y_positions = [1.52, 2.38, 3.24, 4.10, 4.96, 5.82]
    for i, (layer, services, accent) in enumerate(layers):
        y = y_positions[i]
        add_shape(slide, 0.82, y, 2.25, 0.52, accent, None)
        add_text(slide, 0.96, y + 0.15, 1.95, 0.16, layer, 9.5, "white", True, PP_ALIGN.CENTER)
        add_shape(slide, 3.32, y, 8.95, 0.52, "surface", "line")
        add_text(slide, 3.52, y + 0.14, 8.55, 0.18, services, 10.2, "ink")
        if i < len(layers) - 1:
            conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(6.9), Inches(y + 0.55), Inches(6.9), Inches(y + 0.78))
            conn.line.color.rgb = COLORS["line"]
            conn.line.width = Pt(1.5)


def closing_slide(prs, lang, n):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(slide, COLORS["deep"])
    if lang == "zh":
        main = "不是“AI 给建议”，而是“AI 进入经营系统”。"
        sub = "Project 46 的价值在于把个性化、库存、价格和营销统一成一个有事实、有护栏、有审批、有复盘的零售决策闭环。"
    else:
        main = "Not AI advice. AI inside the retail operating system."
        sub = "Project 46 turns personalization, inventory, pricing and marketing into one fact-based, governed and auditable decision loop."
    add_text(slide, 1.05, 1.82, 11.2, 1.0, main, 31, "white", True, PP_ALIGN.CENTER)
    add_text(slide, 1.55, 3.65, 10.2, 0.9, sub, 18, "soft_green", align=PP_ALIGN.CENTER)
    footer(slide, n, lang)


ZH = [
    ("agenda", "今天的故事线", "把题目要求、业务真实感、系统演示和 Azure 落地放在一条线上。", [
        ("题目匹配", "客户数据整合、全渠道个性化、五个专业 Agent。", "green"),
        ("业务对象", "Retail Decision Case 承接发现、核验、决策、执行和复盘。", "blue"),
        ("页面组件", "SKU 组合、数据与信号、业务规则、四季沙盘各有明确角色。", "amber"),
        ("企业落地", "权限、护栏、审计、Azure 云原生服务和可观测性。", "purple"),
        ("演示路径", "从首页故事线进入区域经理审批，再展示 AI 决策助手。", "red"),
        ("成功标准", "销售提升、库存浪费下降、满意度和 LTV 作为试点指标。", "green"),
    ]),
    ("statement", "1. 核心问题", "零售企业不是缺少渠道，而是缺少跨渠道可信决策闭环。", [
        ("断裂的客户体验", ["线上浏览、移动端加购、门店试穿、POS 成交和售后服务分散在不同系统。", "个性化如果不理解库存、价格、授权和履约，就会变成不可信推荐。"], "red"),
        ("需要的不是单点模型", ["企业需要一个可以审批、执行、审计和学习的经营对象。", "所以系统以 Retail Decision Case 为中心，而不是以聊天窗口为中心。"], "green"),
    ]),
    ("prompt", "2. 题目要求如何被覆盖", "先证明没有偏题，再进入系统设计。", [
        ("Customer Data", "Customer 360 汇总会员、App、POS、门店、市场渠道和售后信号。", "green"),
        ("Omni-channel", "App、微信/小程序、邮件、天猫/京东、门店 POS 和自提服务共享上下文。", "blue"),
        ("Five Agents", "客户理解、个性化、库存、定价、营销五个 Agent 按同一个 Case 协作。", "amber"),
        ("Advantages", "更高转化、更低缺货/滞销、更少无效触达和更强区域经营响应。", "purple"),
        ("Success Criteria", "同店销售、库存浪费、满意度、LTV、审批时效和执行成功率。", "red"),
        ("Asia Challenges", "隐私授权、语言、支付、平台生态、城市/乡镇门店履约差异。", "green"),
    ]),
    ("process", "3. 经营闭环", "所有页面和组件都服务于这五步。", [
        ("发现", "四季沙盘和市场信号发现风险，不直接写生产动作。", "green"),
        ("核验", "数据与信号区确认事实可信度，例如库存置信度和需求来源。", "blue"),
        ("决策", "五个 Agent 形成方案、备选和风险解释。", "amber"),
        ("执行", "授权角色审批后，才进入调拨、补货、促销等系统动作。", "purple"),
        ("复盘", "执行回执和结果反馈进入下一轮预测与规则校准。", "red"),
    ]),
    ("sku", "4. SKU 组合为什么存在", "SKU 组合不是装饰信息，而是零售决策的最小经营粒度。", [
        ("业务含义", ["一个商品在不同尺码、颜色、门店、生命周期阶段会有完全不同的风险。", "例如黑色 M/L 断码会影响转化，但白色 XS 可能只是自然低动销。"], "green"),
        ("决策作用", ["把需求预测、库存可用量、毛利、调拨成本和履约限制绑定到同一个组合。", "避免 AI 给出“整体好看、局部不可执行”的建议。"], "blue"),
    ]),
    ("signals", "5. 数据与信号为什么存在", "它回答：这个 Case 是事实、推断，还是情景模拟？", [
        ("事实信号", ["POS 销售、门店库存、RFID/盘点、会员行为、订单履约、退货投诉。", "用于判断当前业务状态和可执行边界。"], "green"),
        ("外部/预测信号", ["天气、节假日、活动、平台流量、搜索热度、竞争价格。", "只形成风险提示和情景预测，必须标注为模拟。"], "amber"),
    ]),
    ("rules", "6. 业务规则为什么存在", "它让自主 Agent 变成企业可控系统。", [
        ("护栏", ["未授权客户不能触达；低可信库存不能推荐；低于毛利底线的折扣必须阻断。", "高风险动作进入人工审批，不能直接写 ERP/WMS/OMS/CRM。"], "red"),
        ("组织边界", ["店长确认门店事实；区域经理审批补货和调拨；管理层审批重大价格、促销和预算。", "AI 负责推荐、解释、草拟和监控，不越权替代组织责任。"], "purple"),
    ]),
    ("sandbox", "7. 四季沙盘的目的", "它是规划压力测试，不是另一个生产系统。", [
        ("为什么需要", ["零售季节性很强，夏季热浪、冬季寒潮、春节/黄金周都会改变需求和履约压力。", "沙盘帮助发现潜在风险：哪些 SKU、门店和渠道可能出现断码或滞销。"], "blue"),
        ("如何接入主线", ["沙盘只读输出风险信号；通过数据核验后才能生成 Retail Decision Case。", "这样既保留战略视角，又不让模拟结果伪装成真实销售事实。"], "green"),
    ]),
    ("agents", "8. 五个 Agent 如何协作", "它们围绕同一个 Case 共享状态，而不是各讲各话。", [
        ("Customer", "识别客户、意图、授权、偏好、生命周期和服务风险。", "green"),
        ("Personalization", "生成可履约的商品展示、内容、推荐和下一步动作。", "blue"),
        ("Inventory", "预测 SKU/门店/渠道需求，判断 ATP 可信度并建议补货/调拨。", "amber"),
        ("Pricing", "结合需求、竞争、库存和毛利护栏给出价格建议或阻断。", "purple"),
        ("Marketing", "选择已授权高意向人群，生成活动草稿、预算和触达计划。", "red"),
        ("Orchestration", "统一 Case 状态、证据、备选方案、审批和审计。", "green"),
    ]),
    ("decision", "9. AI 决策智能展示什么", "展示给业务用户的是决策，不是内部编排说明书。", [
        ("预测与方案", ["7 日需求区间预测；0/10/15/20/30% 折扣敏感度；不行动、调拨、调拨+会员券、全渠道降价等方案比较。", "渠道侧展示门店当前可售、跨店调拨、配送中心补货和销售限制。"], "blue"),
        ("可审计证据", ["五 Agent 协作轨迹、政策护栏、执行后学习闭环进入按需展开的审计详情。", "已完成 Case 仍保留 AI 结果入口，证明系统有复盘能力。"], "green"),
    ]),
    ("roles", "10. 角色与权限边界", "业务真实感来自组织责任清晰。", [
        ("门店店长", "确认盘点、收货、陈列和门店事实；没有审批调价或跨店调拨权限。", "green"),
        ("区域经理", "查看区域异常和门店影响，审批补货、调拨并追踪执行。", "blue"),
        ("经营管理层", "审批重大促销、价格例外、预算和跨市场资源配置。", "amber"),
        ("AI 系统", "推荐、解释、草拟、预警和复盘；所有生产动作由授权角色批准。", "purple"),
    ], 2),
    ("demo", "11. 现场演示路径", "演示按故事线走，不按功能菜单走。", [
        ("第一步", "首页：说明题目覆盖、五 Agent、Retail Decision Case 和 Azure-ready 架构。", "green"),
        ("第二步", "区域经理：打开待审批 Case，说明 SKU、信号、风险和建议。", "blue"),
        ("第三步", "AI 决策助手：展示预测、方案比较、护栏和可执行边界。", "amber"),
        ("第四步", "审计/复盘：说明完成态仍保留 AI 结果和持续监控入口。", "purple"),
    ], 2),
    ("azure_list", "12. Azure 服务清单", "从 demo 到企业级生产可以自然演进。", [
        ("AI 与编排", "Azure OpenAI / Azure AI Foundry：推理、Agent 编排、评估和安全测试。", "green"),
        ("运行时", "Azure Container Apps：FastAPI Agent Runtime、自动扩缩容、revision 和流量切换。", "blue"),
        ("数据层", "Azure Cosmos DB：Customer 360、Retail Decision Case、Agent 状态、审计日志。", "amber"),
        ("检索与知识", "Azure AI Search：商品、政策、FAQ、历史案例和知识库检索。", "purple"),
        ("集成与异步", "API Management、Service Bus / Event Grid：企业 API 网关和异步 Agent 任务。", "red"),
        ("安全与运维", "Managed Identity、Key Vault、App Configuration、Application Insights、Log Analytics、Fabric / Power BI。", "green"),
    ]),
    ("architecture", "13. Azure 架构图", "核心是把前端体验、Agent Runtime、AI、数据和治理分层。"),
    ("metrics", "14. 成功指标", "指标不只看模型效果，更看经营闭环是否有效。", [
        ("增长", "同店销售提升、转化率、客单价、复购和会员 LTV。", "green"),
        ("库存", "缺货率、滞销率、库存浪费、调拨成功率和履约时效。", "blue"),
        ("客户", "满意度、触达投诉率、渠道一致性和个性化接受率。", "amber"),
        ("治理", "审批时效、护栏命中率、执行成功率、审计完整性和回滚能力。", "purple"),
    ], 2),
    ("close",),
]


EN = [
    ("agenda", "Today’s Storyline", "One storyline connects the prompt, business realism, live demo and Azure implementation.", [
        ("Prompt fit", "Customer data integration, omni-channel personalization and five specialist Agents.", "green"),
        ("Business object", "Retail Decision Case carries discover, verify, decide, execute and learn.", "blue"),
        ("Page components", "SKU combinations, signals, business rules and seasonal sandbox each have a clear job.", "amber"),
        ("Enterprise readiness", "Roles, guardrails, audit, Azure cloud-native services and observability.", "purple"),
        ("Demo path", "From storyline page to regional approval, then AI decision support.", "red"),
        ("Success targets", "Sales uplift, waste reduction, customer satisfaction and LTV.", "green"),
    ]),
    ("statement", "1. The Core Problem", "Retailers do not lack channels. They lack one trusted decision loop across channels.", [
        ("Fragmented customer experience", ["Online browsing, mobile cart, store try-on, POS purchase and after-sales service are often split across systems.", "Personalization becomes unreliable if it does not understand inventory, price, consent and fulfillment."], "red"),
        ("The answer is not a single model", ["The enterprise needs a business object that can be approved, executed, audited and improved.", "That is why the system is centered on Retail Decision Case, not on a chat window."], "green"),
    ]),
    ("prompt", "2. Prompt Coverage", "This slide proves the design stays aligned with the original assignment.", [
        ("Customer Data", "Customer 360 combines loyalty, app, POS, store, marketplace and service signals.", "green"),
        ("Omni-channel", "App, WeChat mini-program, email, marketplaces, store POS and pickup share context.", "blue"),
        ("Five Agents", "Customer, Personalization, Inventory, Pricing and Marketing Agents collaborate on the same Case.", "amber"),
        ("Advantages", "Higher conversion, fewer stockouts and markdown losses, fewer irrelevant touches, faster regional response.", "purple"),
        ("Success Criteria", "Same-store sales, waste, satisfaction, LTV, approval cycle time and execution success rate.", "red"),
        ("Asia Challenges", "Consent, language, payment ecosystems, platform channels and urban/rural fulfillment gaps.", "green"),
    ]),
    ("process", "3. Operating Loop", "Every page and component serves this five-step loop.", [
        ("Discover", "Seasonal sandbox and market signals detect risk without writing production actions.", "green"),
        ("Verify", "Data and signals confirm fact confidence, such as inventory reliability and demand source.", "blue"),
        ("Decide", "Five Agents produce options, alternatives and risk explanations.", "amber"),
        ("Execute", "Only approved actions enter replenishment, transfer, campaign or pricing systems.", "purple"),
        ("Learn", "Execution receipts and results feed the next prediction and rule calibration cycle.", "red"),
    ]),
    ("sku", "4. Why SKU Combinations Exist", "SKU combination is the smallest operating unit for a real retail decision.", [
        ("Business meaning", ["The same product can carry different risk by size, color, store and lifecycle stage.", "Black M/L stockout can hurt conversion, while white XS slow movement may be normal demand shape."], "green"),
        ("Decision role", ["It binds demand forecast, available supply, margin, transfer cost and fulfillment limits.", "It prevents AI from giving a recommendation that looks good in aggregate but cannot be executed locally."], "blue"),
    ]),
    ("signals", "5. Why Data and Signals Exist", "They answer whether a Case is fact, inference or scenario simulation.", [
        ("Fact signals", ["POS sales, store inventory, RFID/counting, member behavior, order fulfillment, returns and complaints.", "They define current business state and executable boundaries."], "green"),
        ("External and predictive signals", ["Weather, holidays, campaigns, platform traffic, search heat and competitor prices.", "They create risk alerts and forecasts, but must be labeled as simulation."], "amber"),
    ]),
    ("rules", "6. Why Business Rules Exist", "Rules turn autonomous Agents into a governable enterprise system.", [
        ("Guardrails", ["No contact without consent. No recommendation on low-confidence inventory. Discounts below margin floor are blocked.", "High-impact actions enter human approval and do not directly write ERP, WMS, OMS or CRM."], "red"),
        ("Role boundaries", ["Store manager confirms store facts. Regional manager approves replenishment and transfers. Executives approve major price, promotion and budget moves.", "AI recommends, explains, drafts and monitors without taking organizational accountability away from people."], "purple"),
    ]),
    ("sandbox", "7. Why the Four-Season Sandbox Exists", "It is planning stress-test, not another production system.", [
        ("Why it is needed", ["Retail is seasonal. Heatwaves, cold snaps, Spring Festival and Golden Week change demand and fulfillment pressure.", "The sandbox identifies which SKUs, stores and channels may face stockout or markdown risk."], "blue"),
        ("How it joins the storyline", ["The sandbox only produces read-only risk signals. A Retail Decision Case can be created only after data verification.", "This keeps strategic context without pretending simulated output is real sales fact."], "green"),
    ]),
    ("agents", "8. How the Five Agents Collaborate", "They share one Case state instead of talking separately.", [
        ("Customer", "Understands identity, intent, consent, preference, lifecycle and service risk.", "green"),
        ("Personalization", "Creates fulfillable product display, content, recommendations and next best actions.", "blue"),
        ("Inventory", "Forecasts SKU/store/channel demand, checks ATP confidence and proposes replenishment or transfer.", "amber"),
        ("Pricing", "Combines demand, competition, inventory and margin guardrails to recommend or block prices.", "purple"),
        ("Marketing", "Selects consented high-intent audiences and drafts campaigns, budget and channel plans.", "red"),
        ("Orchestration", "Keeps Case state, evidence, alternatives, approval and audit in one flow.", "green"),
    ]),
    ("decision", "9. What AI Decision Intelligence Shows", "Business users see decisions, not internal orchestration manuals.", [
        ("Forecasts and options", ["7-day demand interval forecast; 0/10/15/20/30% discount sensitivity; no action, transfer, transfer plus member coupon, and full-channel markdown options.", "Channel view shows store sellable stock, cross-store transfer, DC replenishment and sales limitations."], "blue"),
        ("Auditable evidence", ["Five-Agent trace, policy guardrails and post-execution learning are kept in expandable audit detail.", "Completed Cases still keep AI result entry, proving the system can review and learn."], "green"),
    ]),
    ("roles", "10. Roles and Permission Boundaries", "Business realism comes from clear accountability.", [
        ("Store Manager", "Confirms stock count, receiving, display and store facts; no approval for price changes or cross-store transfers.", "green"),
        ("Regional Manager", "Reviews regional exceptions and store impact, approves replenishment and transfer, tracks execution.", "blue"),
        ("Executive", "Approves major promotions, price exceptions, budgets and cross-market allocation.", "amber"),
        ("AI System", "Recommends, explains, drafts, alerts and learns; all production actions require authorized approval.", "purple"),
    ], 2),
    ("demo", "11. Live Demo Path", "The demo follows the storyline, not the menu.", [
        ("Step 1", "Home: explain prompt coverage, five Agents, Retail Decision Case and Azure-ready architecture.", "green"),
        ("Step 2", "Regional manager: open the approval Case and explain SKU, signals, risk and recommendation.", "blue"),
        ("Step 3", "AI decision support: show forecast, option comparison, guardrails and executable boundaries.", "amber"),
        ("Step 4", "Audit and learning: show completed Case still keeps AI result and continuous monitoring entry.", "purple"),
    ], 2),
    ("azure_list", "12. Azure Service List", "The demo can naturally evolve into enterprise-grade production.", [
        ("AI and Orchestration", "Azure OpenAI / Azure AI Foundry for reasoning, agent orchestration, evaluation and safety testing.", "green"),
        ("Runtime", "Azure Container Apps for FastAPI Agent Runtime, autoscaling, revisions and traffic shifting.", "blue"),
        ("Data Layer", "Azure Cosmos DB for Customer 360, Retail Decision Case, Agent state and audit logs.", "amber"),
        ("Retrieval", "Azure AI Search for products, policies, FAQ, historical cases and knowledge retrieval.", "purple"),
        ("Integration and Async", "API Management, Service Bus / Event Grid for enterprise API gateway and async Agent tasks.", "red"),
        ("Security and Ops", "Managed Identity, Key Vault, App Configuration, Application Insights, Log Analytics, Fabric / Power BI.", "green"),
    ]),
    ("architecture", "13. Azure Architecture", "The key is layered separation of experience, runtime, AI, data and governance."),
    ("metrics", "14. Success Metrics", "Measure business loop performance, not just model output.", [
        ("Growth", "Same-store sales, conversion, basket size, repeat purchase and member LTV.", "green"),
        ("Inventory", "Stockout rate, slow-moving stock, waste, transfer success rate and fulfillment lead time.", "blue"),
        ("Customer", "Satisfaction, contact complaint rate, channel consistency and personalization acceptance.", "amber"),
        ("Governance", "Approval cycle time, guardrail hit rate, execution success, audit completeness and rollback ability.", "purple"),
    ], 2),
    ("close",),
]


ARCH_ZH = [
    ("体验层", "浏览器 / 区域经理工作台 / 现场演示入口 / Power BI 管理看板", "green"),
    ("入口与 API", "Azure Container Apps Ingress + API Management / MCP Gateway", "blue"),
    ("Agent Runtime", "FastAPI on Azure Container Apps · Retail Case API · Decision Intelligence API", "amber"),
    ("AI 编排", "Azure OpenAI + Azure AI Foundry · 五 Agent 协作、评估和安全护栏", "purple"),
    ("数据与知识", "Cosmos DB · Azure AI Search · Storage / Fabric · Customer 360、Case、审计、商品和政策知识", "red"),
    ("安全与运维", "Managed Identity · Key Vault · App Configuration · Application Insights · Log Analytics", "green"),
]

ARCH_EN = [
    ("Experience", "Browser / Regional manager workspace / Live demo entry / Power BI executive dashboard", "green"),
    ("Ingress and API", "Azure Container Apps Ingress + API Management / MCP Gateway", "blue"),
    ("Agent Runtime", "FastAPI on Azure Container Apps · Retail Case API · Decision Intelligence API", "amber"),
    ("AI Orchestration", "Azure OpenAI + Azure AI Foundry · five-Agent collaboration, evaluation and safety guardrails", "purple"),
    ("Data and Knowledge", "Cosmos DB · Azure AI Search · Storage / Fabric · Customer 360, Cases, audit, product and policy knowledge", "red"),
    ("Security and Ops", "Managed Identity · Key Vault · App Configuration · Application Insights · Log Analytics", "green"),
]


SCRIPT_ZH = [
    "我今天用一条更清楚的故事线讲 Project 46：五个 Agent 不是五个聊天机器人，而是一套能跑通发现、核验、决策、执行和复盘的零售经营系统。",
    "这页先告诉评委我会怎么讲。前面回答题目要求，中间解释页面组件为什么存在，后面讲系统演示和 Azure 企业级落地。",
    "核心问题是零售企业有很多渠道，但没有一个跨渠道可信决策闭环。个性化如果脱离库存、价格、授权和履约，就会变成不可靠建议。",
    "这页证明没有偏题。客户数据整合、全渠道个性化、五个 Agent、优势、成功标准和亚洲挑战，都在系统里有对应设计。",
    "完整闭环是发现、核验、决策、执行和复盘。四季沙盘发现风险，数据与信号核验事实，Agent 形成方案，授权角色审批执行，结果再进入学习。",
    "SKU 组合是零售决策的最小粒度。同一商品在不同尺码、颜色、门店和生命周期阶段风险不同，所以 AI 必须围绕具体组合做判断。",
    "数据与信号区回答可信度问题：哪些是已发生事实，哪些是外部信号，哪些只是情景模拟。这样可以避免把预测当成真实销售。",
    "业务规则是企业护栏。未授权客户不能触达，低可信库存不能推荐，低于毛利底线的折扣要阻断，高风险动作必须进入审批。",
    "四季沙盘是规划压力测试，不是生产执行系统。它发现季节性风险，经过数据核验后，才可能生成 Retail Decision Case。",
    "五个 Agent 围绕同一个 Case 协作。客户 Agent 讲人，个性化 Agent 讲体验，库存 Agent 讲履约，定价 Agent 讲毛利和价格，营销 Agent 讲触达。",
    "AI 决策智能展示的是业务决策：需求预测、折扣敏感度、供货限制、方案比较和政策护栏。内部轨迹放在审计详情，而不是打扰业务用户。",
    "角色边界让系统真实。店长确认门店事实，区域经理审批调拨和补货，高层审批重大促销和预算，AI 只推荐、解释、草拟和监控。",
    "现场演示按故事线走：先首页讲题目覆盖，再进区域经理审批 Case，再看 AI 决策助手，最后看审计和复盘入口。",
    "这页是 Azure 服务清单。运行时在 Azure Container Apps，AI 用 Azure OpenAI 和 AI Foundry，数据用 Cosmos DB，知识检索用 AI Search，安全和运维用 Key Vault、Managed Identity、Application Insights 和 Log Analytics。",
    "这页是架构图。上层是体验和 API，中间是 Agent Runtime 和 AI 编排，下层是数据、知识、安全和可观测性。这说明 demo 可以自然演进到企业生产架构。",
    "成功指标不只看模型回答，而看经营闭环：销售增长、库存浪费下降、客户满意度、审批效率、执行成功率和审计完整性。",
    "最后我的结论是：这不是 AI 给建议，而是 AI 进入经营系统。Project 46 的价值是把个性化、库存、价格和营销统一成一个可控的决策闭环。",
]

SCRIPT_EN = [
    "Today I will present Project 46 with a clearer storyline. The five Agents are not five chatbots. They form an operating system for discover, verify, decide, execute and learn.",
    "This slide shows the flow. I first answer the assignment prompt, then explain why each product component exists, and finally show the demo and Azure implementation.",
    "The core problem is that retailers have many channels, but not one trusted cross-channel decision loop. Personalization becomes unreliable if it ignores inventory, pricing, consent and fulfillment.",
    "This slide proves the project stays on prompt. Customer data integration, omni-channel personalization, five Agents, advantages, success criteria and Asia challenges are all covered.",
    "The full loop is discover, verify, decide, execute and learn. The seasonal sandbox detects risk, data and signals verify facts, Agents generate options, authorized roles approve execution, and results feed learning.",
    "SKU combination is the smallest unit for retail decisions. The same product has different risk by size, color, store and lifecycle, so AI must reason at the exact combination level.",
    "The data and signals section answers confidence. Which inputs are facts, which are external signals, and which are scenario simulations. This prevents forecasts from being presented as real sales.",
    "Business rules are enterprise guardrails. No contact without consent, no recommendation on low-confidence inventory, discounts below margin floor are blocked, and high-risk actions require approval.",
    "The four-season sandbox is a planning stress-test, not a production execution system. It detects seasonal risk, and only after verification can a Retail Decision Case be created.",
    "The five Agents collaborate around the same Case. Customer understands the person, Personalization designs the experience, Inventory checks fulfillment, Pricing protects margin, and Marketing plans activation.",
    "AI Decision Intelligence shows business decisions: demand forecast, discount sensitivity, supply limits, option comparison and policy guardrails. Internal traces stay in audit details instead of distracting users.",
    "Role boundaries create business realism. Store managers confirm store facts, regional managers approve transfer and replenishment, executives approve major promotion and budget, and AI recommends, explains, drafts and monitors.",
    "The live demo follows the storyline: home page for prompt coverage, regional manager approval Case, AI decision support, and finally audit and learning entry.",
    "This is the Azure service list. Runtime uses Azure Container Apps, AI uses Azure OpenAI and AI Foundry, data uses Cosmos DB, retrieval uses AI Search, and security and operations use Key Vault, Managed Identity, Application Insights and Log Analytics.",
    "This is the architecture diagram. Experience and API are on top, Agent Runtime and AI orchestration are in the middle, and data, knowledge, security and observability are at the bottom. The demo can evolve into production architecture.",
    "Success metrics measure the operating loop, not only model answers: sales uplift, lower waste, satisfaction, approval efficiency, execution success and audit completeness.",
    "My closing message is: not AI advice, but AI inside the retail operating system. Project 46 unifies personalization, inventory, pricing and marketing into one governed decision loop.",
]


def build_deck(lang):
    prs = new_prs()
    data = ZH if lang == "zh" else EN
    arch = ARCH_ZH if lang == "zh" else ARCH_EN
    cover(prs, lang, 1)
    slide_no = 2
    for entry in data:
        kind = entry[0]
        if kind in {"agenda", "prompt", "agents", "azure_list", "metrics", "roles", "demo"}:
            title, subtitle, items = entry[1], entry[2], entry[3]
            cols = entry[4] if len(entry) > 4 else 3
            grid_slide(prs, lang, slide_no, title, subtitle, items, cols=cols)
        elif kind in {"statement", "sku", "signals", "rules", "sandbox", "decision"}:
            _, title, subtitle, pair = entry
            left, right = pair
            two_col_slide(prs, lang, slide_no, title, subtitle, left, right)
        elif kind == "process":
            _, title, subtitle, steps = entry
            process_slide(prs, lang, slide_no, title, subtitle, steps)
        elif kind == "architecture":
            _, title, subtitle = entry
            architecture_slide(prs, lang, slide_no, title, subtitle, arch)
        elif kind == "close":
            closing_slide(prs, lang, slide_no)
        slide_no += 1
    return prs


def write_script():
    lines = [
        "# AMA 项目46逐页口述脚本 / Project 46 Speaker Script",
        "",
        "用途：配合新版中文和英文 PPT。中文可直接用于答辩；英文保持简单口语，方便现场切换。",
        "",
    ]
    titles_zh = ["封面"] + [e[1] if len(e) > 1 else "收尾" for e in ZH]
    titles_en = ["Cover"] + [e[1] if len(e) > 1 else "Closing" for e in EN]
    for i, (tz, te, sz, se) in enumerate(zip(titles_zh, titles_en, SCRIPT_ZH, SCRIPT_EN), start=1):
        lines.extend([
            f"## Slide {i}: {tz} / {te}",
            "",
            "中文：",
            sz,
            "",
            "English:",
            se,
            "",
        ])
    SCRIPT.write_text("\n".join(lines), encoding="utf-8")


def main():
    zh = build_deck("zh")
    en = build_deck("en")
    zh.save(OUT_ZH)
    en.save(OUT_EN)
    write_script()

    STATIC.mkdir(parents=True, exist_ok=True)
    (STATIC / OUT_ZH.name).write_bytes(OUT_ZH.read_bytes())
    (STATIC / OUT_EN.name).write_bytes(OUT_EN.read_bytes())
    (STATIC / SCRIPT.name).write_bytes(SCRIPT.read_bytes())


if __name__ == "__main__":
    main()
