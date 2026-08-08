# AMA 二次过堂正式汇报讲稿（35-40 分钟版）

定位：PPT 是给评委看的主叙事，不放 Q&A。Q&A 只放在本文最后，作为你自己的备忘。

建议节奏：
- PPT 主讲：28-32 分钟
- 系统演示：6-8 分钟
- 收尾：1 分钟
- Q&A：预留约 10 分钟

## 开场总句

中文：
各位老师好，我的项目是 Autonomous Retail Intelligence Agent Platform。题目要求的是整合客户数据，并跨渠道自主实现个性化体验。所以我这次的汇报不是只展示五个 Agent，而是展示五个 Agent 如何进入一个企业可以接受的零售经营闭环。

English:
Hello everyone. My project is the Autonomous Retail Intelligence Agent Platform. The prompt asks for customer data integration and autonomous omni-channel personalization. So today, I will not only show five Agents. I will show how these Agents become an enterprise-ready retail decision loop.

## Slide 1 Cover

时间：30 秒

中文：
这一版我用一个融合故事线来讲。前半段回答题目要求：客户数据、全渠道个性化和五个 Agent。后半段回答企业落地：审批、执行、审计和 Azure 架构。

English:
This version uses a blended story. The first part answers the prompt: customer data, omni-channel personalization, and five Agents. The second part answers enterprise readiness: approval, execution, audit, and Azure architecture.

## Slide 2 Today’s Storyline

时间：1 分钟

中文：
我会按五段讲。第一，问题和题目匹配。第二，具体业务场景。第三，五个 Agent。第四，Retail Decision Case 和经营闭环。第五，Azure 架构和成功指标。

English:
I will cover five parts. First, the problem and prompt fit. Second, the business scenario. Third, the five Agents. Fourth, the Retail Decision Case and operating loop. Fifth, Azure architecture and success measurement.

## Slide 3 The Core Problem

时间：1.5 分钟

中文：
零售企业不是没有渠道，而是缺少一个跨渠道的可信决策闭环。客户在线上浏览，在手机端加购，到门店试穿，最后可能在 POS 或电商渠道购买。如果这些信号分散在不同系统里，个性化就会出问题。

比如，推荐系统可能推荐一个客户喜欢的商品，但门店没有库存。营销系统可能发出折扣，但这个客户没有授权接收消息。定价系统可能提升转化率，但毛利被打穿。所以我的系统要把客户、库存、价格、营销和履约放在一个决策里。

English:
Retailers do not lack channels. They lack one trusted decision loop across channels. A customer may browse online, add to cart on mobile, try products in store, and buy through POS or e-commerce. If these signals are separated, personalization will fail.

A system may recommend a product the customer likes, but the store has no stock. Marketing may send an offer, but the customer did not give consent. Pricing may improve conversion, but hurt margin. So my system puts customer, inventory, pricing, marketing, and fulfillment into one decision.

## Slide 4 Prompt Coverage

时间：1.5 分钟

中文：
这页是为了先证明没有偏题。题目要求有六类内容：业务用例、五个 Agent、核心优势、成功标准、全渠道体验、亚洲区域挑战。

我的设计逐项覆盖：业务用例是客户数据整合和全渠道个性化；五个 Agent 都保留；优势对应销售提升、个性化和库存优化；成功标准作为试点目标来衡量；全渠道包含 App、邮件、小程序、marketplace、门店 POS 和自提；亚洲挑战进入隐私、语言、支付和门店履约规则。

English:
This slide proves the project matches the prompt. The prompt asks for six things: business use case, five Agents, advantages, success criteria, omni-channel experience, and Asia regional challenges.

My design covers all of them. The business use case is customer data integration and omni-channel personalization. The five Agents are kept. The advantages are sales uplift, personalization, and inventory optimization. The success criteria are treated as pilot targets. Omni-channel includes app, email, mini-program, marketplace, store POS, and pickup. Asia challenges are handled by privacy, language, payment, and fulfillment rules.

## Slide 5 Scenario Assumption

