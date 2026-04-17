"""基础 LLM 客户端接口和异常类。"""

from abc import ABC, abstractmethod
from typing import Iterator


class LLMError(Exception):
    """LLM 客户端错误基类。"""

    pass


class ConfigurationError(LLMError):
    """配置相关错误。"""

    pass


class BaseLLMClient(ABC):
    """LLM 客户端抽象基类。

    所有 LLM 客户端实现必须继承此类并实现必要的方法。
    """

    @abstractmethod
    def send_message(self, messages: list[dict], **kwargs) -> str:
        """发送消息并获取响应。

        Args:
            messages: 已组装好的消息列表。
            **kwargs: 提供商特定的其他参数。

        Returns:
            LLM 的响应文本。

        Raises:
            LLMError: API 调用期间发生错误。
            ConfigurationError: 缺少必要配置。
        """
        pass

    @abstractmethod
    def stream_message(self, messages: list[dict], **kwargs) -> Iterator[str]:
        """发送消息并流式接收响应。

        Args:
            messages: 已组装好的消息列表。
            **kwargs: 提供商特定的其他参数。

        Yields:
            响应内容块，逐块返回。

        Raises:
            LLMError: API 调用期间发生错误。
            ConfigurationError: 缺少必要配置。
        """
        pass
