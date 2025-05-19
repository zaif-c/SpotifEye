import pytest

from app.core.config import Settings, get_settings


def test_settings_loading() -> None:
    """Test that settings are loaded correctly with defaults."""
    settings = get_settings()

    # Test API settings
    assert settings.API_V1_STR == "/api/v1"
    assert settings.PROJECT_NAME == "SpotifEye"
    assert settings.BACKEND_HOST == "0.0.0.0"
    assert settings.BACKEND_PORT == 8000

    # Test Frontend settings
    assert settings.FRONTEND_URL == "http://localhost:5173"
    assert settings.FRONTEND_CALLBACK_PATH == "/callback"

    # Test Spotify settings
    assert settings.SPOTIFY_REDIRECT_URI == "http://127.0.0.1:8000/callback"
    assert "user-read-private" in settings.SPOTIFY_SCOPES
    assert "user-read-email" in settings.SPOTIFY_SCOPES

    # Test Security settings
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30


def test_settings_validation() -> None:
    """Test that required settings are validated."""
    with pytest.raises(ValueError):
        # Try to create settings without required values
        Settings(SPOTIFY_CLIENT_ID=None, SPOTIFY_CLIENT_SECRET=None, SECRET_KEY=None)
