# Retail Merchandise Operations Decision Case Platform

> **AMA Capstone Project — Project 46**
> Multi-Agent Intelligent Retail Platform based on Contoso Fashion (Contoso Retail)
> 基于Contoso 服装店的多 Agent 智能零售平台设计

---

🌐 **Language / 语言**: [English](#english) | [简体中文](#简体中文)

---

<a id="english"></a>
## 🇬🇧 English

### Overview

This project implements a realistic fashion-retail exception handling and decision platform powered by five AI capability domains. A shared Retail Decision Case connects planning policy, operational signals, multi-agent reasoning, controlled execution, and measurable feedback.

### Operational Proof Metrics

| Metric | Prototype evidence |
|--------|--------------------|
| Decision latency | Case detection to versioned Decision Packet |
| Inventory safety | ATP deducts reservations, safety stock, frozen and outbound units |
| Decision quality | Low-confidence stock pauses commercial action and creates a cycle-count task |
| Governance | Role-based approval, policy lineage and immutable audit events |
| Execution reliability | Idempotency, retry, partial-failure receipt and compensation path |

Sales uplift and margin impact are not claimed by the prototype. They require a time-boxed test/control store experiment.

### Current Demo (v3) — Retail Decision Cases

The production-shaped demo supports two bounded workflows:

1. `BROKEN_SIZE_STOCKOUT`: ATP, size breaks, cycle count, replenishment/transfer and `NO_CAMPAIGN`.
2. `SEASONAL_OVERSTOCK`: transfer, promotion versus markdown, margin guardrails and store-capacity constraints.

Five agents participate only when a case needs their domain judgment. Deterministic services calculate stock, margin, consent and policy facts; the LLM explains evidence and recommendations but does not invent transactional truth.

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8080
# Open http://localhost:8080/workflow
```

The UI follows real operating roles instead of exposing the orchestration model:

- **Store Manager** receives concrete store tasks such as cycle counts and submits physical truth.
- **Regional Manager** reviews store impact and approves transfers or replenishment within regional authority.
- **International Management** compares market planning contexts and approves strategic promotion, pricing, and resource-allocation decisions.
- **AI Decision Intelligence** shows a seven-day demand range, discount sensitivity, option comparison, channel supply caps, five-agent collaboration, guardrails, and post-decision learning checkpoints.
- Technical Agent output, packet IDs, and policy versions stay inside on-demand audit details.

The current UI also integrates the useful capabilities from the earlier platform without mixing simulation with production execution:

- **SKU Portfolio** connects case-level variants to seasonal assortment planning.
- **Data & Signals** maps source systems and feature groups to time-stamped Case evidence.
- **Agent Capabilities** links the five-agent registry to actual Case participation, skip and block states.
- **Scenario Lab** preserves the four-season model as a read-only planning sandbox.
- `/` and `/workflow` serve the integrated platform; the former full-platform demo remains available at `/legacy`.

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


### Legacy compatibility demo (v4) — 15-Day Fashion Retail Launch

This earlier scenario is retained for API compatibility. It is no longer the primary Project 46 operating model.

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
| [Project 46 Architecture Decision Document](docs/en/project-46-architecture-decision-document.md) | Review-ready scenario assumptions and architecture decisions |
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

本项目实现一个面向服装零售真实经营异常的五 Agent 协同决策平台。系统以统一的 Retail Decision Case 串联计划政策、经营信号、多 Agent 判断、受控执行和结果反馈，而不是让 AI 直接自动经营门店。

### 可验证运营指标

| 指标 | 原型证据 |
|------|----------|
| 决策时效 | 从异常形成到生成带版本的 Decision Packet |
| 库存安全 | ATP 扣除软预留、安全库存、冻结品和待调出库存 |
| 决策质量 | 库存可信度不足时暂停商业动作并创建门店盘点任务 |
| 治理完整性 | 角色审批、政策版本和完整审计事件 |
| 执行可靠性 | 幂等、重试、部分失败回执和补偿路径 |

系统不把销售或毛利增量作为已经实现的结果；业务增量必须通过 test/control 门店实验验证。

### 当前演示（v3）— Retail Decision Case

当前主版本聚焦两个边界清晰的真实流程：

1. `BROKEN_SIZE_STOCKOUT`：ATP、断码、盘点、补货/调拨和 `NO_CAMPAIGN`。
2. `SEASONAL_OVERSTOCK`：调拨、促销与 markdown、毛利护栏和门店容量约束。

五个 Agent 根据 Case 类型按需参与。库存、毛利、授权和政策事实由确定性服务计算，LLM 只负责证据解释与建议表达。

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8080
# 打开 http://localhost:8080/workflow
```

界面按照真实岗位职责设计，不要求业务用户理解底层编排：

- **门店店长**：只接收盘点、收货等门店任务并提交实物真值。
- **区域经理**：查看区域影响，在权限内审批调拨和补货。
- **跨国经营管理层**：比较各国家/区域规划上下文，审批促销、价格例外与资源配置等重大经营方案。
- **AI 决策智能**：展示 7 天需求区间、折扣敏感度、方案比较、渠道供货上限、五 Agent 协作、护栏和决策后的学习节点。
- Agent 输出、决策包 ID 和政策版本默认收进按需展开的审计详情。

当前界面也整合了原系统中有价值的能力，但不会再把沙盘和生产执行混在一起：

- **SKU 组合**：关联 Case 商品变体与季节商品规划。
- **数据与信号**：把原数据源和 Feature Store 映射到带时间快照的 Case 证据。
- **Agent 能力**：将五 Agent Registry 与实际参与、跳过和阻断状态关联。
- **四季沙盘**：保留原四季模型，定位为只读计划模拟。
- `/` 与 `/workflow` 进入统一平台，原完整演示保留在 `/legacy`。

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
