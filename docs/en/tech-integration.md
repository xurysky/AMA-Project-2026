# Technical Architecture — Course Knowledge Integration

## Course Technical Points Mapping

| Course | Core Technology | Integration Point |
|--------|----------------|-------------------|
| **TT205** Synthetic Persona | TinyTroupe virtual customers | Customer Understanding Agent cold start |
| **TT203** Three-Layer Hybrid Architecture | Data(ML) → LLM → App | Decision architecture for all Agents |
| **TT203** Econometrics | Linear regression / price elasticity | Pricing Agent pricing model |
| **WRK761** Agent Memory | Episodic + Long-term | Memory mechanism for all Agents |
| **BRK180** GenAI Personalization | Understand-Act-Learn | Personalization Agent |
| **BRK177** Foundry AI Gateway | Production-grade architecture | Infrastructure layer |
| **LAB181** Multi-Agent | Agent collaboration | Orchestration layer |
| **LAB184** Responsible AI | Security & compliance | Global |

---

## 1. Synthetic Persona (TT205) — Cold Start Solution

### Problem
New customers have no historical data, making it impossible for Agents to personalize.

### Solution
Use TinyTroupe to generate synthetic customer Personas that simulate real customer behavior.

```python
# src/agents/synthetic_persona.py

from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

class SyntheticPersonaGenerator:
    """
    Based on TT205 course: Synthetic Persona Generator
    Uses TinyTroupe to create virtual customers, solving the cold start problem
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
        """Generate a synthetic customer Persona"""
        template = self.persona_templates.get(segment, self.persona_templates["young_professional"])
        
        # Create TinyTroupe Agent
        persona = TinyPerson(
            name=f"synthetic_{segment}_{region}",
            traits=[
                f"age_{template['age'][0]}_{template['age'][1]}",
                f"income_{template['income']}",
                f"lifestyle_{template['lifestyle']}"
            ]
        )
        
        # Configure shopping behavior patterns
        persona.configure({
            "shopping_channels": self._get_channels(region),
            "preferred_categories": self._get_categories(segment),
            "price_range": self._get_price_range(template["price_sensitivity"]),
            "interaction_style": self._get_interaction_style(segment)
        })
        
        return persona
    
    def simulate_behavior(self, persona: TinyPerson, scenario: str) -> Dict:
        """Simulate customer behavior sequence"""
        # Have the Persona execute shopping scenarios
        world = TinyWorld("retail_store", [persona])
        
        if scenario == "browse_and_buy":
            persona.act("Browse thermal underwear collection")
            persona.act("Check prices and reviews")
            persona.act("Add to cart")
            persona.act("Complete purchase")
        elif scenario == "window_shopping":
            persona.act("Browse new arrivals")
            persona.act("Try on several items")
            persona.act("Leave the store")
        
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

## 2. Econometric Model (TT203) — Price Elasticity

### Problem
How to set prices scientifically to maximize profit?

### Solution
Use linear regression to estimate price elasticity coefficients.

```python
# src/models/price_elasticity.py

import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict, List, Tuple

class PriceElasticityModel:
    """
    Based on TT203 course: Econometric linear regression
    Estimates price elasticity coefficients for dynamic pricing
    """
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_fitted = False
    
    def fit(self, data: Dict[str, List[float]]):
        """
        Train the price elasticity model
        
        Data format:
        {
            "price": [99, 129, 79, ...],        # Price
            "quantity": [150, 120, 180, ...],    # Quantity sold
            "competitor_price": [119, 119, 89, ...],  # Competitor price
            "promotion": [0, 1, 0, ...],         # Whether on promotion
            "season": [1, 2, 3, ...]             # Season
        }
        """
        X = np.column_stack([
            np.log(data["price"]),           # Log price
            np.log(data["competitor_price"]), # Log competitor price
            data["promotion"],               # Promotion dummy variable
            data["season"]                   # Season
        ])
        y = np.log(data["quantity"])         # Log quantity
        
        self.model.fit(X, y)
        self.is_fitted = True
        
        # Price elasticity = β1 (log-log model)
        self.price_elasticity = self.model.coef_[0]
        self.competitor_elasticity = self.model.coef_[1]
        self.promotion_effect = self.model.coef_[2]
    
    def predict_quantity(self, price: float, competitor_price: float, 
                         promotion: bool, season: int) -> float:
        """Predict quantity sold"""
        if not self.is_fitted:
            raise ValueError("Model not trained")
        
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
        Calculate optimal price
        
        Based on profit maximization: max (P - C) * Q(P)
        Where Q(P) = exp(α + β*ln(P) + γ*ln(Pc) + δ*Promo + ε*Season)
        """
        best_price = cost
        best_profit = 0
        
        # Search for optimal price (from cost to 2x competitor price)
        for price in np.arange(cost * 1.1, competitor_price * 2, 0.1):
            quantity = self.predict_quantity(price, competitor_price, promotion, season)
            profit = (price - cost) * quantity
            
            if profit > best_profit:
                best_profit = profit
                best_price = price
        
        # Calculate elasticity
        elasticity = self.price_elasticity
        
        # Profit maximization condition: P* = C / (1 + 1/ε)
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

## 3. TT203 Three-Layer Hybrid Architecture

### Architecture
```
┌─────────────────────────────────────────────┐
│           Application Layer (LLM)           │
│   Strategy reasoning, anomaly analysis,     │
│   natural language reporting                │
├─────────────────────────────────────────────┤
│             ML Layer (Models)               │
│   Price elasticity, demand forecasting,     │
│   customer segmentation                     │
├─────────────────────────────────────────────┤
│            Data Layer (Ground Truth)        │
│   Historical data, real-time data,          │
│   external data                             │
└─────────────────────────────────────────────┘
```

### Implementation
```python
# src/agents/hybrid_agent.py

class HybridAgent(BaseAgent):
    """
    Based on TT203 course: Three-layer hybrid architecture
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
        
        # Merge results
        return {
            "data": raw_data,
            "predictions": ml_predictions,
            "reasoning": llm_reasoning,
            "confidence": self._calculate_confidence(ml_predictions, llm_reasoning)
        }
