# 5 Agent Detailed Design

## Agent 1: Customer Understanding Agent

### Responsibilities
Build a unified customer profile from multi-channel behaviors to achieve a 360° customer view.

### Input Data Sources
| Data Source | Type | Frequency | Azure Service |
|-------------|------|-----------|---------------|
| App / Mini Program Behavior | Clickstream, browsing, search | Real-time | Event Hubs |
| Store RFID | Store entry, fitting, purchase | Real-time | IoT Hub |
| JD / Tmall | Orders, reviews, browsing | Hourly sync | Data Factory |
| Membership System | Basic info, points, tier | Daily sync | Cosmos DB |
| Customer Service Records | Inquiries, complaints, returns | Real-time | Communication Services |

### Core Capabilities
1. **Unified Identity Resolution**: Cross-channel ID-Mapping (phone number, WeChat OpenID, member ID, device ID)
2. **Behavioral Sequence Modeling**: Temporal Transformer encoding of user behavior paths
3. **Synthetic Persona**: Generate virtual customers based on TT205 to address cold start and privacy issues
4. **Agent Memory**: Episodic (short-term interactions) + Long-term (long-term preferences) memory architecture

### Outputs
- Unified customer profile (JSON Schema)
- Behavior prediction vector (128-dimensional)
- Customer segmentation tags (RFM + behavioral clustering)

### Tech Stack
```python
# Azure Service Mapping
Azure OpenAI Service    # GPT-4o: behavior understanding, intent inference
Azure AI Foundry        # Agent orchestration
Cosmos DB               # Customer profile storage + vector search
Azure ML                # Behavior prediction model
Event Hubs              # Real-time data streams
```

### Implementation Steps
1. **Week 1**: Set up data pipelines (Event Hubs + Data Factory)
2. **Week 2**: Implement unified identity resolution (ID-Mapping algorithm)
3. **Week 3**: Train behavior prediction model (Azure ML)
4. **Week 4**: Integrate Agent Memory (Cosmos DB vector search)
5. **Week 5**: Synthetic Persona generation + cold start testing

---

## Agent 2: Personalization Agent

### Responsibilities
Dynamically customize product displays, emails, and recommendations based on customer profiles and real-time behavior.

### Inputs
| Data | Source | Purpose |
|------|--------|---------|
| Customer Profile | Customer Understanding Agent | Preference foundation |
| Real-time Behavior | Event Hubs | Context awareness |
| Inventory Status | Inventory Agent | Available products |
| Historical Conversion | Cosmos DB | Recommendation optimization |

### Core Capabilities
1. **U-A-L Three Pillars** (BRK180): Understand → Act → Learn
2. **Hybrid AI** (TT203): LLM reasoning + ML precision
3. **Cross-channel Consistency**: Unified recommendations across App → Store → Mini Program
4. **Real-time Personalization**: Page load response <200ms

### Outputs
- Personalized recommendation list (Top-N products)
- Next action suggestions (push/email/coupon)
- Recommendation rationale (explainability)

### Tech Stack
```python
Azure OpenAI Service    # GPT-4o: recommendation rationale generation
Azure ML                # Collaborative filtering + deep learning recommendation model
Cosmos DB               # Recommendation result caching
Azure Cache for Redis   # Real-time recommendation cache (<200ms)
```

### Implementation Steps
1. **Week 1**: Recommendation model training (Azure ML + collaborative filtering)
2. **Week 2**: LLM recommendation rationale generation (Azure OpenAI)
3. **Week 3**: Cross-channel recommendation consistency engine
4. **Week 4**: Real-time recommendation cache (Redis)
5. **Week 5**: A/B testing framework

---

## Agent 3: Inventory Agent

### Responsibilities
Demand forecasting + store-level inventory optimization + automatic replenishment.

### Inputs
| Data | Source | Frequency |
|------|--------|-----------|
| Historical Sales | POS System | Daily |
| Weather Data | Weather API | Hourly |
| Promotional Plans | Marketing System | Weekly |
| Competitive Data | Crawlers / API | Daily |
| RFID Inventory | Store System | Real-time |

### Core Capabilities
1. **Time Series Forecasting**: Prophet + LSTM hybrid model
2. **Demand Sensing**: Weather / holiday / promotional event-driven
3. **Automatic Replenishment**: Safety stock + Economic Order Quantity (EOQ)
4. **Slow-moving Alert**: Inventory turnover monitoring + promotional suggestions

### Outputs
- 7-day demand forecast per store
- Replenishment recommendations (SKU × Store × Quantity)
- Slow-moving inventory alert list
- Inventory health score

