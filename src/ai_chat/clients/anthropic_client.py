"""Anthropic Claude 客户端实现。"""

from typing import Any, Iterator

from anthropic import Anthropic

from .base import BaseLLMClient, ConfigurationError, LLMError


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude 模型客户端。

    使用 Anthropic SDK 与 Claude 模型通信。
    """

    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229", **kwargs: Any) -> None:
        """初始化 Anthropic 客户端。

        Args:
            api_key: Anthropic API 密钥。
            model: 模型标识符（默认: claude-3-sonnet-20240229）。
            **kwargs: 其他参数（max_tokens, temperature）。

        Raises:
            ConfigurationError: API 密钥为空或仅包含空白字符。
        """
        if not api_key or not api_key.strip():
            raise ConfigurationError("Anthropic API key is required")

        self._client = Anthropic(api_key=api_key)
        self._model = model
        self._kwargs = kwargs

    def send_message(self, message: str, **kwargs: Any) -> str:
        """发送消息并接收响应。

        Args:
            message: 用户消息。
            **kwargs: 其他参数（system_prompt, model 覆盖等, conversation_messages 历史消息）。

        Returns:
            模型的响应文本。

        Raises:
            LLMError: API 调用失败。
        """
        try:
            system_prompt = kwargs.pop("system_prompt", None)
            conversation_messages = kwargs.pop("conversation_messages", None)
            max_tokens = kwargs.pop("max_tokens", 1024)

            # 构建消息列表
            messages = []
            if conversation_messages:
                for msg in conversation_messages:
                    if msg["role"] != "system":
                        messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": message})

            response = self._client.messages.create(
                model=kwargs.pop("model", self._model),
                system=system_prompt,
                max_tokens=max_tokens,
                messages=messages,
                **{**self._kwargs, **kwargs}
            )
            return response.content[0].text
        except Exception as e:
            raise LLMError(f"Anthropic API error: {e}") from e

    def stream_message(self, message: str, **kwargs: Any) -> Iterator[str]:
        """流式接收响应内容块。

        Args:
            message: 用户消息。
            **kwargs: 其他参数（conversation_messages 历史消息）。

        Yields:
            响应内容块，逐块返回。

        Raises:
            LLMError: API 调用失败。
        """
        try:
            system_prompt = kwargs.pop("system_prompt", None)
            conversation_messages = kwargs.pop("conversation_messages", None)
            max_tokens = kwargs.pop("max_tokens", 1024)

            # 构建消息列表
            messages = []
            if conversation_messages:
                for msg in conversation_messages:
                    if msg["role"] != "system":
                        messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": message})

            with self._client.messages.stream(
                model=kwargs.pop("model", self._model),
                system=system_prompt,
                max_tokens=max_tokens,
                messages=messages,
                **{**self._kwargs, **kwargs}
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            raise LLMError(f"Anthropic API error: {e}") from e
