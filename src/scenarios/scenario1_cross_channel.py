"""
场景 1：跨渠道个性化推荐
演示 Customer Understanding Agent + Personalization Agent 协作

运行方式:
  MOCK=true  python -m src.scenarios.scenario1_cross_channel   # Mock 模式（无需 Azure）
  MOCK=false python -m src.scenarios.scenario1_cross_channel   # 真实 Azure OpenAI
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# 确保 src 在路径中
_src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from config import AzureConfig
from agents.customer_understanding import CustomerUnderstandingAgent
from agents.personalization import PersonalizationAgent
from agents.pricing import PricingAgent
from agents.inventory import InventoryAgent
from agents.marketing import MarketingAgent


async def run_scenario():
    """运行跨渠道个性化推荐场景"""

    mode = "MOCK" if AzureConfig.MOCK else "🔴 LIVE (Azure OpenAI)"
    deployment = AzureConfig.get_deployment_name()

    print("=" * 70)
    print(f"🎬 场景 1：跨渠道个性化推荐")
    print(f"   模式: {mode}")
    print(f"   模型: {deployment}")
    print(f"   Customer Understanding Agent + Personalization Agent 协作")
    print("=" * 70)

    # 初始化 Agent（自动选择 Mock 或 Azure OpenAI）
    customer_agent = CustomerUnderstandingAgent()
    personalization_agent = PersonalizationAgent()
    pricing_agent = PricingAgent()
    inventory_agent = InventoryAgent()
    marketing_agent = MarketingAgent()

    # 模拟客户数据
    customer_data = {
        "customer_id": "UNIQLO_2026_001",
        "channels": {
            "app": {
                "recent_views": ["保暖内衣", "摇粒绒外套", "牛仔裤"],
                "cart_items": ["保暖内衣 L 黑色"],
                "purchase_history": [
                    {"item": "HEATTECH 保暖内衣", "date": "2026-03-15", "amount": 199},
                    {"item": "弹力牛仔裤", "date": "2026-02-01", "amount": 249}
                ]
            },
            "store_rfid": {
                "last_visit": "2026-04-20",
                "tried_items": ["摇粒绒外套 M", "羽绒服 L"],
                "dwell_time_minutes": 25
            },
            "jd": {
                "orders": 3,
                "total_spend": 899,
                "reviews": 5
            }
        }
    }

    # ---- Step 1: Customer Understanding Agent ----
    print("\n" + "-" * 70)
    print("📊 Step 1: Customer Understanding Agent 构建统一画像")
    print("-" * 70)
    profile = await customer_agent.process(customer_data)

    # ---- Step 2: Personalization Agent ----
    print("\n" + "-" * 70)
    print("🎯 Step 2: Personalization Agent 生成个性化推荐")
    print("-" * 70)

    recommendation_input = {
        "customer_profile": profile,
        "context": {
            "channel": "app",
            "time": datetime.utcnow().isoformat(),
            "location": "shanghai",
            "weather": {"temperature": -2, "condition": "cold_snap"}
        },
        "inventory": [
            {"id": "001", "name": "HEATTECH 保暖内衣", "category": "basics", "price": 199, "stock": 150},
            {"id": "002", "name": "摇粒绒拉链外套", "category": "outerwear", "price": 299, "stock": 80},
            {"id": "003", "name": "弹力牛仔裤", "category": "pants", "price": 249, "stock": 200},
            {"id": "004", "name": "轻型羽绒服", "category": "outerwear", "price": 499, "stock": 45},
        ]
    }

    recommendations = await personalization_agent.process(recommendation_input)

    # ---- Step 3: Inventory Agent ----
    print("\n" + "-" * 70)
    print("📦 Step 3: Inventory Agent 需求预测")
    print("-" * 70)
    inventory_result = await inventory_agent.process({
        "sku_id": "004",
        "store_id": "SH-001",
        "forecast_days": 7
    })
    print(f"  📦 需求预测: {inventory_result['forecast'][:3]}...")
    print(f"  📦 补货建议: {inventory_result['reorder_suggestion']}")

    # ---- Step 4: Pricing Agent ----
    print("\n" + "-" * 70)
    print("💰 Step 4: Pricing Agent 动态定价")
    print("-" * 70)
    pricing_result = await pricing_agent.process({
        "sku_id": "004",
        "store_id": "SH-001",
        "current_price": 499,
        "cost": 299
    })
    print(f"  💰 最优价格: ¥{pricing_result.get('optimal_price', 'N/A')}")
    print(f"  💰 策略: {pricing_result.get('strategy', 'N/A')}")

    # ---- Step 5: Marketing Agent ----
    print("\n" + "-" * 70)
    print("📢 Step 5: Marketing Agent 营销活动")
    print("-" * 70)
    marketing_result = await marketing_agent.process({
        "objective": "保暖穿搭推广",
        "target_segment": "high_value_active",
        "budget": 5000,
        "channels": ["app_push", "wechat_mini"]
    })
    print(f"  📢 活动: {marketing_result['campaign'].get('name', 'N/A')}")
    print(f"  📢 预期 ROI: {marketing_result['predicted_results'].get('predicted_roi', 'N/A')}")

    # ---- 汇总 ----
    print("\n" + "=" * 70)
    print("📋 场景汇总")
    print("=" * 70)
    print(f"  运行模式:    {mode}")
    print(f"  模型部署:    {deployment}")
    print(f"  客户 ID:     {profile.get('customer_id', 'N/A')}")
    print(f"  客户分段:    {profile.get('rfm_segment', 'N/A')}")
    print(f"  推荐商品数:  {len(recommendations.get('recommendations', []))}")
    print()

    print("  推荐列表:")
    for i, rec in enumerate(recommendations.get("recommendations", [])[:5], 1):
        if isinstance(rec, dict):
            print(f"    {i}. {rec.get('name', 'N/A')} (¥{rec.get('price', 'N/A')}) — 评分: {rec.get('score', 'N/A')}")
            print(f"       理由: {rec.get('reason', 'N/A')}")

    print("\n" + "=" * 70)
    print(f"✅ 场景 1 完成 — 5 Agent 协作 ({mode})")
    print("=" * 70)

    return {
        "profile": profile,
        "recommendations": recommendations,
        "inventory": inventory_result,
        "pricing": pricing_result,
        "marketing": marketing_result
    }


if __name__ == "__main__":
    result = asyncio.run(run_scenario())
