"""Settings management for AI Chat.

This module provides Pydantic-based settings validation.
"""

from typing import Any

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings with validation.

    All API keys are optional to allow partial configuration.
    Users can configure only the LLM providers they want to use.
    """

    openai_api_key: str | None = Field(
        default=None,
        description="OpenAI API key for GPT models"
    )

    anthropic_api_key: str | None = Field(
        default=None,
        description="Anthropic API key for Claude models"
    )

    model: str = Field(
        default="gpt-4",
        description="Default LLM model to use"
    )

    max_tokens: int = Field(
        default=4096,
        description="Maximum number of tokens in response"
    )

    temperature: float = Field(
        default=0.7,
        description="LLM temperature setting (0.0-2.0)"
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
