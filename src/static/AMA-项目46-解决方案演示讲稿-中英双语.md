# Project 46 解决方案演示讲稿 / Solution Demo Speaker Script

定位：这版是解决方案演示稿，不是问题答复稿。问题点会自然嵌入故事，而不是单独答疑。

## Slide 1: 封面 / Cover

中文：
各位老师好，我的项目是 Project 46，自主零售智能 Agent 平台。今天我不按功能菜单讲，而是按一个真实零售经营事件讲：系统如何整合客户数据，跨渠道做个性化，并让五个 Agent 形成可审批、可执行、可审计的经营动作。

English:
Hello everyone. My project is Project 46, the Autonomous Retail Intelligence Agent Platform. I will not present it as a feature menu. I will use one retail operating event to show how the system integrates customer data, delivers omni-channel personalization, and turns five Agents into approvable, executable and auditable business actions.

## Slide 2: 今天的演示逻辑 / Today’s Solution Story

中文：
今天的逻辑是完整解决方案。先讲课题目标，再进入上海夏季热浪场景，然后讲 Customer 360、Retail Decision Case、五个 Agent、人工审批和 Azure 架构，最后说明如何验证业务指标。

English:
The logic today is a complete solution story. I start with the assignment goal, then the Shanghai heatwave scenario, then Customer 360, Retail Decision Case, five Agents, human approval and Azure architecture, and finally business measurement.

## Slide 3: 1. Project 46 要解决什么 / 1. What Project 46 Solves

中文：
Project 46 的核心不是做一个 AI 菜单。它要解决的是：个性化必须同时理解客户、库存、价格、授权和履约，否则推荐会不可执行，营销会有合规风险。

English:
The core of Project 46 is not an AI menu. Personalization must understand customer, inventory, price, consent and fulfillment at the same time. Otherwise, recommendations cannot be executed and campaigns create compliance risk.

## Slide 4: 2. 业务场景：上海夏季热浪 / 2. Business Scenario: Shanghai Heatwave

中文：
我用上海热浪作为演示场景。高温带来需求上升，App 搜索和门店转化都变强，但黑色 M/L 出现断码风险，同时部分门店有可调拨库存。

English:
I use a Shanghai heatwave as the demo scenario. Hot weather increases demand. App search and store conversion rise, but black M/L sizes face stockout risk, while some stores still have transferable inventory.

## Slide 5: 3. 解决方案总览 / 3. Solution Overview

中文：
解决方案从 Customer 360 开始，把客户、门店和渠道信号合到一起。然后形成 Retail Decision Case，再由五个 Agent 生成方案，最后由人审批并执行。

English:
The solution starts with Customer 360, combines customer, store and channel signals, creates a Retail Decision Case, lets five Agents produce options, and then routes high-risk actions to human approval and execution.

## Slide 6: 4. 客户数据整合：Customer 360 / 4. Customer Data Integration: Customer 360

中文：
Customer 360 是个性化的基础。它不是把所有数据随便拼起来，而是在授权范围内统一身份、行为、意图、渠道偏好和客户价值。

English:
Customer 360 is the foundation of personalization. It does not freely combine all data. It aligns identity, behavior, intent, channel preference and customer value only within consent boundaries.

## Slide 7: 5. 全渠道个性化旅程 / 5. Omni-channel Personalization Journey

中文：
全渠道体验的关键是上下文连续。客户从 App 到门店再到售后，系统始终知道这个人看过什么、是否授权、附近门店有没有货，以及下一步适合做什么。

English:
The key to omni-channel experience is context continuity. From app to store to service, the system knows what the customer viewed, whether consent exists, whether nearby inventory exists, and what next action is suitable.

## Slide 8: 6. Retail Decision Case：系统的业务对象 / 6. Retail Decision Case: The Business Object

中文：
Retail Decision Case 是系统里的业务对象。它把门店、商品、SKU、库存、信号、SLA、方案、审批和审计放在一起，让 Agent 输出可以被企业处理。

English:
Retail Decision Case is the business object of the system. It keeps store, product, SKU, inventory, signals, SLA, options, approval and audit together, so Agent output becomes enterprise-processable.

## Slide 9: 7. 五个 Agent 的分工 / 7. Five-Agent Operating Model

中文：
五个 Agent 是五个业务能力域。Customer 理解客户，Personalization 做体验，Inventory 判断履约，Pricing 保护毛利，Marketing 负责受控触达。

English:
The five Agents are business domains. Customer understands the customer, Personalization designs the experience, Inventory checks fulfillment, Pricing protects margin, and Marketing handles governed outreach.

## Slide 10: 8. Agent 如何协作形成决策包 / 8. How Agents Create A Decision Packet

中文：
Agent 协作不是五个机器人聊天，而是围绕同一个 Case 逐步回答：对谁、给什么、能不能履约、价格是否安全、怎么触达。

