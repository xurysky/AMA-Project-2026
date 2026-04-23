# 实现步骤 — 从零到一

## Phase 1: 基础设施搭建（Week 1）

### Step 1.1: Azure 环境准备
```bash
# 登录 Azure
az login

# 创建资源组
az group create --name rg-ama-retail --location eastasia

# 创建 Azure OpenAI Service
az cognitiveservices account create \
  --name ama-openai \
  --resource-group rg-ama-retail \
  --kind OpenAI \
  --sku S0 \
  --location eastasia

# 部署 GPT-4o 模型
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

### Step 1.2: 数据层搭建
```bash
# 创建 Cosmos DB（客户画像 + 向量存储）
az cosmosdb create \
  --name ama-cosmos \
  --resource-group rg-ama-retail \
  --kind GlobalDocumentDB \
  --enable-serverless true

# 创建 Event Hubs（实时数据流）
az eventhubs namespace create \
  --name ama-eventhub \
  --resource-group rg-ama-retail \
  --location eastasia \
  --sku Standard

# 创建 Azure ML Workspace
az ml workspace create \
  --name ama-ml \
  --resource-group rg-ama-retail \
  --location eastasia
```

### Step 1.3: Agent 编排层
```bash
# 创建 Azure AI Foundry 资源
az cognitiveservices account create \
  --name ama-foundry \
  --resource-group rg-ama-retail \
  --kind AIServices \
  --sku S0 \
  --location eastasia
```

---

## Phase 2: Agent 开发（Week 2-3）

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
        """构建统一客户画像"""
        # 1. 从 Cosmos DB 获取多渠道数据
        channels_data = self._fetch_channel_data(customer_id)
        
        # 2. 统一身份解析
        unified_id = self._resolve_identity(channels_data)
        
        # 3. 行为序列建模
        behavior_vector = self._encode_behavior(channels_data)
        
        # 4. LLM 推理意图
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
        """需求预测"""
        # 1. 获取历史销售数据
        history = self._get_sales_history(sku_id, store_id)
        
        # 2. 获取外部特征（天气、促销）
        features = self._get_external_features(store_id)
        
        # 3. 混合预测（Prophet + LSTM）
        forecast = self._hybrid_forecast(history, features, days)
        
        # 4. 生成补货建议
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
        """动态定价"""
        # 1. 获取需求弹性
        elasticity = self._get_elasticity(sku_id)
        
        # 2. 获取竞争价格
        competitor_prices = self._get_competitor_prices(sku_id)
        
        # 3. 获取库存水平
        inventory_level = self._get_inventory_level(sku_id, store_id)
        
        # 4. ML 模型计算最优价格
        optimal_price = self._ml_pricing_model(
            elasticity, competitor_prices, inventory_level
        )
        
        # 5. LLM 生成定价理由
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

## Phase 3: 场景演示（Week 4）

### 场景 1: 跨渠道个性化推荐
```
用户在 App 浏览 → Agent 理解偏好 → 推荐搭配 → 门店体验 → 小程序复购
```

### 场景 2: 智能库存管理
```
RFID 检测库存 → Agent 预测需求 → 自动补货 → 滞销预警 → 促销建议
```

### 场景 3: 动态定价
```
监控竞争价格 → 分析需求弹性 → 计算最优价格 → 人工审批 → 生效
```

---

## Phase 4: 集成测试（Week 5）

### 测试矩阵
| 测试类型 | 覆盖范围 | 工具 |
|----------|---------|------|
| 单元测试 | 每个 Agent | pytest |
| 集成测试 | Agent 间协作 | Azure DevOps |
| 性能测试 | 响应时间 <200ms | Locust |
| 安全测试 | 数据隐私 | Azure Defender |

---

## Azure 资源清单

| 资源 | 用途 | SKU |
|------|------|-----|
| Azure OpenAI Service | LLM 推理 | S0 |
| Cosmos DB | 客户画像 + 向量存储 | Serverless |
| Event Hubs | 实时数据流 | Standard |
| Azure ML | ML 模型训练 | Standard |
| Azure AI Foundry | Agent 编排 | S0 |
| Azure API Management | MCP Gateway | Standard |
| Azure Functions | 定价规则引擎 | Consumption |
| Azure Cache for Redis | 推荐缓存 | Standard |
| Azure Monitor | 可观测性 | 基础 |
