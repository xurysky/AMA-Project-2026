"""
Pricing Agent — 基于 三层混合架构
Data Layer (ML) → LLM Layer (Reasoning) → Application Layer (决策)
"""

from typing import Any, Dict, List, Tuple
import numpy as np
from sklearn.linear_model import LinearRegression
from .base_agent import BaseAgent, AzureConfig


class PriceElasticityModel:
    """
    计量经济学线性回归模型
    基于 Hybrid AI 方法：用对数-对数模型估算价格弹性
    """
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_fitted = False
        self.price_elasticity = 0.0
        self.competitor_elasticity = 0.0
        self.promotion_effect = 0.0
    
    def fit(self, data: Dict[str, List[float]]):
        """
        训练价格弹性模型
        对数-对数模型: ln(Q) = α + β*ln(P) + γ*ln(Pc) + δ*Promo + ε*Season
        β 就是价格弹性系数
        """
        X = np.column_stack([
            np.log(data["price"]),
            np.log(data["competitor_price"]),
            data["promotion"],
            data["season"]
        ])
        y = np.log(data["quantity"])
        
        self.model.fit(X, y)
        self.is_fitted = True
        
        self.price_elasticity = self.model.coef_[0]
        self.competitor_elasticity = self.model.coef_[1]
        self.promotion_effect = self.model.coef_[2]
    
    def predict(self, price: float, competitor_price: float, 
                promotion: bool, season: int) -> float:
        """预测销量"""
        if not self.is_fitted:
            return 100.0  # 默认值
        
        X = np.array([[
            np.log(price),
            np.log(competitor_price),
            1 if promotion else 0,
            season
        ]])
        return float(np.exp(self.model.predict(X)[0]))
    
    def optimal_price(self, cost: float, competitor_price: float,
                       promotion: bool, season: int) -> Tuple[float, Dict]:
        """
        利润最大化定价
        max (P - C) * Q(P)
        理论最优: P* = C / (1 + 1/ε)
        """
        best_price = cost * 1.5
        best_profit = 0
        
        for price in np.arange(cost * 1.1, competitor_price * 2, 0.5):
            qty = self.predict(price, competitor_price, promotion, season)
            profit = (price - cost) * qty
            if profit > best_profit:
                best_profit = profit
                best_price = price
        
        theoretical = cost / (1 + 1/self.price_elasticity) if self.price_elasticity < -1 else cost * 1.5
        
        return float(best_price), {
            "price_elasticity": round(float(self.price_elasticity), 3),
            "competitor_elasticity": round(float(self.competitor_elasticity), 3),
            "promotion_effect": round(float(self.promotion_effect), 3),
            "theoretical_optimal": round(float(theoretical), 2),
            "expected_profit": round(float(best_profit), 2)
        }


