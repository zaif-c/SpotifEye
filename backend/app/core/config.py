from functools import lru_cache
from typing import Optional, Any

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SpotifEye"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # Frontend Settings
    FRONTEND_URL: str = "http://localhost:5173"
    FRONTEND_CALLBACK_PATH: str = "/callback"

    # Spotify Settings
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str = "http://127.0.0.1:8000/callback"
    SPOTIFY_SCOPES: str = (
        "user-read-private user-read-email user-read-playback-state user-modify-playback-state "
        "user-read-currently-playing user-read-recently-played user-top-read "
        "playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private "
        "user-library-read user-library-modify user-follow-read user-follow-modify"
    )

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
