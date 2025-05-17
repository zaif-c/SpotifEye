from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any

from app.api.auth import get_current_user
from app.services.spotify import SpotifyService

router = APIRouter()

@router.get("/top-tracks")
async def get_top_tracks(
    current_user: str = Depends(get_current_user),
    limit: int = Query(default=20, ge=1, le=50),
    time_range: str = Query(default="medium_term", regex="^(short_term|medium_term|long_term)$")
) -> List[Dict[str, Any]]:
    """
    Get user's top tracks.
    
    Args:
        limit: Number of tracks to return (1-50)
        time_range: Over what time frame to calculate top tracks
            - short_term: ~4 weeks
            - medium_term: ~6 months
            - long_term: calculated from several years of data
    
    Returns:
        List of track objects
    """
    spotify_service = SpotifyService(current_user)
    return await spotify_service.get_top_tracks(limit=limit, time_range=time_range)

@router.get("/top-artists")
async def get_top_artists(
    current_user: str = Depends(get_current_user),
    limit: int = Query(default=20, ge=1, le=50),
    time_range: str = Query(default="medium_term", regex="^(short_term|medium_term|long_term)$")
) -> List[Dict[str, Any]]:
    """
    Get user's top artists.
    
    Args:
        limit: Number of artists to return (1-50)
        time_range: Over what time frame to calculate top artists
            - short_term: ~4 weeks
            - medium_term: ~6 months
            - long_term: calculated from several years of data
    
    Returns:
        List of artist objects
    """
    spotify_service = SpotifyService(current_user)
    return await spotify_service.get_top_artists(limit=limit, time_range=time_range)

@router.get("/recently-played")
async def get_recently_played(
    current_user: str = Depends(get_current_user),
    limit: int = Query(default=50, ge=1, le=50)
) -> List[Dict[str, Any]]:
    """
    Get user's recently played tracks.
    
    Args:
        limit: Number of tracks to return (1-50)
    
    Returns:
        List of recently played track objects
    """
    spotify_service = SpotifyService(current_user)
    return await spotify_service.get_recently_played(limit=limit) 