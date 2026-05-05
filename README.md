# Autonomous Retail Intelligence Agent Platform

> **AMA Capstone Project — Project 46**
> Multi-Agent Intelligent Retail Platform based on Uniqlo (Fast Retailing)
> 基于优衣库（迅销集团）的多 Agent 智能零售平台设计

---

🌐 **Language / 语言**: [English](#english) | [简体中文](#简体中文)

---

<a id="english"></a>
## 🇬🇧 English

### Overview

This project designs a multi-agent intelligent retail platform powered by 5 AI Agents, using Uniqlo as the prototype to demonstrate cross-channel personalization, inventory optimization, and dynamic pricing.

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

### Documentation

| Document | Description |
|----------|-------------|
| [Agent Design](docs/en/agents.md) | 5 Agent detailed design |
| [Agent Collaboration](docs/en/agent-collaboration.md) | Handoff / Reflection / State Graph patterns |
| [Architecture Decisions](docs/en/architecture-decisions.md) | 8 ADRs with rationale |
| [Uniqlo Case Study](docs/en/uniqlo-case-study.md) | Prototype analysis |
| [Asia Specifics](docs/en/asia-specific.md) | Regional considerations |
| [Security Architecture](docs/en/security-architecture.md) | Zero-trust design |
| [CI/CD & Day 2 Ops](docs/en/cicd-day2ops.md) | Deployment pipeline |
| [Monitoring & Observability](docs/en/monitoring-observability.md) | Logging, metrics, alerting |
| [Performance & Reliability](docs/en/performance-reliability.md) | HA, DR, scalability |
| [Testing Strategy](docs/en/testing-strategy.md) | Multi-layer testing |
| [Tech Integration](docs/en/tech-integration.md) | Course knowledge mapping |
| [Implementation Plan](docs/en/implementation.md) | Step-by-step guide |
| [Q&A Preparation](docs/en/qa-preparation.md) | 15 panel questions + C-suite cheat sheet |

### Quick Start

```bash
git clone https://github.com/xurysky/AMA-Project-2026.git
cd AMA-Project-2026
pip install -r requirements.txt
cp .env.example .env

# Run demo (mock mode, no Azure required)
python -m src.scenarios.scenario1_cross_channel
```

### Expected Impact

| Metric | Source | Logic |
|--------|--------|-------|
| Sales +40% | McKinsey: AI personalization boosts 20-35% conversion | 5 Agent协同 |
| Inventory -50% | Gartner: AI forecasting reduces 20-50% waste | Inventory Agent |
| Satisfaction 85% | Forrester: AI service提升25% satisfaction | Omnichannel Agent |
| CLV +60% | Harvard: personalization提升40% CLV | Relationship management |

### Team

- **Project Lead**: Yuan Wang
- **Role**: Senior Solution Engineer, Azure & AI Platform

### License

MIT License — For academic research only

---

<a id="简体中文"></a>
## 🇨🇳 简体中文

### 项目概述

本项目设计并实现一个由 5 个 AI Agent 驱动的智能零售平台，以优衣库为原型，展示如何通过 Agent 架构实现跨渠道个性化体验、库存优化和动态定价。

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

### 文档目录

| 文档 | 说明 |
|------|------|
| [Agent 设计](docs/zh/agents.md) | 5 Agent 详细设计 |
| [Agent 协作](docs/zh/agent-collaboration.md) | Handoff / Reflection / State Graph 模式 |
| [架构决策](docs/zh/architecture-decisions.md) | 8 个 ADR（含理由和权衡） |
| [优衣库案例](docs/zh/uniqlo-case-study.md) | 原型分析 |
| [亚洲特殊性](docs/zh/asia-specific.md) | 区域性考量 |
| [安全架构](docs/zh/security-architecture.md) | 零信任设计 |
| [CI/CD 与运维](docs/zh/cicd-day2ops.md) | 部署流水线 |
| [监控与可观测性](docs/zh/monitoring-observability.md) | 日志、指标、告警 |
| [性能与可靠性](docs/zh/performance-reliability.md) | 高可用、灾备、扩展性 |
| [测试策略](docs/zh/testing-strategy.md) | 多层测试 |
| [技术集成](docs/zh/tech-integration.md) | 课程知识映射 |
| [实现计划](docs/zh/implementation.md) | 分步指南 |
| [Q&A 准备](docs/zh/qa-preparation.md) | 15 个 Panel 问题 + C-suite 速查表 |

### 快速开始

```bash
git clone https://github.com/xurysky/AMA-Project-2026.git
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
- **角色**: 资深解决方案工程师, Azure & AI 平台

### 许可证

MIT License — 仅供学术研究使用
