from functools import lru_cache
from typing import Any, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SpotifEye"
    BACKEND_HOST: str
    BACKEND_PORT: int

    # Frontend Settings
    FRONTEND_URL: str
    FRONTEND_CALLBACK_PATH: str = "/callback"

    # Spotify Settings
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str
    SPOTIFY_SCOPES: str

    # Security Settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_spotify_redirect_uri(self) -> str:
        """Return the Spotify redirect URI."""
        return self.SPOTIFY_REDIRECT_URI


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
