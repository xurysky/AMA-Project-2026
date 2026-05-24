# AMA Recovery Pack

## Current Position

This project has working Azure deployment evidence. The gap to close for the Azure Master Architect panel is not whether the prototype exists, but whether the repository, deployment artifacts, architecture decisions, and narrative make the work reproducible and reviewable.

## Live Azure Evidence

- Live demo: https://ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io/
- Health endpoint: https://ama-retail-control-tower.whitemushroom-e4cd40d2.japaneast.azurecontainerapps.io/health
- Azure resource group: `ama-retail-agent`
- Azure Container App: `ama-retail-control-tower`
- Region: `Japan East`
- Container image: `amaregistry.azurecr.io/ama-retail-agent:20260519-120038`
- Active revision: `ama-retail-control-tower--0000006`
- Runtime health: `Healthy`
- State store: `Cosmos DB`

Health response captured on 2026-05-24:

```json
{
  "status": "healthy",
  "active_runs": 2,
  "state_store": "cosmos_db"
}
```

## Azure Resources Observed

The `ama-retail-agent` resource group contains:

- Azure OpenAI resources: `ama-openai`, `ama-openai-jp`
- Cosmos DB: `ama-cosmos`
- Azure Container Apps environment: `ama-cae`
- Azure Container Registry: `amaregistry`
- Container App: `ama-retail-control-tower`
- Log Analytics workspace / managed workspace resources
- Temporary VM resources used during earlier demo hosting and validation

## Architecture Narrative

The project is an Autonomous Retail Intelligence Agent Platform for a fashion retail operating model. It decomposes retail decision-making into five cooperating agents:

- Customer Understanding Agent
- Personalization Agent
- Inventory Agent
- Pricing Agent
- Marketing Agent

The architectural premise is that retail decisions are interdependent. Pricing cannot ignore inventory, personalization cannot recommend unavailable items, and marketing should be constrained by margin, stockout risk, consent, and channel context. The demo therefore focuses on a shared operating state, work orders, approval flow, traceable agent handoff, and state persistence.

## Azure-Native Target

The intended architecture is Azure-native:

```text
Browser / evaluator
  -> Azure Container Apps ingress
  -> FastAPI Agent Runtime
  -> Azure OpenAI / Azure AI Foundry
  -> Cosmos DB for run state, work orders, Customer 360, and audit logs
  -> Application Insights + Log Analytics
  -> API Management / Managed Identity / Key Vault for enterprise integration
```

The current implementation already demonstrates the core runtime pattern through Azure Container Apps and Cosmos-backed state. The repository also includes a Bicep template, GitHub Actions workflow, and deployment scripts to make the deployment path reviewable.

## What Was Missing From the Panel View

The strongest engineering evidence was not fully visible because local work had not been consolidated and pushed:

- Six local commits were ahead of `origin/main`.
- Azure-native deployment docs were local only.
- Bicep infrastructure and GitHub Actions workflow were local only.
- Container Apps deployment script was local only.
- Cosmos-backed state integration and runtime evidence were not packaged as panel material.

The recovery work is to make this evidence visible, reproducible, and easy for the mentor and panel to evaluate.

## Evidence Checklist

- [x] Live Azure Container App running
- [x] Health endpoint returns `healthy`
- [x] Cosmos-backed state store enabled
- [x] Container image exists in ACR
- [x] Azure-native deployment document exists
- [x] Bicep infrastructure template exists
- [x] GitHub Actions deployment workflow exists
- [x] Deployment script exists
- [ ] Clean repository commit prepared
- [ ] Repository pushed after explicit approval
- [ ] Architecture diagram refreshed for final panel narrative
- [ ] Panel dry-run story prepared

## Four-Week Mentoring Track Alignment

### Week 1: Strengths & Gap Assessment

Bring this pack as the baseline. Ask the mentor to pressure-test:

- Whether the Azure-native architecture is deep enough for the credential.
- Which trade-offs require more explicit explanation.
- Whether the demo should be positioned as a production target architecture, a working prototype, or both.

### Week 2: Closing the Gaps

Prioritize gaps that matter to a Master Architect panel:

- Identity and secret management path: Managed Identity, Key Vault, and GitHub OIDC.
- State and audit design: Cosmos DB schema, work order lifecycle, approval history.
- Reliability and operations: observability, rollback, scaling, failure modes.
- Security and compliance: consent, PIPL/GDPR positioning, data residency by region.

### Week 3: Storytelling & Narrative

Frame the work as an architecture decision journey:

1. Business problem: fashion retail decisions are fragmented and slow.
2. Architectural insight: AI agents need shared state, constraints, and governance.
3. Azure design: Container Apps runtime, Cosmos state, Azure OpenAI reasoning, observability and enterprise integration.
4. Trade-offs: prototype scope vs production path, simulation vs validated ROI, speed vs governance.
5. Outcome: a reviewable, deployable, extensible agent operating model.

### Week 4: Final Panel Preparation

Run the panel story end-to-end:

- Open live URL.
- Show `/health`.
- Show repository structure.
- Walk through architecture diagram.
- Explain two key ADRs.
- Demonstrate one run from trigger to agent handoff to approval.
- Answer trade-off questions without overclaiming production validation.

