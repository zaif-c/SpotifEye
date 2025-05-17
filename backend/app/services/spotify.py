from typing import List, Dict, Any
import logging
from fastapi import HTTPException
import spotipy
from spotipy.exceptions import SpotifyException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpotifyService:
    """Service class for interacting with Spotify Web API."""
    
    def __init__(self, access_token: str):
        """Initialize Spotify client with user's access token."""
        self.client = spotipy.Spotify(auth=access_token)
        self.logger = logging.getLogger(__name__)

    async def get_top_tracks(self, limit: int = 20, time_range: str = "medium_term") -> List[Dict[str, Any]]:
        """
        Get user's top tracks.
        
        Args:
            limit: Number of tracks to return (max 50)
            time_range: Over what time frame to calculate top tracks
                - short_term: ~4 weeks
                - medium_term: ~6 months
                - long_term: calculated from several years of data
        
        Returns:
            List of track objects
        """
        try:
            results = self.client.current_user_top_tracks(limit=limit, time_range=time_range)
            self.logger.info(f"Successfully fetched top {limit} tracks")
            return results["items"]
        except SpotifyException as e:
            self.logger.error(f"Error fetching top tracks: {str(e)}")
            raise HTTPException(status_code=e.http_status, detail=str(e))

    async def get_top_artists(self, limit: int = 20, time_range: str = "medium_term") -> List[Dict[str, Any]]:
        """
        Get user's top artists.
        
        Args:
            limit: Number of artists to return (max 50)
            time_range: Over what time frame to calculate top artists
                - short_term: ~4 weeks
                - medium_term: ~6 months
                - long_term: calculated from several years of data
        
        Returns:
            List of artist objects
        """
        try:
            results = self.client.current_user_top_artists(limit=limit, time_range=time_range)
            self.logger.info(f"Successfully fetched top {limit} artists")
            return results["items"]
        except SpotifyException as e:
            self.logger.error(f"Error fetching top artists: {str(e)}")
            raise HTTPException(status_code=e.http_status, detail=str(e))

    async def get_recently_played(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's recently played tracks.
        
        Args:
            limit: Number of tracks to return (max 50)
        
        Returns:
            List of recently played track objects
        """
        try:
            results = self.client.current_user_recently_played(limit=limit)
            self.logger.info(f"Successfully fetched {limit} recently played tracks")
            return results["items"]
        except SpotifyException as e:
            self.logger.error(f"Error fetching recently played tracks: {str(e)}")
            raise HTTPException(status_code=e.http_status, detail=str(e)) 