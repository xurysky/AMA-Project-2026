# Azure 云原生部署

当前原型已经容器化，但目标架构不是“单台 Azure VM 托管一个应用”，而是 Azure 云原生运行方式。

## 目标运行架构

```text
浏览器 / 评委访问
  -> Azure Container Apps Ingress
  -> FastAPI Agent Runtime
  -> Azure OpenAI / Azure AI Foundry
  -> Cosmos DB 保存 Agent 状态、工单、Customer 360、审计日志
  -> Application Insights + Log Analytics 可观测性
```

生产化可扩展为：

- Azure Static Web Apps 或 Storage Static Website 托管前端。
- Azure Container Apps 托管 FastAPI Agent Runtime。
- Azure Cosmos DB 保存 run state、work orders、shared memory、audit logs。
- Azure OpenAI 和 Azure AI Foundry 负责推理、编排、评估。
- Azure AI Search 提供商品、FAQ、政策知识库检索。
- API Management 作为企业 API/MCP 网关。
- Managed Identity、Key Vault、App Configuration 管理身份、密钥和配置。
- Event Grid 或 Service Bus 驱动异步 Agent 任务。
- Microsoft Fabric 和 Power BI 承接 BI feedback loop。

## 本仓库当前可部署内容

`infra/main.bicep` 提供一个务实的 demo 环境：

- Azure Container Apps 环境和公开访问的 Container App。
- Cosmos DB serverless account，包含 `customer360` 和 `agentRuns` 容器。
- Log Analytics workspace。
- Application Insights。
- 为了 demo 简洁，Container Apps 使用 ACR pull credentials 拉取镜像；生产环境建议替换为 Managed Identity + `AcrPull`。

当环境变量开启后，Container App 会把仿真 run、工单和审计日志写入 Cosmos DB：

```bash
ENABLE_COSMOS_RUN_STORE=true
```

这样 demo 状态不再只存在 VM/进程内存中，而是进入持久化云原生状态层。

## 手动部署

前提：

- Azure CLI 已登录。
- 目标订阅里有或准备创建一个 Azure Container Registry。
- 已有 Azure OpenAI endpoint 和模型 deployment。

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

脚本会输出公开 API 地址。访问：

```text
https://<container-app-url>/
https://<container-app-url>/health
```

## GitHub Actions 部署

`.github/workflows/azure-container-apps.yml` 需要以下 repo secrets：

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`
- `AZURE_CONTAINER_REGISTRY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_KEY`
- `AZURE_OPENAI_DEPLOYMENT`

建议使用 GitHub Actions OIDC federated credentials，不要把 Azure 密码或本地 `.env` 提交到仓库。

## 对评委的表述

如果当前 demo 暂时跑在其他地方，可以这样解释：

> 当前 demo 已容器化，可以部署到 Azure Container Apps。目标架构是 Azure 云原生：Azure Container Apps 承载 Agent Runtime，Cosmos DB 保存 Agent 状态和审计日志，Azure OpenAI / AI Foundry 负责推理和编排，Application Insights 做可观测性，API Management / Managed Identity / Key Vault 提供企业级集成和安全。
