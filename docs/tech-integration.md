# 技术架构 — 课程知识融合

## 课程技术点映射

| 课程 | 核心技术 | 融入位置 |
|------|---------|---------|
| **TT205** 合成 Persona | TinyTroupe 虚拟客户 | Customer Understanding Agent 冷启动 |
| **TT203** 三层混合架构 | Data(ML) → LLM → App | 所有 Agent 的决策架构 |
| **TT203** 计量经济学 | 线性回归/价格弹性 | Pricing Agent 定价模型 |
| **WRK761** Agent Memory | Episodic + Long-term | 所有 Agent 的记忆机制 |
| **BRK180** GenAI 个性化 | Understand-Act-Learn | Personalization Agent |
| **BRK177** Foundry AI Gateway | 生产级架构 | 基础设施层 |
| **LAB181** 多 Agent | Agent 协作 | 编排层 |
| **LAB184** 负责任 AI | 安全合规 | 全局 |

---

## 1. 合成 Persona（TT205）— 冷启动解决方案

### 问题
新客户没有历史数据，Agent 无法个性化。

### 解决方案
用 TinyTroupe 生成合成客户 Persona，模拟真实客户行为。

```python
# src/agents/synthetic_persona.py

from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

class SyntheticPersonaGenerator:
    """
    基于 TT205 课程：合成 Persona 生成器
    用 TinyTroupe 创建虚拟客户，解决冷启动问题
    """
    
    def __init__(self):
        self.persona_templates = {
            "young_professional": {
                "age": (25, 35),
                "income": "medium_high",
                "lifestyle": "busy",
                "shopping_behavior": "online_first",
                "price_sensitivity": "low"
            },
            "family_shopper": {
                "age": (30, 45),
                "income": "medium",
                "lifestyle": "family_oriented",
                "shopping_behavior": "value_conscious",
                "price_sensitivity": "medium"
            },
            "senior_comfort": {
                "age": (55, 70),
                "income": "medium",
                "lifestyle": "comfort_focused",
                "shopping_behavior": "store_first",
                "price_sensitivity": "high"
            }
        }
    
    def generate_persona(self, segment: str, region: str = "china") -> TinyPerson:
        """生成一个合成客户 Persona"""
        template = self.persona_templates.get(segment, self.persona_templates["young_professional"])
        
        # 创建 TinyTroupe Agent
        persona = TinyPerson(
            name=f"synthetic_{segment}_{region}",
            traits=[
                f"age_{template['age'][0]}_{template['age'][1]}",
                f"income_{template['income']}",
                f"lifestyle_{template['lifestyle']}"
            ]
        )
        
        # 设置购物行为模式
        persona.configure({
            "shopping_channels": self._get_channels(region),
            "preferred_categories": self._get_categories(segment),
            "price_range": self._get_price_range(template["price_sensitivity"]),
            "interaction_style": self._get_interaction_style(segment)
        })
        
        return persona
    
    def simulate_behavior(self, persona: TinyPerson, scenario: str) -> Dict:
        """模拟客户行为序列"""
        # 让 Persona 执行购物场景
        world = TinyWorld("retail_store", [persona])
        
        if scenario == "browse_and_buy":
            persona.act("浏览保暖内衣系列")
            persona.act("查看价格和评价")
            persona.act("加入购物车")
            persona.act("完成购买")
        elif scenario == "window_shopping":
            persona.act("浏览新品")
            persona.act("试穿几件衣服")
            persona.act("离开店铺")
        
        return persona.get_memory()
    
    def _get_channels(self, region: str) -> List[str]:
        if region == "china":
            return ["app", "wechat_mini", "jd", "tmall", "store"]
        elif region == "japan":
            return ["app", "store", "web"]
        return ["app", "store"]
    
    def _get_categories(self, segment: str) -> List[str]:
        categories_map = {
            "young_professional": ["basics", "office", "outerwear"],
            "family_shopper": ["basics", "kids", "home"],
            "senior_comfort": ["basics", "comfort", "health"]
        }
        return categories_map.get(segment, ["basics"])
    
    def _get_price_range(self, sensitivity: str) -> Dict:
        ranges = {
            "low": {"min": 199, "max": 999},
            "medium": {"min": 99, "max": 499},
            "high": {"min": 59, "max": 299}
        }
        return ranges.get(sensitivity, ranges["medium"])
    
    def _get_interaction_style(self, segment: str) -> str:
        styles = {
            "young_professional": "quick_decisive",
            "family_shopper": "comparison_shopping",
            "senior_comfort": "careful_browsing"
        }
        return styles.get(segment, "normal")
```

