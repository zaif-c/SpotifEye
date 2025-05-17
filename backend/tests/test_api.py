from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app

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
    response = client.options("/", headers={"Origin": "http://127.0.0.1:5173"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"


def test_callback_endpoint() -> None:
    """Test the callback endpoint with a mock authorization code."""
    # Test with invalid code
    with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
        mock_get_token.return_value = {"error": "invalid_grant", "error_description": "Invalid authorization code"}
        response = client.get("/auth/callback?code=invalid_code")
        assert response.status_code == 400
        assert "Invalid authorization code" in response.json()["detail"]
    # Test with missing code
    response = client.get("/auth/callback")
    assert response.status_code == 422  # FastAPI validation error
    # Note: We can't test successful callback without a real Spotify code
    # as it requires actual Spotify API interaction


def test_login_endpoint() -> None:
    """Test the login endpoint returns a valid Spotify authorization URL."""
    response = client.get("/auth/login")
    assert response.status_code == 200
    data = response.json()
    assert "auth_url" in data
    assert data["auth_url"].startswith("https://accounts.spotify.com/authorize")
    assert "client_id=" in data["auth_url"]
    assert "redirect_uri=" in data["auth_url"]
    assert "scope=" in data["auth_url"]


def test_protected_endpoint_without_token() -> None:
    """Test that protected endpoint requires authentication."""
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers


def test_protected_endpoint_with_invalid_token() -> None:
    """Test that protected endpoint rejects invalid tokens."""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


def test_callback_with_invalid_code() -> None:
    """Test callback endpoint with an invalid authorization code."""
    with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
        mock_get_token.return_value = {"error": "invalid_grant", "error_description": "Invalid authorization code"}
        response = client.get("/auth/callback?code=invalid_code")
        assert response.status_code == 400
        assert "Invalid authorization code" in response.json()["detail"]


def test_callback_with_missing_code() -> None:
    """Test callback endpoint without providing a code."""
    response = client.get("/auth/callback")
    assert response.status_code == 422  # FastAPI validation error


def test_callback_with_expired_code() -> None:
    """Test callback endpoint with an expired authorization code."""
    with patch("spotipy.oauth2.SpotifyOAuth.get_access_token") as mock_get_token:
        mock_get_token.return_value = {"error": "invalid_grant", "error_description": "Authorization code expired"}
        response = client.get("/auth/callback?code=expired_code")
        assert response.status_code == 400
        assert "Authorization code expired" in response.json()["detail"]


def test_protected_endpoint_with_expired_token() -> None:
    """Test protected endpoint with an expired JWT token."""
    # Create an expired token
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9.4Adcj3UFYzPUVaVF43Fm5SW87J68re8R9Qe8cGmJ0U8"
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert "Invalid authentication credentials" in response.json()["detail"]


def test_protected_endpoint_with_malformed_token() -> None:
    """Test protected endpoint with a malformed JWT token."""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer not.a.valid.jwt"}
    )
    assert response.status_code == 401
    assert "Invalid authentication credentials" in response.json()["detail"]


def test_logout_endpoint_without_token() -> None:
    """Test that logout endpoint requires authentication."""
    response = client.post("/auth/logout")
    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers


def test_logout_endpoint_with_invalid_token() -> None:
    """Test that logout endpoint rejects invalid tokens."""
    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert "Invalid authentication credentials" in response.json()["detail"]


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
                "expires_in": 3600
            }
            
            # First get a valid token
            response = client.get("/auth/callback?code=valid_code")
            assert response.status_code == 200
            token = response.json()["access_token"]
            
            # Now test logout
            response = client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert response.json()["message"] == "Successfully logged out"
            mock_session.close.assert_called_once()


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
                "expires_in": 3600
            }
            
            # First get a valid token
            response = client.get("/auth/callback?code=valid_code")
            assert response.status_code == 200
            token = response.json()["access_token"]
            
            # Now test logout with error
            response = client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 401
            assert "Invalid authentication credentials" in response.json()["detail"]


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
                "expires_in": 3600
            }
            
            # First get a valid token
            response = client.get("/auth/callback?code=valid_code")
            assert response.status_code == 200
            token = response.json()["access_token"]
            
            # Logout to blacklist the token
            response = client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 401
            assert "Invalid authentication credentials" in response.json()["detail"]
            
            # Try to use the blacklisted token
            response = client.get(
                "/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 401
            assert "Invalid authentication credentials" in response.json()["detail"]


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
                "expires_in": 3600
            }
            
            # First get a valid token
            response = client.get("/auth/callback?code=valid_code")
            assert response.status_code == 200
            token = response.json()["access_token"]
            
            # First logout
            response = client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 401
            assert "Invalid authentication credentials" in response.json()["detail"]
            
            # Try to logout again with the same token
            response = client.post(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 401
            assert "Invalid authentication credentials" in response.json()["detail"]
