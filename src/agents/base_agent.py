"""
Base Agent — 所有 Agent 的基类
实现 Agent 模式：消息传递、生命周期管理、健康检查
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from pydantic import BaseModel
from datetime import datetime
import logging
import uuid
import json
import sys
import os

# 确保 src 目录在路径中
_src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from config import AzureConfig

logger = logging.getLogger(__name__)


class AgentMessage(BaseModel):
    """Agent 间通信消息（A2A Protocol 兼容）"""
    message_id: str = None
    sender: str
    receiver: str
    content: Dict[str, Any]
    message_type: str  # "handoff_request", "handoff_result", "event", "state_update"
    correlation_id: Optional[str] = None
    priority: str = "normal"  # "critical", "high", "normal", "low"
    timestamp: str = None

    def __init__(self, **data):
        if data.get("message_id") is None:
            data["message_id"] = str(uuid.uuid4())
        if data.get("timestamp") is None:
            data["timestamp"] = datetime.utcnow().isoformat()
        if data.get("correlation_id") is None:
            data["correlation_id"] = str(uuid.uuid4())
        super().__init__(**data)


class AgentMetrics:
    """Agent 性能指标收集"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.requests_total = 0
        self.requests_success = 0
        self.requests_failed = 0
        self.latency_ms: List[float] = []
        self.last_health_check: Optional[datetime] = None

    def record_request(self, success: bool, latency_ms: float):
        self.requests_total += 1
        if success:
            self.requests_success += 1
        else:
            self.requests_failed += 1
        self.latency_ms.append(latency_ms)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "requests_total": self.requests_total,
            "success_rate": self.requests_success / max(self.requests_total, 1),
            "avg_latency_ms": sum(self.latency_ms) / max(len(self.latency_ms), 1),
            "p95_latency_ms": sorted(self.latency_ms)[int(len(self.latency_ms) * 0.95)] if self.latency_ms else 0,
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None
        }


class BaseAgent(ABC):
    """
    Agent 基类 — 实现 Agent 设计模式
    
    所有 Agent 继承此类，实现：
    - process(): 核心业务逻辑
    - health_check(): 健康检查
    - handle_message(): 处理其他 Agent 的消息
    """

    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.logger = logging.getLogger(f"agent.{agent_id}")
        self.metrics = AgentMetrics(agent_id)
        self._message_handlers: Dict[str, Callable] = {}
        self._state: Dict[str, Any] = {}

        # 注册默认处理器
        self.register_handler("health_check", self._handle_health_check)
        self.register_handler("metrics", self._handle_metrics)

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理输入数据，返回结果 — 子类必须实现"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """健康检查 — 子类必须实现"""
        pass

    async def handle_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """处理来自其他 Agent 的消息"""
        start_time = datetime.utcnow()

        self.logger.info(f"Received {message.message_type} from {message.sender} "
                        f"[correlation_id={message.correlation_id}]")

        handler = self._message_handlers.get(message.message_type)
        if handler:
            try:
                result = await handler(message)
                latency = (datetime.utcnow() - start_time).total_seconds() * 1000
                self.metrics.record_request(success=True, latency_ms=latency)
                return result
            except Exception as e:
                latency = (datetime.utcnow() - start_time).total_seconds() * 1000
                self.metrics.record_request(success=False, latency_ms=latency)
                self.logger.error(f"Error handling message: {e}")
                return AgentMessage(
                    sender=self.agent_id,
                    receiver=message.sender,
                    content={"error": str(e), "original_message_id": message.message_id},
                    message_type="error",
                    correlation_id=message.correlation_id
                )
        else:
            self.logger.warning(f"No handler for message type: {message.message_type}")
            return None

    def register_handler(self, message_type: str, handler: Callable):
        """注册消息处理器"""
        self._message_handlers[message_type] = handler
        self.logger.debug(f"Registered handler for message type: {message_type}")

    async def send_message(self, message: AgentMessage):
        """发送消息给其他 Agent（通过 Event Hub / A2A Protocol）"""
        self.logger.info(f"Sending {message.message_type} to {message.receiver} "
                        f"[correlation_id={message.correlation_id}]")
        # 实际实现：通过 Event Hub 发送
        # await self.event_hub.send(message.model_dump())

    async def send_and_wait(self, request: AgentMessage, timeout_ms: int = 5000) -> Dict[str, Any]:
        """发送请求并等待响应（同步 handoff）"""
        await self.send_message(request)
        # 实际实现：等待响应消息
        # response = await self.response_queue.wait(request.correlation_id, timeout_ms)
        # return response.content
        return {"status": "mock_response"}

    async def _handle_health_check(self, message: AgentMessage) -> AgentMessage:
        """默认健康检查处理器"""
        is_healthy = await self.health_check()
        self.metrics.last_health_check = datetime.utcnow()
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            content={"healthy": is_healthy, "metrics": self.metrics.get_summary()},
            message_type="health_check_response",
            correlation_id=message.correlation_id
        )

    async def _handle_metrics(self, message: AgentMessage) -> AgentMessage:
        """默认指标查询处理器"""
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            content=self.metrics.get_summary(),
            message_type="metrics_response",
            correlation_id=message.correlation_id
        )

    def get_state(self, key: str, default: Any = None) -> Any:
        """获取 Agent 状态"""
        return self._state.get(key, default)

    def set_state(self, key: str, value: Any):
        """设置 Agent 状态"""
        self._state[key] = value

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.agent_id} name={self.name}>"
