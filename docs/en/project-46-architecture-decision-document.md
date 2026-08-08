# Architecture Decision Document

## Project 46: Autonomous Retail Intelligence Agent Platform

**Owner:** Yuan Wang  
**Scenario:** Contoso Fashion Asia summer launch and omni-channel personalization  
**Document purpose:** AMA second review architecture decision record  
**Status:** Review-ready prototype architecture  

## 1. Scenario Assumptions

Contoso Fashion operates an Asia retail network across China Mainland, Japan, Southeast Asia, and Korea. The business has mobile app, marketplace, mini-program, store POS, RFID fitting-room signals, CRM membership data, inventory systems, and campaign tools, but the decision process is still coordinated manually across merchandising, marketing, supply chain, store operations, and finance.

For the review scenario, Shanghai enters an early summer heatwave. App search, store POS, RFID try-ons, social comments, and marketplace browse-to-cart behavior all show demand for breathable, quick-dry, UV protection, and kids anti-sweat products. The platform must detect the event, identify consented high-intent customers, generate personalized product recommendations, protect in-season margin, move off-season inventory, allocate marketing spend, and open work orders for human approval where business risk is high.

The demo uses target hypotheses from the AMA brief:

- Same-store sales target: +40% through agent-powered personalization.
- Inventory waste target: -50% through demand forecasting and stock rebalancing.
- Customer satisfaction target: 85% through contextual omni-channel experiences.
- LTV target: +60% through ongoing customer relationship management.
- Omni-channel requirement: keep context across app, mini-program, marketplace, email, live commerce, store POS, and pickup/transfer journeys.

These numbers are business targets for architectural validation, not validated production ROI.

## 2. Business Architecture Decision

### Decision

Design the platform as an AI operating system for retail decisions, not as a dashboard. The platform receives business events, decomposes them into agent tasks, creates executable work orders, records approvals, and maintains audit history.

### Rationale

A dashboard can show signals, but it cannot close the loop from signal to decision to action. The AMA requirement asks for autonomous personalization, inventory optimization, pricing, marketing, and continuous customer relationship management. That requires an event-driven operating loop:

1. Detect business event.
2. Build customer and product context.
3. Let specialized agents decide within guardrails.
4. Create work orders and approval gates.
5. Execute through business systems.
6. Feed results back to BI, feature store, and agent memory.

### Trade-off

This is more complex than a single recommendation engine, but it better matches real retail operations where inventory, pricing, customer consent, margin, fulfillment, and campaign budget are interdependent.

## 3. Agent Architecture Decision

### Decision

Use five core domain agents plus an orchestrator and compliance gate:

- Customer Understanding Agent: resolves customer identity and builds consent-aware Customer 360 profiles from online, mobile, and store behavior.
- Personalization Agent: creates contextual product displays, recommendations, copy, and channel-specific next best actions.
- Inventory Agent: forecasts demand and optimizes stock by store, warehouse, and transfer route.
- Pricing Agent: adjusts prices and promotions using demand, competition, margin, and inventory guardrails.
- Marketing Agent: launches and optimizes campaigns, budget allocation, creative variants, and customer journeys.
- Orchestrator Agent: decomposes events, coordinates dependencies, and aggregates decisions.
- Compliance Agent: checks privacy, consent, data residency, auditability, and approval requirements.

### Rationale

Retail decisions are not independent. Inventory risk constrains pricing; pricing affects personalization; personalization determines marketing segments; compliance can block or modify all customer-level actions. A multi-agent system makes these dependencies explicit and auditable.

### Alternative Considered

A monolithic AI service would be easier to deploy, but it would hide ownership boundaries and make it harder to explain why a price, campaign, or replenishment action was chosen.

## 4. Data Architecture Decision

### Decision

Use an event-driven lakehouse plus operational memory pattern:

- Azure Event Hubs ingests POS, app, RFID, CRM, weather, social, competitor price, and inventory events.
- Microsoft Fabric OneLake stores historical and analytical data.
- Azure Cosmos DB stores agent runs, work orders, customer profile documents, shared memory, and audit records.
- Azure AI Search stores product knowledge, campaign playbooks, FAQ, policy references, and vectorized brand/retail knowledge.
- Azure ML Feature Store or Fabric feature tables provide customer, product, session, and operational features.

### Rationale

Agent decisions need both real-time context and historical evidence. Event Hubs captures live signals; Fabric supports BI and training; Cosmos DB gives low-latency operational state; AI Search grounds LLM responses in enterprise knowledge.

### Key Data Objects

- Customer 360 profile: consent, identity graph, preferred channel, language, payment preference, purchase history, LTV score, price sensitivity.
- Product state: SKU, lifecycle, stock, warehouse availability, safety stock, margin floor, competitor price, demand trend.
- Agent run: trigger, region, agent decisions, work orders, approvals, execution trace, audit log.
- Campaign state: audience, channel budget, creative variants, A/B results, conversion feedback.

## 5. Azure Platform Decision

### Decision

Deploy the review prototype on Azure Container Apps, backed by Cosmos DB and Azure OpenAI, while documenting the production target on Azure AI Foundry, Fabric, Event Hubs, AI Search, APIM, Logic Apps, Application Insights, Key Vault, and Managed Identity.

### Prototype Deployment

