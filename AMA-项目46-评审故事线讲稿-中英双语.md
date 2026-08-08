# Project 46 评审故事线讲稿 / Review Story Speaker Script

定位：这版以评审逻辑为核心，开头先讲 46 号课题的问题和解法，中段只保留支撑主线的证明链。

## Slide 1: 封面 / Cover

中文：
各位老师好，我的项目是 Project 46，自主零售智能 Agent 平台。我先用一页讲清楚课题问题和我的解法，然后用一个上海热浪场景证明这套方案如何落地。

English:
Hello everyone. My project is Project 46, the Autonomous Retail Intelligence Agent Platform. I will first clarify the assignment question and my solution, then use a Shanghai heatwave scenario to prove how the solution works.

## Slide 2: 1. 46 号课题的问题与我的解法 / 1. The Project 46 Question and My Answer

中文：
我会先用这一页把 46 号课题说清楚：题目问的是如何整合客户数据，并跨渠道自主交付个性化体验。我的解法不是单点推荐，而是 Customer 360、Retail Decision Case 和五个 Agent 组成的经营决策系统。

English:
I start by making the Project 46 question clear. The assignment asks how to integrate customer data and autonomously deliver personalized experiences across channels. My answer is not point recommendation. It is Customer 360, Retail Decision Case and five Agents as a retail decision system.

## Slide 3: 2. 我的解决方案蓝图 / 2. My Solution Blueprint

中文：
这一页是我的解决方案蓝图：Customer 360 负责客户上下文，Retail Case 承接经营异常，五个 Agent 生成方案，人工审批控制风险，执行系统留下回执，Azure 支撑规模化落地。

English:
This slide is my solution blueprint: Customer 360 provides customer context, Retail Case carries operating exceptions, five Agents create a plan, human approval controls risk, execution systems keep receipts, and Azure supports scale.

## Slide 4: 3. 为什么传统零售系统做不好这件事 / 3. Why Traditional Retail Systems Fail Here

中文：
传统零售系统的问题是割裂。客户、库存、价格、营销和履约分散优化，所以推荐可能没货，折扣可能亏毛利，触达可能没有授权。

English:
Traditional retail systems fail because they are fragmented. Customer, inventory, price, marketing and fulfillment optimize separately, so a recommendation may be unavailable, unprofitable or non-compliant.

## Slide 5: 4. 主演示 Case：AIRism 黑色 M/L 断码风险 / 4. Main Demo Case: AIRism Black M/L Stockout Risk

中文：
这一页我会把主线收回到系统里真实可点的 Case：AIRism 黑色 M/L 断码风险。上海热浪不是一个独立功能页，而是 Case 里的需求触发信号；主演示入口是区域经理的待我审批。

English:
This slide brings the story back to the real clickable Case: AIRism black M/L stockout risk. Shanghai heatwave is not a standalone feature page. It is the demand trigger inside the Case, and the main demo entry is the regional manager’s My approvals.

## Slide 6: 5. 我的系统解法：从信号到经营动作 / 5. My Solution: From Signals To Retail Action

中文：
系统主线是五步：整合客户，形成 Case，Agent 推理，人工审批，执行复盘。这五步就是演示逻辑，不是菜单导航。

English:
The system storyline has five steps: unify customer, create Case, Agent reasoning, human approval, execute and learn. These steps are the demo logic, not menu navigation.

## Slide 7: 6. 门店店长故事线：把现场事实变成可信输入 / 6. Store Manager Storyline: Turn Store Facts Into Trusted Input

中文：
第一条角色故事线是门店店长。店长不负责审批，他负责让系统相信门店事实：库存不可信时先做实物盘点，确认后 Case 才能继续流转。

English:
The first role storyline is the store manager. The store manager does not approve commercial decisions. They make store facts trusted: when inventory confidence is low, the system asks for a physical count before the Case moves on.

## Slide 8: 7. 区域经理故事线：从异常到可审批方案 / 7. Regional Manager Storyline: From Exception To Approvable Plan

中文：
第二条角色故事线是区域经理，这是现场演示主线。区域经理打开待审批 Case，看到预测、供货能力、业务护栏和建议方案，然后决定是否批准。

English:
The second role storyline is the regional manager, which is the main live demo. The manager opens an approval Case, reviews forecast, fulfillable supply, guardrails and the recommended plan, then decides whether to approve.

## Slide 9: 8. 跨国经营管理层故事线：看市场组合和重大例外 / 8. International Management Storyline: Market Portfolio And Major Exceptions

中文：
第三条角色故事线是跨国经营管理层。管理层不处理门店小任务，而是看国家组合、重大促销、价格例外、预算和跨区域资源配置。

English:
The third role storyline is international management. Executives do not handle store-level tasks. They review market portfolio, major campaigns, price exceptions, budget and cross-region resources.

## Slide 10: 9. 证明链一：个性化为什么可信 / 9. Proof Chain 1: Why Personalization Is Credible

中文：
第一条证明链是个性化可信。Customer 360 解决客户是谁和是否授权，经营信号解决 SKU、门店、库存、补货、价格和毛利约束。

English:
The first proof chain is credible personalization. Customer 360 handles who the customer is and whether consent exists. Operating signals constrain SKU, store, inventory, replenishment, price and margin.

