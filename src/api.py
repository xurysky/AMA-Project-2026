from dotenv import load_dotenv
load_dotenv()
"""
AMA Retail Agent Platform — FastAPI service
Scenario-driven 5-Agent demo for Autonomous Retail Intelligence.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from src.azure_services import (
    DEPLOYMENT,
    agent_decide,
    orchestrator_decompose,
    query_customers,
    read_run,
    run_store_enabled,
    upsert_customer,
    upsert_run,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.scenario_engine import RetailScenarioEngine

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
RUNS: Dict[str, Dict[str, Any]] = {}

app = FastAPI(
    title="AMA Retail Agent Platform",
    description="Autonomous Retail Intelligence Agent Platform - scenario-driven 5 Agent decision loop",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_work_orders(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create executable work orders from agent decisions."""
    loop = result["decision_loop"]
    inventory = next(d for d in loop if d["agent"] == "Inventory Agent")
    pricing = next(d for d in loop if d["agent"] == "Pricing Agent")
    marketing = next(d for d in loop if d["agent"] == "Marketing Agent")
    season = result.get("season", "season")
    orders: List[Dict[str, Any]] = []

    def next_order_id() -> str:
        return f"WO-{season.upper()}-{len(orders)+1:03d}"

    def add_order(order: Dict[str, Any], title_en: str, detail_en: str, title_zh: str, detail_zh: str) -> None:
        """Keep a Chinese default for old UI paths, plus explicit EN/ZH fields for language-aware pages."""
        order.update({
            # Default fields stay English as a cache-safe fallback for old JS bundles.
            # The current UI still uses title_zh/detail_zh when the user switches to Chinese.
            "title": title_en,
            "detail": detail_en,
            "title_en": title_en,
            "detail_en": detail_en,
            "title_zh": title_zh,
            "detail_zh": detail_zh,
        })
        orders.append(order)

    for p in inventory["decision"].get("products", []):
        if p.get("recommended_replenishment", 0) > 0:
            add_order({
                "id": next_order_id(),
                "type": "REPLENISHMENT",
                "sku_id": p["sku_id"],
                "owner": "Store Ops / Supply Chain",
                "status": "PENDING_APPROVAL" if p.get("stock_risk") == "high" else "READY",
                "agent": "Inventory Agent",
                "created_at": now_iso(),
                "completed_at": None,
            },
                title_en=f"Replenishment / transfer: {p['name']}",
                detail_en=f"Recommend replenishing {p['recommended_replenishment']} units; current stock {p['current_stock']}; safety stock {p['safety_stock']}; risk {p['stock_risk']}",
                title_zh=f"补货/调拨：{p['name']}",
                detail_zh=f"建议补货 {p['recommended_replenishment']} 件；当前库存 {p['current_stock']}；安全库存 {p['safety_stock']}；风险 {p['stock_risk']}",
            )

    for a in pricing["decision"].get("pricing_actions", []):
        if "clearance" in a.get("strategy", "") or a.get("requires_approval"):
            add_order({
                "id": next_order_id(),
                "type": "PRICE_PROMOTION",
                "sku_id": a["sku_id"],
                "owner": "Merchandising / Finance",
                "status": "PENDING_APPROVAL" if a.get("requires_approval") else "READY",
                "agent": "Pricing Agent",
                "created_at": now_iso(),
                "completed_at": None,
            },
                title_en=f"Pricing / promotion: {a['name']}",
                detail_en=f"{a['strategy']}: ¥{a['current_price']} → ¥{a['recommended_price']}; gross margin {a['gross_margin']}",
                title_zh=f"定价/促销：{a['name']}",
                detail_zh=f"{a['strategy']}：¥{a['current_price']} → ¥{a['recommended_price']}；毛利 {a['gross_margin']}",
            )

    for channel, plan in marketing["decision"].get("channel_plan", {}).items():
        add_order({
            "id": next_order_id(),
            "type": "CAMPAIGN",
            "sku_id": None,
            "owner": "CRM / Marketing",
            "status": "PENDING_APPROVAL" if marketing.get("human_approval_required") else "READY",
            "agent": "Marketing Agent",
            "created_at": now_iso(),
            "completed_at": None,
        },
            title_en=f"Channel activation: {channel}",
            detail_en=f"{plan['customers']} customer(s); budget ¥{plan['budget']}; expected conversions {plan['expected_conversions']}",
            title_zh=f"渠道触达：{channel}",
            detail_zh=f"{plan['customers']} 个客户；预算 ¥{plan['budget']}；预计转化 {plan['expected_conversions']}",
        )

    launch = build_fashion_launch_story(result)
    best_visual = max(launch["visual_lab"]["variants"], key=lambda v: v["predicted_ctr"])
    visual_variant_en = str(best_visual["variant"]).replace("A. 通勤地铁清凉场景", "A. Cool commuter metro scene").replace("B. 儿童运动后防闷汗场景", "B. Kids sports anti-sweat scene").replace("C. 亲子周末出游场景", "C. Family weekend outing scene")
    add_order(
        {
            "id": next_order_id(),
            "type": "AIGC_VISUAL_TEST",
            "sku_id": launch["hero_sku"],
            "owner": "E-commerce Creative / BI",
            "status": "READY",
            "agent": "Visual Intelligence Agent",
            "created_at": now_iso(),
            "completed_at": None,
        },
        title_en=f"AIGC visual test launch: {visual_variant_en}",
        detail_en=f"Use the CTR {best_visual['predicted_ctr']}% winning creative for e-commerce hero image/detail page; SKU coverage: {launch['visual_lab']['sku_coverage']}",
        title_zh=f"AIGC 测图上线：{best_visual['variant']}",
        detail_zh=f"选择 CTR {best_visual['predicted_ctr']}% 的素材进入电商主图/详情页；覆盖 {launch['visual_lab']['sku_coverage']} SKU",
    )
    add_order(
        {
            "id": next_order_id(),
            "type": "LIVE_COMMERCE",
            "sku_id": launch["hero_sku"],
            "owner": "Live Commerce / Private Domain",
            "status": "PENDING_APPROVAL",
            "agent": "Live Commerce Agent",
            "created_at": now_iso(),
            "completed_at": None,
        },
        title_en="Digital human live commerce: recover long-tail unmanned slots",
        detail_en=f"Add {launch['live_commerce']['empty_slots_recovered']} unmanned hours; add {launch['live_commerce']['faq_updates']} FAQ knowledge-base entries",
        title_zh="数字人直播：填补深夜长尾时段",
        detail_zh=f"新增 {launch['live_commerce']['empty_slots_recovered']} 小时无人时段；FAQ 知识库新增 {launch['live_commerce']['faq_updates']} 条",
    )
    add_order(
        {
            "id": next_order_id(),
            "type": "ROI_REVIEW",
            "sku_id": launch["hero_sku"],
            "owner": "Finance / Business Owner",
            "status": "PENDING_APPROVAL",
            "agent": "Finance ROI Agent",
            "created_at": now_iso(),
            "completed_at": None,
        },
        title_en="Finance ROI Review: 15-day launch business hypothesis",
        detail_en=f"Cycle time {launch['launch_kpis']['baseline_cycle_days']}→{launch['launch_kpis']['target_cycle_days']} days; visual cost saving ¥{launch['launch_kpis']['visual_cost_saving_cny']:,}; demo simulation only",
        title_zh="Finance ROI Review：15 天上新商业假设",
        detail_zh=f"周期 {launch['launch_kpis']['baseline_cycle_days']}→{launch['launch_kpis']['target_cycle_days']} 天；视觉成本节省 ¥{launch['launch_kpis']['visual_cost_saving_cny']:,}；均为 demo simulation",
    )

    return orders