时间：1.5 分钟

中文：
我假设一个具体场景：上海夏季热浪。天气升温后，用户搜索透气、防晒、速干商品；门店 RFID 显示试穿上升；POS 显示部分 SKU 转化变好；但门店库存并不均匀。

这时系统要回答四个问题：哪些客户值得触达？哪些商品可以推荐？哪些门店需要补货或调拨？价格和营销动作是否允许？

English:
I use a concrete scenario: a summer heatwave in Shanghai. After the temperature rises, customers search for breathable, sun-protection, and quick-dry products. Store RFID shows more try-ons. POS shows better conversion for some SKUs. But store inventory is uneven.

The system needs to answer four questions: which customers should be reached, which products can be recommended, which stores need replenishment or transfer, and which pricing or marketing actions are allowed.

## Slide 6 End-to-End Customer Journey

时间：1.5 分钟

中文：
这页回答全渠道体验。客户先在 App 浏览，之后收到个性化内容，再查看附近门店库存，到门店试穿，购买后继续收到售后和下一次推荐。

关键不是每个渠道单独智能，而是上下文连续。系统要知道这个人是谁、看过什么、是否授权、附近门店有没有货，以及上一次触达过什么。

English:
This slide answers omni-channel experience. A customer browses in the app, receives personalized content, checks nearby store inventory, tries products in store, buys, and later receives service or the next recommendation.

The key is not intelligence in each channel alone. The key is context continuity. The system needs to know who the customer is, what they viewed, whether they gave consent, whether the nearby store has stock, and what message was already sent.

## Slide 7 Customer Understanding Agent

时间：1.5 分钟

中文：
Customer Understanding Agent 负责构建统一客户画像。它整合会员、App、门店、POS、退货、投诉、渠道偏好等信号。

但这个 Agent 不是随便用所有数据。它必须理解 consent，也就是客户授权；还要理解区域语言和服务偏好。这样客户画像才适合亚洲市场。

English:
The Customer Understanding Agent builds a unified customer profile. It integrates loyalty, app, store, POS, return, complaint, and channel preference signals.

But this Agent cannot use all data freely. It must understand consent, meaning customer permission. It must also understand local language and service preference. This makes the customer profile suitable for Asia.

## Slide 8 Personalization Agent

时间：1.5 分钟

中文：
Personalization Agent 负责动态定制商品展示、邮件内容、推荐列表和下一步动作。

我这里强调一个词：fulfillable personalization。也就是个性化必须可履约。不能推荐没库存的商品，不能重复打扰客户，不能向未授权客户发送营销信息。

English:
The Personalization Agent creates product display, email content, recommendation lists, and next best actions.

I emphasize one phrase: fulfillable personalization. Personalization must be executable. It should not recommend unavailable products. It should not repeat the same message too often. It should not send marketing to customers without consent.

## Slide 9 Inventory Agent

时间：1.5 分钟

中文：
Inventory Agent 解决库存优化。它预测 SKU、门店和渠道的未来需求，判断 ATP 可信度，并建议补货或调拨。

这和个性化直接相关。库存不准，个性化就是错的。城市门店和乡村门店履约能力不同，所以库存 Agent 也要理解不同门店网络。

English:
The Inventory Agent optimizes inventory. It forecasts demand by SKU, store, and channel. It checks ATP confidence and suggests replenishment or transfer.

This is directly related to personalization. If inventory is wrong, personalization is wrong. Urban stores and rural stores have different fulfillment capabilities, so the Inventory Agent must understand different store networks.

## Slide 10 Pricing Agent

时间：1.5 分钟

中文：
Pricing Agent 根据需求、竞争、库存和毛利护栏给出价格建议。它可以建议折扣，也可以阻断折扣。

真实企业里，动态定价不能只追求转化率。它还要保护毛利、品牌和审批流程。

English:
The Pricing Agent recommends prices based on demand, competition, inventory, and margin guardrails. It can suggest a discount, and it can also block a discount.

