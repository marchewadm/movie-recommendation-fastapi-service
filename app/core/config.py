from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Store the settings of the application"""

    SCRIPT_DIR: Path = Path(__file__).parent.parent
    PROJECT_DIR: Path = SCRIPT_DIR.parent
    MODELS_DIR: Path = PROJECT_DIR / "app" / "models"
    TRAINED_PKL_FILE: str = "recommendation_model.pkl"


@lru_cache
def get_settings() -> Settings:
    """Used to get the settings of the application.

    Returns:
        Settings:
            The settings of the application.
    """

    return Settings()


settings = get_settings()
