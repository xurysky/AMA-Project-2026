# Panel Readiness Notes

## One-Minute Opening

I built an Autonomous Retail Intelligence Agent Platform for fashion retail. The core problem is that retail decisions are interconnected: inventory, pricing, customer intent, personalization, and marketing cannot be optimized in isolation.

My architecture uses a multi-agent operating model with shared state, work orders, human approval, auditability, and Azure-native deployment. The current prototype is running on Azure Container Apps with Cosmos DB-backed state, and the target architecture extends to Azure OpenAI / AI Foundry, API Management, Managed Identity, Key Vault, Application Insights, and Log Analytics.

The value of the project is not a single demo screen. It is a reviewable path from business problem to architecture decisions, cloud deployment, operational evidence, and a production expansion model.

## What To Say About The Gap

The main gap was not lack of work; it was packaging and evidence visibility. I had a working Azure deployment and local engineering artifacts, but I did not consolidate the repository, deployment evidence, and architectural narrative clearly enough for the panel to review. I am using the mentoring track to make the work reproducible, auditable, and easier to evaluate.

## Current Demo Facts

- Live URL: https://ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io/
- Runtime: Azure Container Apps
- State store: Cosmos DB
- Health: `/health` returns `healthy`
- Image: `amaregistry.azurecr.io/ama-retail-agent:20260519-120038`
- Active revision: `ama-retail-control-tower--0000006`

## Architecture Decisions To Emphasize

### 1. Container Apps over a VM

The VM was useful as a temporary demo host, but the target runtime is Azure Container Apps. Container Apps better supports containerized deployment, revisioning, scale-out, and a clearer path to managed identity and platform observability.

### 2. Cosmos DB for shared agent state

Agent demos often fail because each step is stateless or hidden inside a notebook. Cosmos DB makes the run state, work orders, shared memory, and audit trail durable and inspectable.

### 3. Human approval in the loop

Pricing, promotion, and stock decisions carry business risk. The architecture uses work orders and approval states instead of pretending that agents should autonomously execute every decision.

### 4. Region-aware architecture

The demo includes region-specific concerns such as China data residency, consent, PIPL, local channels, and marketplace context. This is important for real enterprise adoption in Asia.

### 5. Simulation claims are separated from production evidence

ROI, conversion, and cycle-compression numbers are target hypotheses or simulation assumptions. The validated evidence is the architecture pattern, deployed runtime, state management, and operational flow.

## Questions To Ask The Mentor

- What specific architectural depth did the panel expect to see but did not see?
- Should I focus more on enterprise security, operations, or agent orchestration patterns?
- Which two trade-offs should I make most explicit for the final panel?
- Is the Azure-native deployment path sufficient, or should I add a deployment walkthrough video and architecture diagram?
- Should the business narrative focus on retail operating model transformation or on reusable multi-agent platform architecture?

## Panel Answer Pattern

Use this shape for difficult questions:

1. Acknowledge the concern.
2. State the design choice.
3. Explain the trade-off.
4. Point to evidence in the repo or live deployment.
5. State the production hardening path.

Example:

> That is a fair concern. In the prototype, I chose Azure Container Apps and Cosmos DB because I wanted a reviewable runtime with durable run state rather than a notebook-only demo. The trade-off is that some enterprise controls, such as Managed Identity-only ACR pull and Key Vault integration, are documented as the production path rather than fully hardened in the demo. The evidence is the running Container App, the health endpoint, the Cosmos-backed state store, and the Bicep deployment template. The next hardening step is to replace demo registry credentials with Managed Identity plus AcrPull, and to move all secrets into Key Vault.

