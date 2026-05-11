"""
Azure AI Foundry 配置模块
统一管理 Azure OpenAI、Cosmos DB 等连接
"""

import os
from dotenv import load_dotenv

load_dotenv()


class AzureConfig:
    """Azure AI Foundry 连接配置"""

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT = os.getenv(
        "AZURE_OPENAI_ENDPOINT",
        "https://aif-ni7mzwp3nog6i.cognitiveservices.azure.com/"
    )
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.4-mini")

    # Cosmos DB
    COSMOS_DB_ENDPOINT = os.getenv("COSMOS_DB_ENDPOINT", "")
    COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY", "")
    COSMOS_DB_DATABASE = os.getenv("COSMOS_DB_DATABASE", "ama-retail")

    # App
    MOCK = os.getenv("MOCK", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def get_openai_client(cls):
        """获取 Azure OpenAI 客户端"""
        if cls.MOCK:
            from mock_clients import MockOpenAIClient
            return MockOpenAIClient()

        from openai import AzureOpenAI
        return AzureOpenAI(
            azure_endpoint=cls.AZURE_OPENAI_ENDPOINT,
            api_key=cls.AZURE_OPENAI_API_KEY,
            api_version=cls.AZURE_OPENAI_API_VERSION,
        )

    @classmethod
    def get_deployment_name(cls) -> str:
        """获取模型部署名称"""
        return cls.AZURE_OPENAI_DEPLOYMENT
