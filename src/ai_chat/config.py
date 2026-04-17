from dotenv import load_dotenv

from .settings import ENV_FILE, get_settings


def load_config() -> None:
    """Compatibility helper that reuses the shared settings source."""
    get_settings()

    if ENV_FILE.exists():
        load_dotenv(ENV_FILE)
        return

    load_dotenv()


def get_env(key: str, default: str | None = None) -> str | None:
    """Get an environment variable value.

    Args:
        key: The environment variable name.
        default: Default value if key is not found.

    Returns:
        The environment variable value or default.
    """
    import os
    return os.environ.get(key, default)