In real enterprises, dynamic pricing cannot only chase conversion. It must protect margin, brand, and approval process.

## Slide 11 Marketing Agent

时间：1.5 分钟

中文：
Marketing Agent 负责活动计划、预算分配、内容草稿和渠道选择。但它不会直接乱发营销。

它会选择已授权、高意向客户，生成活动草稿，然后进入审批或实验设计。这样自主营销是受控的。

English:
The Marketing Agent plans campaigns, budget allocation, content drafts, and channel selection. But it does not send messages without control.

It selects consented and high-intent customers, creates campaign drafts, and then enters approval or experiment design. So autonomous marketing is controlled.

## Slide 12 Multi-Agent Collaboration

时间：1.5 分钟

中文：
这页讲五个 Agent 如何协同。Customer Agent 回答客户是谁，Personalization Agent 回答给什么体验，Inventory Agent 回答能不能履约，Pricing Agent 回答价格是否安全，Marketing Agent 回答如何触达。

它们不是五个分散的 chatbot，而是围绕同一个 Case 共享状态。

English:
This slide explains how the five Agents collaborate. The Customer Agent answers who the customer is. The Personalization Agent answers what experience to give. The Inventory Agent answers whether we can fulfill it. The Pricing Agent answers whether the price is safe. The Marketing Agent answers how to activate the customer.

They are not five separate chatbots. They share the same Case state.

## Slide 13 Why Retail Decision Case

时间：1.5 分钟

中文：
这是这次故事线升级的关键。Agent 输出不能只是聊天文本。它必须变成一个 Decision Packet，里面有事实、证据、备选方案、政策检查和审批状态。

这样评委可以看到：AI 不是在空中给建议，而是在企业经营流程里产生一个可处理对象。

English:
This is the key upgrade in my story. Agent output cannot be only chat text. It must become a Decision Packet with facts, evidence, alternatives, policy checks, and approval state.

This shows that AI is not giving advice in the air. It creates an object that the enterprise can process.

## Slide 14 Decision Operating Loop

时间：1.5 分钟

中文：
完整闭环是五步：业务异常、可信事实、Agent 协同、人工决策、受控执行。

这里要强调：AI 可以很自主，但不是 uncontrolled。事实计算、授权、毛利、审批和执行都由确定性服务和规则控制。

English:
The full loop has five steps: exception, truth, Agents, decision, and execution.

The key point is: AI can be autonomous, but not uncontrolled. Truth calculation, consent, margin, approval, and execution are controlled by deterministic services and rules.

## Slide 15 Human Roles and Boundaries

时间：1.5 分钟

中文：
不同角色负责不同事情。门店店长确认门店事实，区域经理审批补货和调拨，高层审批重大价格、促销和预算动作。AI 负责推荐、解释、草拟和监控。

这让系统符合企业组织结构，而不是让 AI 直接替代所有人。

English:
Different roles own different tasks. The store manager confirms store facts. The regional manager approves replenishment and transfers. Executives approve major pricing, promotion, and budget actions. AI recommends, explains, drafts, and monitors.

This fits enterprise organization. AI does not replace everyone directly.

## Slide 16 Production Guardrails

时间：1.5 分钟

中文：
这页是评委会关心的风险控制。未授权客户不能触达；低可信库存不能推荐；低于毛利底线的折扣要阻断；执行要有幂等；每个动作要可追踪；失败要能重试或补偿。

English:
This slide covers risk control. Customers without consent cannot be contacted. Low-confidence inventory cannot be recommended. Discounts below margin floor are blocked. Execution needs idempotency. Every action must be traceable. Failures need retry or compensation.

## Slide 17 Live Demo Plan

时间：30 秒

中文：
接下来我用 6 到 8 分钟演示系统。演示只服务于刚才的故事线：先看题目覆盖，再看 Case，再看五个 Agent，再看审批、执行和审计。

English:
Now I will use 6 to 8 minutes to show the system. The demo supports the story: prompt coverage, Case, five Agents, approval, execution, and audit.

## 系统演示口令