```

---

## 4. Agent Memory (WRK761)

### Memory Architecture
```
┌─────────────────────────────────────────────┐
│              Agent Memory                    │
├─────────────────┬───────────────────────────┤
│   Episodic      │      Long-term            │
│   (Short-term)  │      (Long-term)          │
│                 │                           │
│   Recent        │      Preferences/Habits   │
│   interactions  │      Historical behavior  │
│   Current       │      Learned patterns     │
│   session       │                           │
│   Temporary     │                           │
│   state         │                           │
├─────────────────┴───────────────────────────┤
│              Semantic Memory                │
│   Knowledge graph, product relationships,   │
│   brand perception                          │
└─────────────────────────────────────────────┘
```

### Implementation
```python
# src/memory/agent_memory.py

from azure.cosmos import CosmosClient
from typing import Dict, List, Optional
import json

class AgentMemory:
    """
    Based on WRK761 course: Agent Memory architecture
    Episodic + Long-term + Semantic three-layer memory
    """
    
    def __init__(self, cosmos_client: CosmosClient, agent_id: str):
        self.cosmos = cosmos_client
        self.agent_id = agent_id
        self.episodic_db = cosmos_client.get_database_client("episodic_memory")
        self.longterm_db = cosmos_client.get_database_client("longterm_memory")
        self.semantic_db = cosmos_client.get_database_client("semantic_memory")
    
    async def store_episodic(self, session_id: str, event: Dict):
        """Store short-term memory (current session)"""
        container = self.episodic_db.get_container_client(session_id)
        await container.upsert_item({
            "id": f"{session_id}_{event['timestamp']}",
            "agent_id": self.agent_id,
            "event": event,
            "ttl": 3600  # 1 hour expiry
        })
    
    async def store_longterm(self, customer_id: str, pattern: Dict):
        """Store long-term memory (preferences/habits)"""
        container = self.longterm_db.get_container_client("patterns")
        
        # Check if memory already exists
        existing = await self._get_existing_pattern(customer_id, pattern["type"])
        
        if existing:
            # Update existing memory (exponential moving average)
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
        """Retrieve relevant memories"""
        # 1. Retrieve short-term memory
        episodic = await self._get_episodic(customer_id, context)
        
        # 2. Retrieve long-term memory
        longterm = await self._get_longterm(customer_id)
        
        # 3. Retrieve semantic memory
        semantic = await self._get_semantic(context)
        
        # 4. Fuse memories
        return self._fuse_memories(episodic, longterm, semantic)
    
    def _fuse_memories(self, episodic: List, longterm: Dict, semantic: Dict) -> Dict:
        """Fuse three-layer memories"""
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

## Course Integration Summary

| Course | Technology | Integrated Agent | Value |
|--------|-----------|-----------------|-------|
| TT205 | Synthetic Persona | Customer Understanding | Cold start + privacy protection |
| TT203 | Three-Layer Hybrid Architecture | All Agents | ML precision + LLM reasoning |
| TT203 | Linear Regression / Elasticity | Pricing | Scientific pricing |
| WRK761 | Agent Memory | All Agents | Continuous learning |
| BRK180 | U-A-L Three Pillars | Personalization | Personalization closed loop |
| BRK177 | Foundry Gateway | Infrastructure | Production-grade architecture |
| LAB181 | Multi-Agent Collaboration | Orchestration | End-to-end automation |
| LAB184 | Responsible AI | Global | Compliance + security |
