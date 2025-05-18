import os

import pytest

from app.core.config import Settings, settings


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Create test settings with mock values."""
    return Settings(
        SPOTIFY_CLIENT_ID="test_client_id",
        SPOTIFY_CLIENT_SECRET="test_client_secret",
        SECRET_KEY="test_secret_key",
        FRONTEND_URL="http://localhost:5173",
        FRONTEND_CALLBACK_PATH="/callback",
    )

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    # Set test environment variables
    os.environ["SPOTIFY_CLIENT_ID"] = "test_client_id"
    os.environ["SPOTIFY_CLIENT_SECRET"] = "test_client_secret"
    os.environ["SPOTIFY_REDIRECT_URI"] = "http://127.0.0.1:8000/callback"
    os.environ["SECRET_KEY"] = "test_secret_key"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
    
    # Reset settings to use test environment
    settings.SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
    settings.SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
    settings.SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
    settings.SECRET_KEY = os.environ["SECRET_KEY"]
    settings.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    
    yield
    
    # Clean up after tests
    for key in ["SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "SPOTIFY_REDIRECT_URI", 
                "SECRET_KEY", "ACCESS_TOKEN_EXPIRE_MINUTES"]:
        if key in os.environ:
            del os.environ[key]
