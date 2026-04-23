"""
Pricing Agent
基于需求/竞争/库存动态定价
"""

from typing import Any, Dict, List
from openai import OpenAI
from .base_agent import BaseAgent


class PricingAgent(BaseAgent):
    """动态定价 Agent — 利润最大化"""
    
    def __init__(self, openai_client: OpenAI):
        super().__init__("pricing", "Pricing Agent")
        self.openai = openai_client
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        动态定价处理
        
        Args:
            input_data: {
                "sku_id": "xxx",
                "store_id": "xxx",
                "current_price": 99.0,
                "cost": 45.0
            }
        """
        sku_id = input_data["sku_id"]
        store_id = input_data["store_id"]
        current_price = input_data["current_price"]
        cost = input_data["cost"]
        
        # 1. 获取需求弹性
        elasticity = await self._get_elasticity(sku_id)
        
        # 2. 获取竞争价格
        competitor_prices = await self._get_competitor_prices(sku_id)
        
        # 3. 获取库存水平
        inventory_level = await self._get_inventory_level(sku_id, store_id)
        
        # 4. ML 模型计算最优价格
        optimal_price = self._ml_pricing_model(
            current_price, cost, elasticity, competitor_prices, inventory_level
        )
        
        # 5. LLM 生成定价理由
        reasoning = await self._generate_reasoning(
            sku_id, current_price, optimal_price, elasticity, competitor_prices
        )
        
        # 6. 利润影响预测
        profit_impact = self._estimate_profit_impact(
            current_price, optimal_price, inventory_level
        )
        
        return {
            "sku_id": sku_id,
            "store_id": store_id,
            "current_price": current_price,
            "optimal_price": optimal_price,
            "reasoning": reasoning,
            "profit_impact": profit_impact,
            "requires_approval": abs(optimal_price - current_price) / current_price > 0.1
        }
    
    async def _get_elasticity(self, sku_id: str) -> float:
        """获取需求弹性系数"""
        # TODO: 从 ML 模型获取
        return -1.5  # 弹性系数
    
    async def _get_competitor_prices(self, sku_id: str) -> Dict[str, float]:
        """获取竞争价格"""
        return {"zara": 129.0, "h&m": 79.0, "gap": 89.0}
    
    async def _get_inventory_level(self, sku_id: str, store_id: str) -> Dict[str, Any]:
        """获取库存水平"""
        return {"current": 150, "target": 200, "days_of_supply": 12}
    
    def _ml_pricing_model(self, current_price: float, cost: float, 
                          elasticity: float, competitors: Dict, inventory: Dict) -> float:
        """ML 定价模型"""
        # 简化实现：基于竞争和库存调整
        avg_competitor = sum(competitors.values()) / len(competitors)
        inventory_ratio = inventory["current"] / inventory["target"]
        
        if inventory_ratio > 1.2:  # 库存过高，降价
            optimal = current_price * 0.9
        elif inventory_ratio < 0.8:  # 库存偏低，可以提价
            optimal = current_price * 1.05
        else:  # 库存正常，参考竞争价格
            optimal = (current_price + avg_competitor) / 2
        
        # 确保不低于成本
        return max(optimal, cost * 1.1)
    
    async def _generate_reasoning(self, sku_id: str, current: float, 
                                   optimal: float, elasticity: float, competitors: Dict) -> str:
        """LLM 生成定价理由"""
        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个零售定价专家。解释定价决策的理由。"},
                {"role": "user", "content": f"当前价格：{current}，建议价格：{optimal}，弹性：{elasticity}，竞争价格：{competitors}"}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    
    def _estimate_profit_impact(self, current: float, optimal: float, inventory: Dict) -> Dict[str, Any]:
        """利润影响预测"""
        price_change = (optimal - current) / current
        return {
            "price_change_pct": round(price_change * 100, 1),
            "estimated_revenue_change_pct": round(price_change * 0.7 * 100, 1),
            "estimated_profit_change_pct": round(price_change * 1.2 * 100, 1)
        }
    
    async def health_check(self) -> bool:
        return True
