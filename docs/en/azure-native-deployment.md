# Azure-Native Deployment

The prototype is containerized for demonstration, but the intended architecture is Azure-native rather than a single VM-hosted application.

## Target Runtime

```text
Browser / evaluator
  -> Azure Container Apps ingress
  -> FastAPI Agent Runtime
  -> Azure OpenAI / Azure AI Foundry
  -> Cosmos DB agent state, work orders, Customer 360 and audit log
  -> Application Insights + Log Analytics
```

Recommended production expansion:

- Azure Static Web Apps or Storage Static Website for the UI.
- Azure Container Apps for the FastAPI agent runtime.
- Azure Cosmos DB for run state, work orders, shared memory and audit logs.
- Azure OpenAI and Azure AI Foundry for reasoning, orchestration and evaluation.
- Azure AI Search for product, FAQ and policy knowledge retrieval.
- API Management as the enterprise API/MCP gateway.
- Managed Identity, Key Vault and App Configuration for secrets and settings.
- Event Grid or Service Bus for asynchronous agent work.
- Microsoft Fabric and Power BI for BI feedback loops.

## What This Repo Deploys

The included Bicep template deploys a pragmatic demo environment:

- Azure Container Apps environment and public Container App.
- Cosmos DB serverless account with `customer360` and `agentRuns` containers.
- Log Analytics workspace.
- Application Insights instance.
- ACR pull credentials wired into Container Apps for demo simplicity. For production, replace this with Managed Identity plus `AcrPull`.

The Container App stores stateful simulation runs in Cosmos DB when:

```bash
ENABLE_COSMOS_RUN_STORE=true
```

This moves the demo from VM process memory to a durable cloud-native state store.

## Manual Deployment

Prerequisites:

- Azure CLI logged in.
- An Azure Container Registry name available in the target subscription.
- Azure OpenAI endpoint and deployment already provisioned.

```bash
export AZURE_RESOURCE_GROUP=rg-ama-retail
export AZURE_LOCATION=eastasia
export AZURE_CONTAINER_REGISTRY=<your-acr-name>
export APP_NAME=amaretail
export AZURE_OPENAI_ENDPOINT=https://<your-aoai-resource>.openai.azure.com/
export AZURE_OPENAI_KEY=<your-aoai-key>
export AZURE_OPENAI_DEPLOYMENT=gpt-4o

bash scripts/deploy-container-app.sh
```

The script prints the public API URL. Open:

```text
https://<container-app-url>/
https://<container-app-url>/health
```

## GitHub Actions Deployment

The workflow `.github/workflows/azure-container-apps.yml` expects these repository secrets:

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`
- `AZURE_CONTAINER_REGISTRY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_KEY`
- `AZURE_OPENAI_DEPLOYMENT`

Use OIDC federated credentials for the GitHub Actions identity. Do not store Azure passwords or local `.env` files in the repo.

## Demo Positioning

If the prototype is temporarily hosted elsewhere, describe that as a hosting shortcut:

> The current demo is containerized and can be deployed to Azure Container Apps. The target architecture is Azure-native: Azure Container Apps for the agent runtime, Cosmos DB for persistent agent state and audit logs, Azure OpenAI / AI Foundry for reasoning and orchestration, Application Insights for observability, and API Management / Managed Identity / Key Vault for enterprise integration.
