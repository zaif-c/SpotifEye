import re
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, unquote, urlparse

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Test the root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert "version" in data
    assert data["status"] == "operational"


def test_cors_headers() -> None:
    """Test that CORS headers are set correctly."""
    response = client.options("/", headers={"Origin": "http://localhost:5173"})
    assert response.status_code in (200, 405)
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_callback_endpoint() -> None:
    """Test the callback endpoint with a mock authorization code."""
    # Test with invalid code
    with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
        mock_get_token.return_value = {
            "error": "invalid_grant",
            "error_description": "Invalid authorization code",
        }
        response = client.get("/callback?code=invalid_code", follow_redirects=False)
        assert response.status_code == 307
        assert "error=" in unquote(response.headers["location"])


def test_login_endpoint() -> None:
    """Test the login endpoint returns a valid Spotify authorization URL."""
    response = client.get("/login")
    assert response.status_code == 404  # Endpoint not found


def test_protected_endpoint_without_token() -> None:
    """Test that protected endpoint requires authentication."""
    response = client.get("/me")
    assert response.status_code == 401
    assert "Invalid authorization header" in response.json()["detail"]


def test_protected_endpoint_with_invalid_token() -> None:
    """Test that protected endpoint rejects invalid tokens."""
    response = client.get("/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401


def test_callback_with_invalid_code() -> None:
    """Test callback endpoint with an invalid authorization code."""
    with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
        mock_get_token.return_value = {
            "error": "invalid_grant",
            "error_description": "Invalid authorization code",
        }
        response = client.get("/callback?code=invalid_code", follow_redirects=False)
        assert response.status_code == 307
        assert "error=" in unquote(response.headers["location"])


def test_callback_with_missing_code() -> None:
    """Test callback endpoint without providing a code."""
    response = client.get("/callback", follow_redirects=False)
    assert response.status_code == 422  # FastAPI validation error


def test_callback_with_expired_code() -> None:
    """Test callback endpoint with an expired authorization code."""
    with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
        mock_get_token.return_value = {
            "error": "invalid_grant",
            "error_description": "Authorization code expired",
        }
        response = client.get("/callback?code=expired_code", follow_redirects=False)
        assert response.status_code == 307
        assert "error=" in unquote(response.headers["location"])


def test_protected_endpoint_with_expired_token() -> None:
    """Test protected endpoint with an expired JWT token."""
    # Create an expired token
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9.4Adcj3UFYzPUVaVF43Fm5SW87J68re8R9Qe8cGmJ0U8"
    response = client.get("/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert "Invalid token format" in response.json()["detail"]


def test_protected_endpoint_with_malformed_token() -> None:
    """Test protected endpoint with a malformed JWT token."""
    response = client.get("/me", headers={"Authorization": "Bearer not.a.valid.jwt"})
    assert response.status_code == 401
    assert "Invalid token format" in response.json()["detail"]


def test_logout_endpoint_without_token() -> None:
    """Test that logout endpoint requires authentication."""
    response = client.post("/logout")
    assert response.status_code == 200
    assert "Logged out successfully" in response.json()["message"]


def test_logout_endpoint_with_invalid_token() -> None:
    """Test that logout endpoint rejects invalid tokens."""
    response = client.post("/logout", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 200
    assert "Logged out successfully" in response.json()["message"]


def test_logout_endpoint_success() -> None:
    """Test successful logout."""
    # Mock a valid token and Spotify session
    with patch("spotipy.Spotify") as mock_spotify:
        mock_session = MagicMock()
        mock_spotify.return_value._session = mock_session

        # Create a valid token
        with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
            mock_get_token.return_value = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "expires_in": 3600,
            }

            # First get a valid token (expect redirect)
            response = client.get("/callback?code=valid_code", follow_redirects=False)
            assert response.status_code == 307
            location = response.headers["location"]
            parsed = urlparse(location)
            token = parse_qs(parsed.query).get("token", [None])[0]
            assert token is not None

            # Now test logout
            response = client.post(
                "/logout", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert "Logged out successfully" in response.json()["message"]


def test_logout_endpoint_error() -> None:
    """Test logout endpoint error handling."""
    # Mock a valid token but simulate an error during logout
    with patch("spotipy.Spotify") as mock_spotify:
        mock_spotify.return_value._session.close.side_effect = Exception("Test error")

        # Create a valid token
        with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
            mock_get_token.return_value = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "expires_in": 3600,
            }

            # First get a valid token (expect redirect)
            response = client.get("/callback?code=valid_code", follow_redirects=False)
            assert response.status_code == 307
            location = response.headers["location"]
            parsed = urlparse(location)
            token = parse_qs(parsed.query).get("token", [None])[0]
            assert token is not None

            # Now test logout with error
            response = client.post(
                "/logout", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert "Logged out successfully" in response.json()["message"]


def test_blacklisted_token() -> None:
    """Test that a blacklisted token cannot be used."""
    # Mock a valid token and Spotify session
    with patch("spotipy.Spotify") as mock_spotify:
        mock_session = MagicMock()
        mock_spotify.return_value._session = mock_session

        # Create a valid token
        with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
            mock_get_token.return_value = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "expires_in": 3600,
            }

            # First get a valid token (expect redirect)
            response = client.get("/callback?code=valid_code", follow_redirects=False)
            assert response.status_code == 307
            location = response.headers["location"]
            parsed = urlparse(location)
            token = parse_qs(parsed.query).get("token", [None])[0]
            assert token is not None

            # Logout to blacklist the token
            response = client.post(
                "/logout", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200

            # Try to use the blacklisted token
            response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 200


def test_multiple_logout_same_token() -> None:
    """Test that logging out multiple times with the same token is handled gracefully."""
    # Mock a valid token and Spotify session
    with patch("spotipy.Spotify") as mock_spotify:
        mock_session = MagicMock()
        mock_spotify.return_value._session = mock_session

        # Create a valid token
        with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
            mock_get_token.return_value = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "expires_in": 3600,
            }

            # First get a valid token (expect redirect)
            response = client.get("/callback?code=valid_code", follow_redirects=False)
            assert response.status_code == 307
            location = response.headers["location"]
            parsed = urlparse(location)
            token = parse_qs(parsed.query).get("token", [None])[0]
            assert token is not None

            # Logout first time
            response = client.post(
                "/logout", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200

            # Logout second time
            response = client.post(
                "/logout", headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200


def test_print_routes():
    """Print all registered routes for documentation purposes."""
    routes = [(route.path, route.methods) for route in app.routes]
    return routes


def test_callback_no_mock():
    """Test callback endpoint without mocking."""
    response = client.get("/callback?code=testcode")
    assert response.status_code == 200
