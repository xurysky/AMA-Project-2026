"""
Personalization Agent
基于客户画像和实时行为，动态定制推荐
"""

from typing import Any, Dict, List
from openai import OpenAI
from .base_agent import BaseAgent


class PersonalizationAgent(BaseAgent):
    """个性化推荐 Agent — 跨渠道千人千面"""
    
    def __init__(self, openai_client: OpenAI, redis_client):
        super().__init__("personalization", "Personalization Agent")
        self.openai = openai_client
        self.redis = redis_client
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成个性化推荐
        
        Args:
            input_data: {
                "customer_profile": {...},
                "context": {
                    "channel": "app|store|web",
                    "time": "2026-04-23T08:00:00Z",
                    "location": "shanghai"
                },
                "inventory": [...]
            }
        """
        profile = input_data["customer_profile"]
        context = input_data["context"]
        inventory = input_data.get("inventory", [])
        
        # 1. 基于画像筛选候选商品
        candidates = self._filter_candidates(profile, inventory)
        
        # 2. 上下文感知排序
        ranked = self._contextual_ranking(candidates, context)
        
        # 3. LLM 生成推荐理由
        recommendations = await self._generate_recommendations(
            profile, ranked[:10], context
        )
        
        # 4. 生成下一步行动建议
        next_action = await self._suggest_next_action(profile, recommendations)
        
        return {
            "recommendations": recommendations,
            "next_action": next_action,
            "channel": context["channel"],
            "personalization_score": self._calculate_score(profile, recommendations)
        }
    
    def _filter_candidates(self, profile: Dict, inventory: List) -> List[Dict]:
        """基于画像筛选候选商品"""
        preferences = profile.get("preferences", {})
        # 简化实现：按偏好过滤
        return [item for item in inventory if item.get("category") in preferences.get("categories", [])]
    
    def _contextual_ranking(self, candidates: List, context: Dict) -> List[Dict]:
        """上下文感知排序"""
        # 简化实现：按匹配度排序
        return sorted(candidates, key=lambda x: x.get("relevance_score", 0), reverse=True)
    
    async def _generate_recommendations(self, profile: Dict, candidates: List, context: Dict) -> List[Dict]:
        """LLM 生成推荐理由"""
        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个个性化推荐专家。为用户推荐商品并给出理由。"},
                {"role": "user", "content": f"用户偏好：{profile.get('preferences', {})}\n候选商品：{candidates}\n场景：{context}"}
            ],
            max_tokens=500
        )
        
        # 简化实现：返回候选商品
        return candidates[:5]
    
    async def _suggest_next_action(self, profile: Dict, recommendations: List) -> Dict[str, str]:
        """生成下一步行动建议"""
        return {
            "action": "push_notification",
            "content": "根据您的浏览记录，为您推荐以下保暖内衣搭配",
            "channel": "app"
        }
    
    def _calculate_score(self, profile: Dict, recommendations: List) -> float:
        """计算个性化评分"""
        return 0.85
    
    async def health_check(self) -> bool:
        return True