English:
Agent collaboration is not five chatbots talking. It answers step by step: who, what experience, can we fulfill, is the price safe, and how should we activate.

## Slide 11: 9. AI 决策智能：业务用户真正看到什么 / 9. What Business Users Actually See

中文：
业务用户看到的是经营方案，不是内部模型流水线。区域经理主要看预测、供货限制、方案比较和护栏；详细轨迹放在审计里。

English:
Business users see operating decisions, not internal model pipelines. The regional manager sees forecast, supply limits, option comparison and guardrails. The detailed trace stays in audit.

## Slide 12: 10. 业务规则与人工审批 / 10. Business Rules and Human Approval

中文：
业务规则和人工审批让自主 Agent 可控。未授权客户不能触达，低可信库存不能推荐，低于毛利底线的折扣被阻断，审批前不写生产系统。

English:
Business rules and human approval make autonomy controllable. No outreach without consent, no recommendation on low-confidence inventory, discounts below margin floor are blocked, and no production write happens before approval.

## Slide 13: 11. 四季沙盘如何服务主线 / 11. How The Seasonal Sandbox Fits

中文：
四季沙盘是风险发现入口。它帮助提前发现季节性风险，但不直接发起生产动作；只有经过数据核验，才可能变成 Retail Decision Case。

English:
The seasonal sandbox is a risk discovery entry point. It detects seasonal risks early, but it does not trigger production actions. Only verified signals can become a Retail Decision Case.

## Slide 14: 12. 现场系统演示路径 / 12. Live System Demo Path

中文：
现场演示我会按业务故事走：首页说明课题贴合，区域经理打开上海 Case，进入决策助手，看预测和方案，再看审批、审计和四季沙盘。

English:
The live demo follows the business story: home page for prompt fit, regional manager opens the Shanghai Case, decision support shows forecast and options, then approval, audit and seasonal sandbox.

## Slide 15: 13. Azure 云原生架构 / 13. Azure Cloud-Native Architecture

中文：
Azure 架构分层很清楚：体验层、入口和 API、Agent Runtime、AI 编排、数据知识层、安全和运维层。

English:
The Azure architecture is layered: experience, ingress and API, Agent Runtime, AI orchestration, data and knowledge, security and operations.

## Slide 16: 14. Azure 服务栈 / 14. Azure Service Stack

中文：
Azure 服务栈不是堆名字。Container Apps 负责运行时，Azure OpenAI 和 AI Foundry 负责 Agent，Cosmos DB 保存状态，AI Search 做知识检索，APIM 和 Service Bus 做集成，Key Vault 和可观测性做治理。

English:
The Azure service stack is not name-dropping. Container Apps runs the runtime. Azure OpenAI and AI Foundry power Agents. Cosmos DB stores state. AI Search retrieves knowledge. APIM and Service Bus handle integration. Key Vault and observability provide governance.

## Slide 17: 15. 为什么这些 Azure 服务是先进且必要的 / 15. Why These Azure Services Are Advanced and Necessary

中文：
这些先进服务对应企业级问题：AI Foundry 让 Agent 可编排和可评估，Container Apps 支持灰度和弹性，Cosmos DB 支持低延迟状态，APIM、身份和监控让系统可治理。

English:
These advanced services map to enterprise problems. AI Foundry enables orchestration and evaluation. Container Apps supports rollout and elasticity. Cosmos DB supports low-latency state. APIM, identity and monitoring make the system governable.

## Slide 18: 16. 当前实现证据 / 16. Current Implementation Evidence

中文：
当前原型已经证明系统形态：有生产应用、Case API、AI 决策智能、角色工作台、审计护栏和中英可点击演示。

English:
The current prototype proves the system shape: production app, Case API, AI decision intelligence, role workspaces, audit guardrails and bilingual clickable demo.

## Slide 19: 17. 成功指标如何验证 / 17. How Success Will Be Measured

中文：
最后，课题里的 +40%、-50%、85% 和 +60% 是试点目标，不是 demo 已经实现。后续要用 test/control 门店和 cohort 来验证。

English:
Finally, +40%, -50%, 85% and +60% are pilot targets from the assignment, not demo achievements. They should be validated by test/control stores and customer cohorts.

## Slide 20: 18. 最终结论 / 18. Closing Message

中文：
我的结论是：Project 46 不是展示五个 Agent，而是展示 AI 如何进入零售企业经营系统，把个性化从推荐内容升级为受控经营决策。

English:
My conclusion is: Project 46 is not a demo of five Agents. It shows how AI enters the retail operating system and upgrades personalization from recommendation content to governed retail decisions.

## Slide 21: 收尾 / Closing

中文：
我的结论是：Project 46 不是展示五个 Agent，而是展示 AI 如何进入零售企业经营系统，把个性化从推荐内容升级为受控经营决策。

English:
My conclusion is: Project 46 is not a demo of five Agents. It shows how AI enters the retail operating system and upgrades personalization from recommendation content to governed retail decisions.
