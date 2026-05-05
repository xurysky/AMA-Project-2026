# Implementation Steps — From Zero to One

## Phase 1: Infrastructure Setup (Week 1)

### Step 1.1: Azure Environment Preparation
```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-ama-retail --location eastasia

# Create Azure OpenAI Service
az cognitiveservices account create \
  --name ama-openai \
  --resource-group rg-ama-retail \
  --kind OpenAI \
  --sku S0 \
  --location eastasia

# Deploy GPT-4o model
az cognitiveservices account deployment create \
  --name ama-openai \
  --resource-group rg-ama-retail \
  --deployment-name gpt-4o \
  --model-name gpt-4o \
  --model-version "2024-08-06" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name "Standard"
```

### Step 1.2: Data Layer Setup
```bash
# Create Cosmos DB (customer profiles + vector storage)
az cosmosdb create \
  --name ama-cosmos \
  --resource-group rg-ama-retail \
  --kind GlobalDocumentDB \
  --enable-serverless true

# Create Event Hubs (real-time data streams)
az eventhubs namespace create \
  --name ama-eventhub \
  --resource-group rg-ama-retail \
  --location eastasia \
  --sku Standard

# Create Azure ML Workspace
az ml workspace create \
  --name ama-ml \
  --resource-group rg-ama-retail \
  --location eastasia
```

### Step 1.3: Agent Orchestration Layer
```bash
# Create Azure AI Foundry resource
az cognitiveservices account create \
  --name ama-foundry \
  --resource-group rg-ama-retail \
  --kind AIServices \
  --sku S0 \
  --location eastasia
```

---

## Phase 2: Agent Development (Week 2-3)

### Step 2.1: Customer Understanding Agent
```python
# src/agents/customer_understanding.py

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

class CustomerUnderstandingAgent:
    def __init__(self):
        self.project_client = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint="https://ama-foundry.openai.azure.com/"
        )
    
    def build_unified_profile(self, customer_id: str) -> dict:
        """Build unified customer profile"""
        # 1. Fetch multi-channel data from Cosmos DB
        channels_data = self._fetch_channel_data(customer_id)
        
        # 2. Unified identity resolution
        unified_id = self._resolve_identity(channels_data)
        
        # 3. Behavior sequence modeling
        behavior_vector = self._encode_behavior(channels_data)
        
        # 4. LLM intent inference
        intent = self._infer_intent(channels_data)
        
        return {
            "customer_id": unified_id,
            "behavior_vector": behavior_vector,
            "intent": intent,
            "rfm_segment": self._calculate_rfm(channels_data),
            "preferences": self._extract_preferences(channels_data)
        }
```

### Step 2.2: Inventory Agent
```python
# src/agents/inventory.py

class InventoryAgent:
    def __init__(self):
        self.ml_client = MLClient(credential, subscription_id, resource_group)
    
    def forecast_demand(self, sku_id: str, store_id: str, days: int = 7):
        """Demand forecasting"""
        # 1. Get historical sales data
        history = self._get_sales_history(sku_id, store_id)
        
        # 2. Get external features (weather, promotions)
        features = self._get_external_features(store_id)
        
        # 3. Hybrid forecast (Prophet + LSTM)
        forecast = self._hybrid_forecast(history, features, days)
        
        # 4. Generate reorder suggestions
        reorder = self._calculate_reorder(sku_id, store_id, forecast)
        
        return {
            "forecast": forecast,
            "reorder_suggestion": reorder,
            "health_score": self._health_score(sku_id, store_id)
        }
```

### Step 2.3: Pricing Agent
```python
# src/agents/pricing.py

class PricingAgent:
    def __init__(self):
        self.openai_client = OpenAI(api_key=api_key, base_url=base_url)
    
    def dynamic_pricing(self, sku_id: str, store_id: str):
        """Dynamic pricing"""
        # 1. Get demand elasticity
        elasticity = self._get_elasticity(sku_id)
        
        # 2. Get competitor prices
        competitor_prices = self._get_competitor_prices(sku_id)
        
        # 3. Get inventory level
        inventory_level = self._get_inventory_level(sku_id, store_id)
        
        # 4. ML model calculates optimal price
        optimal_price = self._ml_pricing_model(
            elasticity, competitor_prices, inventory_level
        )
        
        # 5. LLM generates pricing rationale
        reasoning = self._generate_reasoning(
            sku_id, optimal_price, elasticity, competitor_prices
        )
        
        return {
            "optimal_price": optimal_price,
            "reasoning": reasoning,
            "profit_impact": self._estimate_profit_impact(sku_id, optimal_price)
        }
```

---

## Phase 3: Scenario Demos (Week 4)

### Scenario 1: Cross-Channel Personalized Recommendations
```
User browses in App → Agent understands preferences → Recommends outfits → In-store experience → Mini-program repurchase
```

### Scenario 2: Intelligent Inventory Management
```
RFID detects inventory → Agent forecasts demand → Auto-reorder → Slow-moving alerts → Promotion suggestions
```

### Scenario 3: Dynamic Pricing
```
Monitor competitor prices → Analyze demand elasticity → Calculate optimal price → Manual approval → Go live
```

---

## Phase 4: Integration Testing (Week 5)

### Test Matrix
| Test Type | Coverage | Tool |
|-----------|----------|------|
| Unit Tests | Each Agent | pytest |
| Integration Tests | Inter-Agent collaboration | Azure DevOps |
| Performance Tests | Response time <200ms | Locust |
| Security Tests | Data privacy | Azure Defender |

---

## Azure Resource Inventory

| Resource | Purpose | SKU |
|----------|---------|-----|
| Azure OpenAI Service | LLM inference | S0 |
| Cosmos DB | Customer profiles + vector storage | Serverless |
| Event Hubs | Real-time data streams | Standard |
| Azure ML | ML model training | Standard |
| Azure AI Foundry | Agent orchestration | S0 |
| Azure API Management | MCP Gateway | Standard |
| Azure Functions | Pricing rule engine | Consumption |
| Azure Cache for Redis | Recommendation caching | Standard |
| Azure Monitor | Observability | Basic |
