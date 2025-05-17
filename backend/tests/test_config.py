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
    assert settings.FRONTEND_URL == "http://127.0.0.1:5173"
    assert settings.FRONTEND_CALLBACK_PATH == "/callback"

    # Test that redirect URI is constructed correctly
    expected_redirect = f"{settings.FRONTEND_URL}{settings.FRONTEND_CALLBACK_PATH}"
    assert settings.SPOTIFY_REDIRECT_URI == expected_redirect


def test_settings_validation() -> None:
    """Test that required settings are validated."""
    with pytest.raises(ValueError):
        # Try to create settings without required values
        Settings(SPOTIFY_CLIENT_ID=None, SPOTIFY_CLIENT_SECRET=None, SECRET_KEY=None)