## Slide 11: 10. 证明链二：Agent 输出如何进入企业流程 / 10. Proof Chain 2: How Agent Output Enters Enterprise Workflow

中文：
第二条证明链是 Agent 输出能进入企业流程。Retail Decision Case 把事实、方案、审批、政策、执行和审计放在一起，让 AI 建议可处理。

English:
The second proof chain is enterprise workflow. Retail Decision Case keeps facts, options, approval, policy, execution and audit together, so AI suggestions become processable.

## Slide 12: 11. 证明链三：自主决策如何不失控 / 11. Proof Chain 3: How Autonomy Stays Controlled

中文：
第三条证明链是自主不失控。AI 可以生成方案，但未授权、低可信库存、毛利底线和生产写入都由规则和人工审批控制。

English:
The third proof chain is controlled autonomy. AI creates options, but consent, inventory confidence, margin floor and production writes are controlled by rules and human approval.

## Slide 13: 12. 一张 Decision Packet 如何生成 / 12. How One Decision Packet Is Generated

中文：
这一页讲一张 Decision Packet 是怎么生成的。五个 Agent 不是五个功能按钮，而是围绕同一个上海热浪 Case 共同确认客户、体验、履约、价格和触达审批。

English:
This slide explains how one Decision Packet is generated. The five Agents are not five feature buttons. They jointly confirm customer, experience, fulfillment, price, activation and approval around the same Shanghai heatwave Case.

## Slide 14: 13. 区域经理看到的不是 AI，而是下一步经营决策 / 13. A Regional Manager Sees The Next Retail Decision, Not The AI Internals

中文：
这一页把演示视角切到区域经理。区域经理不需要看 AI 内部编排，他需要看到断码风险、七天预测、可承接供货、备选方案和审批后才能执行的动作。

English:
This slide shifts the demo to the regional manager. The manager does not need to see internal AI orchestration. They need stockout risk, seven-day forecast, fulfillable supply, alternative actions and approval before execution.

## Slide 15: 14. 从单个热浪 Case 扩展到四季经营规划 / 14. From One Heatwave Case To Seasonal Retail Planning

中文：
这一页讲四季沙盘的业务价值。它让系统从今天的热浪 Case 扩展到春夏秋冬的经营规划，但沙盘只是规划信号，必须核验后才能形成 Case 并进入审批。

English:
This slide explains the business value of the seasonal sandbox. It expands the system from today’s heatwave Case to seasonal retail planning, but sandbox output is only a planning signal and must be verified before becoming a Case.

## Slide 16: 15. 沙盒演示故事线：从天气信号到季节经营规划 / 15. Sandbox Demo Storyline: From Weather Signal To Seasonal Planning

中文：
这一页把沙盒演示放进故事线。它承接上海热浪信号，但不是审批入口；它展示天气、搜索、动销、试穿和仓库可用量如何先形成季节规划推演，只有被真实销售、库存和门店事实核验后，才进入 Retail Decision Case。

English:
This slide places the sandbox demo into the storyline. It extends the Shanghai heatwave signal, but it is not the approval entry. It shows how weather, search, sell-through, try-ons and warehouse availability first become seasonal planning simulation. Only signals verified by real sales, inventory and store facts enter a Retail Decision Case.

## Slide 17: 16. Azure 架构：为什么方案能落地 / 16. Azure Architecture: Why It Can Land

中文：
Azure 架构页回答的是企业可落地。分层包括体验、API、Agent Runtime、AI 编排、数据知识、安全运维。

English:
The Azure architecture answers enterprise landing. The layers are experience, API, Agent Runtime, AI orchestration, data and knowledge, security and operations.

## Slide 18: 17. Azure 服务栈如何支撑故事 / 17. Azure Services Mapped To The Story

中文：
Azure 服务栈要绑定故事：Container Apps 跑运行时，Azure OpenAI 和 AI Foundry 跑 Agent，Cosmos DB 存 Case 和审计，AI Search 做知识检索，APIM 和 Service Bus 做集成，Fabric 和 Power BI 做指标。

English:
The Azure service stack must bind to the story: Container Apps runs runtime, Azure OpenAI and AI Foundry run Agents, Cosmos DB stores Cases and audit, AI Search retrieves knowledge, APIM and Service Bus integrate systems, and Fabric / Power BI measure outcomes.

## Slide 19: 18. 当前原型证明了什么 / 18. What The Prototype Proves

中文：
当前原型证明的是系统形态：角色工作台、Case 流转、AI 决策、审批审计、中英文和移动端关键路径。业务增长指标还需要试点。

English:
The prototype proves system shape: role workspace, Case flow, AI decision, approval, audit, bilingual demo and mobile critical path. Business lift still needs pilot validation.

## Slide 20: 19. 业务效果怎么验证 / 19. How Business Impact Will Be Proven

中文：
业务效果用实验验证：baseline、pilot、control、measure、scale。这样课题里的指标不是口号，而是可衡量的试点目标。

English:
Business impact is proven through experiment design: baseline, pilot, control, measure and scale. This turns assignment metrics into measurable pilot targets.

## Slide 21: 20. 结论：一句话总结 / 20. Closing: One Sentence For The Panel

中文：
最后一句话：Project 46 不是功能集合，而是一套让 AI 进入零售经营决策的系统方案。

English:
Final sentence: Project 46 is not a collection of features. It is a system design for bringing AI into retail operating decisions.