- Azure Container Apps: FastAPI agent runtime and operational UI.
- Azure Container Registry: container image build and storage.
- Azure Cosmos DB serverless: run, work-order, Customer 360, and audit persistence.
- Azure OpenAI: agent reasoning and content generation.
- Log Analytics and Application Insights: runtime observability.

### Production Target

- Azure AI Foundry: agent lifecycle, evaluation, tracing, and model governance.
- Azure API Management: MCP/API gateway for POS, CRM, payment, campaign, OMS, and ERP tools.
- Logic Apps / Azure Functions / Power Automate: business execution layer.
- Microsoft Fabric / Power BI: management cockpit and KPI feedback.
- Key Vault and Managed Identity: secretless service access.
- Private Link / Front Door WAF: secure network boundary.

### Rationale

Container Apps is appropriate for a reviewable prototype because it is fast to deploy, externally reachable, and easy to inspect. The target architecture remains Azure-native and enterprise-ready.

## 6. Regional Architecture Decision

### Decision

Use region-aware policy, language, payment, and data-residency configuration instead of one global behavior.

### Regional Handling

- China Mainland: PIPL, China data residency, zh-CN, WeChat Mini Program, Tmall, JD, WeChat Pay, Alipay.
- Japan: APPI, Japan-preferred storage, ja-JP, LINE, Rakuten, PayPay.
- Southeast Asia: PDPA variants, country-level localization, multilingual content, Shopee, Lazada, WhatsApp, GrabPay, OVO, GoPay.
- Korea: PIPA, Korea data residency, ko-KR, Kakao, Naver, Kakao Pay, Naver Pay.

### Rationale

Asia retail cannot be treated as one market. Privacy rules, languages, marketplace penetration, store density, and payments vary sharply. The platform therefore carries region policy into each agent decision and into the Compliance Agent gate.

## 7. Privacy and Governance Decision

### Decision

Apply privacy-by-design:

- Process only consented customer data for personalization.
- Keep region-specific data residency rules in policy configuration.
- Use synthetic personas for cold start, testing, and demos.
- Mask PII in agent traces and logs.
- Require human approval for risky actions such as major pricing changes, sensitive customer targeting, and large campaign spend.

### Rationale

The platform must personalize across channels while respecting PDPA, PIPL, APPI, PIPA, and local data protection laws. The safest architecture is to make compliance part of the agent workflow, not an after-the-fact checklist.

## 8. Omni-channel Experience Decision

### Decision

Maintain context through a shared Customer 360 profile and session memory that can be used across app, mini-program, marketplace, email, live commerce, store POS, and pickup/transfer journeys.

### Example

A customer views a kids anti-sweat tee in the app, tries a related SKU in store, receives a consented mini-program recommendation, sees localized copy in the marketplace, and picks up from the nearest store. The Personalization Agent uses the same profile and the Inventory Agent only recommends SKUs that can be fulfilled by local store, warehouse, or nearby transfer.

### Rationale

The success criteria explicitly require seamless omni-channel shopping with context continuity. This cannot be achieved with channel-isolated personalization.

## 9. Inventory and Pricing Decision

### Decision

Make Inventory Agent the first operational agent in the decision chain, then let Pricing Agent act under inventory and margin guardrails.

### Rationale

Dynamic pricing without inventory context can create stockouts or margin damage. Inventory forecast must first classify SKUs as high stockout risk, healthy, or overstock. Pricing then protects high-demand in-season items while selectively clearing off-season inventory.

## 10. Marketing Automation Decision

### Decision

Marketing Agent can draft campaigns, allocate budgets, choose channels, and generate creative variants, but execution is gated by policy, inventory availability, and approval thresholds.

### Rationale

Autonomous marketing can improve speed and budget allocation, but unchecked campaign execution can violate consent, oversell inventory, or over-discount products. The platform therefore supports autonomy with business guardrails.

## 11. Urban and Rural Store Network Decision

### Decision

Use tiered store strategies:

- Urban flagship stores: real-time personalization, full assortment, ship-from-store, and local events.
- New tier-1 and tier-2 stores: standard recommendations and hourly replenishment.
- Lower-tier and rural stores: inventory-first recommendations, curated SKU sets, batch synchronization, and transfer-aware fulfillment.

### Rationale

Store infrastructure and customer behavior vary across city tiers. The same recommendation should not be shown if a rural store cannot fulfill it or if payment/logistics options differ.

## 12. Success Measurement Decision

### Decision

Measure outcomes through a Fabric / Power BI KPI loop:

- Same-store sales uplift by test/control store cohort.
- Inventory waste reduction by markdown, stockout, and aging-stock metrics.
- Customer satisfaction by post-purchase survey, complaint rate, return rate, and service resolution.
- LTV uplift by cohort retention, repeat purchase, and member tier migration.
- Omni-channel continuity by cross-touchpoint journey completion rate.

### Rationale

The AMA success criteria are outcome-based. Architecture is credible only if the system can measure and improve those outcomes over time.

## 13. Final Architecture Position

The proposed system is an Azure-native, event-driven, multi-agent retail operating platform. It turns disconnected channel signals into coordinated decisions across customer understanding, personalization, inventory, pricing, and marketing, while preserving human approval, privacy compliance, regional adaptation, and measurable business outcomes.

The review prototype demonstrates the core loop on Azure Container Apps. The production architecture extends the same loop into Azure AI Foundry, Fabric, Event Hubs, AI Search, APIM, Logic Apps, Application Insights, Key Vault, and regional governance controls.
