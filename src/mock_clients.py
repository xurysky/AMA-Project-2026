"""
Mock 客户端 — 用于本地开发和演示
当 MOCK=true 时使用，不需要真实 Azure 连接
"""

import json
from typing import Any


class MockChatMessage:
    def __init__(self, content: str):
        self.content = content


class MockChoice:
    def __init__(self, content: str):
        self.message = MockChatMessage(content)


class MockChatCompletions:
    def create(self, model: str, messages: list, **kwargs) -> Any:
        user_msg = messages[-1]["content"] if messages else ""

        if "画像" in user_msg or "profile" in user_msg.lower():
            result = {
                "customer_id": "CONTOSO_2026_001",
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
            }
        elif "推荐" in user_msg or "recommend" in user_msg.lower():
            result = {
                "recommendations": [
                    {"sku": "004", "name": "轻型羽绒服", "price": 499,
                     "score": 0.95, "reason": "根据浏览记录和当前气温，羽绒服是最佳选择"},
                    {"sku": "002", "name": "摇粒绒拉链外套", "price": 299,
                     "score": 0.88, "reason": "门店试穿过类似款式，适合日常穿搭"},
                    {"sku": "001", "name": "HEATTECH 保暖内衣", "price": 199,
                     "score": 0.82, "reason": "已购买过，回购率高，冬季必备"},
                    {"sku": "003", "name": "弹力牛仔裤", "price": 249,
                     "score": 0.71, "reason": "搭配外套的经典选择"}
                ],
                "next_action": {
                    "action": "push_notification",
                    "content": "降温了！为您推荐保暖穿搭，新客首单9折",
                    "channel": "app"
                },
                "personalization_score": 0.91
            }
        elif "定价" in user_msg or "pric" in user_msg.lower():
            result = {
                "optimal_price": 499,
                "confidence": 0.87,
                "strategy": "maintain_premium",
                "reasoning": "库存紧张 + 需求激增 = 维持溢价",
                "risk_level": "low"
            }
        elif "营销" in user_msg or "market" in user_msg.lower():
            result = {
                "campaign": "保暖穿搭推送",
                "channels": ["app_push", "wechat_mini"],
                "target_segment": "high_value_active",
                "budget": 5000,
                "expected_roi": 3.2
            }
        elif "库存" in user_msg or "inventory" in user_msg.lower():
            result = {
                "demand_forecast": [120, 135, 150, 140, 125],
                "reorder_point": 200,
                "recommended_action": "紧急补货",
                "confidence": 0.92
            }
        else:
            result = {"status": "processed", "input_summary": user_msg[:100]}

        class MockResponse:
            def __init__(self):
                self.choices = [MockChoice(json.dumps(result, ensure_ascii=False))]

        return MockResponse()


class MockCompletions:
    def __init__(self):
        self.completions = MockChatCompletions()



class MockOpenAIClient:
    """Mock Azure OpenAI Client"""
    def __init__(self):
        self.chat = MockCompletions()
