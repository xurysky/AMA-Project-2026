# AMA 项目46逐页口述脚本 / Project 46 Speaker Script

用途：配合新版中文和英文 PPT。中文可直接用于答辩；英文保持简单口语，方便现场切换。

## Slide 1: 封面 / Cover

中文：
我今天用一条更清楚的故事线讲 Project 46：五个 Agent 不是五个聊天机器人，而是一套能跑通发现、核验、决策、执行和复盘的零售经营系统。

English:
Today I will present Project 46 with a clearer storyline. The five Agents are not five chatbots. They form an operating system for discover, verify, decide, execute and learn.

## Slide 2: 今天的故事线 / Today’s Storyline

中文：
这页先告诉评委我会怎么讲。前面回答题目要求，中间解释页面组件为什么存在，后面讲系统演示和 Azure 企业级落地。

English:
This slide shows the flow. I first answer the assignment prompt, then explain why each product component exists, and finally show the demo and Azure implementation.

## Slide 3: 1. 核心问题 / 1. The Core Problem

中文：
核心问题是零售企业有很多渠道，但没有一个跨渠道可信决策闭环。个性化如果脱离库存、价格、授权和履约，就会变成不可靠建议。

English:
The core problem is that retailers have many channels, but not one trusted cross-channel decision loop. Personalization becomes unreliable if it ignores inventory, pricing, consent and fulfillment.

## Slide 4: 2. 题目要求如何被覆盖 / 2. Prompt Coverage

中文：
这页证明没有偏题。客户数据整合、全渠道个性化、五个 Agent、优势、成功标准和亚洲挑战，都在系统里有对应设计。

English:
This slide proves the project stays on prompt. Customer data integration, omni-channel personalization, five Agents, advantages, success criteria and Asia challenges are all covered.

## Slide 5: 3. 经营闭环 / 3. Operating Loop

中文：
完整闭环是发现、核验、决策、执行和复盘。四季沙盘发现风险，数据与信号核验事实，Agent 形成方案，授权角色审批执行，结果再进入学习。

English:
The full loop is discover, verify, decide, execute and learn. The seasonal sandbox detects risk, data and signals verify facts, Agents generate options, authorized roles approve execution, and results feed learning.

## Slide 6: 4. SKU 组合为什么存在 / 4. Why SKU Combinations Exist

中文：
SKU 组合是零售决策的最小粒度。同一商品在不同尺码、颜色、门店和生命周期阶段风险不同，所以 AI 必须围绕具体组合做判断。

English:
SKU combination is the smallest unit for retail decisions. The same product has different risk by size, color, store and lifecycle, so AI must reason at the exact combination level.

## Slide 7: 5. 数据与信号为什么存在 / 5. Why Data and Signals Exist

中文：
数据与信号区回答可信度问题：哪些是已发生事实，哪些是外部信号，哪些只是情景模拟。这样可以避免把预测当成真实销售。

English:
The data and signals section answers confidence. Which inputs are facts, which are external signals, and which are scenario simulations. This prevents forecasts from being presented as real sales.

## Slide 8: 6. 业务规则为什么存在 / 6. Why Business Rules Exist

中文：
业务规则是企业护栏。未授权客户不能触达，低可信库存不能推荐，低于毛利底线的折扣要阻断，高风险动作必须进入审批。

English:
Business rules are enterprise guardrails. No contact without consent, no recommendation on low-confidence inventory, discounts below margin floor are blocked, and high-risk actions require approval.

## Slide 9: 7. 四季沙盘的目的 / 7. Why the Four-Season Sandbox Exists

中文：
四季沙盘是规划压力测试，不是生产执行系统。它发现季节性风险，经过数据核验后，才可能生成 Retail Decision Case。

English:
The four-season sandbox is a planning stress-test, not a production execution system. It detects seasonal risk, and only after verification can a Retail Decision Case be created.

## Slide 10: 8. 五个 Agent 如何协作 / 8. How the Five Agents Collaborate

中文：
五个 Agent 围绕同一个 Case 协作。客户 Agent 讲人，个性化 Agent 讲体验，库存 Agent 讲履约，定价 Agent 讲毛利和价格，营销 Agent 讲触达。

English:
The five Agents collaborate around the same Case. Customer understands the person, Personalization designs the experience, Inventory checks fulfillment, Pricing protects margin, and Marketing plans activation.

## Slide 11: 9. AI 决策智能展示什么 / 9. What AI Decision Intelligence Shows

中文：
AI 决策智能展示的是业务决策：需求预测、折扣敏感度、供货限制、方案比较和政策护栏。内部轨迹放在审计详情，而不是打扰业务用户。

English:
AI Decision Intelligence shows business decisions: demand forecast, discount sensitivity, supply limits, option comparison and policy guardrails. Internal traces stay in audit details instead of distracting users.

## Slide 12: 10. 角色与权限边界 / 10. Roles and Permission Boundaries

中文：
角色边界让系统真实。店长确认门店事实，区域经理审批调拨和补货，高层审批重大促销和预算，AI 只推荐、解释、草拟和监控。

English:
Role boundaries create business realism. Store managers confirm store facts, regional managers approve transfer and replenishment, executives approve major promotion and budget, and AI recommends, explains, drafts and monitors.

## Slide 13: 11. 现场演示路径 / 11. Live Demo Path

中文：
现场演示按故事线走：先首页讲题目覆盖，再进区域经理审批 Case，再看 AI 决策助手，最后看审计和复盘入口。

English:
The live demo follows the storyline: home page for prompt coverage, regional manager approval Case, AI decision support, and finally audit and learning entry.

## Slide 14: 12. Azure 服务清单 / 12. Azure Service List

中文：
这页是 Azure 服务清单。运行时在 Azure Container Apps，AI 用 Azure OpenAI 和 AI Foundry，数据用 Cosmos DB，知识检索用 AI Search，安全和运维用 Key Vault、Managed Identity、Application Insights 和 Log Analytics。

English:
This is the Azure service list. Runtime uses Azure Container Apps, AI uses Azure OpenAI and AI Foundry, data uses Cosmos DB, retrieval uses AI Search, and security and operations use Key Vault, Managed Identity, Application Insights and Log Analytics.

## Slide 15: 13. Azure 架构图 / 13. Azure Architecture

中文：
这页是架构图。上层是体验和 API，中间是 Agent Runtime 和 AI 编排，下层是数据、知识、安全和可观测性。这说明 demo 可以自然演进到企业生产架构。

English:
This is the architecture diagram. Experience and API are on top, Agent Runtime and AI orchestration are in the middle, and data, knowledge, security and observability are at the bottom. The demo can evolve into production architecture.

## Slide 16: 14. 成功指标 / 14. Success Metrics

中文：
成功指标不只看模型回答，而看经营闭环：销售增长、库存浪费下降、客户满意度、审批效率、执行成功率和审计完整性。

English:
Success metrics measure the operating loop, not only model answers: sales uplift, lower waste, satisfaction, approval efficiency, execution success and audit completeness.

## Slide 17: 收尾 / Closing

中文：
最后我的结论是：这不是 AI 给建议，而是 AI 进入经营系统。Project 46 的价值是把个性化、库存、价格和营销统一成一个可控的决策闭环。

English:
My closing message is: not AI advice, but AI inside the retail operating system. Project 46 unifies personalization, inventory, pricing and marketing into one governed decision loop.
