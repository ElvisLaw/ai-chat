from pathlib import Path

import pytest
from dotenv import dotenv_values

from app import settings as settings_module


ENV_KEY_TO_FIELD = {
    "OPENAI_API_KEY": "openai_api_key",
    "ANTHROPIC_API_KEY": "anthropic_api_key",
    "OPENAI_BASE_URL": "openai_base_url",
    "MODEL": "model",
    "MAX_TOKENS": "max_tokens",
    "TEMPERATURE": "temperature",
    "CORS_ORIGINS": "cors_origins",
    "API_HOST": "api_host",
    "API_PORT": "api_port",
}


def test_settings_env_file_points_to_project_root() -> None:
    expected = Path(__file__).resolve().parents[1] / ".env"

    assert settings_module.ENV_FILE == expected
    assert Path(settings_module.Settings.model_config["env_file"]) == expected


def test_get_settings_returns_shared_instance() -> None:
    original = settings_module._settings_instance
    try:
        settings_module._settings_instance = None
        first = settings_module.get_settings()
        second = settings_module.get_settings()
        assert first is second
    finally:
        settings_module._settings_instance = original


def test_settings_load_from_root_env_when_cwd_changes(monkeypatch: pytest.MonkeyPatch) -> None:
    env_values = dotenv_values(settings_module.ENV_FILE)
    candidates = [
        (key, value)
        for key, value in env_values.items()
        if key in ENV_KEY_TO_FIELD and value not in (None, "")
    ]

    if not candidates:
        pytest.skip("No supported keys found in the project .env file")

    key, expected = candidates[0]
    field_name = ENV_KEY_TO_FIELD[key]
    original = settings_module._settings_instance

    try:
        settings_module._settings_instance = None
        for env_key in ENV_KEY_TO_FIELD:
            monkeypatch.delenv(env_key, raising=False)
        monkeypatch.chdir(Path("/"))

        settings = settings_module.Settings()
        assert str(getattr(settings, field_name)) == str(expected)
    finally:
        settings_module._settings_instance = original