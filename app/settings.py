"""Settings management for AI Chat.

This module provides Pydantic-based settings validation.
"""

from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Provider-specific default models
DEFAULT_MODELS = {
    "openai": "gpt-4",
    "anthropic": "claude-3-sonnet-20240229",
}

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"

# Settings singleton instance
_settings_instance: "Settings | None" = None


def get_settings() -> "Settings":
    """获取 Settings 单例。

    首次调用时自动加载 .env 文件，之后返回同一实例。

    Returns:
        Settings 单例。
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance


class Settings(BaseSettings):
    """Application settings with validation.

    Automatically loads from environment variables.
    All API keys are optional to allow partial configuration.
    Users can configure only the LLM providers they want to use.
    """

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Allow extra fields in .env
    )

    openai_api_key: str | None = Field(
        default=None,
        validation_alias="OPENAI_API_KEY"
    )

    anthropic_api_key: str | None = Field(
        default=None,
        validation_alias="ANTHROPIC_API_KEY"
    )

    openai_base_url: str | None = Field(
        default=None,
        validation_alias="OPENAI_BASE_URL"
    )

    model: str | None = Field(
        default=None,
        validation_alias="MODEL",
        description="全局默认模型（可选）"
    )

    max_tokens: int = Field(
        default=4096,
        validation_alias="MAX_TOKENS"
    )

    # Memory settings
    memory_buffer_size: int = Field(
        default=20,
        validation_alias="MEMORY_BUFFER_SIZE",
        description="对话缓冲最大消息数"
    )

    memory_max_tokens: int = Field(
        default=4000,
        validation_alias="MEMORY_MAX_TOKENS",
        description="对话缓冲最大 Token 数"
    )

    memory_summarize_threshold_messages: int = Field(
        default=15,
        validation_alias="MEMORY_SUMMARIZE_THRESHOLD_MESSAGES",
        description="触发摘要的消息数阈值"
    )

    memory_summarize_threshold_tokens: int = Field(
        default=3000,
        validation_alias="MEMORY_SUMMARIZE_THRESHOLD_TOKENS",
        description="触发摘要的 Token 数阈值"
    )

    memory_retain_recent: int = Field(
        default=5,
        validation_alias="MEMORY_RETAIN_RECENT",
        description="摘要后保留的最新消息数"
    )

    memory_summary_max_chars: int = Field(
        default=2000,
        validation_alias="MEMORY_SUMMARY_MAX_CHARS",
        description="摘要最大字符数（约 500 字）"
    )

    conversation_store_type: str = Field(
        default="memory",
        validation_alias="CONVERSATION_STORE_TYPE",
        description="会话存储类型: memory 或 file"
    )

    temperature: float = Field(
        default=0.7,
        validation_alias="TEMPERATURE"
    )

    cors_origins: str | list[str] = Field(
        default="*",
        validation_alias="CORS_ORIGINS",
        description="CORS 允许的源"
    )

    api_host: str = Field(
        default="0.0.0.0",
        validation_alias="API_HOST",
        description="API 服务地址"
    )

    api_port: int = Field(
        default=8000,
        validation_alias="API_PORT",
        description="API 服务端口"
    )

    def is_openai_configured(self) -> bool:
        """Check if OpenAI is properly configured.

        Returns:
            True if openai_api_key is set and non-empty.
        """
        return bool(self.openai_api_key and self.openai_api_key.strip())

    def is_anthropic_configured(self) -> bool:
        """Check if Anthropic is properly configured.

        Returns:
            True if anthropic_api_key is set and non-empty.
        """
        return bool(self.anthropic_api_key and self.anthropic_api_key.strip())

    def get_default_model(self, provider: str) -> str:
        """Get the default model for a provider.

        Args:
            provider: LLM provider name (openai/anthropic).

        Returns:
            Default model name for the provider.
        """
        # Anthropic 始终使用自己的默认模型，不受全局 MODEL 影响
        if provider == "anthropic":
            return DEFAULT_MODELS["anthropic"]
        # OpenAI 兼容接口使用全局 MODEL 或默认
        return self.model or DEFAULT_MODELS.get(provider, "gpt-4")

    def get_model_config(self) -> dict[str, Any]:
        """Get the model configuration for LLM API calls.

        Returns:
            Dictionary with model, max_tokens, and temperature.
        """
        return {
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
