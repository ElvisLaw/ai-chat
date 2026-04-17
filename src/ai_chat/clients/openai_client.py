"""OpenAI GPT 客户端实现。"""

from typing import Any, Iterator

from openai import OpenAI

from .base import BaseLLMClient, ConfigurationError, LLMError


class OpenAIClient(BaseLLMClient):
    """OpenAI GPT 模型客户端。

    使用 OpenAI SDK 与 GPT 模型通信。
    支持自定义 base_url，可用于 MiniMax 等 API 兼容提供商。
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        base_url: str | None = None,
        **kwargs: Any,
    ) -> None:
        """初始化 OpenAI 客户端。

        Args:
            api_key: OpenAI API 密钥。
            model: 模型标识符（默认: gpt-4）。
            base_url: 可选的自定义 API 基础 URL（例如用于 MiniMax）。
            **kwargs: 其他参数（max_tokens, temperature）。

        Raises:
            ConfigurationError: API 密钥为空或仅包含空白字符。
        """
        if not api_key or not api_key.strip():
            raise ConfigurationError("OpenAI API key is required")

        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        self._client = OpenAI(**client_kwargs)
        self._model = model
        self._kwargs = kwargs

    def send_message(self, messages: list[dict], **kwargs: Any) -> str:
        """发送消息并接收响应。

        Args:
            messages: 完整消息历史列表（包含 system、user、assistant 消息）。
            **kwargs: 其他参数（model 覆盖等）。

        Returns:
            模型的响应文本。

        Raises:
            LLMError: API 调用失败。
        """
        try:
            response = self._client.chat.completions.create(
                model=kwargs.pop("model", self._model),
                messages=messages,
                **{**self._kwargs, **kwargs}
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise LLMError(f"OpenAI API error: {e}") from e

    def stream_message(self, messages: list[dict], **kwargs: Any) -> Iterator[str]:
        """流式接收响应内容块。

        Args:
            messages: 完整消息历史列表。
            **kwargs: 其他参数（model 覆盖等）。

        Yields:
            响应内容块，逐块返回。

        Raises:
            LLMError: API 调用失败。
        """
        try:
            stream = self._client.chat.completions.create(
                model=kwargs.pop("model", self._model),
                messages=messages,
                stream=True,
                **{**self._kwargs, **kwargs}
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            raise LLMError(f"OpenAI API error: {e}") from e
