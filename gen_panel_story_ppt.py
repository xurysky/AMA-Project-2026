#!/usr/bin/env python3
"""Generate a panel-ready AMA story deck aligned with the redesigned demo UI."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.util import Inches, Pt


OUT = "AMA-二次过堂-故事线演示版.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

W = prs.slide_width
H = prs.slide_height

INK = RGBColor(32, 35, 33)
MUTED = RGBColor(97, 105, 101)
BG = RGBColor(245, 245, 242)
SURFACE = RGBColor(255, 255, 255)
LINE = RGBColor(217, 220, 215)
FOCUS = RGBColor(35, 137, 116)
FOCUS_DARK = RGBColor(24, 68, 61)
FOCUS_SOFT = RGBColor(232, 246, 241)
RED = RGBColor(215, 38, 56)
AMBER = RGBColor(154, 90, 0)
BLUE = RGBColor(36, 95, 143)


def set_bg(slide, color=BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def rect(slide, x, y, w, h, fill, line=None, radius=False):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    else:
        s.line.fill.background()
    return s


def text(slide, x, y, w, h, value, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    p = tf.paragraphs[0]
    p.text = value
    p.font.name = "Microsoft YaHei"
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return box


def title(slide, value, sub=None):
    text(slide, 0.55, 0.35, 9.6, 0.48, value, 23, INK, True)
    if sub:
        text(slide, 0.58, 0.88, 11.3, 0.35, sub, 11, MUTED)
    rect(slide, 0.55, 1.28, 12.2, 0.02, LINE)


def pill(slide, x, y, value, color=FOCUS, w=1.65):
    rect(slide, x, y, w, 0.33, RGBColor(255, 255, 255), color, True)
    text(slide, x + 0.08, y + 0.07, w - 0.16, 0.18, value, 8.5, color, True, PP_ALIGN.CENTER)


def card(slide, x, y, w, h, heading, body, accent=FOCUS):
    rect(slide, x, y, w, h, SURFACE, LINE, True)
    rect(slide, x, y, 0.07, h, accent)
    text(slide, x + 0.22, y + 0.2, w - 0.38, 0.35, heading, 14, INK, True)
    text(slide, x + 0.22, y + 0.65, w - 0.38, h - 0.82, body, 10.5, MUTED)


def bullets(slide, x, y, w, items, size=14, color=INK):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.name = "Microsoft YaHei"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(7)
    return box


def footer(slide, n):
    text(slide, 0.55, 7.08, 4, 0.22, "AMA Project 46 · Retail Decision Case Platform", 8.5, MUTED)
    text(slide, 12.25, 7.08, 0.6, 0.22, str(n), 8.5, MUTED, align=PP_ALIGN.RIGHT)


def add_cover():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, FOCUS_DARK)
    rect(s, 0, 0, 13.333, 0.08, RED)
    text(s, 0.85, 0.72, 2.3, 0.33, "AMA 二次过堂", 12, RGBColor(189, 231, 219), True)
    text(s, 0.85, 1.45, 10.9, 1.45, "Autonomous Retail Intelligence\nAgent Platform", 42, SURFACE, True)
    text(s, 0.9, 3.16, 10.8, 0.65, "从会演示的 Agent，升级为可审计、可审批、可执行的零售经营决策系统", 19, RGBColor(218, 237, 231))
    rect(s, 0.9, 4.2, 11.6, 1.35, RGBColor(255, 255, 255), None, True)
    text(s, 1.2, 4.48, 10.8, 0.58, "一句话主线：AI 不直接经营门店，而是把复杂经营信号收敛成一个 Retail Decision Case。", 20, FOCUS_DARK, True, PP_ALIGN.CENTER)
    text(s, 0.9, 6.35, 4.5, 0.3, "王缘 · Project 46 · AMA Capstone", 12, RGBColor(218, 237, 231))
    footer(s, 1)


def add_storyline():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    title(s, "1. 明天过堂的故事线", "先讲业务闭环，再讲 Agent 和 Azure；不要从技术菜单开始。")
    steps = [
        ("发现异常", "天气、POS、RFID、OMS、门店容量触发经营异常"),
        ("核验事实", "ATP、库存可信度、毛利、授权、政策版本进入同一快照"),
        ("Agent 协同", "Inventory、Pricing、Customer、Personalization、Marketing 按需参与"),
        ("人工决策", "店长、区域经理、跨国经营管理层审批 Decision Packet"),
        ("受控执行", "审批后写 ERP/WMS/CRM/门店任务，产生回执和审计"),
    ]
    for i, (h, b) in enumerate(steps):
        x = 0.55 + i * 2.55
        rect(s, x, 1.7, 2.25, 4.15, SURFACE, LINE, True)
        rect(s, x + 0.18, 1.95, 0.42, 0.42, FOCUS_SOFT, FOCUS, True)
        text(s, x + 0.29, 2.05, 0.2, 0.12, str(i + 1), 9, FOCUS_DARK, True, PP_ALIGN.CENTER)
        text(s, x + 0.22, 2.6, 1.85, 0.32, h, 15, INK, True)
        text(s, x + 0.22, 3.1, 1.8, 1.35, b, 10.5, MUTED)
        pill(s, x + 0.22, 5.15, "Demo Step", FOCUS, 1.15)
    footer(s, 2)


def add_problem():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    title(s, "2. 问题不是“有没有 Agent”，而是经营决策被割裂", "零售决策天然跨域：库存、价格、会员、营销、门店执行互相制约。")
    card(s, 0.8, 1.65, 3.8, 1.45, "原始痛点", "库存数据、营销动作、价格策略和门店执行分散在不同系统，异常出现后无法形成一个统一决策对象。", RED)
    card(s, 4.85, 1.65, 3.8, 1.45, "Agent 常见误区", "只展示 Agent 文本输出，容易被追问：事实从哪里来？谁批准？执行失败怎么办？怎么审计？", AMBER)
    card(s, 8.9, 1.65, 3.6, 1.45, "我的重新定位", "把系统设计成 Retail Decision Case Platform：每个异常都有证据、建议、审批、执行、回执和复盘。", FOCUS)
    bullets(s, 1.1, 3.65, 11.2, [
        "演示对象从“Agent 控制台”改为“经营决策驾驶舱”。",
        "评委先看到业务闭环，再按需要深入 Agent、数据源、Azure 架构与审计。",
        "销售增长、ROI、LTV 是假设或未来试点指标；原型可证明的是流程、治理和系统形态。",
    ], 16)
    footer(s, 3)


def add_solution():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    title(s, "3. 解决方案：Retail Decision Case 是系统的中心对象", "所有 Agent 和人类角色围绕同一个 Case 工作，而不是各自生成孤立建议。")
    rect(s, 4.35, 2.2, 4.6, 1.2, FOCUS_DARK, None, True)
    text(s, 4.6, 2.55, 4.1, 0.3, "Retail Decision Case", 21, SURFACE, True, PP_ALIGN.CENTER)
    left = [("Operational Signals", "POS / RFID / OMS / ERP / Weather"), ("Planning Policy", "Lifecycle / margin / store cluster"), ("Customer Context", "Consent / segment / channel")]
    right = [("Decision Packet", "Recommendation / rationale / alternatives"), ("Work Orders", "ERP / WMS / CRM / Store task"), ("Audit & Learning", "Receipts / retry / KPI review")]
    for i, (h, b) in enumerate(left):
        card(s, 0.8, 1.55 + i * 1.35, 3.0, 0.95, h, b, BLUE)
    for i, (h, b) in enumerate(right):
        card(s, 9.5, 1.55 + i * 1.35, 3.0, 0.95, h, b, FOCUS)
    text(s, 4.35, 4.12, 4.7, 0.95, "核心原则：LLM 解释证据和建议，但 ATP、毛利、授权、审批状态、幂等键由确定性服务控制。", 15, INK, True, PP_ALIGN.CENTER)
    footer(s, 4)


def add_demo_flow():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    title(s, "4. 现场演示流程：6 分钟一条线讲完", "每一步都有一句话价值点和可点击证据。")
    rows = [
        ("00:00-01:00", "首页故事模式", "讲清主线：AI 把异常收敛成 Case，不直接写生产系统。"),
        ("01:00-02:30", "打开当前 Case", "展示业务建议、库存 ATP、证据快照、下一步人工任务。"),
        ("02:30-03:45", "AI 决策助手", "展示七天需求、选项比较、毛利/渠道/库存护栏。"),
        ("03:45-05:00", "审批与执行", "证明人类审批后才生成可执行工单，并且执行有回执。"),
        ("05:00-06:00", "Agent / Audit 深潜", "回应架构追问：五 Agent、共享控制面、Azure 部署和审计留痕。"),
    ]
    for i, row in enumerate(rows):
        y = 1.55 + i * 0.9
        rect(s, 0.75, y, 11.85, 0.72, SURFACE, LINE, True)
        pill(s, 0.95, y + 0.2, row[0], FOCUS if i < 4 else BLUE, 1.55)
        text(s, 2.75, y + 0.18, 2.0, 0.2, row[1], 13, INK, True)
        text(s, 5.0, y + 0.16, 7.1, 0.25, row[2], 12, MUTED)
    footer(s, 5)


def add_ui():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    title(s, "5. 界面重设计：评委先看故事，再看系统", "首页新增 Panel Story Mode，避免从菜单解释开始。")
    card(s, 0.75, 1.6, 3.8, 1.55, "第一屏", "一句话定位 + 6 分钟演示按钮 + 2 分钟流程 walkthrough。", FOCUS)
    card(s, 4.75, 1.6, 3.8, 1.55, "证据面板", "Case 数、人工介入数、Policy 阻断、执行回执、Agent 能力域。", BLUE)
    card(s, 8.75, 1.6, 3.8, 1.55, "五步地图", "发现、核验、决策、执行、复盘，当前 Case 自动高亮。", AMBER)
    card(s, 0.75, 3.65, 5.8, 1.65, "点击路径", "首页 → 当前 Case → AI 决策助手 → 审批/执行 → 审计/Azure 深潜。PPT 和系统完全同一条线。", FOCUS)
    card(s, 6.75, 3.65, 5.8, 1.65, "回答追问", "评委问事实、治理、落地、扩展时，从顶部按钮直接进入 Data、Agent、Audit、Scenario。", RED)
    footer(s, 6)


def add_architecture():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    title(s, "6. 架构口径：Azure-native，不是 VM Demo", "VM 可以临时承载演示，但目标架构是容器化和托管服务。")
    layers = [
        ("Experience", "Browser / store task / regional approval / executive cockpit"),
        ("Runtime", "Azure Container Apps · FastAPI Agent Runtime"),
        ("Agent & AI", "Azure OpenAI / AI Foundry · five Agent domains · policy control"),
        ("State", "Cosmos DB · run state · cases · work orders · audit log"),
        ("Integration", "API Management · Managed Identity · Key Vault · Logic Apps"),
        ("Observability", "Application Insights · Log Analytics · health checks"),
    ]
    for i, (h, b) in enumerate(layers):
        y = 1.45 + i * 0.78
        rect(s, 1.1, y, 11.1, 0.58, SURFACE, LINE, True)
        text(s, 1.35, y + 0.14, 2.1, 0.16, h, 12, FOCUS_DARK, True)
        text(s, 3.65, y + 0.13, 7.9, 0.18, b, 12, INK)
    footer(s, 7)


def add_governance():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    title(s, "7. 治理设计：让 Agent 能进入企业，而不是只做 Demo", "核心是人类审批、策略阻断、数据边界和执行回执。")
    card(s, 0.8, 1.6, 2.8, 2.0, "Human-in-the-loop", "价格、促销、调拨、客户触达等高风险动作必须由角色审批。", FOCUS)
    card(s, 3.9, 1.6, 2.8, 2.0, "Policy Guardrails", "毛利底线、客户授权、库存可信度、审批角色和 packet expiry 可阻断动作。", RED)
    card(s, 7.0, 1.6, 2.8, 2.0, "Deterministic Truth", "ATP、库存可信度、毛利计算不交给 LLM 猜测。", BLUE)
    card(s, 10.1, 1.6, 2.45, 2.0, "Auditability", "每个建议、审批、执行和失败补偿都有事件记录。", AMBER)
    bullets(s, 1.0, 4.25, 11.2, [
        "对评委主动澄清：原型不声称已经实现销售增长，只证明可治理的经营决策闭环。",
        "生产化路径：Managed Identity、Key Vault、APIM、RBAC、Application Insights、真实数据接入、test/control 门店试点。",
    ], 15)
    footer(s, 8)


def add_panel_qna():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    title(s, "8. 高概率追问与回答口径", "每个回答都落到设计选择、取舍、证据和下一步。")
    qa = [
        ("为什么不是纯自动化？", "零售价格、库存和客户触达有商业风险，所以我选择可审批的 Agentic workflow，而不是让 LLM 直接写生产系统。"),
        ("Agent 价值在哪里？", "五个 Agent 对应五个业务能力域；价值不是文本，而是把跨域信号变成一个可执行的决策包。"),
        ("怎么证明不是模拟？", "业务增量是试点假设；但部署、Case 状态、审批、工单、审计和 API 是可运行证据。"),
        ("怎么上生产？", "用 Container Apps 承载 runtime，Cosmos DB 存状态，APIM/MI/Key Vault 管集成与安全，App Insights 做运营观测。"),
    ]
    for i, (q, a) in enumerate(qa):
        card(s, 0.85, 1.5 + i * 1.15, 11.6, 0.88, q, a, [FOCUS, BLUE, AMBER, RED][i])
    footer(s, 9)


def add_close():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, FOCUS_DARK)
    text(s, 0.9, 1.35, 11.3, 0.95, "Closing Message", 20, RGBColor(189, 231, 219), True, PP_ALIGN.CENTER)
    text(s, 1.25, 2.35, 10.8, 1.1, "这不是一个零售 Agent 玩具，而是一条企业可接受的 Agentic Decision Operating Model。", 32, SURFACE, True, PP_ALIGN.CENTER)
    text(s, 1.45, 4.15, 10.4, 0.8, "我的项目证明的是：复杂经营异常可以被结构化、被协同判断、被人工治理、被受控执行、被审计复盘。", 18, RGBColor(218, 237, 231), align=PP_ALIGN.CENTER)
    footer(s, 10)


for fn in [
    add_cover,
    add_storyline,
    add_problem,
    add_solution,
    add_demo_flow,
    add_ui,
    add_architecture,
    add_governance,
    add_panel_qna,
    add_close,
]:
    fn()

prs.save(OUT)
print(OUT)