---

## 2. 计量经济学模型（TT203）— 价格弹性

### 问题
如何科学定价，最大化利润？

### 解决方案
用线性回归估算价格弹性系数。

```python
# src/models/price_elasticity.py

import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict, List, Tuple

class PriceElasticityModel:
    """
    基于 TT203 课程：计量经济学线性回归
    估算价格弹性系数，用于动态定价
    """
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_fitted = False
    
    def fit(self, data: Dict[str, List[float]]):
        """
        训练价格弹性模型
        
        数据格式:
        {
            "price": [99, 129, 79, ...],        # 价格
            "quantity": [150, 120, 180, ...],    # 销量
            "competitor_price": [119, 119, 89, ...],  # 竞争价格
            "promotion": [0, 1, 0, ...],         # 是否促销
            "season": [1, 2, 3, ...]             # 季节
        }
        """
        X = np.column_stack([
            np.log(data["price"]),           # 对数价格
            np.log(data["competitor_price"]), # 对数竞争价格
            data["promotion"],               # 促销虚拟变量
            data["season"]                   # 季节
        ])
        y = np.log(data["quantity"])         # 对数销量
        
        self.model.fit(X, y)
        self.is_fitted = True
        
        # 价格弹性 = β1 (对数-对数模型)
        self.price_elasticity = self.model.coef_[0]
        self.competitor_elasticity = self.model.coef_[1]
        self.promotion_effect = self.model.coef_[2]
    
    def predict_quantity(self, price: float, competitor_price: float, 
                         promotion: bool, season: int) -> float:
        """预测销量"""
        if not self.is_fitted:
            raise ValueError("模型未训练")
        
        X = np.array([[
            np.log(price),
            np.log(competitor_price),
            1 if promotion else 0,
            season
        ]])
        
        return np.exp(self.model.predict(X)[0])
    
    def optimal_price(self, cost: float, competitor_price: float, 
                       promotion: bool, season: int,
                       margin_target: float = 0.4) -> Tuple[float, Dict]:
        """
        计算最优价格
        
        基于利润最大化: max (P - C) * Q(P)
        其中 Q(P) = exp(α + β*ln(P) + γ*ln(Pc) + δ*Promo + ε*Season)
        """
        best_price = cost
        best_profit = 0
        
        # 搜索最优价格（从成本到竞争价格的 2 倍）
        for price in np.arange(cost * 1.1, competitor_price * 2, 0.1):
            quantity = self.predict_quantity(price, competitor_price, promotion, season)
            profit = (price - cost) * quantity
            
            if profit > best_profit:
                best_profit = profit
                best_price = price
        
        # 计算弹性
        elasticity = self.price_elasticity
        
        # 利润最大化条件: P* = C / (1 + 1/ε)
        theoretical_optimal = cost / (1 + 1/elasticity)
        
        return best_price, {
            "price_elasticity": round(elasticity, 3),
            "competitor_elasticity": round(self.competitor_elasticity, 3),
            "promotion_effect": round(self.promotion_effect, 3),
            "theoretical_optimal": round(theoretical_optimal, 2),
            "practical_optimal": round(best_price, 2),
            "expected_profit": round(best_profit, 2)
        }
```

---

## 3. TT203 三层混合架构

### 架构
```
┌─────────────────────────────────────────────┐
│           Application Layer (LLM)           │
│   策略推理、异常分析、自然语言报告           │
├─────────────────────────────────────────────┤
│             ML Layer (Models)               │
│   价格弹性、需求预测、客户分群              │
├─────────────────────────────────────────────┤
│            Data Layer (Ground Truth)        │
│   历史数据、实时数据、外部数据              │
└─────────────────────────────────────────────┘
```

### 实现
```python
# src/agents/hybrid_agent.py

class HybridAgent(BaseAgent):
    """
    基于 TT203 课程：三层混合架构
    Data Layer → ML Layer → LLM Layer
    """
    
    def __init__(self, openai_client, ml_models):
        super().__init__("hybrid", "Hybrid Agent")
        self.openai = openai_client
        self.ml = ml_models
    
    async def process(self, input_data: Dict) -> Dict:
        # Layer 1: Data Layer (Ground Truth)
        raw_data = await self._fetch_data(input_data)
        
        # Layer 2: ML Layer (Models)
        ml_predictions = self._run_ml_models(raw_data)
        
        # Layer 3: LLM Layer (Reasoning)
        llm_reasoning = await self._llm_reasoning(raw_data, ml_predictions)
        
        # 合并结果
        return {
            "data": raw_data,
            "predictions": ml_predictions,
            "reasoning": llm_reasoning,
            "confidence": self._calculate_confidence(ml_predictions, llm_reasoning)
        }
```

