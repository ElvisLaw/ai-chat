"""Settings management for AI Chat.

This module provides Pydantic-based settings validation.
"""

from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation.

    Automatically loads from environment variables.
    All API keys are optional to allow partial configuration.
    Users can configure only the LLM providers they want to use.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
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

    model: str = Field(
        default="gpt-4",
        validation_alias="MODEL"
    )

    max_tokens: int = Field(
        default=4096,
        validation_alias="MAX_TOKENS"
    )

    temperature: float = Field(
        default=0.7,
        validation_alias="TEMPERATURE"
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

    def get_model_config(self) -> dict[str, Any]:
        """Get the model configuration for LLM API calls.

        Returns:
            Dictionary with model, max_tokens, and temperature.
        """
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
