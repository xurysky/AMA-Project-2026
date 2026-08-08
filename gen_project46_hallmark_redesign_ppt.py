#!/usr/bin/env python3
"""Generate Hallmark-redesigned Project 46 review decks.

This creates a post-report archive version without overwriting the deck used
in the live AMA presentation. The content spine stays the same, while the
visual system moves away from card/stripe AI-slide patterns.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import shorten

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR
from pptx.util import Cm, Pt

from gen_project46_review_story_ppt import EN, ZH


ROOT = Path(__file__).resolve().parent
OUT_ZH = ROOT / "AMA-项目46-评审故事线-Hallmark重设计版-中文.pptx"
OUT_EN = ROOT / "AMA-Project46-Review-Story-Hallmark-Redesign-English.pptx"

W = Cm(33.867)
H = Cm(19.05)

PAPER = "F6F3EA"
PAPER_2 = "ECE7DC"
INK = "17201C"
MUTED = "65706A"
RULE = "D8D2C5"
TEAL = "0F766E"
BLUE = "2563EB"
AMBER = "B7791F"
PLUM = "6D5BD0"
RED = "C24132"
WHITE = "FFFFFF"

ACCENTS = [TEAL, BLUE, AMBER, PLUM, RED]
DISPLAY_FONT_ZH = "Microsoft YaHei"
BODY_FONT_ZH = "Microsoft YaHei"
DISPLAY_FONT_EN = "Aptos Display"
BODY_FONT_EN = "Aptos"


def rgb(hex_value: str) -> RGBColor:
    value = hex_value.strip("#")
    return RGBColor(int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def prs() -> Presentation:
    deck = Presentation()
    deck.slide_width = W
    deck.slide_height = H
    return deck


def blank(deck: Presentation):
    slide = deck.slides.add_slide(deck.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = rgb(PAPER)
    return slide


def box(slide, x, y, w, h, fill=PAPER, line=None, radius=True):
    shape_type = MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE
    s = slide.shapes.add_shape(shape_type, Cm(x), Cm(y), Cm(w), Cm(h))
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(fill)
    s.line.color.rgb = rgb(line or fill)
    s.line.width = Pt(0.75 if line else 0)
    return s


def text(slide, value, x, y, w, h, size=20, color=INK, bold=False, font="Aptos", align=PP_ALIGN.LEFT):
    t = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = t.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    tf.vertical_anchor = MSO_ANCHOR.TOP
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = value
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = rgb(color)
    return t


def add_bullets(slide, bullets, x, y, w, h, font, size=16, color=INK, bullet_color=None):
    t = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = t.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    for idx, b in enumerate(bullets):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(6)
        r = p.add_run()
        r.text = f"• {b}"
        r.font.name = font
        r.font.size = Pt(size)
        r.font.color.rgb = rgb(bullet_color or color)
    return t


def footer(slide, lang, slide_no, total, accent=TEAL):
    label = "AMA Project 46 · Autonomous Retail Intelligence" if lang == "en" else "AMA 项目 46 · 自主零售智能"
    text(slide, label, 1.25, 18.0, 15, 0.45, size=8.5, color=MUTED, font=BODY_FONT_EN if lang == "en" else BODY_FONT_ZH)
    text(slide, f"{slide_no:02d}/{total:02d}", 31.2, 18.0, 1.4, 0.45, size=8.5, color=MUTED, font=BODY_FONT_EN, align=PP_ALIGN.RIGHT)
    slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Cm(1.25), Cm(17.72), Cm(30.9), Cm(0.03)).fill.solid()
    slide.shapes[-1].fill.fore_color.rgb = rgb(RULE)
    slide.shapes[-1].line.width = Pt(0)
    slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Cm(1.25), Cm(17.72), Cm(3.8), Cm(0.05)).fill.solid()
    slide.shapes[-1].fill.fore_color.rgb = rgb(accent)
    slide.shapes[-1].line.width = Pt(0)


def top_label(slide, label, x, y, fill, font):
    box(slide, x, y, 4.1, 0.72, fill=fill, line=fill, radius=False)
    text(slide, label.upper(), x + 0.18, y + 0.11, 3.75, 0.42, size=8.5, color=WHITE, bold=True, font=font)


def title_block(slide, title, subtitle, lang, slide_no, accent=TEAL):
    font_d = DISPLAY_FONT_EN if lang == "en" else DISPLAY_FONT_ZH
    font_b = BODY_FONT_EN if lang == "en" else BODY_FONT_ZH
    text(slide, title, 1.25, 1.0, 24.5, 1.55, size=30, color=INK, bold=True, font=font_d)
    if subtitle:
        text(slide, subtitle, 1.28, 2.55, 22, 0.72, size=13.5, color=MUTED, font=font_b)
    # Numbered evidence motif, not a decorative title underline.
    box(slide, 29.6, 0.86, 2.55, 1.15, fill=accent, line=accent, radius=False)
    text(slide, f"{slide_no-1:02d}", 29.93, 0.92, 1.65, 0.8, size=20, color=WHITE, bold=True, font=DISPLAY_FONT_EN, align=PP_ALIGN.CENTER)


def split_title(entry_title: str) -> str:
    if ". " in entry_title[:5]:
        return entry_title.split(". ", 1)[1]
    return entry_title


def flatten(entry):
    kind = entry[0]
    if kind == "thesis":
        _, title, subtitle, main, bullets = entry
        return kind, title, subtitle, main, bullets
    if kind == "grid":
        _, title, subtitle, items = entry
        return kind, title, subtitle, items
    if kind == "two":
        _, title, subtitle, left, right = entry
        return kind, title, subtitle, left, right
    if kind == "process":
        _, title, subtitle, steps = entry
        return kind, title, subtitle, steps
    if kind == "architecture":
        _, title, subtitle = entry
        return kind, title, subtitle
    raise ValueError(kind)


def cover(slide, lang):
    font_d = DISPLAY_FONT_EN if lang == "en" else DISPLAY_FONT_ZH
    font_b = BODY_FONT_EN if lang == "en" else BODY_FONT_ZH
    box(slide, 0, 0, 33.87, 19.05, fill=PAPER, radius=False)
    box(slide, 22.4, 0, 11.47, 19.05, fill=INK, radius=False)
    text(slide, "46", 22.95, 1.2, 8.8, 4.2, size=92, color=PAPER, bold=True, font=DISPLAY_FONT_EN)
    text(slide, "PROJECT", 23.15, 5.55, 5.6, 0.65, size=12, color="B7C9C3", bold=True, font=DISPLAY_FONT_EN)
    text(slide, "CASE · AGENTS · AZURE", 23.15, 16.8, 8.0, 0.55, size=10, color="B7C9C3", bold=True, font=DISPLAY_FONT_EN)
    if lang == "en":
        title = "Autonomous Retail Intelligence"
        subtitle = "From customer data to governed retail decisions"
        owner = "Yuan Wang · AMA Capstone · Hallmark redesign"
        bullets = ["Customer 360", "Retail Decision Case", "Five-agent decision packet", "Azure landing"]
    else:
        title = "自主零售智能 Agent 平台"
        subtitle = "从客户数据整合到可治理的零售经营决策"
        owner = "王缘 · AMA 终汇报留档 · Hallmark 重设计版"
        bullets = ["Customer 360", "Retail Decision Case", "五 Agent 决策包", "Azure 企业落地"]
    text(slide, "Project 46", 1.35, 1.3, 8, 0.8, size=17, color=TEAL, bold=True, font=font_b)
    text(slide, title, 1.25, 3.35, 19.2, 2.2, size=37, color=INK, bold=True, font=font_d)
    text(slide, subtitle, 1.32, 5.85, 17.5, 0.9, size=17, color=MUTED, font=font_b)
    box(slide, 1.25, 8.45, 17.7, 3.8, fill=PAPER_2, line=PAPER_2, radius=False)
    for i, b in enumerate(bullets):
        x = 1.85 + (i % 2) * 8.0
        y = 9.0 + (i // 2) * 1.25
        text(slide, f"{i+1:02d}", x, y, 1.2, 0.45, size=11, color=TEAL, bold=True, font=DISPLAY_FONT_EN)
        text(slide, b, x + 1.05, y - 0.02, 6.1, 0.55, size=13.5, color=INK, bold=True, font=font_b)
    text(slide, owner, 1.32, 16.95, 15, 0.6, size=10.5, color=MUTED, font=font_b)


def thesis_slide(slide, entry, lang, slide_no, total):
    _, title, subtitle, main, bullets = flatten(entry)
    title_block(slide, split_title(title), subtitle, lang, slide_no, TEAL)
    font_d = DISPLAY_FONT_EN if lang == "en" else DISPLAY_FONT_ZH
    font_b = BODY_FONT_EN if lang == "en" else BODY_FONT_ZH
    box(slide, 1.25, 5.0, 19.3, 5.4, fill=INK, line=INK, radius=False)
    text(slide, main, 2.0, 5.72, 17.8, 3.5, size=24, color=PAPER, bold=True, font=font_d)
    top_label(slide, "Answer" if lang == "en" else "我的回答", 22.25, 5.0, TEAL, font_b)
    add_bullets(slide, bullets, 22.3, 6.12, 9.2, 6.0, font_b, size=14.2, color=INK)
    footer(slide, lang, slide_no, total, TEAL)


def grid_slide_h(slide, entry, lang, slide_no, total):
    _, title, subtitle, items = flatten(entry)
    accent = BLUE if slide_no % 2 else TEAL
    title_block(slide, split_title(title), subtitle, lang, slide_no, accent)
    font_b = BODY_FONT_EN if lang == "en" else BODY_FONT_ZH
    x0, y0, gap = 1.25, 4.55, 0.48
    card_w, card_h = 10.1, 3.45
    for idx, item in enumerate(items[:6]):
        name, desc, _ = item
        col, row = idx % 3, idx // 3
        x, y = x0 + col * (card_w + gap), y0 + row * (card_h + gap)
        fill = [WHITE, PAPER_2, WHITE, PAPER_2, WHITE, PAPER_2][idx]
        box(slide, x, y, card_w, card_h, fill=fill, line=RULE, radius=False)
        box(slide, x, y, card_w, 0.18, fill=ACCENTS[idx % len(ACCENTS)], line=ACCENTS[idx % len(ACCENTS)], radius=False)
        text(slide, f"{idx+1:02d}", x + 0.42, y + 0.55, 1.0, 0.5, size=10, color=ACCENTS[idx % len(ACCENTS)], bold=True, font=DISPLAY_FONT_EN)
        text(slide, name, x + 1.5, y + 0.48, 7.8, 0.55, size=14, color=INK, bold=True, font=font_b)
        text(slide, desc, x + 0.45, y + 1.35, 8.9, 1.45, size=11.6, color=MUTED, font=font_b)
    footer(slide, lang, slide_no, total, accent)


def two_slide_h(slide, entry, lang, slide_no, total):
    _, title, subtitle, left, right = flatten(entry)
    accent = ACCENTS[(slide_no - 2) % len(ACCENTS)]
    title_block(slide, split_title(title), subtitle, lang, slide_no, accent)
    font_b = BODY_FONT_EN if lang == "en" else BODY_FONT_ZH
    panels = [(left, 1.25, 4.55, 15.0, accent), (right, 17.55, 4.55, 15.05, TEAL if accent != TEAL else BLUE)]
    for panel, x, y, w, color in panels:
        heading, bullets, _ = panel
        box(slide, x, y, w, 10.95, fill=WHITE, line=RULE, radius=False)
        box(slide, x, y, w, 0.62, fill=color, line=color, radius=False)
        text(slide, heading, x + 0.55, y + 1.05, w - 1.1, 0.7, size=17, color=INK, bold=True, font=font_b)
        add_bullets(slide, bullets[:4], x + 0.6, y + 2.18, w - 1.25, 7.8, font_b, size=13.7, color=INK)
    footer(slide, lang, slide_no, total, accent)


def process_slide_h(slide, entry, lang, slide_no, total):
    _, title, subtitle, steps = flatten(entry)
    title_block(slide, split_title(title), subtitle, lang, slide_no, AMBER)
    font_b = BODY_FONT_EN if lang == "en" else BODY_FONT_ZH
    y = 6.0
    x0 = 1.25
    usable = 31.15
    step_w = usable / len(steps)
    for idx, (name, desc, _) in enumerate(steps):
        x = x0 + idx * step_w
        color = ACCENTS[idx % len(ACCENTS)]
        box(slide, x + 0.1, y, step_w - 0.35, 4.85, fill=WHITE if idx % 2 == 0 else PAPER_2, line=RULE, radius=False)
        text(slide, f"{idx+1:02d}", x + 0.55, y + 0.48, 1.3, 0.55, size=13, color=color, bold=True, font=DISPLAY_FONT_EN)
        text(slide, name, x + 0.55, y + 1.35, step_w - 1.0, 0.82, size=13.5, color=INK, bold=True, font=font_b)
        text(slide, desc, x + 0.55, y + 2.45, step_w - 1.05, 1.65, size=10.8, color=MUTED, font=font_b)
        if idx < len(steps) - 1:
            line = slide.shapes.add_connector(1, Cm(x + step_w - 0.18), Cm(y + 2.42), Cm(x + step_w + 0.1), Cm(y + 2.42))
            line.line.color.rgb = rgb(INK)
            line.line.width = Pt(1.0)
    text(slide, "Decision Packet" if lang == "en" else "决策包生成路径", 1.55, 12.4, 11.5, 0.65, size=14, color=TEAL, bold=True, font=font_b)
    box(slide, 1.55, 13.25, 30.55, 1.1, fill=INK, line=INK, radius=False)
    text(slide, "Customer context → Case object → Agent reasoning → Approval → Execution evidence" if lang == "en" else "客户上下文 → 经营 Case → Agent 推理 → 人工审批 → 执行回执", 2.0, 13.48, 29.0, 0.45, size=13.5, color=PAPER, bold=True, font=font_b, align=PP_ALIGN.CENTER)
    footer(slide, lang, slide_no, total, AMBER)


def architecture_slide_h(slide, entry, lang, slide_no, total):
    _, title, subtitle = flatten(entry)
    title_block(slide, split_title(title), subtitle, lang, slide_no, BLUE)
    font_b = BODY_FONT_EN if lang == "en" else BODY_FONT_ZH
    layers = [
        ("Experience", "Role workbench / mobile / bilingual UI"),
        ("API & Control", "APIM · MCP tools · governance"),
        ("Agent Runtime", "Container Apps · revisions · health"),
        ("AI & Knowledge", "Azure OpenAI · AI Foundry · AI Search"),
        ("Data & Events", "Cosmos DB · Service Bus · Event Grid"),
        ("Observability", "App Insights · Log Analytics · Power BI"),
    ]
    if lang != "en":
        layers = [
            ("体验层", "角色工作台 / 移动端 / 中英文"),
            ("API 与控制", "APIM · MCP 工具 · 治理"),
            ("Agent 运行时", "Container Apps · revision · 健康探针"),
            ("AI 与知识", "Azure OpenAI · AI Foundry · AI Search"),
            ("数据与事件", "Cosmos DB · Service Bus · Event Grid"),
            ("观测与复盘", "App Insights · Log Analytics · Power BI"),
        ]
    for i, (name, desc) in enumerate(layers):
        y = 4.45 + i * 1.85
        color = ACCENTS[i % len(ACCENTS)]
        box(slide, 2.0 + i * 0.45, y, 28.1 - i * 0.9, 1.25, fill=WHITE if i % 2 == 0 else PAPER_2, line=RULE, radius=False)
        text(slide, name, 2.55 + i * 0.45, y + 0.28, 6.0, 0.45, size=13.5, color=color, bold=True, font=font_b)
        text(slide, desc, 10.0, y + 0.3, 17.8, 0.45, size=12.2, color=INK, font=font_b)
    footer(slide, lang, slide_no, total, BLUE)


def build(data, lang):
    deck = prs()
    total = len(data) + 1
    s = blank(deck)
    cover(s, lang)
    footer(s, lang, 1, total, TEAL)
    for idx, entry in enumerate(data, 2):
        s = blank(deck)
        kind = entry[0]
        if kind == "thesis":
            thesis_slide(s, entry, lang, idx, total)
        elif kind == "grid":
            grid_slide_h(s, entry, lang, idx, total)
        elif kind == "two":
            two_slide_h(s, entry, lang, idx, total)
        elif kind == "process":
            process_slide_h(s, entry, lang, idx, total)
        elif kind == "architecture":
            architecture_slide_h(s, entry, lang, idx, total)
    return deck


def main():
    # Hallmark · pre-emit critique: P4 H4 E4 S4 R4 V4
    zh = build(ZH, "zh")
    en = build(EN, "en")
    zh.save(OUT_ZH)
    en.save(OUT_EN)
    print(OUT_ZH)
    print(OUT_EN)


if __name__ == "__main__":
    main()