时间：6-8 分钟

中文：
第一步，首页停一下，指给评委看题目要点覆盖。  
第二步，打开上海 Case，讲线上、移动端、门店、库存和会员信号进入同一个 Case。  
第三步，打开 AI 决策助手，讲五个 Agent 的协同结果。  
第四步，展示 policy block 和 approval，说明 AI 不直接写生产。  
第五步，展示 audit 或 execution receipt，说明系统可审计。

English:
First, stay on the home page and point to prompt coverage.  
Second, open the Shanghai Case and show online, mobile, store, inventory, and member signals in one Case.  
Third, open AI decision support and explain the five-Agent result.  
Fourth, show policy block and approval, and explain that AI does not directly write to production.  
Fifth, show audit or execution receipt, and explain that the system is auditable.

## Slide 18 Asia Regional Specificity

时间：1.5 分钟

中文：
亚洲不是一个统一市场。中国大陆有 PIPL、微信、小程序、天猫、京东和本地支付。日本有 APPI、LINE、Rakuten 和 PayPay。东南亚有多种 PDPA、多语言、Shopee、Lazada 和本地钱包。韩国有 PIPA、Kakao 和 Naver。

所以我的系统不是复制一个推荐模型到所有国家，而是把区域政策、语言、支付、渠道和门店履约放进 Agent context。

English:
Asia is not one single market. China Mainland has PIPL, WeChat, mini-programs, Tmall, JD, and local payments. Japan has APPI, LINE, Rakuten, and PayPay. Southeast Asia has different PDPA rules, many languages, Shopee, Lazada, and local wallets. Korea has PIPA, Kakao, and Naver.

So my system does not copy one recommendation model to every country. It puts regional policy, language, payment, channel, and store fulfillment into Agent context.

## Slide 19 Data and Privacy Architecture

时间：1.5 分钟

中文：
客户智能必须 privacy-aware by design。系统分清客户画像、商品、库存、价格、营销和审计数据。隐私控制包括区域政策、客户授权、用途限制和审计。

English:
Customer intelligence must be privacy-aware by design. The system separates customer profile, product, inventory, pricing, marketing, and audit data. Privacy controls include regional policy, customer consent, purpose limitation, and audit.

## Slide 20 Success Metrics and Measurement

时间：1.5 分钟

中文：
题目里的数字我不会说 Demo 已经实现。更严谨的说法是：这些是试点目标。销售 +40% 用 test/control 门店衡量；库存损耗 -50% 用老化库存、缺货、markdown loss 和调拨效率衡量；满意度 85% 用调查、投诉和退货原因衡量；LTV +60% 用 cohort 留存和复购衡量。

English:
I do not claim the demo already achieved the numbers in the prompt. A better statement is: these are pilot targets. Sales +40% will be measured by test/control stores. Waste -50% will be measured by aging stock, stockout, markdown loss, and transfer efficiency. Satisfaction 85% will be measured by surveys, complaints, and return reasons. LTV +60% will be measured by cohort retention and repeat purchase.

## Slide 21 Experiment Design

时间：1.5 分钟

中文：
业务效果要通过实验验证。先选 baseline，再做 pilot，同时保留 control group。然后衡量销售、库存、满意度和 LTV。只有当护栏和 KPI 都稳定后才扩大规模。

English:
Business impact must be proven by experiment. First choose the baseline, then run a pilot, and keep a control group. Then measure sales, inventory, satisfaction, and LTV. Scale only after guardrails and KPIs are stable.

## Slide 22 Azure Architecture

时间：2 分钟

中文：
当前原型部署在 Azure Container Apps。FastAPI 是 Agent Runtime，Cosmos DB 保存 Case、审批、工单和审计。Azure OpenAI / AI Foundry 提供推理能力。生产路径可以接 Event Hubs、Fabric、AI Search、APIM、Key Vault、Managed Identity 和 Application Insights。

