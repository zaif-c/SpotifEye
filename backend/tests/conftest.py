import pytest
import os
from app.core.config import Settings

@pytest.fixture(scope="session")
def test_settings():
    """Create test settings with mock values."""
    return Settings(
        SPOTIFY_CLIENT_ID="test_client_id",
        SPOTIFY_CLIENT_SECRET="test_client_secret",
        SECRET_KEY="test_secret_key",
        FRONTEND_URL="http://localhost:5173",
        FRONTEND_CALLBACK_PATH="/callback"
    ) 