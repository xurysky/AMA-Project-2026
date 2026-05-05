# Autonomous Retail Intelligence Agent Platform

> **AMA Capstone Project — Project 46**
> 基于优衣库（迅销集团）的多 Agent 智能零售平台设计

## 📋 项目概述

本项目设计并实现一个由 5 个 AI Agent 驱动的智能零售平台，以优衣库为原型，展示如何通过 Agent 架构实现跨渠道个性化体验、库存优化和动态定价。

### 核心指标

| 指标 | 基线 | 目标 | 提升幅度 |
|------|------|------|---------|
| 同店销售增长 | +11.7% (2025) | +40% | Agent 个性化驱动 |
| 库存浪费 | 行业平均 30%+ | -50% | Agent 需求预测 |
| 客户满意度 | 未公开 | 85% | Agent 体验优化 |
| 客户终身价值 | 2 亿粉丝基础 | +60% | Agent 持续关系管理 |
| 电商渗透率 | 25% (大中华区) | 35%+ | Agent 跨渠道推荐 |

## 🏗️ 架构设计

### 整体架构（三层 + 五 Agent）

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│   App / 小程序 / Web / 门店 POS / 智能穿戴设备 / 京东/天猫    │
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
│  + 合成 Persona (TinyTroupe) + 向量数据库 + RFID 数据        │
└─────────────────────────────────────────────────────────────┘
```

### 5 Agent 详细设计

详见 [docs/agents.md](docs/agents.md)

### 优衣库案例研究

详见 [docs/uniqlo-case-study.md](docs/uniqlo-case-study.md)

### 亚洲特殊性方案

详见 [docs/asia-specific.md](docs/asia-specific.md)

## 📁 项目结构

```
ama-project/
├── README.md                    # 项目概述
├── docs/
│   ├── agents.md                # 5 Agent 详细设计
│   ├── uniqlo-case-study.md     # 优衣库案例研究
│   ├── asia-specific.md         # 亚洲特殊性方案
│   ├── architecture.md          # 技术架构文档
│   ├── implementation.md        # 实现步骤
│   └── qa-preparation.md        # Q&A 准备
├── src/
│   ├── agents/                  # Agent 实现代码
│   │   ├── customer_understanding.py
│   │   ├── personalization.py
│   │   ├── inventory.py
│   │   ├── pricing.py
│   │   └── marketing.py
│   ├── infra/                   # 基础设施配置
│   │   ├── azure-bicep/         # Azure Bicep 模板
│   │   └── docker/              # 容器配置
│   └── scenarios/               # 业务场景演示
│       ├── scenario1_cross_channel.py
│       ├── scenario2_inventory.py
│       └── scenario3_pricing.py
├── assets/                      # 图片、图表等
└── scripts/                     # 部署和测试脚本
```

## 🚀 快速开始

### 前置条件

- Azure 订阅（Visual Studio Enterprise）
- Python 3.10+
- Azure CLI
- Docker (可选)

### 安装

```bash
git clone https://github.com/<your-org>/ama-project.git
cd ama-project
pip install -r requirements.txt
```

### 配置

```bash
cp .env.example .env
# 编辑 .env 填入 Azure 凭据
```

### 运行演示

```bash
# 场景 1：跨渠道个性化推荐
python src/scenarios/scenario1_cross_channel.py

# 场景 2：智能库存管理
python src/scenarios/scenario2_inventory.py

# 场景 3：动态定价
python src/scenarios/scenario3_pricing.py
```

## 📊 预期效果数据支撑

| 指标 | 数据来源 | 支撑逻辑 |
|------|---------|---------|
| 同店销售 +40% | McKinsey: AI 个性化可提升 20-35% 转化率 | 5 Agent 协同个性化 |
| 库存 -50% | Gartner: AI 需求预测可减少 20-50% 库存 | Inventory Agent 精准预测 |
| 满意度 85% | Forrester: AI 客服可提升 25% 满意度 | 全渠道 Agent 体验 |
| CLV +60% | Harvard: 个性化可提升 40% CLV | 持续关系管理 |

## 📅 项目时间线

| 阶段 | 时间 | 交付物 |
|------|------|--------|
| 知识沉淀 | 4/1 - 4/7 | 技术组件清单 ✅ |
| 架构设计 | 4/8 - 4/21 | 架构图 v1 ✅ |
| 方案撰写 | 4/22 - 5/5 | PPT + 文档 |
| 演练打磨 | 5/6 - 5/11 | 最终版本 |
| Panel | 5/11 - 5/21 | 答辩 |

## 👥 团队

- **Project Lead**: Yuan Wang (圆子)
- **Role**: Senior Cloud Solution Architect, Azure & AI Platform

## 📄 License

MIT License — 仅供学术研究使用
