"""
AMA Retail Agent Platform - Base Agent
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class AgentMessage(BaseModel):
    """Agent 间通信消息"""
    sender: str
    receiver: str
    content: Dict[str, Any]
    message_type: str  # "request", "response", "event"
    correlation_id: Optional[str] = None


class BaseAgent(ABC):
    """Agent 基类"""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self._message_handlers = {}
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理输入数据，返回结果"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """健康检查"""
        pass
    
    async def handle_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """处理来自其他 Agent 的消息"""
        handler = self._message_handlers.get(message.message_type)
        if handler:
            return await handler(message)
        self.logger.warning(f"No handler for message type: {message.message_type}")
        return None
    
    def register_handler(self, message_type: str, handler):
        """注册消息处理器"""
        self._message_handlers[message_type] = handler
    
    async def send_message(self, message: AgentMessage):
        """发送消息给其他 Agent（通过 Event Hub）"""
        self.logger.info(f"Sending message to {message.receiver}: {message.message_type}")
        # TODO: 实现 Event Hub 发送
        pass