---

## 4. Agent Memory（WRK761）

### 记忆架构
```
┌─────────────────────────────────────────────┐
│              Agent Memory                    │
├─────────────────┬───────────────────────────┤
│   Episodic      │      Long-term            │
│   (短期记忆)     │      (长期记忆)           │
│                 │                           │
│   最近交互       │      偏好/习惯            │
│   当前会话       │      历史行为             │
│   临时状态       │      学习到的模式         │
├─────────────────┴───────────────────────────┤
│              Semantic (语义记忆)             │
│   知识图谱、商品关系、品牌认知               │
└─────────────────────────────────────────────┘
```

### 实现
```python
# src/memory/agent_memory.py

from azure.cosmos import CosmosClient
from typing import Dict, List, Optional
import json

class AgentMemory:
    """
    基于 WRK761 课程：Agent Memory 架构
    Episodic + Long-term + Semantic 三层记忆
    """
    
    def __init__(self, cosmos_client: CosmosClient, agent_id: str):
        self.cosmos = cosmos_client
        self.agent_id = agent_id
        self.episodic_db = cosmos_client.get_database_client("episodic_memory")
        self.longterm_db = cosmos_client.get_database_client("longterm_memory")
        self.semantic_db = cosmos_client.get_database_client("semantic_memory")
    
    async def store_episodic(self, session_id: str, event: Dict):
        """存储短期记忆（当前会话）"""
        container = self.episodic_db.get_container_client(session_id)
        await container.upsert_item({
            "id": f"{session_id}_{event['timestamp']}",
            "agent_id": self.agent_id,
            "event": event,
            "ttl": 3600  # 1 小时过期
        })
    
    async def store_longterm(self, customer_id: str, pattern: Dict):
        """存储长期记忆（偏好/习惯）"""
        container = self.longterm_db.get_container_client("patterns")
        
        # 检查是否已有记忆
        existing = await self._get_existing_pattern(customer_id, pattern["type"])
        
        if existing:
            # 更新现有记忆（指数移动平均）
            updated = self._update_pattern(existing, pattern)
        else:
            updated = pattern
        
        await container.upsert_item({
            "id": f"{customer_id}_{pattern['type']}",
            "customer_id": customer_id,
            "pattern": updated,
            "confidence": pattern.get("confidence", 0.5),
            "last_updated": pattern["timestamp"]
        })
    
    async def retrieve(self, customer_id: str, context: Dict) -> Dict:
        """检索相关记忆"""
        # 1. 检索短期记忆
        episodic = await self._get_episodic(customer_id, context)
        
        # 2. 检索长期记忆
        longterm = await self._get_longterm(customer_id)
        
        # 3. 检索语义记忆
        semantic = await self._get_semantic(context)
        
        # 4. 融合记忆
        return self._fuse_memories(episodic, longterm, semantic)
    
    def _fuse_memories(self, episodic: List, longterm: Dict, semantic: Dict) -> Dict:
        """融合三层记忆"""
        return {
            "recent_interactions": episodic,
            "established_preferences": longterm,
            "contextual_knowledge": semantic,
            "confidence_score": self._calculate_memory_confidence(
                len(episodic), longterm.get("confidence", 0), semantic.get("relevance", 0)
            )
        }
```

---

## 课程融合总结

| 课程 | 技术 | 融入的 Agent | 价值 |
|------|------|-------------|------|
| TT205 | 合成 Persona | Customer Understanding | 冷启动 + 隐私保护 |
| TT203 | 三层混合架构 | 所有 Agent | ML 精确性 + LLM 推理 |
| TT203 | 线性回归/弹性 | Pricing | 科学定价 |
| WRK761 | Agent Memory | 所有 Agent | 持续学习 |
| BRK180 | U-A-L 三支柱 | Personalization | 个性化闭环 |
| BRK177 | Foundry Gateway | 基础设施 | 生产级架构 |
| LAB181 | 多 Agent 协作 | 编排层 | 端到端自动化 |
| LAB184 | 负责任 AI | 全局 | 合规 + 安全 |
