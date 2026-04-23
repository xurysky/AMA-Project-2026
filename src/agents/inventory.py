"""
Inventory Agent
需求预测 + 按门店优化库存 + 自动补货
"""

from typing import Any, Dict, List
from openai import OpenAI
from .base_agent import BaseAgent


class InventoryAgent(BaseAgent):
    """库存优化 Agent — 精准预测 + 自动补货"""
    
    def __init__(self, openai_client: OpenAI, ml_client):
        super().__init__("inventory", "Inventory Agent")
        self.openai = openai_client
        self.ml = ml_client
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        库存优化处理
        
        Args:
            input_data: {
                "sku_id": "xxx",
                "store_id": "xxx",
                "forecast_days": 7
            }
        """
        sku_id = input_data["sku_id"]
        store_id = input_data["store_id"]
        days = input_data.get("forecast_days", 7)
        
        # 1. 获取历史销售数据
        history = await self._get_sales_history(sku_id, store_id)
        
        # 2. 获取外部特征
        features = await self._get_external_features(store_id)
        
        # 3. 需求预测
        forecast = await self._forecast_demand(history, features, days)
        
        # 4. 计算补货建议
        reorder = self._calculate_reorder(sku_id, store_id, forecast)
        
        # 5. 滞销预警
        alerts = await self._check_slow_moving(sku_id, store_id)
        
        # 6. 健康度评分
        health_score = self._health_score(sku_id, store_id, forecast)
        
        return {
            "sku_id": sku_id,
            "store_id": store_id,
            "forecast": forecast,
            "reorder_suggestion": reorder,
            "slow_moving_alerts": alerts,
            "health_score": health_score
        }
    
    async def _get_sales_history(self, sku_id: str, store_id: str) -> List[Dict]:
        """获取历史销售数据"""
        # TODO: 从 Cosmos DB / Fabric 获取
        return [{"date": "2026-04-22", "quantity": 15, "revenue": 599}]
    
    async def _get_external_features(self, store_id: str) -> Dict[str, Any]:
        """获取外部特征（天气、促销）"""
        return {
            "weather": "sunny",
            "temperature": 22,
            "is_holiday": False,
            "promotion_active": False
        }
    
    async def _forecast_demand(self, history: List, features: Dict, days: int) -> List[Dict]:
        """需求预测（Prophet + LSTM 混合）"""
        # TODO: 调用 Azure ML 预测模型
        return [{"day": f"day_{i}", "predicted_quantity": 12 + i} for i in range(days)]
    
    def _calculate_reorder(self, sku_id: str, store_id: str, forecast: List) -> Dict[str, Any]:
        """计算补货建议"""
        total_demand = sum(f["predicted_quantity"] for f in forecast)
        safety_stock = total_demand * 0.2  # 20% 安全库存
        reorder_point = total_demand + safety_stock
        
        return {
            "reorder_quantity": int(reorder_point),
            "reorder_point": int(reorder_point * 0.7),
            "urgency": "medium" if reorder_point > 50 else "low"
        }
    
    async def _check_slow_moving(self, sku_id: str, store_id: str) -> List[Dict[str, str]]:
        """滞销预警"""
        return []
    
    def _health_score(self, sku_id: str, store_id: str, forecast: List) -> float:
        """库存健康度评分"""
        return 0.82
    
    async def health_check(self) -> bool:
        return True
