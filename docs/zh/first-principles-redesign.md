# 第一性原理重构：自主零售智能代理平台

## 1. 第一性原理

零售智能的本质不是在架构图里放 5 个 Agent，而是优化一个互相耦合的业务决策系统：

> 在合适时间、合适渠道、以合适价格，把合适商品推荐给合适顾客，同时保证库存、毛利、隐私和运营风险不失控。

因此，本项目重构为场景驱动的决策闭环：

`突然降温 -> 需求上升 -> 库存风险 -> 定价护栏 -> 客户意图 -> 个性化推荐 -> 营销触达 -> 人工审批 -> 反馈学习`

## 2. 当前演示实现

当前原型已经实现：

- 统一 `Retail State` 场景数据：`data/fixtures/cold_snap.json`
- 场景决策引擎：`src/scenario_engine.py`
- 五个 Agent 消费前序 Agent 输出，而不是孤立硬编码
- 专业 Agent Control Tower UI：`/`
- 场景 API：`/api/v1/scenario/cold-snap`
- API 输出中包含技术模式映射和数据来源映射

原型不声称已经验证生产 ROI。销售 +40%、库存浪费 -50%、满意度 85%、CLV +60% 是课题目标假设，不是当前 demo 已验证结果。

## 3. 五个 Agent 的真实职责

| Agent | 业务问题 | 输入 | 输出 |
|---|---|---|---|
| Inventory Agent | 哪些 SKU 会缺货或积压？ | 天气、销量、浏览、加购、RFID、仓库库存 | 需求预测、库存风险、补货建议 |
| Pricing Agent | 在库存和毛利约束下，什么价格动作是安全的？ | 库存风险、成本、竞品价格、审批规则 | 价格策略、建议价格、审批标记 |
| Customer Understanding Agent | 谁有高购买意图且允许触达？ | 行为、会员、位置、渠道偏好、授权 | 目标客群、意图分、隐私友好画像 |
| Personalization Agent | 每个客户下一步该看到什么？ | 客户意图、库存风险、价格策略 | 个性化推荐和理由 |
| Marketing Agent | 触达谁、用什么渠道、花多少预算？ | 推荐、渠道指标、库存风险、授权 | 营销计划、A/B 测试、审批队列 |

## 4. 技术模式映射

- **Synthetic Persona**：合成 Persona 与客户行为模拟，用于客户理解和冷启动。
- **U-A-L**：Understand -> Act -> Learn 个性化闭环。
- **Hybrid AI**：数据层 + ML 校验 + LLM 业务推理。
- **Agent Memory**：Agent Memory：短期、情节、长期记忆。
- **Real-Time Architecture**：MCP/API Gateway，用于连接零售工具、竞品监控、支付和渠道 API。
- **Multi-Agent**：多 Agent 应用模式和 Spec Driven Development。
- **Responsible AI**：Responsible AI、隐私、审批和审计。

## 5. Azure 原生目标架构

当前原型：

`FastAPI + Scenario Engine + Static UI + Azure OpenAI-ready integration`

目标架构：

`Azure Container Apps + Azure AI Foundry + Event Hubs + Cosmos DB/Fabric + Azure ML + APIM/MCP Gateway + Application Insights`

这版演示的定位更诚实：先证明业务决策链路，再映射到 Azure 原生生产架构。
