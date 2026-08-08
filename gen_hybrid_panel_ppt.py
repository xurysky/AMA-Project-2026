#!/usr/bin/env python3
"""Generate the AMA second-review formal presentation deck.

This version is designed for a 45-minute panel session:
35-40 minutes of prepared presentation + live demo, with Q&A kept outside
the main deck and covered by the separate speaker script.
"""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.util import Inches, Pt


OUT = "AMA-二次过堂-故事线演示版.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

INK = RGBColor(31, 35, 33)
MUTED = RGBColor(91, 99, 95)
BG = RGBColor(246, 246, 243)
SURFACE = RGBColor(255, 255, 255)
LINE = RGBColor(216, 220, 215)
GREEN = RGBColor(35, 137, 116)
DARK = RGBColor(22, 68, 61)
SOFT = RGBColor(229, 246, 241)
RED = RGBColor(211, 47, 47)
AMBER = RGBColor(160, 94, 12)
BLUE = RGBColor(34, 96, 146)
PURPLE = RGBColor(104, 74, 142)


def set_bg(slide, color=BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def shape(slide, x, y, w, h, fill=SURFACE, line=LINE, rounded=True):
    s = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    else:
        s.line.fill.background()
    return s


def text(slide, x, y, w, h, value, size=15, color=INK, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.word_wrap = True
    frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    p = frame.paragraphs[0]
    p.text = value
    p.font.name = "Microsoft YaHei"
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return box


def header(slide, title, subtitle=None):
    text(slide, 0.58, 0.35, 11.7, 0.42, title, 22, INK, True)
    if subtitle:
        text(slide, 0.6, 0.86, 11.4, 0.26, subtitle, 10.5, MUTED)
    shape(slide, 0.58, 1.22, 12.15, 0.018, LINE, None, False)


def footer(slide, n):
    text(slide, 0.58, 7.08, 6.8, 0.2, "AMA Project 46 · Autonomous Retail Intelligence Agent Platform", 8.5, MUTED)
    text(slide, 12.2, 7.08, 0.55, 0.2, str(n), 8.5, MUTED, align=PP_ALIGN.RIGHT)


def card(slide, x, y, w, h, head, body, accent=GREEN):
    shape(slide, x, y, w, h, SURFACE, LINE)
    shape(slide, x, y, 0.07, h, accent, None, False)
    text(slide, x + 0.18, y + 0.16, w - 0.32, 0.28, head, 13.2, INK, True)
    text(slide, x + 0.18, y + 0.55, w - 0.32, h - 0.65, body, 10.3, MUTED)


def tag(slide, x, y, value, color=GREEN, w=1.35):
    shape(slide, x, y, w, 0.31, SURFACE, color)
    text(slide, x + 0.05, y + 0.07, w - 0.1, 0.16, value, 8.5, color, True, PP_ALIGN.CENTER)


def bullets(slide, x, y, w, items, size=13.5, color=INK):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(5.4))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.name = "Microsoft YaHei"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(6)


def cover(n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, DARK)
    shape(s, 0, 0, 13.333, 0.08, RED, None, False)
    text(s, 0.82, 0.72, 5.0, 0.3, "AMA Project 46 · Second Review", 12, RGBColor(190, 232, 220), True)
    text(s, 0.82, 1.35, 11.4, 1.36, "Autonomous Retail Intelligence\nAgent Platform", 40, SURFACE, True)
    text(s, 0.86, 3.06, 11.2, 0.44, "Customer data integration · Omni-channel personalization · Five Agents · Auditable execution", 17.5, RGBColor(220, 239, 233))
    shape(s, 0.9, 4.0, 11.55, 1.55, SURFACE, None)
    text(s, 1.18, 4.24, 11.0, 0.82, "融合主线：先回答题目要求，再证明这些 Agent 能进入企业级审批、执行和审计闭环。", 20, DARK, True, PP_ALIGN.CENTER)
    text(s, 0.9, 6.34, 4.6, 0.25, "王缘 · AMA Capstone", 12, RGBColor(220, 239, 233))
    footer(s, n)


def agenda(n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    header(s, "Today’s Storyline", "35-40 minutes prepared presentation, plus around 10 minutes discussion.")
    items = [
        ("1", "Problem & Prompt Fit", "Why the project matches Autonomous Retail Intelligence Agent Platform."),
        ("2", "Business Scenario", "A concrete Asia retail scenario across online, mobile and store touchpoints."),
        ("3", "Five-Agent System", "How customer, personalization, inventory, pricing and marketing Agents collaborate."),
        ("4", "Decision Operating Model", "How Agent output becomes approved, executable and auditable work."),
        ("5", "Architecture & Measurement", "Azure implementation, governance, and success metric design."),
    ]
    for i, (num, head, body) in enumerate(items):
        y = 1.52 + i * 0.95
        shape(s, 0.85, y, 0.55, 0.55, [GREEN, BLUE, AMBER, PURPLE, RED][i], None)
        text(s, 1.02, y + 0.14, 0.2, 0.14, num, 10, SURFACE, True, PP_ALIGN.CENTER)
        text(s, 1.7, y + 0.07, 3.6, 0.22, head, 14, INK, True)
        text(s, 5.15, y + 0.07, 6.7, 0.26, body, 12, MUTED)
    footer(s, n)


def two_col(n, title_text, subtitle, left_head, left_items, right_head, right_items, left_color=GREEN, right_color=BLUE):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    header(s, title_text, subtitle)
    card(s, 0.75, 1.55, 5.85, 4.95, left_head, "\n".join(left_items), left_color)
    card(s, 6.95, 1.55, 5.65, 4.95, right_head, "\n".join(right_items), right_color)
    footer(s, n)


def grid(n, title_text, subtitle, items, cols=3):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    header(s, title_text, subtitle)
    rows = (len(items) + cols - 1) // cols
    w = 11.75 / cols
    h = 4.75 / rows
    for i, item in enumerate(items):
        x = 0.78 + (i % cols) * (w + 0.12)
        y = 1.55 + (i // cols) * (h + 0.18)
        head, body, color = item
        card(s, x, y, w - 0.12, h, head, body, color)
    footer(s, n)


def process(n, title_text, subtitle, steps):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    header(s, title_text, subtitle)
    for i, (head, body, color) in enumerate(steps):
        x = 0.72 + i * 2.5
        shape(s, x, 1.8, 2.15, 3.55, SURFACE, LINE)
        shape(s, x + 0.72, 1.45, 0.68, 0.68, color, None)
        text(s, x + 0.93, 1.64, 0.22, 0.16, str(i + 1), 10, SURFACE, True, PP_ALIGN.CENTER)
        text(s, x + 0.2, 2.23, 1.75, 0.38, head, 13.2, INK, True, PP_ALIGN.CENTER)
        text(s, x + 0.2, 2.92, 1.75, 1.48, body, 10.2, MUTED, align=PP_ALIGN.CENTER)
    footer(s, n)


def statement(n, title_text, subtitle, main, details, color=DARK):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s)
    header(s, title_text, subtitle)
    shape(s, 0.95, 1.82, 11.45, 1.75, color, None)
    text(s, 1.35, 2.22, 10.65, 0.65, main, 24, SURFACE, True, PP_ALIGN.CENTER)
    bullets(s, 1.2, 4.25, 10.9, details, 15)
    footer(s, n)


def close(n):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, DARK)
    text(s, 0.95, 1.15, 11.5, 0.45, "Closing Message", 18, RGBColor(190, 232, 220), True, PP_ALIGN.CENTER)
    text(s, 1.25, 2.05, 10.9, 1.15, "It is not just five Agents.\nIt is a governable retail decision operating model.", 31, SURFACE, True, PP_ALIGN.CENTER)
    text(s, 1.55, 4.15, 10.3, 0.82, "系统既回答客户数据整合、全渠道个性化和五 Agent，也证明这些能力可以进入企业级审批、执行、审计和持续优化。", 18, RGBColor(220, 239, 233), align=PP_ALIGN.CENTER)
    footer(s, n)


slides = [
    ("cover",),
    ("agenda",),
    ("statement", "1. The Core Problem", "Retailers do not lack channels; they lack one trusted decision loop across channels.", "Personalization fails when customer, inventory, pricing and fulfillment are separated.", [
        "Online behavior, mobile intent, store activity and loyalty data often live in different systems.",
        "A recommendation can be attractive but impossible to fulfill if store ATP is wrong.",
        "A promotion can improve conversion but damage margin or violate consent rules.",
    ], DARK),
    ("grid", "2. Prompt Coverage", "The deck starts by making every required element explicit.", [
        ("Business Use Case", "Integrate customer data and autonomously deliver personalized experiences across channels.", GREEN),
        ("Five Agents", "Customer Understanding, Personalization, Inventory, Pricing and Marketing.", BLUE),
        ("Advantage", "Sales uplift, omni-channel personalization and inventory optimization.", AMBER),
        ("Success Criteria", "+40% same-store sales, -50% waste, 85% satisfaction, +60% LTV.", RED),
        ("Omnichannel", "App, email, marketplace, mini-program, store POS and pickup context.", PURPLE),
        ("Asia Specificity", "Privacy laws, language, payments, channel maturity and urban/rural stores.", GREEN),
    ], 3),
    ("two_col", "3. Scenario Assumption", "A concrete Asia retail scenario keeps the presentation grounded.", "Shanghai Heatwave Retail Event", [
        "Weather signal shows a 7-day heatwave.",
        "App searches for breathable and sun-protection products rise.",
        "Store RFID and POS show strong try-on and conversion signals.",
        "Marketplace traffic increases but store ATP is uneven.",
    ], "Business Decision Needed", [
        "Who should receive personalized offers?",
        "Which products can be safely recommended?",
        "Which stores need replenishment or transfer?",
        "Which price and campaign actions are allowed?",
    ], RED, GREEN),
    ("process", "4. End-to-End Customer Journey", "The same context must follow the customer across touchpoints.", [
        ("Browse", "Customer browses summer products in app and marketplace.", GREEN),
        ("Engage", "Personalized content appears in email or mini-program.", BLUE),
        ("Check", "Customer checks local store inventory and pickup options.", AMBER),
        ("Visit", "In-store try-on and POS actions update the profile.", PURPLE),
        ("Retain", "Post-purchase service and next recommendation use the same context.", RED),
    ]),
    ("grid", "5. Customer Understanding Agent", "Build a consent-aware unified customer profile.", [
        ("Identity", "Unify loyalty ID, app ID, store visit and marketplace identity where allowed.", GREEN),
        ("Behavior", "Browse, search, cart, purchase, return, complaint and try-on signals.", BLUE),
        ("Intent", "Detect needs such as cooling, comfort, gifting, replacement or bargain seeking.", AMBER),
        ("Consent", "Only use data and channels allowed by market and customer permission.", RED),
        ("Language", "Keep market language and tone preferences in the profile.", PURPLE),
        ("Value", "Segment by LTV, retention risk and service sensitivity.", GREEN),
    ], 3),
    ("grid", "6. Personalization Agent", "Generate experiences that are relevant and fulfillable.", [
        ("Product Display", "Rank products by intent, availability, margin and service context.", GREEN),
        ("Email / Message", "Generate localized copy and channel-specific content.", BLUE),
        ("Recommendation", "Recommend only products that can be fulfilled in the right channel.", AMBER),
        ("Next Best Action", "Choose offer, content, service recovery, pickup or no action.", RED),
        ("Channel Memory", "Avoid repeating the same message across app, email and store.", PURPLE),
        ("Human Review", "High-risk customer touch requires approval or policy check.", GREEN),
    ], 3),
    ("grid", "7. Inventory Agent", "Personalization depends on reliable supply.", [
        ("Demand Forecast", "Estimate 7-day SKU/store/channel demand.", BLUE),
        ("ATP Confidence", "Mark low-confidence inventory before recommending it.", RED),
        ("Replenishment", "Suggest warehouse to store replenishment.", GREEN),
        ("Transfer", "Move stock from slower stores to higher demand locations.", AMBER),
        ("Waste Reduction", "Reduce aging stock, markdown loss and dead inventory.", PURPLE),
        ("Rural/Urban", "Use different lead time and service rules by store network.", BLUE),
    ], 3),
    ("grid", "8. Pricing Agent", "Dynamic pricing must respect demand, competition and margin.", [
        ("Demand", "Use heatwave demand and conversion signal.", GREEN),
        ("Competition", "Read competitor and marketplace price pressure.", BLUE),
        ("Inventory", "Discount only when inventory position supports it.", AMBER),
        ("Margin Guardrail", "Block discounts that cross margin floor.", RED),
        ("Exception Approval", "Escalate sensitive price changes.", PURPLE),
        ("Learning", "Feed outcome back into future elasticity estimates.", GREEN),
    ], 3),
    ("grid", "9. Marketing Agent", "Autonomous campaign planning with budget control.", [
        ("Audience", "Select consented high-intent cohorts.", GREEN),
        ("Content", "Create localized campaign drafts.", BLUE),
        ("Budget", "Allocate spend by expected incremental value.", AMBER),
        ("Channel", "Choose app, email, marketplace, mini-program or store task.", PURPLE),
        ("Experiment", "Create test/control or A/B measurement.", GREEN),
        ("Approval", "Do not send high-risk campaigns without approval.", RED),
    ], 3),
    ("process", "10. Multi-Agent Collaboration", "The five business Agents share one case state.", [
        ("Customer", "Who is the customer and what do they need?", GREEN),
        ("Personalization", "What is the right experience or offer?", BLUE),
        ("Inventory", "Can the product be fulfilled?", AMBER),
        ("Pricing", "Is the price commercially safe?", PURPLE),
        ("Marketing", "How should we activate the customer?", RED),
    ]),
    ("statement", "11. Why Retail Decision Case", "This is the upgrade from capability demo to enterprise system.", "Agent output becomes a decision packet, not uncontrolled automation.", [
        "The Case keeps customer context, evidence, alternatives, policy checks and approval state together.",
        "It gives business users one object to approve, reject, execute and audit.",
        "It proves the platform can work inside enterprise operating controls.",
    ], DARK),
    ("process", "12. Decision Operating Loop", "The core product workflow shown in the live demo.", [
        ("Exception", "Signals create a business exception.", RED),
        ("Truth", "Deterministic services compute ATP, margin and consent.", BLUE),
        ("Agents", "Five Agents create alternatives.", GREEN),
        ("Decision", "Human roles approve risky actions.", AMBER),
        ("Execution", "Approved actions write to systems with receipts.", PURPLE),
    ]),
    ("grid", "13. Human Roles and Boundaries", "Autonomy needs clear operating responsibility.", [
        ("Store Manager", "Confirms inventory, receiving and store facts.", GREEN),
        ("Regional Manager", "Approves transfer, replenishment and local execution.", BLUE),
        ("Executive", "Reviews high-impact pricing, promotion and budget decisions.", AMBER),
        ("AI System", "Recommends, explains, drafts and monitors.", PURPLE),
        ("Policy Layer", "Blocks unsafe or non-compliant actions.", RED),
        ("Audit Layer", "Records why, who, when and what happened.", GREEN),
    ], 3),
    ("grid", "14. Production Guardrails", "LLM is useful, but deterministic controls own the facts.", [
        ("Consent", "No unauthorized customer outreach.", RED),
        ("Inventory", "No recommendation for low-confidence or unavailable stock.", BLUE),
        ("Margin", "No discount below floor without approval.", AMBER),
        ("Idempotency", "No duplicate execution into downstream systems.", GREEN),
        ("Traceability", "Every suggestion and action is logged.", PURPLE),
        ("Rollback", "Failed writes create retry or compensation tasks.", RED),
    ], 3),
    ("two_col", "15. Live Demo Plan", "The system demo should support the story, not replace the presentation.", "8-Minute Demo Flow", [
        "Open home page and point to Prompt coverage.",
        "Open the Shanghai Case.",
        "Show AI decision support and five-Agent collaboration.",
        "Show approval, blocked action and execution receipt.",
        "Show audit and Azure readiness evidence.",
    ], "What The Panel Should See", [
        "This is not only a chatbot.",
        "The required Agents are present.",
        "Personalization is cross-channel and constrained by operations.",
        "The system is auditable and enterprise-ready.",
    ], GREEN, BLUE),
    ("grid", "16. Asia Regional Specificity", "Regional complexity is part of the architecture, not a footnote.", [
        ("China Mainland", "PIPL, WeChat, mini-program, Tmall/JD, Alipay and WeChat Pay.", RED),
        ("Japan", "APPI, LINE, Rakuten, PayPay and careful service tone.", BLUE),
        ("Southeast Asia", "PDPA variants, multilingual journeys, Shopee/Lazada and local wallets.", GREEN),
        ("Korea", "PIPA, Kakao, Naver and high-frequency mobile touchpoints.", AMBER),
        ("Urban Stores", "High foot traffic, fast pickup, dense stock transfer network.", PURPLE),
        ("Rural Stores", "Longer replenishment lead time and different service expectations.", GREEN),
    ], 3),
    ("two_col", "17. Data and Privacy Architecture", "Customer intelligence must be privacy-aware by design.", "Data Domains", [
        "Customer profile and consent state.",
        "Product, SKU, price and margin.",
        "Store, warehouse, ATP and transfer.",
        "Campaign, channel and engagement.",
    ], "Privacy Controls", [
        "Market-specific policy rules.",
        "Consent-aware personalization.",
        "Purpose limitation and audit trail.",
        "Regional data boundary design for production.",
    ], BLUE, RED),
    ("grid", "18. Success Metrics and Measurement", "The success criteria are pilot targets, not claimed demo results.", [
        ("Sales +40%", "Measure by test/control stores, conversion, basket size and repeat purchase.", GREEN),
        ("Waste -50%", "Measure aging stock, stockout, markdown loss and transfer efficiency.", BLUE),
        ("Satisfaction 85%", "Measure survey, complaint rate, return reason and service resolution.", AMBER),
        ("LTV +60%", "Measure cohort retention, repeat purchase and member tier migration.", RED),
    ], 2),
    ("process", "19. Experiment Design", "How to prove business impact after the prototype.", [
        ("Baseline", "Choose comparable stores and member cohorts.", GREEN),
        ("Pilot", "Run Agent recommendations with human approval.", BLUE),
        ("Control", "Keep a similar group on current process.", AMBER),
        ("Measure", "Track sales, waste, satisfaction and LTV.", PURPLE),
        ("Scale", "Expand only after guardrails and KPIs are stable.", RED),
    ]),
    ("grid", "20. Azure Architecture", "Current prototype plus production path.", [
        ("Experience", "Web app, store task view, regional approval and executive cockpit.", GREEN),
        ("Runtime", "Azure Container Apps and FastAPI Agent Runtime.", BLUE),
        ("Agent AI", "Azure OpenAI / AI Foundry for reasoning and generation.", PURPLE),
        ("State", "Cosmos DB for Case, work order, approval and audit state.", AMBER),
        ("Data Platform", "Event Hubs, Fabric, AI Search and Power BI feedback.", GREEN),
        ("Security/Ops", "APIM, Managed Identity, Key Vault and Application Insights.", RED),
    ], 3),
    ("grid", "21. Current Implementation Evidence", "What has been built for the review.", [
        ("Deployed App", "Azure Container Apps revisioned deployment with public endpoint.", GREEN),
        ("Case State", "Shared Retail Decision Case state in the runtime.", BLUE),
        ("AI Decision API", "Read-only decision intelligence endpoint for each Case.", PURPLE),
        ("Approval Flow", "Business roles approve or block high-risk actions.", AMBER),
        ("Audit Evidence", "Agent reasoning, policy blocks and execution receipts are visible.", RED),
        ("Bilingual UI", "Chinese and English presentation-ready flow.", GREEN),
    ], 3),
    ("two_col", "22. Architecture Decisions", "The key design choices and trade-offs.", "Decisions", [
        "Use Case-centric orchestration instead of Agent menu navigation.",
        "Keep deterministic services for ATP, consent, margin and execution.",
        "Use human approval for risky customer, price and inventory actions.",
        "Treat success numbers as pilot targets with measurement design.",
    ], "Trade-offs", [
        "Less flashy than fully autonomous execution.",
        "More credible for enterprise retail governance.",
        "Supports regional compliance and operational variation.",
        "Makes the prototype defensible under panel questioning.",
    ], GREEN, AMBER),
    ("statement", "23. What I Want The Panel To Remember", "This is the final synthesis before the live system view.", "The platform turns personalization into controlled retail decisions.", [
        "It integrates customer data across online, mobile and physical store touchpoints.",
        "It uses five Agents to personalize, optimize inventory, price and activate marketing.",
        "It adds approval, execution, audit and measurement so the system can be trusted.",
    ], DARK),
    ("close",),
]


for idx, spec in enumerate(slides, 1):
    kind = spec[0]
    if kind == "cover":
        cover(idx)
    elif kind == "agenda":
        agenda(idx)
    elif kind == "two_col":
        _, a, b, c, d, e, f, g, h = spec
        two_col(idx, a, b, c, d, e, f, g, h)
    elif kind == "grid":
        _, a, b, c, d = spec
        grid(idx, a, b, c, d)
    elif kind == "process":
        _, a, b, c = spec
        process(idx, a, b, c)
    elif kind == "statement":
        _, a, b, c, d, e = spec
        statement(idx, a, b, c, d, e)
    elif kind == "close":
        close(idx)

prs.save(OUT)
print(OUT)