def build_fashion_launch_story(result: Dict[str, Any]) -> Dict[str, Any]:
    """Semir-inspired fashion launch loop: 6 months -> 15 days.

    Values are simulation assumptions for the demo, not validated production ROI.
    """
    season = result.get("season", "summer")
    event = result.get("trigger", {})
    products = result.get("products") or result.get("scenario", {}).get("products") or []
    hero = next((p for p in products if p.get("lifecycle", "").endswith("in_season")), products[0] if products else {})
    hero_name = hero.get("name", "Contoso Air Kids Anti-sweat Tee")
    hero_sku = hero.get("sku_id", "CAIR-KIDS-001")
    views = hero.get("app_views_24h", 28600)
    return {
        "positioning": "Industry benchmark-inspired demo simulation; not validated production results.",
        "story_name": "15-Day AI-Powered Fashion Launch",
        "benchmark_inspiration": "Semir-style AI + BI + RPA full-chain automation: planning, AIGC visual, testing, live commerce, operations and finance.",
        "business_trigger": {
            "event": event.get("type", "heatwave"),
            "city": event.get("city", "Shanghai"),
            "signal": "High-temperature commuting + kids sports anti-sweat demand spikes in comments/search/POS.",
            "formula": "Revenue = impressions × CTR × conversion × AOV",
        },
        "hero_sku": hero_sku,
        "hero_product": hero_name,
        "launch_kpis": {
            "baseline_cycle_days": 180,
            "target_cycle_days": 15,
            "cycle_compression_pct": 91.7,
            "baseline_photo_lead_time_days": 60,
            "ai_visual_generation_minutes": 6,
            "visual_cost_saving_cny": 380000,
            "sample_development_saving_cny": 220000,
            "expected_incremental_revenue_cny": 1280000,
            "roi_positioning": "Demo simulation / target assumption only",
        },
        "parallel_workstreams": [
            {"stream": "Trend Insight", "before": "等待月度报告", "after": "实时总结趋势报告、天气、搜索、评论", "azure": ["Event Hubs", "Fabric", "Azure OpenAI"]},
            {"stream": "Product Planning", "before": "企划完成后才设计", "after": "企划、设计、视觉并行探索", "azure": ["AI Foundry", "Cosmos DB", "AI Search"]},
            {"stream": "AIGC Visual", "before": "约模特/拍摄/修图 1-2 个月", "after": "几分钟生成多版本场景图并测图", "azure": ["Azure OpenAI", "Blob Storage", "Azure ML"]},
            {"stream": "Live Commerce", "before": "深夜/长尾时段无人运营", "after": "数字人脚本 + FAQ 知识库填补空白时段", "azure": ["Azure AI Search", "Azure OpenAI", "Logic Apps"]},
            {"stream": "Automation", "before": "人工跨系统录入/报名/对账", "after": "API + RPA 执行上架、活动、财务同步", "azure": ["API Management", "Logic Apps", "Power Automate"]},
        ],
        "visual_lab": {
            "sku_coverage": "full SKU coverage, not only hero products",
            "input_assets": ["historical model photos", "brand visual guideline", "product catalog", "scene prompts"],
            "variants": [
                {"variant": "A. 通勤地铁清凉场景", "prompt": "Shanghai commuter, light breathable Contoso Air, clean Contoso Fashion style", "predicted_ctr": 5.8, "status": "candidate"},
                {"variant": "B. 儿童运动后防闷汗场景", "prompt": "kids running after school, anti-sweat comfort, mother concern", "predicted_ctr": 6.3, "status": "winner"},
                {"variant": "C. 亲子周末出游场景", "prompt": "family weekend outdoor, breathable quick-dry clothing", "predicted_ctr": 5.5, "status": "candidate"},
            ],
            "ctr_baseline_pct": 5.0,
            "ctr_winner_pct": 6.3,
            "learning_loop": "Low CTR variants update prompt + scene + pose, then regenerate and retest.",
        },
        "consumer_language": {
            "brand_feature": "吸湿透气 / quick dry / breathable fabric",
            "consumer_buying_language": "孩子运动出汗后不容易闷汗着凉；通勤高温也能保持清爽",
            "geo_query": "元旦/暑假去户外或高温通勤，孩子怎么穿不闷汗？",
            "agents": ["Selling Point Analyst", "Audience Analyst", "Copywriter", "Review Expert", "Optimization Expert"],
        },
        "live_commerce": {
            "logic": "Recover unmanned long-tail hours; incremental GMV rather than cannibalizing human live streams.",
            "empty_slots_recovered": 42,
            "script_topics": ["Contoso Air 防闷汗", "夏季亲子出游", "尺码/洗护 FAQ", "库存有限提醒"],
            "faq_updates": 18,
            "knowledge_feedback": "Unanswered bullet-screen questions are written back to AI Search FAQ index for next session.",
            "expected_incremental_gmv_cny": 360000,
        },
        "automation_map": [
            {"domain": "Private Domain", "scenarios": ["企微建群", "活动群发", "签收关怀", "邀好评/回评"], "azure_execution": "Logic Apps + Power Automate + API Management"},
            {"domain": "Customer Service", "scenarios": ["评价回复", "售后工单", "批量退款", "优惠券推送"], "azure_execution": "Azure OpenAI + Functions + OMS API"},
            {"domain": "Logistics", "scenarios": ["24h未发货处理", "退款订单截回", "自动催派", "WOS拦截"], "azure_execution": "Event Grid + Durable Functions + WMS API"},
            {"domain": "Supply Chain", "scenarios": ["供应商准入", "原材料价格采集", "SCM/PLM自动操作"], "azure_execution": "Data Factory + APIM + RPA"},
            {"domain": "Finance", "scenarios": ["投流充值", "账单下载", "银行流水核对", "回款看板"], "azure_execution": "Document Intelligence + Fabric + Power BI"},
        ],
    }