### Tech Stack
```python
Azure ML                # Time series forecasting model
Fabric Data Agent       # Data lake queries
Azure OpenAI Service    # Anomaly analysis, natural language reports
Cosmos DB               # Forecast result storage
```

### Implementation Steps
1. **Week 1**: Demand forecasting model training (Azure ML + Prophet)
2. **Week 2**: Weather / event feature engineering
3. **Week 3**: Replenishment algorithm (EOQ + safety stock)
4. **Week 4**: Slow-moving inventory alert rule engine
5. **Week 5**: Integration with Ariake Project warehouse system

---

## Agent 4: Pricing Agent

### Responsibilities
Dynamic pricing based on demand / competition / inventory to maximize profit.

### Inputs
| Data | Source | Purpose |
|------|--------|---------|
| Demand Forecast | Inventory Agent | Demand elasticity |
| Competitive Prices | Crawlers / API | Market positioning |
| Inventory Levels | Inventory Agent | Clearance / premium pricing |
| Customer Profile | Customer Understanding Agent | Price sensitivity |
| Cost Data | ERP System | Profit floor |

### Core Capabilities
1. **Three-layer Architecture** (TT203): Data → ML → LLM
2. **Price Elasticity Modeling**: Bayesian regression to estimate elasticity coefficients
3. **Competitive Response**: Real-time monitoring of competitor price changes
4. **Human-in-the-Loop**: Key decisions require human confirmation

### Outputs
- Dynamic pricing recommendations (SKU × Store × Price)
- Promotional strategies (discount / threshold reduction / bundling)
- Profit impact forecast
- Price anomaly alerts

### Tech Stack
```python
Azure ML                # Price elasticity model
Azure OpenAI Service    # Strategy reasoning, anomaly analysis
Azure Functions         # Pricing rule engine
Cosmos DB               # Price history + strategy storage
```

### Implementation Steps
1. **Week 1**: Price elasticity model (Bayesian regression)
2. **Week 2**: Competitive price monitoring pipeline
3. **Week 3**: Dynamic pricing algorithm
4. **Week 4**: Human-in-the-Loop approval workflow
5. **Week 5**: Profit impact simulator

---

## Agent 5: Marketing Agent

### Responsibilities
Autonomously run marketing campaigns + optimize budget allocation.

### Inputs
| Data | Source | Purpose |
|------|--------|---------|
| Customer Profile | Customer Understanding Agent | Precision targeting |
| Market Trends | Social media / search trends | Campaign planning |
| Competitive Dynamics | Competitor monitoring | Differentiation |
| Historical Campaigns | CRM System | Performance optimization |

### Core Capabilities
1. **Autonomous Decision Engine**: Reinforcement learning-based campaign optimization
2. **A/B Testing Framework**: Automated experiment design and analysis
3. **Budget Optimization**: ROI-maximizing budget allocation
4. **Multi-channel Orchestration**: WeChat / SMS / Push / Store coordination

### Outputs
- Marketing campaign plan (channel / timing / content / budget)
- A/B testing plan
- Budget allocation recommendations
- Campaign performance forecast

### Tech Stack
```python
Azure OpenAI Service    # Campaign copy generation, strategy reasoning
Azure ML                # ROI prediction model
Azure Communication Services # Multi-channel outreach
Application Insights    # Campaign performance tracking
```

### Implementation Steps
1. **Week 1**: Campaign template library + copy generation
2. **Week 2**: A/B testing framework
3. **Week 3**: Budget optimization algorithm
4. **Week 4**: Multi-channel orchestration engine
5. **Week 5**: Attribution analysis

---

## Inter-Agent Collaboration Protocol

### Data Flow
```
Customer Understanding Agent
    │
    ├──→ Personalization Agent (profile + predictions)
    ├──→ Marketing Agent (segmentation + outreach)
    │
Inventory Agent
    │
    ├──→ Pricing Agent (inventory levels)
    ├──→ Personalization Agent (available products)
    │
Pricing Agent
    │
    └──→ Marketing Agent (promotional strategies)
```

### Communication Protocols
- **Synchronous Calls**: REST API (APIM Gateway)
- **Asynchronous Events**: Event Hubs (decoupling)
- **State Sharing**: Cosmos DB (unified state storage)
- **Agent Orchestration**: Azure AI Foundry Agent Framework

### Conflict Resolution
- **Priority Mechanism**: Customer Understanding > Inventory > Pricing > Marketing
- **Human Arbitration**: Notify humans when conflicts exceed threshold
- **Rollback Mechanism**: Decisions can be rolled back to the last stable state
