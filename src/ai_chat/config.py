from pathlib import Path
from dotenv import load_dotenv


def load_config() -> None:
    """Load configuration from .env file.

    This function searches for a .env file in the project root
    and loads all environment variables from it.
    """
    # Find the project root (where .env should be located)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent

    env_path = project_root / ".env"

    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Try current directory as fallback
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
