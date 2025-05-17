from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient
from fastapi import Depends

from app.main import app
from app.services.spotify import SpotifyService
from app.api.auth import get_current_user

client = TestClient(app)

# Mock Spotify API responses
MOCK_TOP_TRACKS = {
    "items": [
        {
            "id": "track1",
            "name": "Test Track 1",
            "artists": [{"id": "artist1", "name": "Test Artist 1"}],
            "album": {"id": "album1", "name": "Test Album 1"}
        },
        {
            "id": "track2",
            "name": "Test Track 2",
            "artists": [{"id": "artist2", "name": "Test Artist 2"}],
            "album": {"id": "album2", "name": "Test Album 2"}
        }
    ]
}

MOCK_TOP_ARTISTS = {
    "items": [
        {
            "id": "artist1",
            "name": "Test Artist 1",
            "genres": ["pop", "rock"],
            "images": [{"url": "http://example.com/image1.jpg"}]
        },
        {
            "id": "artist2",
            "name": "Test Artist 2",
            "genres": ["jazz", "blues"],
            "images": [{"url": "http://example.com/image2.jpg"}]
        }
    ]
}

MOCK_RECENTLY_PLAYED = {
    "items": [
        {
            "track": {
                "id": "track1",
                "name": "Test Track 1",
                "artists": [{"id": "artist1", "name": "Test Artist 1"}],
                "album": {"id": "album1", "name": "Test Album 1"}
            },
            "played_at": "2024-01-01T00:00:00Z"
        },
        {
            "track": {
                "id": "track2",
                "name": "Test Track 2",
                "artists": [{"id": "artist2", "name": "Test Artist 2"}],
                "album": {"id": "album2", "name": "Test Album 2"}
            },
            "played_at": "2024-01-01T01:00:00Z"
        }
    ]
}

@pytest.mark.asyncio
async def test_spotify_service_top_tracks():
    """Test SpotifyService get_top_tracks method."""
    with patch("spotipy.Spotify") as mock_spotify:
        mock_spotify.return_value.current_user_top_tracks.return_value = MOCK_TOP_TRACKS
        
        service = SpotifyService("test_token")
        tracks = await service.get_top_tracks(limit=2)
        
        assert len(tracks) == 2
        assert tracks[0]["name"] == "Test Track 1"
        assert tracks[1]["name"] == "Test Track 2"
        mock_spotify.return_value.current_user_top_tracks.assert_called_once_with(
            limit=2, time_range="medium_term"
        )

@pytest.mark.asyncio
async def test_spotify_service_top_artists():
    """Test SpotifyService get_top_artists method."""
    with patch("spotipy.Spotify") as mock_spotify:
        mock_spotify.return_value.current_user_top_artists.return_value = MOCK_TOP_ARTISTS
        
        service = SpotifyService("test_token")
        artists = await service.get_top_artists(limit=2)
        
        assert len(artists) == 2
        assert artists[0]["name"] == "Test Artist 1"
        assert artists[1]["name"] == "Test Artist 2"
        mock_spotify.return_value.current_user_top_artists.assert_called_once_with(
            limit=2, time_range="medium_term"
        )

@pytest.mark.asyncio
async def test_spotify_service_recently_played():
    """Test SpotifyService get_recently_played method."""
    with patch("spotipy.Spotify") as mock_spotify:
        mock_spotify.return_value.current_user_recently_played.return_value = MOCK_RECENTLY_PLAYED
        
        service = SpotifyService("test_token")
        tracks = await service.get_recently_played(limit=2)
        
        assert len(tracks) == 2
        assert tracks[0]["track"]["name"] == "Test Track 1"
        assert tracks[1]["track"]["name"] == "Test Track 2"
        mock_spotify.return_value.current_user_recently_played.assert_called_once_with(limit=2)

def test_top_tracks_endpoint():
    """Test /spotify/top-tracks endpoint."""
    with patch("spotipy.Spotify") as mock_spotify:
        mock_spotify.return_value.current_user_top_tracks.return_value = MOCK_TOP_TRACKS
        
        # Override the get_current_user dependency
        app.dependency_overrides[get_current_user] = lambda: "test_token"
        
        try:
            response = client.get("/spotify/top-tracks?limit=2")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "Test Track 1"
            assert data[1]["name"] == "Test Track 2"
        finally:
            # Clean up the dependency override
            app.dependency_overrides = {}

def test_top_artists_endpoint():
    """Test /spotify/top-artists endpoint."""
    with patch("spotipy.Spotify") as mock_spotify:
        mock_spotify.return_value.current_user_top_artists.return_value = MOCK_TOP_ARTISTS
        
        # Override the get_current_user dependency
        app.dependency_overrides[get_current_user] = lambda: "test_token"
        
        try:
            response = client.get("/spotify/top-artists?limit=2")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "Test Artist 1"
            assert data[1]["name"] == "Test Artist 2"
        finally:
            # Clean up the dependency override
            app.dependency_overrides = {}

def test_recently_played_endpoint():
    """Test /spotify/recently-played endpoint."""
    with patch("spotipy.Spotify") as mock_spotify:
        mock_spotify.return_value.current_user_recently_played.return_value = MOCK_RECENTLY_PLAYED
        
        # Override the get_current_user dependency
        app.dependency_overrides[get_current_user] = lambda: "test_token"
        
        try:
            response = client.get("/spotify/recently-played?limit=2")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["track"]["name"] == "Test Track 1"
            assert data[1]["track"]["name"] == "Test Track 2"
        finally:
            # Clean up the dependency override
            app.dependency_overrides = {}

def test_endpoints_without_auth():
    """Test that endpoints require authentication."""
    response = client.get("/spotify/top-tracks")
    assert response.status_code == 401
    
    response = client.get("/spotify/top-artists")
    assert response.status_code == 401
    
    response = client.get("/spotify/recently-played")
    assert response.status_code == 401

def test_endpoints_with_invalid_params():
    """Test endpoints with invalid query parameters."""
    # Override the get_current_user dependency
    app.dependency_overrides[get_current_user] = lambda: "test_token"
    
    try:
        # Test invalid limit
        response = client.get("/spotify/top-tracks?limit=51")
        assert response.status_code == 422
        
        # Test invalid time_range
        response = client.get("/spotify/top-tracks?time_range=invalid")
        assert response.status_code == 422
    finally:
        # Clean up the dependency override
        app.dependency_overrides = {}

def test_me_endpoint():
    """Test /me endpoint."""
    # Mock the get_current_user dependency to return a valid token
    app.dependency_overrides[get_current_user] = lambda: "valid_spotify_token"
    fake_user = {"id": "test_user", "display_name": "Test User"}
    with patch("spotipy.Spotify") as mock_spotify:
        mock_spotify.return_value.current_user.return_value = fake_user
        try:
            response = client.get("/me")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "test_user"
        finally:
            app.dependency_overrides = {} 