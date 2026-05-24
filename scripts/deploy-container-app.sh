#!/usr/bin/env bash
set -euo pipefail

: "${AZURE_RESOURCE_GROUP:?Set AZURE_RESOURCE_GROUP}"
: "${AZURE_LOCATION:=eastasia}"
: "${AZURE_CONTAINER_REGISTRY:?Set AZURE_CONTAINER_REGISTRY, for example amaacr1234}"
: "${APP_NAME:=amaretail}"
: "${AZURE_OPENAI_ENDPOINT:=}"
: "${AZURE_OPENAI_KEY:=}"
: "${AZURE_OPENAI_DEPLOYMENT:=gpt-4o}"

IMAGE_TAG="${IMAGE_TAG:-$(git rev-parse --short HEAD 2>/dev/null || date +%Y%m%d%H%M%S)}"
IMAGE="${AZURE_CONTAINER_REGISTRY}.azurecr.io/${APP_NAME}:${IMAGE_TAG}"

az group create \
  --name "${AZURE_RESOURCE_GROUP}" \
  --location "${AZURE_LOCATION}" \
  --output none

for provider in Microsoft.App Microsoft.ContainerRegistry Microsoft.DocumentDB Microsoft.Insights Microsoft.OperationalInsights; do
  az provider register --namespace "$provider" --wait --output none
done

az acr show --name "${AZURE_CONTAINER_REGISTRY}" --resource-group "${AZURE_RESOURCE_GROUP}" --output none 2>/dev/null || \
az acr create \
  --name "${AZURE_CONTAINER_REGISTRY}" \
  --resource-group "${AZURE_RESOURCE_GROUP}" \
  --sku Basic \
  --admin-enabled true \
  --output none

az acr update \
  --name "${AZURE_CONTAINER_REGISTRY}" \
  --admin-enabled true \
  --output none

az acr build \
  --registry "${AZURE_CONTAINER_REGISTRY}" \
  --image "${APP_NAME}:${IMAGE_TAG}" \
  .

ACR_USERNAME="$(az acr credential show --name "${AZURE_CONTAINER_REGISTRY}" --query username --output tsv)"
ACR_PASSWORD="$(az acr credential show --name "${AZURE_CONTAINER_REGISTRY}" --query 'passwords[0].value' --output tsv)"

az deployment group create \
  --resource-group "${AZURE_RESOURCE_GROUP}" \
  --template-file infra/main.bicep \
  --parameters \
    appName="${APP_NAME}" \
    location="${AZURE_LOCATION}" \
    containerImage="${IMAGE}" \
    containerRegistryServer="${AZURE_CONTAINER_REGISTRY}.azurecr.io" \
    containerRegistryUsername="${ACR_USERNAME}" \
    containerRegistryPassword="${ACR_PASSWORD}" \
    azureOpenAIEndpoint="${AZURE_OPENAI_ENDPOINT}" \
    azureOpenAIKey="${AZURE_OPENAI_KEY}" \
    azureOpenAIDeployment="${AZURE_OPENAI_DEPLOYMENT}" \
  --query properties.outputs.apiUrl.value \
  --output tsv
