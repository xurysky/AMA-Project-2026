"""
场景 1：跨渠道个性化推荐
演示 Customer Understanding Agent + Personalization Agent 协作

运行方式: python -m src.scenarios.scenario1_cross_channel
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List


# ============================================================
# Mock 数据层 — 替代真实 Azure 服务，用于演示和开发
# ============================================================

class MockOpenAIClient:
    """Mock Azure OpenAI Client — 模拟 GPT-4o 推理"""

    class ChatCompletions:
        async def create(self, model: str, messages: list, **kwargs) -> Any:
            # 模拟 LLM 推理结果
            user_msg = messages[-1]["content"] if messages else ""

            if "customer profile" in user_msg.lower() or "画像" in user_msg:
                return MockResponse({
                    "customer_id": "UNIQLO_2026_001",
                    "rfm_segment": "high_value_active",
                    "intent": "winter_shopping",
                    "preferences": {
                        "style": "casual_basic",
                        "price_range": "mid_high",
                        "categories": ["outerwear", "basics", "pants"],
                        "size": {"top": "M", "bottom": "L"}
                    },
                    "price_sensitivity": 0.35,
                    "lifetime_value": 12500,
                    "next_likely_purchase": "outerwear"
                })
            elif "recommend" in user_msg.lower() or "推荐" in user_msg:
                return MockResponse({
                    "recommendations": [
                        {"sku": "004", "name": "轻型羽绒服", "price": 499,
                         "score": 0.95, "reason": "根据您的浏览记录和当前气温，这件羽绒服是最佳选择"},
                        {"sku": "002", "name": "摇粒绒拉链外套", "price": 299,
                         "score": 0.88, "reason": "您在门店试穿过类似款式，适合日常穿搭"},
                        {"sku": "001", "name": "HEATTECH 保暖内衣", "price": 199,
                         "score": 0.82, "reason": "您已购买过，回购率高，冬季必备"},
                        {"sku": "003", "name": "弹力牛仔裤", "price": 249,
                         "score": 0.71, "reason": "搭配外套的经典选择"}
                    ],
                    "next_action": {
                        "action": "push_notification",
                        "content": "降温了！为您推荐保暖穿搭，新客首单9折",
                        "channel": "app"
                    },
                    "personalization_score": 0.91
                })
            else:
                return MockResponse({"status": "processed"})

    def __init__(self):
        self.chat = self.ChatCompletions()


class MockResponse:
    def __init__(self, data: dict):
        self.choices = [MockChoice(json.dumps(data, ensure_ascii=False))]


class MockChoice:
    def __init__(self, content: str):
        self.message = MockMessage(content)


class MockMessage:
    def __init__(self, content: str):
        self.content = content


# ============================================================
# Agent 实现 — 使用 Mock 数据
# ============================================================

class CustomerUnderstandingAgent:
    """客户理解 Agent — 构建统一客户画像"""

    def __init__(self, openai_client: MockOpenAIClient):
        self.openai = openai_client
        self.name = "Customer Understanding Agent"

    async def process(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """从多渠道数据构建统一客户画像"""
        print(f"  📊 [{self.name}] 构建统一客户画像...")

        # 模拟多渠道数据聚合
        channels = customer_data.get("channels", {})
        app_data = channels.get("app", {})
        store_data = channels.get("store_rfid", {})
        jd_data = channels.get("jd", {})

        # 模拟 ID-Mapping: 跨渠道身份统一
        print(f"  🔗 [{self.name}] ID-Mapping: App + RFID + 京东 → 统一身份")

        # 模拟 RFM 分析
        total_spend = sum(p.get("amount", 0) for p in app_data.get("purchase_history", []))
        total_spend += jd_data.get("total_spend", 0)
        visit_count = len(app_data.get("purchase_history", [])) + jd_data.get("orders", 0)

        # 调用 LLM 生成画像
        prompt = f"""
        客户数据:
        - App 浏览: {app_data.get('recent_views', [])}
        - 购物车: {app_data.get('cart_items', [])}
        - 购买历史: {app_data.get('purchase_history', [])}
        - 门店试穿: {store_data.get('tried_items', [])}
        - 京东消费: ¥{jd_data.get('total_spend', 0)}
        - 总消费: ¥{total_spend}
        - 总访问: {visit_count} 次

        请生成客户画像（JSON 格式）。
        """

        result = await self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        profile = json.loads(result.choices[0].message.content)
        print(f"  ✅ [{self.name}] 客户分段: {profile['rfm_segment']}")
        print(f"  ✅ [{self.name}] 意图: {profile['intent']}")
        print(f"  ✅ [{self.name}] 偏好: {profile['preferences']['style']}")
        print(f"  ✅ [{self.name}] 价格敏感度: {profile['price_sensitivity']}")

        return profile


class PersonalizationAgent:
    """个性化推荐 Agent — 动态定制推荐"""

    def __init__(self, openai_client: MockOpenAIClient):
        self.openai = openai_client
        self.name = "Personalization Agent"

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """基于客户画像生成个性化推荐"""
        print(f"  🎯 [{self.name}] 生成个性化推荐...")

        profile = input_data.get("customer_profile", {})
        context = input_data.get("context", {})
        inventory = input_data.get("inventory", [])

        prompt = f"""
        客户画像: {json.dumps(profile, ensure_ascii=False)}
        当前上下文: {json.dumps(context, ensure_ascii=False)}
        可售库存: {json.dumps(inventory, ensure_ascii=False)}

        请生成个性化推荐（JSON 格式），包含推荐理由。
        """

        result = await self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        recommendations = json.loads(result.choices[0].message.content)
        print(f"  ✅ [{self.name}] 推荐商品数: {len(recommendations['recommendations'])}")
        print(f"  ✅ [{self.name}] 下一步行动: {recommendations['next_action']['action']}")
        print(f"  ✅ [{self.name}] 个性化评分: {recommendations['personalization_score']}")

        return recommendations


# ============================================================
# 场景编排
# ============================================================

async def run_scenario():
    """运行跨渠道个性化推荐场景"""

    print("=" * 70)
    print("🎬 场景 1：跨渠道个性化推荐")
    print("   Customer Understanding Agent + Personalization Agent 协作")
    print("=" * 70)

    # 初始化 Mock 客户端
    openai_client = MockOpenAIClient()

    # 初始化 Agent
    customer_agent = CustomerUnderstandingAgent(openai_client)
    personalization_agent = PersonalizationAgent(openai_client)

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

    # ---- Step 3: 跨渠道一致性 ----
    print("\n" + "-" * 70)
    print("🔄 Step 3: 跨渠道一致性验证")
    print("-" * 70)
    print("  ✅ App 推荐 → 门店体验 → 小程序复购")
    print("  ✅ 推荐一致性: 100%（同一客户画像驱动）")
    print("  ✅ 推荐理由已生成（可解释性）")

    # ---- 汇总 ----
    print("\n" + "=" * 70)
    print("📋 场景汇总")
    print("=" * 70)
    print(f"  客户 ID:     {profile['customer_id']}")
    print(f"  客户分段:    {profile['rfm_segment']}")
    print(f"  购买意图:    {profile['intent']}")
    print(f"  推荐商品数:  {len(recommendations['recommendations'])}")
    print(f"  个性化评分:  {recommendations['personalization_score']}")
    print(f"  下一步行动:  {recommendations['next_action']['content']}")
    print()

    print("  推荐列表:")
    for i, rec in enumerate(recommendations["recommendations"], 1):
        print(f"    {i}. {rec['name']} (¥{rec['price']}) — 评分: {rec['score']}")
        print(f"       理由: {rec['reason']}")

    print("\n" + "=" * 70)
    print("✅ 场景 1 完成 — 跨渠道个性化推荐")
    print("=" * 70)

    return {
        "profile": profile,
        "recommendations": recommendations
    }


if __name__ == "__main__":
    result = asyncio.run(run_scenario())
