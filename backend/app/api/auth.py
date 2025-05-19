import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Set

import spotipy
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from spotipy.cache_handler import CacheHandler
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# OAuth2 scheme for token authentication
oauth2_scheme = HTTPBearer()

# Secret key for JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Token blacklist to track invalidated tokens
token_blacklist: Set[str] = set()


class NoCacheHandler(CacheHandler):
    """Custom cache handler that doesn't persist tokens."""

    def get_cached_token(self):
        return None

    def save_token_to_cache(self, token_info):
        pass


class CallbackRequest(BaseModel):
    code: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT token."""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating JWT token: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error creating authentication token"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> str:
    """Validate JWT token and return Spotify access token."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        # Check if token is blacklisted
        if token in token_blacklist:
            raise credentials_exception

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        spotify_token: str = payload.get("sub")
        if spotify_token is None:
            raise credentials_exception

        # Try to use the token
        sp = spotipy.Spotify(auth=spotify_token)
        try:
            # Test the token with a simple API call
            sp.current_user()
            return spotify_token
        except SpotifyException as e:
            if e.http_status == 401:
                # Token is expired, try to refresh
                refresh_token = payload.get("refresh_token")
                if refresh_token:
                    try:
                        sp_oauth = SpotifyOAuth(
                            client_id=settings.SPOTIFY_CLIENT_ID,
                            client_secret=settings.SPOTIFY_CLIENT_SECRET,
                            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
                            scope=settings.SPOTIFY_SCOPES,
                        )
                        new_token_info = sp_oauth.refresh_access_token(refresh_token)
                        # Create new JWT with refreshed token
                        new_jwt = create_access_token(
                            data={
                                "sub": new_token_info["access_token"],
                                "refresh_token": new_token_info["refresh_token"],
                            }
                        )
                        raise HTTPException(
                            status_code=401,
                            detail="Token expired",
                            headers={"X-New-Token": new_jwt},
                        )
                    except Exception as e:
                        logger.error(f"Error refreshing token: {str(e)}")
                        raise credentials_exception
            logger.error(f"Spotify API error: {str(e)}")
            raise credentials_exception
    except JWTError:
        raise credentials_exception


@router.get("/login")
async def login():
    # Clear any existing sessions
    token_blacklist.clear()

    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=settings.SPOTIFY_SCOPES,
        cache_handler=NoCacheHandler(),
    )
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def callback(code: str):
    try:
        logger.info(f"Received callback with code: {code[:10]}...")
        
        sp_oauth = SpotifyOAuth(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
            scope=settings.SPOTIFY_SCOPES,
            cache_handler=NoCacheHandler(),
        )
        logger.info(f"Created SpotifyOAuth with redirect_uri: {settings.SPOTIFY_REDIRECT_URI}")

        # Exchange code for token
        logger.info("Exchanging code for token...")
        token_info = sp_oauth.get_access_token(code)
        logger.info("Successfully exchanged code for token")

        # Create a JWT token with the Spotify access token
        logger.info("Creating JWT token...")
        jwt_token = create_access_token(
            data={
                "sub": token_info["access_token"],
                "refresh_token": token_info["refresh_token"],
            }
        )
        logger.info("Successfully created JWT token")

        # Redirect to frontend with JWT token
        frontend_url = f"{settings.FRONTEND_URL}/?token={jwt_token}"
        logger.info(f"Redirecting to frontend: {frontend_url}")
        return RedirectResponse(url=frontend_url)
    except Exception as e:
        logger.error(f"Error in callback: {str(e)}")
        error_url = f"{settings.FRONTEND_URL}/?error={str(e)}"
        logger.info(f"Redirecting to frontend with error: {error_url}")
        return RedirectResponse(url=error_url)


@router.get("/me")
async def get_me(request: Request):
    try:
        # Get the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        token = auth_header.split(" ")[1]
        try:
            # Decode the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            spotify_token = payload.get("sub")
            if not spotify_token:
                raise HTTPException(status_code=401, detail="Invalid token format")

            # Create a Spotify client with the token
            sp = spotipy.Spotify(auth=spotify_token)

            # Get user profile
            user = sp.current_user()
            return user
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token format")
    except Exception as e:
        logger.error(f"Error in /me endpoint: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout(request: Request):
    try:
        # Get the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            # Add token to blacklist
            token_blacklist.add(token)
            logger.info("Token added to blacklist")
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")

    return {"message": "Logged out successfully"}