class PricingAgent(BaseAgent):
    """
    动态定价 Agent — 三层混合架构
    
    Layer 1: Data Layer — 历史销售、竞争价格、库存水平
    Layer 2: ML Layer — 价格弹性模型（线性回归）
    Layer 3: LLM Layer — 策略推理、异常分析、自然语言报告
    """
    
    def __init__(self, openai_client=None):
        super().__init__("pricing", "Pricing Agent")
        self.openai = openai_client or AzureConfig.get_openai_client()
        self.deployment = AzureConfig.get_deployment_name()
        self.elasticity_model = PriceElasticityModel()
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        动态定价处理（三层架构）
        
        Args:
            input_data: {
                "sku_id": "xxx",
                "store_id": "xxx",
                "current_price": 99.0,
                "cost": 45.0,
                "historical_data": {...}  # 用于训练模型
            }
        """
        sku_id = input_data["sku_id"]
        store_id = input_data["store_id"]
        current_price = input_data["current_price"]
        cost = input_data["cost"]
        
        # ═══════════════════════════════════════════
        # Layer 1: Data Layer (Ground Truth)
        # ═══════════════════════════════════════════
        data_layer = await self._data_layer(input_data)
        
        # ═══════════════════════════════════════════
        # Layer 2: ML Layer (Price Elasticity Model)
        # ═══════════════════════════════════════════
        ml_layer = self._ml_layer(data_layer, cost, current_price)
        
        # ═══════════════════════════════════════════
        # Layer 3: LLM Layer (Reasoning)
        # ═══════════════════════════════════════════
        llm_layer = await self._llm_layer(data_layer, ml_layer)
        
        # 合并三层结果
        return {
            "sku_id": sku_id,
            "store_id": store_id,
            "current_price": current_price,
            "optimal_price": ml_layer["optimal_price"],
            "elasticity_analysis": ml_layer["elasticity"],
            "llm_reasoning": llm_layer["reasoning"],
            "risk_assessment": llm_layer["risk"],
            "requires_approval": abs(ml_layer["optimal_price"] - current_price) / current_price > 0.1
        }
    
    async def _data_layer(self, input_data: Dict) -> Dict[str, Any]:
        """Layer 1: 数据层 — 获取 Ground Truth"""
        # 获取竞争价格
        competitor_prices = await self._get_competitor_prices(input_data["sku_id"])
        
        # 获取库存水平
        inventory = await self._get_inventory_level(input_data["sku_id"], input_data["store_id"])
        
        # 获取历史销售数据
        historical = input_data.get("historical_data", self._default_historical_data())
        
        return {
            "current_price": input_data["current_price"],
            "cost": input_data["cost"],
            "competitor_prices": competitor_prices,
            "inventory": inventory,
            "historical": historical
        }
    
    def _ml_layer(self, data: Dict, cost: float, current_price: float) -> Dict[str, Any]:
        """Layer 2: ML 层 — 价格弹性模型"""
        # 训练弹性模型
        historical = data["historical"]
        self.elasticity_model.fit(historical)
        
        # 计算最优价格
        avg_competitor = np.mean(list(data["competitor_prices"].values()))
        optimal, elasticity_info = self.elasticity_model.optimal_price(
            cost=cost,
            competitor_price=avg_competitor,
            promotion=False,
            season=2  # 春季
        )
        
        # 预测当前价格和最优价格的销量
        current_qty = self.elasticity_model.predict(current_price, avg_competitor, False, 2)
        optimal_qty = self.elasticity_model.predict(optimal, avg_competitor, False, 2)
        
        return {
            "optimal_price": round(optimal, 2),
            "elasticity": elasticity_info,
            "current_quantity": round(current_qty),
            "optimal_quantity": round(optimal_qty),
            "profit_impact": round((optimal - current_price) * optimal_qty - (current_price - cost) * current_qty, 2)
        }
    
    async def _llm_layer(self, data: Dict, ml_result: Dict) -> Dict[str, Any]:
        """Layer 3: LLM 层 — 策略推理"""
        prompt = f"""你是一个零售定价专家。基于以下数据给出定价建议：

当前价格: ¥{data['current_price']}
成本: ¥{data['cost']}
竞争价格: {data['competitor_prices']}
库存水平: {data['inventory']}
ML 模型建议价格: ¥{ml_result['optimal_price']}
价格弹性: {ml_result['elasticity']['price_elasticity']}
预计利润变化: ¥{ml_result['profit_impact']}

请分析：
1. 这个定价建议是否合理？
2. 有什么风险需要考虑？
3. 是否需要人工审批？
"""
        
        response = self.openai.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": "你是零售定价专家，基于计量经济学模型给出专业建议。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        
        reasoning = response.choices[0].message.content
        
        # 风险评估
        risk = "low"
        if ml_result["elasticity"]["price_elasticity"] > -0.5:
            risk = "high"  # 弹性低，降价效果有限
        elif ml_result["profit_impact"] < 0:
            risk = "medium"  # 可能降低利润
        
        return {
            "reasoning": reasoning,
            "risk": risk
        }
    
    async def _get_competitor_prices(self, sku_id: str) -> Dict[str, float]:
        """获取竞争价格"""
        return {"zara": 129.0, "h&m": 79.0, "gap": 89.0}
    
    async def _get_inventory_level(self, sku_id: str, store_id: str) -> Dict[str, Any]:
        """获取库存水平"""
        return {"current": 150, "target": 200, "days_of_supply": 12}
    
    def _default_historical_data(self) -> Dict[str, List[float]]:
        """默认历史数据（实际应从数据库获取）"""
        np.random.seed(42)
        n = 100
        prices = np.random.uniform(79, 199, n)
        competitor_prices = prices * np.random.uniform(0.8, 1.2, n)
        quantity = 200 - 0.8 * prices + 0.3 * competitor_prices + np.random.normal(0, 10, n)
        
        return {
            "price": prices.tolist(),
            "quantity": quantity.tolist(),
            "competitor_price": competitor_prices.tolist(),
            "promotion": np.random.choice([0, 1], n).tolist(),
            "season": np.random.randint(1, 5, n).tolist()
        }
    
    async def health_check(self) -> bool:
        return True
