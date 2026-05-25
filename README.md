# Autonomous Retail Intelligence Agent Platform

> **AMA Capstone Project — Project 46**
> Multi-Agent Intelligent Retail Platform based on Contoso Fashion (Contoso Retail)
> 基于Contoso 服装店的多 Agent 智能零售平台设计

---

🌐 **Language / 语言**: [English](#english) | [简体中文](#简体中文)

---

<a id="english"></a>
## 🇬🇧 English

### Overview

This project designs a multi-agent intelligent retail platform powered by 5 AI Agents, using Contoso Fashion as the prototype to demonstrate cross-channel personalization, inventory optimization, and dynamic pricing.

### Key Metrics

| Metric | Baseline | Target | Driver |
|--------|----------|--------|--------|
| Same-store sales growth | +11.7% (2025) | +40% | Agent-driven personalization |
| Inventory waste | Industry avg 30%+ | -50% | Agent demand forecasting |
| Customer satisfaction | N/A | 85% | Agent experience optimization |
| Customer lifetime value | 200M fan base | +60% | Agent relationship management |
| E-commerce penetration | 25% (Greater China) | 35%+ | Agent cross-channel recommendations |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│   App / Mini Program / Web / Store POS / IoT / JD/Tmall     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Orchestration Layer                         │
│          Azure AI Foundry + Agent Framework                  │
│          + A2A Protocol + MCP Gateway (APIM)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    5 Agent Layer                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────┐│
│  │ Customer │ │Personal- │ │Inventory │ │Pricing │ │Mktg  ││
│  │Understand│ │ization   │ │  Agent   │ │ Agent  │ │Agent ││
│  │  Agent   │ │  Agent   │ │          │ │        │ │      ││
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ └──────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Data & Infrastructure Layer                   │
│  Azure OpenAI / Fabric / Cosmos DB / APIM / Azure ML        │
│  + Synthetic Persona (TinyTroupe) + Vector DB + RFID         │
└─────────────────────────────────────────────────────────────┘
```

### Azure-native deployment model

The prototype is **containerized for demonstration** and should be presented as an Azure-native architecture, not as a single VM-hosted application:

```text
Azure Static Web Apps / Browser
  -> Azure Container Apps: FastAPI Agent Runtime
  -> Azure OpenAI / Azure AI Foundry: agent reasoning and orchestration
  -> Azure Cosmos DB: run state, work orders, shared memory and audit logs
  -> Application Insights + Log Analytics: observability
  -> API Management / Managed Identity / Key Vault: enterprise integration and security
```

The included `infra/main.bicep` and `.github/workflows/azure-container-apps.yml` deploy the demo runtime to Azure Container Apps with Cosmos DB-backed run persistence. A VM can be used as a temporary demo host, but it is not the intended target architecture.

See [Azure-native deployment](docs/en/azure-native-deployment.md).


### Scenario-driven demo (v4) — 15-Day Fashion Retail Launch

The latest demo is inspired by full-chain fashion retail AI automation benchmarks such as "6 months → 15 days" launch-cycle compression. It reframes the project as a **Fashion Retail AI Operating System**: an Agent Boss coordinates trend insight, product planning, AIGC visual generation, CTR testing, consumer-language copywriting, live commerce, inventory, pricing, marketing, finance ROI review, compliance and human approval.

Key demo loops:

1. **6 months → 15 days**: sequential apparel launch becomes parallel agent workflow.
2. **AIGC visual + CTR testing**: generate multiple model/scene variants in minutes, select winner by simulated CTR.
3. **Digital human live commerce**: recover unmanned long-tail live slots and write unanswered questions back to FAQ knowledge.
4. **AI + BI + Automation**: Azure AI is the brain, Fabric/Power BI are the eyes, Logic Apps/Power Automate/APIM are the hands.

> All ROI, CTR, cycle-compression and cost-saving numbers in the demo are simulation assumptions / target hypotheses, not validated production results.

Open the current UI:

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8080
# Open http://localhost:8080/workflow?v=semir-v4
```

Core stateful endpoint:

```bash
curl -X POST "http://localhost:8080/api/v1/runs/summer?region=china"
```

### Scenario-driven demo (v2)

The demo has been redesigned around first principles: retail decisions are interdependent. Pricing cannot ignore inventory; marketing cannot ignore customer intent; personalization cannot recommend out-of-stock items.

Run the API and open the Agent Control Tower:

```bash
pip install -r requirements.txt
uvicorn src.api:app --host 0.0.0.0 --port 8080
# Open http://localhost:8080
```

Core endpoint:

```bash
curl -X POST http://localhost:8080/api/v1/scenario/cold-snap
```

The current prototype implements a unified Retail State (`data/fixtures/cold_snap.json`) and a five-agent decision loop:

1. Inventory Agent: demand spike and stockout risk
2. Pricing Agent: guardrailed pricing under inventory and margin constraints
3. Customer Understanding Agent: high-intent, consent-aware customer profile
4. Personalization Agent: recommendations constrained by stock and pricing
5. Marketing Agent: precision campaign, A/B test, and human approval queue

See also:

- [First-principles redesign](docs/en/first-principles-redesign.md)

> Note: sales +40%, inventory waste -50%, satisfaction 85%, and CLV +60% are target business hypotheses from the AMA brief, not validated production results from this prototype.

### Documentation

| Document | Description |
|----------|-------------|
| [Agent Design](docs/en/agents.md) | 5 Agent detailed design |
| [Agent Collaboration](docs/en/agent-collaboration.md) | Handoff / Reflection / State Graph patterns |
| [Architecture Decisions](docs/en/architecture-decisions.md) | 8 ADRs with rationale |
| [Contoso Fashion Case Study](docs/en/uniqlo-case-study.md) | Prototype analysis |
| [Asia Specifics](docs/en/asia-specific.md) | Regional considerations |
| [Security Architecture](docs/en/security-architecture.md) | Zero-trust design |
| [CI/CD & Day 2 Ops](docs/en/cicd-day2ops.md) | Deployment pipeline |
| [Monitoring & Observability](docs/en/monitoring-observability.md) | Logging, metrics, alerting |
| [Performance & Reliability](docs/en/performance-reliability.md) | HA, DR, scalability |
| [Azure-native Deployment](docs/en/azure-native-deployment.md) | Container Apps + Cosmos DB deployment path |
| [Testing Strategy](docs/en/testing-strategy.md) | Multi-layer testing |
| [Tech Integration](docs/en/tech-integration.md) | Design Pattern knowledge mapping |
| [Implementation Plan](docs/en/implementation.md) | Step-by-step guide |
| [Q&A Preparation](docs/en/qa-preparation.md) | 15 panel questions + C-suite cheat sheet |

### Quick Start

```bash
git clone https://github.com/dowa_microsoft/AMA-Project-2026.git
cd AMA-Project-2026
pip install -r requirements.txt
cp .env.example .env

# Run demo (mock mode, no Azure required)
python -m src.scenarios.scenario1_cross_channel
```

### Expected Impact

| Metric | Source | Logic |
|--------|--------|-------|
| Sales +40% | McKinsey: AI personalization boosts 20-35% conversion | 5-agent collaboration |
| Inventory -50% | Gartner: AI forecasting reduces 20-50% waste | Inventory agent |
| Satisfaction 85% | Forrester: AI service improves satisfaction by 25% | Omnichannel agent |
| CLV +60% | Harvard: personalization improves CLV by 40% | Relationship management |

### Team

- **Project Lead**: Yuan Wang
- **Role**: Senior Solution Engineer, Cloud & AI Platform (CAIP)

### License

MIT License — For academic research only

---

<a id="简体中文"></a>
## 🇨🇳 简体中文

### 项目概述

本项目设计并实现一个由 5 个 AI Agent 驱动的智能零售平台，以Contoso 服装店为原型，展示如何通过 Agent 架构实现跨渠道个性化体验、库存优化和动态定价。

### 核心指标

| 指标 | 基线 | 目标 | 提升幅度 |
|------|------|------|---------|
| 同店销售增长 | +11.7% (2025) | +40% | Agent 个性化驱动 |
| 库存浪费 | 行业平均 30%+ | -50% | Agent 需求预测 |
| 客户满意度 | 未公开 | 85% | Agent 体验优化 |
| 客户终身价值 | 2 亿粉丝基础 | +60% | Agent 持续关系管理 |
| 电商渗透率 | 25% (大中华区) | 35%+ | Agent 跨渠道推荐 |

### 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    用户界面层                                │
│   App / 小程序 / Web / 门店 POS / 智能穿戴设备 / 京东/天猫    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  编排层                                      │
│          Azure AI Foundry + Agent Framework                  │
│          + A2A Protocol + MCP Gateway (APIM)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    5 Agent 层                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────┐│
│  │ 客户理解 │ │ 个性化   │ │ 库存优化 │ │动态定价│ │营销  ││
│  │  Agent   │ │  Agent   │ │  Agent   │ │ Agent  │ │Agent ││
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ └──────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                数据与基础设施层                               │
│  Azure OpenAI / Fabric / Cosmos DB / APIM / Azure ML        │
│  + 合成 Persona (TinyTroupe) + 向量数据库 + RFID 数据        │
└─────────────────────────────────────────────────────────────┘
```

### Azure 云原生部署模型

本原型已经容器化，建议按 **Azure 云原生架构** 呈现，而不是“单台 VM 托管一个应用”：

```text
Azure Static Web Apps / 浏览器
  -> Azure Container Apps: FastAPI Agent Runtime
  -> Azure OpenAI / Azure AI Foundry: Agent 推理与编排
  -> Azure Cosmos DB: run state、工单、shared memory、审计日志
  -> Application Insights + Log Analytics: 可观测性
  -> API Management / Managed Identity / Key Vault: 企业集成与安全
```

仓库已包含 `infra/main.bicep` 和 `.github/workflows/azure-container-apps.yml`，可将 demo runtime 部署到 Azure Container Apps，并使用 Cosmos DB 持久化 run 状态。VM 只能作为临时演示承载方式，不是目标架构。

详见 [Azure 云原生部署](docs/zh/azure-native-deployment.md)。

### 文档目录

| 文档 | 说明 |
|------|------|
| [Agent 设计](docs/zh/agents.md) | 5 Agent 详细设计 |
| [Agent 协作](docs/zh/agent-collaboration.md) | Handoff / Reflection / State Graph 模式 |
| [架构决策](docs/zh/architecture-decisions.md) | 8 个 ADR（含理由和权衡） |
| [Contoso 服装店案例](docs/zh/uniqlo-case-study.md) | 原型分析 |
| [亚洲特殊性](docs/zh/asia-specific.md) | 区域性考量 |
| [安全架构](docs/zh/security-architecture.md) | 零信任设计 |
| [CI/CD 与运维](docs/zh/cicd-day2ops.md) | 部署流水线 |
| [监控与可观测性](docs/zh/monitoring-observability.md) | 日志、指标、告警 |
| [性能与可靠性](docs/zh/performance-reliability.md) | 高可用、灾备、扩展性 |
| [Azure 云原生部署](docs/zh/azure-native-deployment.md) | Container Apps + Cosmos DB 部署路径 |
| [测试策略](docs/zh/testing-strategy.md) | 多层测试 |
| [技术集成](docs/zh/tech-integration.md) | 技术模式映射 |
| [实现计划](docs/zh/implementation.md) | 分步指南 |
| [Q&A 准备](docs/zh/qa-preparation.md) | 15 个 Panel 问题 + C-suite 速查表 |

### 快速开始

```bash
git clone https://github.com/dowa_microsoft/AMA-Project-2026.git
cd AMA-Project-2026
pip install -r requirements.txt
cp .env.example .env

# 运行演示（Mock 模式，无需 Azure）
python -m src.scenarios.scenario1_cross_channel
```

### 预期效果

| 指标 | 数据来源 | 支撑逻辑 |
|------|---------|---------|
| 销售 +40% | McKinsey: AI 个性化提升 20-35% 转化率 | 5 Agent 协同 |
| 库存 -50% | Gartner: AI 预测减少 20-50% 库存 | Inventory Agent |
| 满意度 85% | Forrester: AI 客服提升 25% 满意度 | 全渠道 Agent |
| CLV +60% | Harvard: 个性化提升 40% CLV | 持续关系管理 |

### 团队

- **项目负责人**: Yuan Wang (圆子)
- **角色**: 资深解决方案工程师, Cloud & AI Platform (CAIP)

### 许可证

MIT License — 仅供学术研究使用
