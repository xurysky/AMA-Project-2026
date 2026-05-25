@description('Azure region for all deployable resources.')
param location string = resourceGroup().location

@description('Short lowercase app name used in resource names.')
@minLength(3)
@maxLength(18)
param appName string = 'amaretail'

@description('Container image to deploy, for example myacr.azurecr.io/ama-retail-agent:latest.')
param containerImage string

@description('Container registry server, for example myacr.azurecr.io.')
param containerRegistryServer string

@description('Container registry username. For production, prefer managed identity with AcrPull.')
param containerRegistryUsername string

@secure()
@description('Container registry password. For production, prefer managed identity with AcrPull.')
param containerRegistryPassword string

@description('Azure OpenAI endpoint. Keep the key in Key Vault or app secrets outside this template.')
param azureOpenAIEndpoint string = ''

@secure()
@description('Azure OpenAI key for the demo app. For production, prefer Managed Identity where supported.')
param azureOpenAIKey string = ''

@description('Azure OpenAI deployment name used by the demo.')
param azureOpenAIDeployment string = 'gpt-4o'

@description('Enable Cosmos DB backed run/work-order/audit persistence.')
param enableCosmosRunStore bool = true

var normalizedAppName = toLower(replace(appName, '-', ''))
var logAnalyticsName = 'law-${normalizedAppName}'
var containerEnvName = 'cae-${normalizedAppName}'
var containerAppName = 'ca-${normalizedAppName}-api'
var cosmosName = 'cosmos-${normalizedAppName}-${uniqueString(resourceGroup().id)}'
var appInsightsName = 'appi-${normalizedAppName}'

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {
  name: cosmosName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-05-15' = {
  parent: cosmos
  name: 'ama-retail'
  properties: {
    resource: {
      id: 'ama-retail'
    }
  }
}

resource customerContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: database
  name: 'customer360'
  properties: {
    resource: {
      id: 'customer360'
      partitionKey: {
        paths: [
          '/customer_id'
        ]
        kind: 'Hash'
      }
    }
  }
}

resource runsContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-05-15' = {
  parent: database
  name: 'agentRuns'
  properties: {
    resource: {
      id: 'agentRuns'
      partitionKey: {
        paths: [
          '/partition_key'
        ]
        kind: 'Hash'
      }
    }
  }
}

resource containerEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: containerEnvName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: containerAppName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8080
        transport: 'auto'
      }
      secrets: [
        {
          name: 'acr-password'
          value: containerRegistryPassword
        }
        {
          name: 'cosmos-key'
          value: cosmos.listKeys().primaryMasterKey
        }
        {
          name: 'azure-openai-key'
          value: azureOpenAIKey
        }
      ]
      registries: [
        {
          server: containerRegistryServer
          username: containerRegistryUsername
          passwordSecretRef: 'acr-password'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'api'
          image: containerImage
          env: [
            {
              name: 'AZURE_OPENAI_ENDPOINT'
              value: azureOpenAIEndpoint
            }
            {
              name: 'AZURE_OPENAI_DEPLOYMENT'
              value: azureOpenAIDeployment
            }
            {
              name: 'AZURE_OPENAI_KEY'
              secretRef: 'azure-openai-key'
            }
            {
              name: 'AZURE_OPENAI_API_KEY'
              secretRef: 'azure-openai-key'
            }
            {
              name: 'AZURE_COSMOS_ENDPOINT'
              value: cosmos.properties.documentEndpoint
            }
            {
              name: 'AZURE_COSMOS_KEY'
              secretRef: 'cosmos-key'
            }
            {
              name: 'AZURE_COSMOS_DB'
              value: database.name
            }
            {
              name: 'AZURE_COSMOS_CONTAINER'
              value: customerContainer.name
            }
            {
              name: 'AZURE_COSMOS_RUNS_CONTAINER'
              value: runsContainer.name
            }
            {
              name: 'ENABLE_COSMOS_RUN_STORE'
              value: string(enableCosmosRunStore)
            }
            {
              name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
              value: appInsights.properties.ConnectionString
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
        rules: [
          {
            name: 'http-scale'
            http: {
              metadata: {
                concurrentRequests: '50'
              }
            }
          }
        ]
      }
    }
  }
}

output apiUrl string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
output cosmosEndpoint string = cosmos.properties.documentEndpoint
output applicationInsightsName string = appInsights.name