def build_execution_trace(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Detailed trace showing Azure service calls for each agent."""
    trace = []
    decisions = {d["agent"]: d for d in result["decision_loop"]}
    season = result.get("season", "winter")
    event = result.get("trigger", {})

    def _inv_trace(d):
        inv_products = d["decision"].get("products", [])
        high_risk = [p for p in inv_products if p.get("stock_risk") == "high"]
        total_replenish = d["decision"].get("total_replenishment_units", 0)
        return [
            {"service": "Azure Event Hubs", "operation": "read", "detail": f"Consumed weather + POS + RFID streams for {event.get('city','Shanghai')}", "latency_ms": 12, "status": "ok"},
            {"service": "Azure Cosmos DB", "operation": "query", "detail": f"Queried current_stock for {len(inv_products)} SKUs from inventory container", "latency_ms": 28, "status": "ok"},
            {"service": "Azure ML Endpoint", "operation": "invoke", "detail": f"Called demand_forecast_v2 model (Prophet + Weather multipliers)", "latency_ms": 180, "status": "ok", "model": "prophet-demand-v2", "input": {"skus": len(inv_products), "forecast_days": 7}, "output": {"high_risk_skus": len(high_risk), "total_replenishment": total_replenish}},
            {"service": "Azure Cosmos DB", "operation": "write", "detail": f"Wrote stock_risk_by_sku + replenishment_recommendation to operational_memory", "latency_ms": 15, "status": "ok"},
        ]

    def _pricing_trace(d):
        actions = d["decision"].get("pricing_actions", [])
        strategies = set(a.get("strategy", "") for a in actions)
        return [
            {"service": "Azure Cosmos DB", "operation": "query", "detail": "Read stock_risk_by_sku from Inventory Agent shared memory", "latency_ms": 8, "status": "ok"},
            {"service": "API Management", "operation": "call", "detail": "Fetched competitor prices (Zara/H&M/GAP) via MCP proxy", "latency_ms": 220, "status": "ok"},
            {"service": "Microsoft Fabric OneLake", "operation": "query", "detail": "Queried Hybrid AI apparel promo history (lift, ROI, incremental profit)", "latency_ms": 95, "status": "ok"},
            {"service": "Azure OpenAI GPT-4o", "operation": "chat_completions", "detail": "Reasoning: pricing strategy selection under inventory constraints", "latency_ms": 680, "status": "ok", "tokens": {"prompt": 1840, "completion": 420}, "model": "gpt-4o", "system_prompt": "You are a retail pricing agent. Select strategy based on inventory risk and margin floor.", "output_summary": f"Strategies: {', '.join(strategies)}"},
            {"service": "Azure Cosmos DB", "operation": "write", "detail": "Wrote pricing_actions + promotion_validation to shared_memory", "latency_ms": 12, "status": "ok"},
        ]

    def _customer_trace(d):
        targets = d["decision"].get("target_customers", [])
        high_intent = [t for t in targets if t.get("purchase_intent") == "high"]
        return [
            {"service": "Azure Cosmos DB", "operation": "query", "detail": f"Queried CRM profiles for {len(targets)} customers from customer_container", "latency_ms": 22, "status": "ok"},
            {"service": "Azure Redis Cache", "operation": "get", "detail": "Retrieved real-time behavioral signals (views, cart, session)", "latency_ms": 4, "status": "ok"},
            {"service": "Azure OpenAI GPT-4o", "operation": "chat_completions", "detail": "Synthesized customer intent from behavioral + contextual signals", "latency_ms": 520, "status": "ok", "tokens": {"prompt": 2100, "completion": 380}, "model": "gpt-4o", "system_prompt": "You are a customer understanding agent. Score purchase intent from behavioral signals.", "output_summary": f"{len(high_intent)} high-intent customers identified"},
            {"service": "Azure Cosmos DB", "operation": "write", "detail": "Wrote target_segments + intent_scores to shared_memory", "latency_ms": 10, "status": "ok"},
        ]

    def _personalization_trace(d):
        recs = d["decision"].get("personalized_recommendations", [])
        total_recs = sum(len(r.get("recommendations", [])) for r in recs)
        return [
            {"service": "Azure Cosmos DB", "operation": "query", "detail": "Read available_stock + price_action from Inventory/Pricing shared memory", "latency_ms": 12, "status": "ok"},
            {"service": "Azure AI Search", "operation": "vector_search", "detail": f"Vector similarity search: matched {total_recs} products to customer segments", "latency_ms": 85, "status": "ok", "index": "product-embeddings", "query_type": "hybrid (vector + filters)", "output_summary": f"{total_recs} product matches across {len(recs)} customers"},
            {"service": "Azure OpenAI Embeddings", "operation": "embeddings", "detail": "Generated customer intent embeddings for personalized ranking", "latency_ms": 120, "status": "ok", "model": "text-embedding-3-large", "dimensions": 3072},
            {"service": "Azure OpenAI GPT-4o", "operation": "chat_completions", "detail": "Reranked recommendations with inventory guardrails and context", "latency_ms": 450, "status": "ok", "tokens": {"prompt": 2400, "completion": 560}, "model": "gpt-4o", "system_prompt": "You are a personalization agent. Generate next-best-action constrained by stock risk and pricing."},
            {"service": "Azure Cosmos DB", "operation": "write", "detail": "Wrote personalized_recommendations to shared_memory", "latency_ms": 14, "status": "ok"},
        ]

    def _marketing_trace(d):
        plan = d["decision"].get("channel_plan", {})
        channels = list(plan.keys())
        return [
            {"service": "Azure Cosmos DB", "operation": "query", "detail": "Read target_segments + recommendations from Customer/Personalization shared memory", "latency_ms": 10, "status": "ok"},
            {"service": "Azure Redis Cache", "operation": "get", "detail": "Retrieved channel conversion rates and cost-per-touch metrics", "latency_ms": 3, "status": "ok"},
            {"service": "Azure OpenAI GPT-4o", "operation": "chat_completions", "detail": f"Generated campaign content and A/B test variants for {len(channels)} channels", "latency_ms": 780, "status": "ok", "tokens": {"prompt": 3200, "completion": 640}, "model": "gpt-4o", "system_prompt": "You are a marketing agent. Generate campaign plan with budget allocation and A/B test design."},
            {"service": "Azure OpenAI GPT-4o", "operation": "chat_completions", "detail": "ROI prediction: estimated conversion and incremental revenue per channel", "latency_ms": 420, "status": "ok", "tokens": {"prompt": 1600, "completion": 320}, "model": "gpt-4o"},
            {"service": "Azure Cosmos DB", "operation": "write", "detail": "Wrote campaign_plan + ab_test to shared_memory + audit_log", "latency_ms": 11, "status": "ok"},
        ]

    def _compliance_trace(d):
        flags = d["decision"].get("flags", [])
        return [
            {"service": "Azure Cosmos DB", "operation": "query", "detail": "Read consent_registry and all agent decisions from shared_memory", "latency_ms": 18, "status": "ok"},
            {"service": "Azure Cosmos DB", "operation": "query", "detail": "Read customer consent status for PIPL/PDPA/APPI compliance check", "latency_ms": 12, "status": "ok"},
            {"service": "Policy Engine", "operation": "evaluate", "detail": f"Evaluated {len(flags)} compliance flags against regional framework", "latency_ms": 8, "status": "ok"},
            {"service": "Azure Cosmos DB", "operation": "write", "detail": "Wrote compliance_decision + audit_trail to governance_container", "latency_ms": 14, "status": "ok"},
        ]

    trace_map = {
        "Inventory Agent": _inv_trace,
        "Pricing Agent": _pricing_trace,
        "Customer Understanding Agent": _customer_trace,
        "Personalization Agent": _personalization_trace,
        "Marketing Agent": _marketing_trace,
        "Compliance Agent": _compliance_trace,
    }

    for idx, d in enumerate(result["decision_loop"], start=1):
        agent = d["agent"]
        svc_calls = trace_map.get(agent, lambda d: [])(d)
        total_svc_ms = sum(c.get("latency_ms", 0) for c in svc_calls)
        total_tokens = sum(c.get("tokens", {}).get("prompt", 0) + c.get("tokens", {}).get("completion", 0) for c in svc_calls)
        trace.append({
            "step": idx,
            "agent": agent,
            "status": "COMPLETED" if not d.get("human_approval_required") else "WAITING_FOR_APPROVAL",
            "reads": [c["detail"].split(". ")[0] for c in svc_calls if c["operation"] in ("read", "query", "get", "call")],
            "writes": [c["detail"].split(". ")[0] for c in svc_calls if c["operation"] in ("write",)],
            "azure_service_calls": svc_calls,
            "total_azure_latency_ms": total_svc_ms,
            "total_tokens": total_tokens,
            "confidence": d["confidence"],
            "evidence_count": len(d.get("evidence", [])),
            "handoff_to": d["decision"].get("handoff_to"),
            "data_packet": {
                "input_summary": d["input_summary"],
                "decision_keys": list(d["decision"].keys()),
                "business_impact": d.get("business_impact", {}),
            },
        })
    launch = build_fashion_launch_story(result)
    views = 28600
    extra = [
        {
            "agent": "Trend Insight Agent",
            "status": "COMPLETED",
            "confidence": 0.91,
            "calls": [
                {"service": "Azure Event Hubs", "operation": "read", "detail": "Consumed search/comment/weather/POS signals for launch trigger", "latency_ms": 14, "status": "ok"},
                {"service": "Microsoft Fabric OneLake", "operation": "query", "detail": "Joined trend reports, CTR history, sales and inventory lakehouse tables", "latency_ms": 96, "status": "ok"},
                {"service": "Azure OpenAI GPT-4o", "operation": "chat_completions", "detail": "Summarized opportunity: kids anti-sweat + commuter cooling demand", "latency_ms": 610, "status": "ok", "tokens": {"prompt": 2200, "completion": 430}, "model": "gpt-4o"},
            ],
            "decision_keys": ["trend_signal", "hero_product", "launch_opportunity"],
            "impact": {"cycle_stage": "trend_to_planning", "parallelized": True},
        },
        {
            "agent": "Product Planning Agent",
            "status": "COMPLETED",
            "confidence": 0.88,
            "calls": [
                {"service": "Azure AI Search", "operation": "vector_search", "detail": "Retrieved product catalog, material knowledge and brand guidelines", "latency_ms": 72, "status": "ok", "index": "retail-iq-product-brand"},
                {"service": "Azure OpenAI GPT-4o", "operation": "chat_completions", "detail": "Generated SKU planning brief and consumer pain point hypotheses", "latency_ms": 690, "status": "ok", "tokens": {"prompt": 2500, "completion": 520}, "model": "gpt-4o"},
                {"service": "Azure Cosmos DB", "operation": "write", "detail": "Wrote planning brief to Retail IQ launch memory", "latency_ms": 13, "status": "ok"},
            ],
            "decision_keys": ["planning_brief", "target_audience", "product_claims"],
            "impact": {"cycle_stage": "planning", "hero_sku": launch["hero_sku"]},
        },
        {
            "agent": "Visual Intelligence Agent",
            "status": "COMPLETED",
            "confidence": 0.9,
            "calls": [
                {"service": "Azure Blob Storage", "operation": "read", "detail": "Loaded historical model photos and product packshots", "latency_ms": 35, "status": "ok"},
                {"service": "Azure OpenAI Image Generation", "operation": "invoke", "detail": "Generated A/B/C model and scenario image variants in minutes", "latency_ms": 980, "status": "ok", "model": "gpt-image", "input": {"variants": 3}, "output_summary": "3 visual variants generated"},
                {"service": "Azure Cosmos DB", "operation": "write", "detail": "Stored visual prompts, assets and lineage for governance", "latency_ms": 18, "status": "ok"},
            ],
            "decision_keys": ["visual_variants", "asset_lineage", "sku_coverage"],
            "impact": {"baseline_photo_days": 60, "ai_generation_minutes": 6},
        },
        {
            "agent": "CTR Testing Agent",
            "status": "COMPLETED",
            "confidence": 0.86,
            "calls": [
                {"service": "Azure ML Endpoint", "operation": "invoke", "detail": "Predicted CTR for AIGC variants using historical campaign features", "latency_ms": 164, "status": "ok", "model": "ctr-prediction-v1", "input": {"variants": 3, "views_24h": views}, "output": {"winner_ctr": launch["visual_lab"]["ctr_winner_pct"]}},
                {"service": "Microsoft Fabric Real-Time Analytics", "operation": "query", "detail": "Compared predicted CTR against historical baseline and SKU cohort", "latency_ms": 88, "status": "ok"},
                {"service": "Azure Cosmos DB", "operation": "write", "detail": "Wrote winning creative and test result to campaign memory", "latency_ms": 12, "status": "ok"},
            ],
            "decision_keys": ["ctr_baseline", "winner_variant", "test_result"],
            "impact": {"ctr_from": launch["visual_lab"]["ctr_baseline_pct"], "ctr_to": launch["visual_lab"]["ctr_winner_pct"]},
        },
        {
            "agent": "Live Commerce Agent",
            "status": "WAITING_FOR_APPROVAL",
            "confidence": 0.84,
            "calls": [
                {"service": "Azure AI Search", "operation": "vector_search", "detail": "Retrieved product FAQ, sizing, washing and inventory answers for digital human script", "latency_ms": 80, "status": "ok", "index": "live-commerce-faq"},
                {"service": "Azure OpenAI GPT-4o", "operation": "chat_completions", "detail": "Generated digital human script for unmanned midnight slots", "latency_ms": 720, "status": "ok", "tokens": {"prompt": 2100, "completion": 780}, "model": "gpt-4o"},
                {"service": "Logic Apps", "operation": "write", "detail": "Prepared live schedule + approval card for business owner", "latency_ms": 120, "status": "ok"},
            ],
            "decision_keys": ["digital_human_script", "faq_updates", "live_schedule"],
            "impact": {"empty_slots_recovered": launch["live_commerce"]["empty_slots_recovered"], "expected_incremental_gmv_cny": launch["live_commerce"]["expected_incremental_gmv_cny"]},
        },
        {
            "agent": "Finance ROI Agent",
            "status": "WAITING_FOR_APPROVAL",
            "confidence": 0.83,
            "calls": [
                {"service": "Microsoft Fabric OneLake", "operation": "query", "detail": "Read cost, CTR, campaign, sample and payback tables", "latency_ms": 102, "status": "ok"},
                {"service": "Azure ML Endpoint", "operation": "invoke", "detail": "Simulated incremental revenue and cost saving assumptions", "latency_ms": 176, "status": "ok", "model": "roi-simulation-v1"},
                {"service": "Power BI", "operation": "write", "detail": "Published launch cycle and ROI simulation dashboard snapshot", "latency_ms": 140, "status": "ok"},
            ],
            "decision_keys": ["cycle_compression", "cost_saving", "roi_assumption"],
            "impact": launch["launch_kpis"],
        },
    ]
    for item in extra:
        idx = len(trace) + 1
        calls = item["calls"]
        trace.append({
            "step": idx,
            "agent": item["agent"],
            "status": item["status"],
            "reads": [c["detail"] for c in calls if c["operation"] in ("read", "query", "get", "vector_search")],
            "writes": [c["detail"] for c in calls if c["operation"] in ("write",)],
            "azure_service_calls": calls,
            "total_azure_latency_ms": sum(c.get("latency_ms", 0) for c in calls),
            "total_tokens": sum(c.get("tokens", {}).get("prompt", 0) + c.get("tokens", {}).get("completion", 0) for c in calls),
            "confidence": item["confidence"],
            "evidence_count": 3,
            "handoff_to": "Compliance Agent" if item["status"] == "WAITING_FOR_APPROVAL" else "next launch workstream",
            "data_packet": {"input_summary": launch["business_trigger"], "decision_keys": item["decision_keys"], "business_impact": item["impact"]},
        })
    return trace


def build_shared_memory(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    inventory = next(d for d in result["decision_loop"] if d["agent"] == "Inventory Agent")
    pricing = next(d for d in result["decision_loop"] if d["agent"] == "Pricing Agent")
    customer = next(d for d in result["decision_loop"] if d["agent"] == "Customer Understanding Agent")
    return [
        {"memory_type": "shared_operational_memory", "writer": "Inventory Agent", "reader": "Pricing Agent", "key": "stockout_guardrail", "value": f"{sum(1 for p in inventory['decision']['products'] if p['stock_risk']=='high')} high-risk SKUs; block broad discounting"},
        {"memory_type": "episodic_case_memory", "writer": "Pricing Agent", "reader": "Marketing Agent", "key": "promotion_guardrail", "value": pricing["decision"]["strategy"]},
        {"memory_type": "customer_memory", "writer": "Customer Understanding Agent", "reader": "Personalization Agent", "key": "target_segment", "value": customer["decision"].get("primary_segment")},
    ]


def build_customer_journey(result: Dict[str, Any], work_orders: List[Dict[str, Any]], kpi: Dict[str, Any]) -> Dict[str, Any]:
    """Build the customer journey from the current run state, not static demo copy."""
    loop = result.get("decision_loop", [])
    customer_decision = next((d.get("decision", {}) for d in loop if d.get("agent") == "Customer Understanding Agent"), {})
    personalization_decision = next((d.get("decision", {}) for d in loop if d.get("agent") == "Personalization Agent"), {})
    pricing_decision = next((d.get("decision", {}) for d in loop if d.get("agent") == "Pricing Agent"), {})
    marketing_decision = next((d.get("decision", {}) for d in loop if d.get("agent") == "Marketing Agent"), {})

    customers = customer_decision.get("target_customers") or result.get("customers") or []
    customer = customers[0] if customers else {}
    customer_id = customer.get("customer_id", "CUSTOMER-001")
    segment = customer.get("segment") or customer_decision.get("primary_segment") or "high_intent_customer"
    preferred_channel = customer.get("preferred_channel") or "app_push"
    intent_score = customer.get("intent_score", 0.7)
    consent = customer.get("marketing_consent", True)

    recommendation_blocks = personalization_decision.get("personalized_recommendations") or personalization_decision.get("recommendations") or []
    rec_block = next((r for r in recommendation_blocks if r.get("customer_id") == customer_id), recommendation_blocks[0] if recommendation_blocks else {})
    recommendations = rec_block.get("recommendations", [])
    hero_rec = recommendations[0] if recommendations else {}
    hero_name = hero_rec.get("name") or result.get("fashion_launch", {}).get("hero_product") or "recommended product"
    hero_price = hero_rec.get("recommended_price")

    pricing_actions = pricing_decision.get("pricing_actions") or []
    hero_price_action = next((a for a in pricing_actions if a.get("sku_id") == hero_rec.get("sku_id")), pricing_actions[0] if pricing_actions else {})
    channel_plan = marketing_decision.get("channel_plan") or {}
    campaign_order = next((o for o in work_orders if o.get("type") == "CAMPAIGN" and preferred_channel in o.get("title", "") + o.get("title_en", "") + o.get("title_zh", "")), None)
    any_campaign_completed = any(o.get("type") == "CAMPAIGN" and o.get("status") == "COMPLETED" for o in work_orders)
    any_replenishment_completed = any(o.get("type") == "REPLENISHMENT" and o.get("status") == "COMPLETED" for o in work_orders)

    progress = kpi.get("current_execution_progress", {})
    execution_ratio = progress.get("execution_ratio", 0)
    conversion = any_campaign_completed and any_replenishment_completed
    if not conversion and execution_ratio >= 0.95:
        conversion = True

    personalization_applied = []
    if recommendations:
        personalization_applied.append(f"Product recommendations ({len(recommendations)} SKUs)")
    if hero_price_action:
        personalization_applied.append(f"Dynamic pricing ({hero_price_action.get('strategy', 'guardrailed price')})")
    if preferred_channel:
        personalization_applied.append(f"Channel preference ({preferred_channel})")
    if channel_plan:
        personalization_applied.append("Timing / channel budget optimization")

    touchpoints = [
        {
            "channel": "Customer 360",
            "action": f"Intent detected: {segment}; score {intent_score}",
            "time": "Day 1",
            "agent": "Customer Understanding Agent",
        },
        {
            "channel": preferred_channel,
            "action": f"Next-best offer: {hero_name}" + (f" at ¥{hero_price}" if hero_price else ""),
            "time": "Day 2",
            "agent": "Personalization Agent",
        },
        {
            "channel": "Pricing Guardrail",
            "action": hero_price_action.get("reason") or "Validated recommended price against margin and inventory risk",
            "time": "Day 2",
            "agent": "Pricing Agent",
        },
        {
            "channel": preferred_channel,
            "action": f"Campaign work order {campaign_order.get('id') if campaign_order else 'planned'}: {(campaign_order or {}).get('status', 'PLANNED')}",
            "time": "Day 3",
            "agent": "Marketing Agent",
        },
        {
            "channel": "Store / E-commerce",
            "action": "Conversion recorded" if conversion else f"Waiting for execution; {sum(1 for o in work_orders if o.get('status') == 'COMPLETED')}/{len(work_orders)} work orders completed",
            "time": "Day 5",
            "agent": "BI Feedback Loop",
        },
    ]

    return {
        "customer_id": customer_id,
        "segments": [segment, customer.get("purchase_intent", "high"), "consented" if consent else "no marketing consent"],
        "touchpoints": touchpoints,
        "context_preserved": bool(customer_id and recommendations and consent),
        "personalization_applied": personalization_applied,
        "outcome": {
            "conversion": conversion,
            "ltv_change": f"+{progress.get('ltv_growth', 0)}%",
            "satisfaction_score": progress.get("customer_satisfaction"),
            "execution_ratio": execution_ratio,
            "source": "current_execution_progress + work_order_status",
        },
    }


def build_kpi_simulation(result: Dict[str, Any], work_orders: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(work_orders) or 1
    completed = sum(1 for o in work_orders if o.get("status") == "COMPLETED")
    ready = sum(1 for o in work_orders if o.get("status") == "READY")
    approved_progress = (completed + ready * 0.35) / total
    execution_ratio = round(min(1.0, approved_progress), 2)
    same_store_sales_growth = round(42 * execution_ratio)
    inventory_waste_rate = round(12.5 - (12.5 - 5.8) * execution_ratio, 1)
    customer_satisfaction = round(72 + (87 - 72) * execution_ratio)
    ltv_growth = round(63 * execution_ratio)
    return {
        "baseline": {
            "same_store_sales_growth": 0,
            "inventory_waste_rate": 12.5,
            "customer_satisfaction": 72,
            "ltv_growth": 0
        },
        "projected_after_full_execution": {
            "same_store_sales_growth": 42,
            "inventory_waste_rate": 5.8,
            "customer_satisfaction": 87,
            "ltv_growth": 63
        },
        "current_execution_progress": {
            "execution_ratio": execution_ratio,
            "completed_work_orders": completed,
            "ready_work_orders": ready,
            "total_work_orders": len(work_orders),
            "same_store_sales_growth": same_store_sales_growth,
            "inventory_waste_rate": inventory_waste_rate,
            "customer_satisfaction": customer_satisfaction,
            "ltv_growth": ltv_growth
        },
        "success_criteria": {
            "same_store_sales_target": 40,
            "inventory_waste_reduction_target": 50,
            "customer_satisfaction_target": 85,
            "ltv_growth_target": 60
        },
        "positioning": "Agent-driven personalization + demand forecasting + cross-channel orchestration."
    }



AGENT_REGISTRY = {
    "Inventory Agent": {
        "id": "agent-inventory-001",
        "domain": "Inventory Intelligence",
        "capabilities": ["demand_forecast", "stockout_risk", "replenishment_optimization", "regional_stock_balance"],
        "tools": ["POS_query", "RFID_reader", "warehouse_API", "weather_API", "demand_model"],
        "sla_ms": 2000,
        "permissions": ["read_inventory", "write_replenishment_order"],
        "risk_level": "medium",
        "requires_approval_above": 500,
    },
    "Pricing Agent": {
        "id": "agent-pricing-002",
        "domain": "Dynamic Pricing",
        "capabilities": ["price_optimization", "margin_guardrail", "competitor_monitoring", "off_season_clearance"],
        "tools": ["competitor_scraper", "promo_validator", "margin_calculator", "elasticity_model"],
        "sla_ms": 1500,
        "permissions": ["read_pricing", "write_price_proposal"],
        "risk_level": "high",
        "requires_approval_above": 0.05,
    },
    "Customer Understanding Agent": {
        "id": "agent-customer-003",
        "domain": "Customer Intelligence",
        "capabilities": ["customer_segmentation", "intent_prediction", "clv_scoring", "consent_management"],
        "tools": ["CRM_query", "behavior_analyzer", "persona_generator", "consent_checker"],
        "sla_ms": 1000,
        "permissions": ["read_customer_profile", "read_behavior", "read_consent"],
        "risk_level": "high",
        "requires_approval_above": None,
    },
    "Personalization Agent": {
        "id": "agent-personalization-004",
        "domain": "Personalization",
        "capabilities": ["next_best_action", "recommendation", "channel_selection", "session_memory"],
        "tools": ["vector_search", "recommendation_engine", "session_tracker", "ab_test_manager"],
        "sla_ms": 200,
        "permissions": ["read_customer_profile", "read_inventory", "read_pricing", "write_recommendation"],
        "risk_level": "medium",
        "requires_approval_above": None,
    },
    "Marketing Agent": {
        "id": "agent-marketing-005",
        "domain": "Marketing Automation",
        "capabilities": ["campaign_generation", "budget_allocation", "ab_testing", "channel_orchestration"],
        "tools": ["campaign_builder", "budget_optimizer", "channel_executor", "roi_predictor"],
        "sla_ms": 3000,
        "permissions": ["read_customer_segment", "write_campaign", "write_budget_allocation"],
        "risk_level": "high",
        "requires_approval_above": 1000,
    },
    "Trend Insight Agent": {
        "id": "agent-trend-007",
        "domain": "Fashion Trend Intelligence",
        "capabilities": ["trend_report_summarization", "consumer_review_mining", "weather_search_pos_signal_fusion"],
        "tools": ["trend_report_reader", "social_listener", "fabric_query", "weather_API"],
        "sla_ms": 1800,
        "permissions": ["read_trend_reports", "read_social_signals", "write_launch_opportunity"],
        "risk_level": "medium",
        "requires_approval_above": None,
    },
    "Product Planning Agent": {
        "id": "agent-planning-008",
        "domain": "Product Planning",
        "capabilities": ["assortment_planning", "consumer_pain_point_mapping", "claim_generation", "launch_brief"],
        "tools": ["product_catalog", "brand_guideline_search", "planning_brief_writer"],
        "sla_ms": 2200,
        "permissions": ["read_product_catalog", "write_planning_brief"],
        "risk_level": "medium",
        "requires_approval_above": None,
    },
    "Visual Intelligence Agent": {
        "id": "agent-visual-009",
        "domain": "AIGC Visual Lab",
        "capabilities": ["image_variant_generation", "model_photo_extension", "scene_prompt_optimization", "asset_lineage"],
        "tools": ["image_generation", "blob_storage", "brand_safety_checker"],
        "sla_ms": 4000,
        "permissions": ["read_assets", "write_visual_variants"],
        "risk_level": "high",
        "requires_approval_above": None,
    },
    "CTR Testing Agent": {
        "id": "agent-ctr-010",
        "domain": "Creative Experimentation",
        "capabilities": ["ctr_prediction", "ab_test_selection", "creative_learning_loop"],
        "tools": ["ctr_model", "experiment_tracker", "fabric_metrics"],
        "sla_ms": 1200,
        "permissions": ["read_campaign_metrics", "write_test_result"],
        "risk_level": "medium",
        "requires_approval_above": None,
    },
    "Live Commerce Agent": {
        "id": "agent-live-011",
        "domain": "Digital Human Live Commerce",
        "capabilities": ["digital_human_script", "faq_grounding", "unmanned_slot_recovery", "bullet_comment_learning"],
        "tools": ["faq_search", "script_generator", "live_scheduler", "logic_apps"],
        "sla_ms": 3000,
        "permissions": ["read_faq", "write_live_schedule", "write_script"],
        "risk_level": "high",
        "requires_approval_above": 1,
    },
    "Finance ROI Agent": {
        "id": "agent-finance-012",
        "domain": "Finance ROI Simulation",
        "capabilities": ["cost_saving_estimation", "incremental_revenue_simulation", "payback_dashboard", "roi_guardrail"],
        "tools": ["fabric_finance", "roi_model", "power_bi"],
        "sla_ms": 1800,
        "permissions": ["read_finance_metrics", "write_roi_review"],
        "risk_level": "high",
        "requires_approval_above": 0,
    },
    "Orchestrator Agent": {
        "id": "agent-orchestrator-000",
        "domain": "Multi-Agent Orchestration",
        "capabilities": ["task_decomposition", "agent_coordination", "priority_setting", "conflict_resolution", "result_aggregation", "progress_monitoring"],
        "tools": ["Semantic_Kernel_Planner", "Durable_Functions", "Agent_Registry", "Shared_Memory"],
        "sla_ms": 500,
        "permissions": ["read_all_inputs", "write_all_tasks", "coordinate_all_agents", "escalate_to_human"],
        "risk_level": "critical",
        "requires_approval_above": None,
    },
    "Compliance Agent": {
        "id": "agent-compliance-006",
        "domain": "Governance & Compliance",
        "capabilities": ["pipl_check", "pdpa_check", "dpdp_check", "data_residency", "consent_validation", "audit_trail"],
        "tools": ["policy_engine", "data_classifier", "consent_registry", "audit_logger"],
        "sla_ms": 100,
        "permissions": ["read_all_decisions", "block_execution", "flag_risk"],
        "risk_level": "critical",
        "requires_approval_above": None,
    },
}

REGIONAL_CONFIG = {
    "china": {
        "region_name": "China Mainland",
        "azure_region": "Azure China (21Vianet)",
        "compliance_framework": "PIPL",
        "privacy_regulation": "PIPL",
        "data_residency": "Must stay in China",
        "languages": ["zh-CN"],
        "language": "zh-CN",
        "touchpoints": ["WeChat Mini Program", "Tmall", "JD", "Offline POS"],
        "payment_methods": ["WeChat Pay", "Alipay"],
        "currency": "CNY",
        "channels": ["app", "wechat_mini", "tmall", "jd", "store_pos"],
        "demo_focus": "Private-domain membership + marketplace launch",
        "launch_angle": "High-temperature commute and kids sports anti-sweat demand",
        "primary_channel": "WeChat Mini Program + Tmall/JD",
        "business_risk": "PIPL consent, China data residency, coupon over-promotion causing stockout",
        "agent_overrides": {"Compliance Agent": {"strict_mode": True, "pii_masking": "full"}},
    },
    "japan": {
        "region_name": "Japan",
        "azure_region": "Azure Japan East",
        "compliance_framework": "APPI",
        "privacy_regulation": "APPI",
        "data_residency": "Preferred Japan, cross-border allowed with consent",
        "languages": ["ja"],
        "language": "ja-JP",
        "touchpoints": ["LINE", "Rakuten", "Offline POS"],
        "payment_methods": ["LINE Pay", "PayPay"],
        "currency": "JPY",
        "channels": ["app", "line", "rakuten", "store_pos"],
        "demo_focus": "Store-first loyal member experience",
        "launch_angle": "Rainy-season breathable commute wear and convenience-store payment journey",
        "primary_channel": "LINE + Rakuten + store POS",
        "business_risk": "APPI consent management, localized Japanese copy, store pickup availability",
        "agent_overrides": {"Compliance Agent": {"strict_mode": True, "pii_masking": "partial"}},
    },
    "southeast_asia": {
        "region_name": "Southeast Asia",
        "azure_region": "Azure Southeast Asia (Singapore)",
        "compliance_framework": "PDPA (SG) / PDPA (TH) / DPDP (ID)",
        "privacy_regulation": "PDPA",
        "data_residency": "Country-level for Indonesia",
        "languages": ["en", "th", "id", "vi", "ms"],
        "language": "en-ID",
        "touchpoints": ["WhatsApp", "Shopee", "Lazada", "Offline POS"],
        "payment_methods": ["GrabPay", "OVO", "GoPay"],
        "currency": "Multi (SGD/THB/IDR/VND/MYR)",
        "channels": ["app", "whatsapp", "line", "lazada", "shopee", "store_pos"],
        "demo_focus": "Mobile-first marketplace and multilingual growth",
        "launch_angle": "Tropical heat, Ramadan/holiday travel, multilingual content variants",
        "primary_channel": "Shopee/Lazada + WhatsApp/LINE",
        "business_risk": "PDPA variants, Indonesia localization, fragmented wallets and logistics SLA",
        "agent_overrides": {"Compliance Agent": {"strict_mode": True, "pii_masking": "full", "indonesia_localization": True}},
    },
    "korea": {
        "region_name": "South Korea",
        "azure_region": "Azure Korea Central",
        "compliance_framework": "PIPA",
        "privacy_regulation": "PIPA",
        "data_residency": "Must stay in Korea",
        "languages": ["ko"],
        "language": "ko-KR",
        "touchpoints": ["Kakao", "Naver", "Offline POS"],
        "payment_methods": ["Kakao Pay", "Naver Pay"],
        "currency": "KRW",
        "channels": ["app", "kakao", "naver", "store_pos"],
        "demo_focus": "Social commerce and fast trend response",
        "launch_angle": "Kakao/Naver campaign with rapid trend testing and strict data residency",
        "primary_channel": "Kakao + Naver + app",
        "business_risk": "PIPA data residency, influencer trend volatility, flash campaign inventory risk",
        "agent_overrides": {"Compliance Agent": {"strict_mode": True, "pii_masking": "full"}},
    },
}

DATA_SOURCES = [
    {"source": "POS System", "type": "batch+stream", "event_hub": "eh-pos-transactions", "features": ["daily_sales", "basket_size", "payment_method"]},
    {"source": "Mobile App / Mini Program", "type": "stream", "event_hub": "eh-app-behavior", "features": ["page_views", "search_queries", "cart_adds", "session_duration"]},
    {"source": "RFID / IoT", "type": "stream", "event_hub": "eh-rfid-tryons", "features": ["try_ons", "shelf_movement", "fitting_room_count"]},
    {"source": "Weather API", "type": "stream", "event_hub": "eh-weather", "features": ["temperature", "forecast", "precipitation"]},
    {"source": "CRM / Membership", "type": "batch", "event_hub": "eh-crm-updates", "features": ["tier", "lifetime_value", "consent_status"]},
    {"source": "Competitor Monitoring", "type": "batch", "event_hub": "eh-competitor-prices", "features": ["competitor_prices", "promo_alerts"]},
    {"source": "ERP / Warehouse", "type": "batch", "event_hub": "eh-inventory", "features": ["stock_levels", "warehouse_availability", "lead_times"]},
    {"source": "Social Media", "type": "stream", "event_hub": "eh-social", "features": ["trending_products", "sentiment", "influencer_mentions"]},
]

FEATURE_STORE = [
    {"feature_group": "customer_features", "features": ["clv_score", "price_sensitivity", "preferred_channel", "intent_score", "churn_risk"], "freshness": "real-time", "store": "Cosmos DB + Redis"},
    {"feature_group": "product_features", "features": ["demand_trend", "stock_risk_score", "margin_health", "competitor_gap", "seasonality_index"], "freshness": "near-real-time", "store": "Fabric OneLake + Redis"},
    {"feature_group": "session_features", "features": ["current_cart", "browsing_pattern", "device_type", "location_context"], "freshness": "real-time", "store": "Redis"},
    {"feature_group": "operational_features", "features": ["store_traffic", "staff_capacity", "fulfillment_sla", "return_rate"], "freshness": "hourly", "store": "Fabric OneLake"},
]


def build_agent_registry() -> Dict[str, Any]:
    return AGENT_REGISTRY

def build_orchestrator_trace(result: Dict[str, Any]) -> Dict[str, Any]:
    """Build Orchestrator (Agent Boss) trace showing task decomposition and coordination."""
    loop = result["decision_loop"]
    event = result.get("trigger", {})
    season = result.get("season", "winter")
    products = result.get("products", [])

    # Count decisions
    agents_called = [d["agent"] for d in loop if d["agent"] != "Orchestrator Agent"]
    total_azure_latency = sum(d.get("total_azure_latency_ms", 0) for d in loop)
    total_tokens = sum(d.get("total_tokens", 0) for d in loop)

    # Build sub-tasks from the event
    sub_tasks = [
        {"task": "Analyze seasonal demand spike", "assigned_to": "Inventory Agent", "status": "COMPLETED", "result": f"Identified {sum(1 for p in loop[0]['decision'].get('products', []) if p.get('stock_risk')=='high')} high-risk SKUs"},
        {"task": "Determine pricing strategy under inventory constraints", "assigned_to": "Pricing Agent", "status": "COMPLETED", "result": f"Strategy: {loop[1]['decision'].get('strategy', 'guardrailed_dynamic_pricing')}"},
        {"task": "Identify high-intent customer segments", "assigned_to": "Customer Understanding Agent", "status": "COMPLETED", "result": f"Found {len(loop[2]['decision'].get('target_customers', []))} target customers"},
        {"task": "Generate personalized recommendations", "assigned_to": "Personalization Agent", "status": "COMPLETED", "result": f"{len(loop[3]['decision'].get('personalized_recommendations', []))} customer segments personalized"},
        {"task": "Create campaign with budget allocation", "assigned_to": "Marketing Agent", "status": "COMPLETED", "result": f"Campaign: {loop[4]['decision'].get('campaign_name', 'Seasonal Campaign')}"},
        {"task": "Compliance gate: validate all decisions", "assigned_to": "Compliance Agent", "status": "COMPLETED" if not any(d.get("human_approval_required") for d in loop) else "WAITING_FOR_APPROVAL", "result": f"Status: {loop[5]['decision'].get('compliance_status', 'PASS')}"},
    ]

    # Build task decomposition
    task_decomposition = {
        "original_event": f"{event.get('city', 'Shanghai')} {event.get('type', 'seasonal_event')}: temperature dropped {event.get('temperature_drop_c', 0)}°C",
        "business_intent": f"Respond to {season} seasonal demand and optimize retail operations",
        "sub_tasks": sub_tasks,
        "dependencies": [
            "Inventory Agent → Pricing Agent (stock risk constrains pricing)",
            "Customer Understanding Agent → Personalization Agent (segments drive recommendations)",
            "Pricing Agent + Personalization Agent → Marketing Agent (price + recs drive campaign)",
            "All Agents → Compliance Agent (all decisions pass compliance gate)",
        ],
        "parallel_groups": [
            ["Inventory Agent", "Customer Understanding Agent"],
            ["Pricing Agent", "Personalization Agent"],
            ["Marketing Agent"],
            ["Compliance Agent"],
        ],
    }

    return {
        "agent": "Orchestrator Agent",
        "domain": "Multi-Agent Orchestration",
        "status": "COMPLETED",
        "business_event": f"{event.get('city', 'Shanghai')} {event.get('type', 'seasonal_event')}",
        "season": season,
        "agents_called": agents_called,
        "total_agents": len(agents_called),
        "total_azure_latency_ms": total_azure_latency,
        "total_tokens": total_tokens,
        "task_decomposition": task_decomposition,
        "decision_summary": {
            "replenishment_units": loop[0]["decision"].get("total_replenishment_units", 0),
            "pricing_strategy": loop[1]["decision"].get("strategy", "guardrailed_dynamic_pricing"),
            "customer_segments": len(loop[2]["decision"].get("target_customers", [])),
            "recommendations": len(loop[3]["decision"].get("personalized_recommendations", [])),
            "campaign_name": loop[4]["decision"].get("campaign_name", "Seasonal Campaign"),
            "compliance_status": loop[5]["decision"].get("compliance_status", "PASS"),
        },
        "orchestrator_tools": ["Semantic Kernel Planner", "Durable Functions", "Agent Registry", "Shared Memory (Cosmos DB)"],
        "human_escalation_needed": any(d.get("human_approval_required") for d in loop),
        "evidence": [
            "Orchestrator decomposed the business event into 6 sub-tasks across 5 specialist agents.",
            "Task dependencies respected: Inventory→Pricing, Customer→Personalization, all→Compliance.",
            "Parallel execution: Inventory and Customer Understanding ran concurrently.",
            "Result aggregated and handed to Compliance Agent for final gate.",
        ],
        "confidence": 0.92,
    }


def build_compliance_decision(state: Dict[str, Any], decisions: List[Dict[str, Any]], region: str) -> Dict[str, Any]:
    region_cfg = REGIONAL_CONFIG.get(region, REGIONAL_CONFIG["china"])
    framework = region_cfg["compliance_framework"]
    flags = []
    for d in decisions:
        if d["agent"] == "Customer Understanding Agent":
            target_customers = d["decision"].get("target_customers", [])
            for c in target_customers:
                if not c.get("marketing_consent") and c.get("preferred_channel") in ["app_push", "wechat_mini"]:
                    flags.append({"agent": d["agent"], "issue": f"Customer {c['customer_id']} missing marketing consent for {c['preferred_channel']}", "severity": "high"})
        if d["agent"] == "Marketing Agent":
            if d.get("human_approval_required"):
                flags.append({"agent": d["agent"], "issue": "Campaign requires human approval before execution", "severity": "medium"})
    return {
        "agent": "Compliance Agent",
        "method_sources": ["Responsible AI", "PIPL/PDPA/DPDP data residency"],
        "input_summary": {
            "region": region,
            "compliance_framework": framework,
            "data_residency": region_cfg["data_residency"],
            "decisions_reviewed": len(decisions),
        },
        "decision": {
            "compliance_status": "PASS_WITH_FLAGS" if flags else "PASS",
            "framework": framework,
            "flags": flags,
            "data_residency_enforced": True,
            "pii_masking_level": region_cfg["agent_overrides"].get("Compliance Agent", {}).get("pii_masking", "standard"),
            "audit_required": True,
        },
        "evidence": [
            f"Compliance framework: {framework}",
            f"Data residency: {region_cfg['data_residency']}",
            f"PII masking: {region_cfg['agent_overrides'].get('Compliance Agent', {}).get('pii_masking', 'standard')}",
            f"Reviewed {len(decisions)} agent decisions for policy violations",
        ],
        "confidence": 0.95,
        "human_approval_required": len([f for f in flags if f["severity"] == "high"]) > 0,
        "business_impact": {"risk_reduced": "regulatory penalty and data breach"},
    }


def build_event_pipeline() -> List[Dict[str, Any]]:
    return DATA_SOURCES


def build_feature_store() -> List[Dict[str, Any]]:
    return FEATURE_STORE


def build_customer_360(customers: List[Dict[str, Any]], region: str) -> List[Dict[str, Any]]:
    region_cfg = REGIONAL_CONFIG.get(region, REGIONAL_CONFIG["china"])
    profiles = []
    for c in customers:
        profiles.append({
            "customer_id": c["customer_id"],
            "segment": c["segment"],
            "region": region,
            "language": c.get("language", region_cfg["languages"][0]),
            "clv_score": c.get("lifetime_value", 0),
            "membership_tier": c.get("membership_tier", "standard"),
            "price_sensitivity": c.get("price_sensitivity", "medium"),
            "preferred_channel": c.get("preferred_channel", "app"),
            "consent": c.get("consent", {}),
            "compliance_status": "consent_valid" if c.get("consent", {}).get("personalization") else "consent_missing",
            "preferred_payment": region_cfg["payment_methods"][0],
            "360_profile": {
                "recent_views": c.get("recent_views", []),
                "cart_items": c.get("cart_items", []),
                "purchase_history": c.get("purchase_history", []),
                "lifetime_value": c.get("lifetime_value", 0),
                "city": c.get("city", ""),
                "membership_tier": c.get("membership_tier", "standard"),
            },
        })
    return profiles


def build_platform_architecture(region: str) -> Dict[str, Any]:
    region_cfg = REGIONAL_CONFIG.get(region, REGIONAL_CONFIG["china"])
    return {
        "data_layer": {
            "ingestion": ["Azure Event Hubs", "Azure Data Factory", "Azure IoT Hub"],
            "storage": ["Microsoft Fabric OneLake", "ADLS Gen2", "Delta Lake"],
            "processing": ["Fabric Spark", "Azure Databricks", "Stream Analytics"],
            "feature_store": ["Azure ML Feature Store", "Redis Cache"],
        },
        "ai_layer": {
            "llm": ["Azure OpenAI GPT-4.1", "GPT-4o", "Embeddings"],
            "search": ["Azure AI Search (RAG)"],
            "ml": ["Azure ML (Prophet, DeepAR, RL)"],
            "agent_framework": ["Semantic Kernel", "AutoGen", "Durable Functions"],
        },
        "agent_layer": {
            "registry": "Cosmos DB (Agent Registry)",
            "orchestrator": "Azure AI Foundry + Semantic Kernel Planner",
            "memory": ["Cosmos DB (long-term)", "Redis (session)", "AI Search (vector)"],
            "tools": ["Azure Functions", "Logic Apps", "API Management"],
        },
        "serving_layer": {
            "api": ["Azure API Management", "Azure Front Door"],
            "compute": ["AKS", "Container Apps"],
            "cache": ["Azure Cache for Redis"],
            "cdn": ["Azure CDN"],
        },
        "governance_layer": {
            "identity": ["Microsoft Entra ID", "RBAC"],
            "security": ["Key Vault", "Private Link", "WAF"],
            "compliance": ["Purview", "Confidential Computing"],
            "monitoring": ["Application Insights", "Azure Monitor", "ML Drift Detection"],
        },
        "azure_region": region_cfg["azure_region"],
        "compliance_framework": region_cfg["compliance_framework"],
    }




def create_run(season: str, region: str = "china") -> Dict[str, Any]:
    result = RetailScenarioEngine().run_season(season)
    return create_run_from_result(result, region)


def create_custom_run(payload: Dict[str, Any], region: str = "china") -> Dict[str, Any]:
    result = RetailScenarioEngine().run_custom_launch(payload)
    return create_run_from_result(result, region)


def create_run_from_result(result: Dict[str, Any], region: str = "china") -> Dict[str, Any]:
    run_id = f"RUN-{uuid4().hex[:8].upper()}"
    customer_signals = {
        "high_intent_customers": 847,
        "churning_risk_customers": 234,
        "new_members_this_week": 156,
        "cross_channel_users": 1203,
        "top_signal": "Summer collection browse-to-cart ratio up 340%",
        "privacy_consent_rate": 0.92
    }
    result["customer_signals"] = customer_signals
    result.setdefault("trigger", {})["customer_signals"] = customer_signals
    work_orders = build_work_orders(result)
    kpi_simulation = build_kpi_simulation(result, work_orders)
    customer_journey = build_customer_journey(result, work_orders, kpi_simulation)
    result["customer_journey"] = customer_journey
    decisions_list = result["decision_loop"]
    compliance = build_compliance_decision(result, decisions_list, region)
    result["decision_loop"] = decisions_list + [compliance]
    run = {
        "run_id": run_id,
        "status": "WAITING_FOR_DECISION",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "region": region,
        "regional_config": REGIONAL_CONFIG.get(region, REGIONAL_CONFIG["china"]),
        "agent_registry": build_agent_registry(),
        "event_pipeline": build_event_pipeline(),
        "feature_store": build_feature_store(),
        "customer_360": build_customer_360(result.get("customers", []), region),
        "platform_architecture": build_platform_architecture(region),
        "fashion_launch": build_fashion_launch_story(result),
        "customer_signals": customer_signals,
        "customer_journey": customer_journey,
        "scenario": result,
        "work_orders": work_orders,
        "execution_trace": build_execution_trace(result),
        "orchestrator_trace": build_orchestrator_trace(result),
        "shared_memory": build_shared_memory(result),
        "kpi_simulation": kpi_simulation,
        "audit_log": [
            {"time": now_iso(), "actor": "System", "action": "RUN_CREATED", "detail": f"Created seasonal run for {result.get('season_label') or season} in {region}"}
        ],
    }
    RUNS[run_id] = run
    upsert_run(run)
    return run


def refresh_run_derived_state(run: Dict[str, Any]) -> None:
    """Recompute derived demo views after approvals/execution mutate work orders."""
    run["kpi_simulation"] = build_kpi_simulation(run["scenario"], run["work_orders"])
    run["customer_journey"] = build_customer_journey(run["scenario"], run["work_orders"], run["kpi_simulation"])
    run["scenario"]["customer_journey"] = run["customer_journey"]


def build_scenario(season: str, region: str = "china") -> Dict[str, Any]:
    """Backward-compatible scenario builder used by demos and smoke tests."""
    return create_run(season, region)


def get_run_or_404(run_id: str) -> Dict[str, Any]:
    if run_id in RUNS:
        return RUNS[run_id]
    persisted = read_run(run_id)
    if persisted:
        RUNS[run_id] = persisted
        return persisted
    raise HTTPException(status_code=404, detail="Run not found")


@app.get("/", response_class=HTMLResponse)
async def home():
    index = STATIC_DIR / "index.html"
    return HTMLResponse(
        content=index.read_text(encoding="utf-8"),
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/workflow", response_class=HTMLResponse)
async def workflow_page():
    index = STATIC_DIR / "index.html"
    return HTMLResponse(
        content=index.read_text(encoding="utf-8"),
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/focused", response_class=HTMLResponse)
async def focused_page():
    focused = STATIC_DIR / "focused.html"
    return HTMLResponse(
        content=focused.read_text(encoding="utf-8"),
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/api")
async def root():
    return {
        "service": "AMA Retail Agent Platform",
        "status": "running",
        "version": "2.1.0",
        "positioning": "Operational seasonal simulation with stateful approvals and work orders",
        "agents": ["Inventory Agent", "Pricing Agent", "Customer Understanding Agent", "Personalization Agent", "Marketing Agent"],
        "core_scenario": "Seasonal Retail Decision Cycle",
        "ui": "/",
        "focused_panel_ui": "/focused",
        "scenario_api": "/api/v1/season/{spring|summer|autumn|winter}",
        "operations_api": "/api/v1/runs/{run_id}/work-orders/{order_id}/{approve|complete}",
        "seasons": RetailScenarioEngine().list_seasons(),
    }




@app.post("/api/v1/agent/decide")
async def agent_decision(body: dict):
    """Real Azure OpenAI agent decision."""
    agent_name = body.get("agent", "Inventory Agent")
    context = body.get("context", "")
    task = body.get("task", "")
    result = agent_decide(agent_name, context, task)
    return {"agent": agent_name, "azure_service": "Azure OpenAI", "deployment": DEPLOYMENT, "result": result}

@app.post("/api/v1/orchestrator/decompose")
async def orchestrator_decomposition(body: dict):
    """Real Orchestrator task decomposition via GPT-4o."""
    event = body.get("event", "Summer heatwave triggered")
    season = body.get("season", "summer")
    region = body.get("region", "China Mainland")
    result = orchestrator_decompose(event, season, region)
    return {"orchestrator": "Agent Orchestrator", "azure_service": "Azure OpenAI", "deployment": DEPLOYMENT, "decomposition": result}

@app.post("/api/v1/customer360/upsert")
async def customer360_upsert(body: dict):
    """Store customer profile in Cosmos DB."""
    result = upsert_customer(body)
    return {"azure_service": "Cosmos DB", "container": "customer360", "result": result}

@app.get("/api/v1/customer360/query")
async def customer360_query(filter: str = None, limit: int = 10):
    """Query customer profiles from Cosmos DB."""
    items = query_customers(filter, limit)
    return {"azure_service": "Cosmos DB", "count": len(items), "customers": items}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": now_iso(),
        "active_runs": len(RUNS),
        "state_store": "cosmos_db" if run_store_enabled() else "memory",
    }


@app.get("/api/v1/scenario/cold-snap")
@app.post("/api/v1/scenario/cold-snap")
async def cold_snap_scenario():
    return RetailScenarioEngine().run_cold_snap()


@app.get("/api/v1/seasons")
async def list_seasons():
    return {"seasons": RetailScenarioEngine().list_seasons()}


@app.get("/api/v1/season/{season}")
@app.post("/api/v1/season/{season}")
async def seasonal_scenario(season: str):
    return RetailScenarioEngine().run_season(season)


@app.post("/api/v1/runs/custom")
async def start_custom_run(payload: Dict[str, Any], region: str = "china"):
    """Start a stateful 15-day launch run from user-entered SKU/business numbers."""
    return create_custom_run(payload, region)


@app.post("/api/v1/runs/{season}")
async def start_run(season: str, region: str = "china"):
    """Start a stateful business simulation run."""
    return create_run(season, region)


@app.get("/api/v1/runs/{run_id}/status")
async def run_status(run_id: str):
    return get_run_or_404(run_id)


@app.post("/api/v1/runs/{run_id}/work-orders/{order_id}/approve")
async def approve_work_order(run_id: str, order_id: str):
    run = get_run_or_404(run_id)
    for order in run["work_orders"]:
        if order["id"] == order_id:
            if order["status"] == "PENDING_APPROVAL":
                order["status"] = "READY"
                run["audit_log"].append({"time": now_iso(), "actor": "Business Decision Maker", "action": "APPROVED", "detail": order_id})
            refresh_run_derived_state(run)
            run["updated_at"] = now_iso()
            upsert_run(run)
            return run
    raise HTTPException(status_code=404, detail="Work order not found")


@app.post("/api/v1/runs/{run_id}/work-orders/{order_id}/complete")
async def complete_work_order(run_id: str, order_id: str):
    run = get_run_or_404(run_id)
    for order in run["work_orders"]:
        if order["id"] == order_id:
            if order["status"] == "PENDING_APPROVAL":
                raise HTTPException(status_code=409, detail="Approve this work order before completion")
            order["status"] = "COMPLETED"
            order["completed_at"] = now_iso()
            run["audit_log"].append({"time": now_iso(), "actor": "Ops Console", "action": "COMPLETED", "detail": order_id})
            if all(o["status"] == "COMPLETED" for o in run["work_orders"]):
                run["status"] = "COMPLETED"
                run["audit_log"].append({"time": now_iso(), "actor": "System", "action": "RUN_COMPLETED", "detail": "All work orders completed"})
            else:
                run["status"] = "IN_EXECUTION"
            refresh_run_derived_state(run)
            run["updated_at"] = now_iso()
            upsert_run(run)
            return run
    raise HTTPException(status_code=404, detail="Work order not found")


@app.get("/api/v1/regions")
async def list_regions():
    return {"regions": REGIONAL_CONFIG}


@app.get("/api/v1/agent-registry")
async def agent_registry():
    return {"agents": AGENT_REGISTRY}


@app.get("/api/v1/data-sources")
async def data_sources():
    return {"sources": DATA_SOURCES, "feature_store": FEATURE_STORE}


@app.post("/api/v1/runs/{run_id}/reset")
async def reset_run(run_id: str):
    old = get_run_or_404(run_id)
    return create_run(old["scenario"].get("season", "winter"), old.get("region", "china"))


# Backward-compatible endpoints for the original demo.
@app.post("/api/v1/recommend")
async def recommend(customer_data: Dict[str, Any]):
    result = RetailScenarioEngine().run_cold_snap()
    personalization = next(d for d in result["decision_loop"] if d["agent"] == "Personalization Agent")
    customer = next(d for d in result["decision_loop"] if d["agent"] == "Customer Understanding Agent")
    return {"note": "Backward-compatible endpoint backed by the scenario-driven engine.", "profile": customer["decision"], "recommendations": personalization["decision"]}


@app.post("/api/v1/inventory/forecast")
async def inventory_forecast(data: Dict[str, Any]):
    result = RetailScenarioEngine().run_cold_snap()
    return next(d for d in result["decision_loop"] if d["agent"] == "Inventory Agent")


@app.post("/api/v1/pricing/optimize")
async def pricing_optimize(data: Dict[str, Any]):
    result = RetailScenarioEngine().run_cold_snap()
    return next(d for d in result["decision_loop"] if d["agent"] == "Pricing Agent")


@app.post("/api/v1/marketing/campaign")
async def marketing_campaign(data: Dict[str, Any]):
    result = RetailScenarioEngine().run_cold_snap()
    return next(d for d in result["decision_loop"] if d["agent"] == "Marketing Agent")