English:
The current prototype runs on Azure Container Apps. FastAPI is the Agent Runtime. Cosmos DB stores Cases, approvals, work orders, and audit logs. Azure OpenAI and AI Foundry provide reasoning. The production path can include Event Hubs, Fabric, AI Search, APIM, Key Vault, Managed Identity, and Application Insights.

## Slide 23 Current Implementation Evidence

时间：1.5 分钟

中文：
这页回答“你到底做出了什么”。我已经有部署好的应用、共享 Case 状态、AI 决策接口、审批流、审计证据和中英文 UI。它不是纯 PPT 概念。

English:
This slide answers: what has been built. I have a deployed app, shared Case state, AI decision API, approval flow, audit evidence, and bilingual UI. It is not only a PPT concept.

## Slide 24 Architecture Decisions

时间：1.5 分钟

中文：
关键架构选择有四个。第一，用 Case-centric orchestration，而不是 Agent 菜单。第二，ATP、授权、毛利和执行交给确定性服务。第三，高风险动作保留人工审批。第四，成功数字作为试点目标，而不是 Demo 结果。

English:
There are four key architecture decisions. First, use Case-centric orchestration, not Agent menu navigation. Second, keep ATP, consent, margin, and execution in deterministic services. Third, keep human approval for high-risk actions. Fourth, treat success numbers as pilot targets, not demo results.

## Slide 25 Panel Memory

时间：1 分钟

中文：
我希望评委记住一句话：这个平台把个性化变成受控的零售经营决策。它不是只推荐商品，而是把客户、库存、价格、营销和履约一起放进一个可执行闭环。

English:
I want the panel to remember one sentence: this platform turns personalization into controlled retail decisions. It does not only recommend products. It puts customer, inventory, pricing, marketing, and fulfillment into one executable loop.

## Slide 26 Closing Message

时间：1 分钟

中文：
所以我的项目不是简单展示五个 Agent。它把客户洞察、全渠道个性化、库存、定价和营销放进一个企业级 Agentic Decision Operating Model。它既贴合题目，也可以被审批、执行、审计和持续优化。

English:
So my project is not just a demo of five Agents. It puts customer understanding, omni-channel personalization, inventory, pricing, and marketing into an enterprise-ready Agentic Decision Operating Model. It matches the prompt, and it can be approved, executed, audited, and continuously improved.

# 私人备忘：高概率 Q&A，不放进 PPT

## Q1: Why did your story change?

English:
Last time I showed Agent capabilities. This time I show how these Agents become an enterprise operating loop. It is the same project, but with a stronger architecture story.

中文：
上一次我展示 Agent 能力。这次我展示这些 Agent 如何进入企业经营闭环。项目方向没变，只是架构叙事更成熟。

## Q2: Where is personalization?

English:
Personalization is still core. But in real retail, personalization must be consent-aware, inventory-aware, price-aware, and fulfillment-aware.

中文：
个性化仍然是核心。但真实零售里，个性化必须受客户授权、库存、价格和履约能力约束。

## Q3: Are the success numbers already achieved?

English:
No. They are target metrics from the prompt. The prototype proves workflow, architecture, approval, execution, and audit. Business impact needs a test/control pilot.

中文：
没有。这些是题目给出的目标指标。Demo 证明的是流程、架构、审批、执行和审计。业务效果需要 test/control 试点验证。

## Q4: Is this really autonomous?

English:
Yes, but it is controlled autonomy. The Agents can analyze, recommend, draft, and prepare work orders. High-risk actions still need approval.

中文：
是自主，但不是失控自主。Agent 可以分析、推荐、起草和准备工单。高风险动作仍然需要审批。

## Q5: What is the production path?

English:
The production path is Azure Container Apps, Cosmos DB, Azure OpenAI / AI Foundry, Event Hubs, Fabric, AI Search, APIM, Key Vault, Managed Identity, and Application Insights.

中文：
生产路径是 Azure Container Apps、Cosmos DB、Azure OpenAI / AI Foundry、Event Hubs、Fabric、AI Search、APIM、Key Vault、Managed Identity 和 Application Insights。
