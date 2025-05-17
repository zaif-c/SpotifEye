from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Set
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import logging

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key for JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Token blacklist to track invalidated tokens
token_blacklist: Set[str] = set()

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
        logger.info("Successfully created new JWT token")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating JWT token: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating authentication token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Validate JWT token and return Spotify access token."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Check if token is blacklisted
        if token in token_blacklist:
            logger.warning("Attempted to use blacklisted token")
            raise credentials_exception

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"JWT payload: {payload}")  # Debug log to inspect payload
        spotify_token: str = payload.get("sub")
        if spotify_token is None:
            logger.warning("JWT token missing Spotify access token")
            raise credentials_exception
            
        # Try to use the token
        sp = spotipy.Spotify(auth=spotify_token)
        try:
            # Test the token with a simple API call
            sp.current_user()
            logger.info("Successfully validated Spotify token")
            return spotify_token
        except SpotifyException as e:
            if e.http_status == 401:
                # Token is expired, try to refresh
                logger.info("Spotify token expired, attempting refresh")
                refresh_token = payload.get("refresh_token")
                logger.debug(f"Refresh token from payload: {refresh_token}")  # Debug log to inspect refresh token
                if refresh_token:
                    try:
                        sp_oauth = SpotifyOAuth(
                            client_id=settings.SPOTIFY_CLIENT_ID,
                            client_secret=settings.SPOTIFY_CLIENT_SECRET,
                            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
                            scope=settings.SPOTIFY_SCOPES
                        )
                        new_token_info = sp_oauth.refresh_access_token(refresh_token)
                        # Create new JWT with refreshed token
                        new_jwt = create_access_token(
                            data={
                                "sub": new_token_info["access_token"],
                                "refresh_token": new_token_info["refresh_token"]
                            }
                        )
                        logger.info("Successfully refreshed Spotify token")
                        raise HTTPException(
                            status_code=401,
                            detail="Token expired",
                            headers={"X-New-Token": new_jwt}
                        )
                    except Exception as e:
                        logger.error(f"Error refreshing token: {str(e)}")
                        raise credentials_exception
            logger.error(f"Spotify API error: {str(e)}")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise credentials_exception

@router.get("/login")
async def login():
    """Redirect user to Spotify's OAuth login page."""
    try:
        sp_oauth = SpotifyOAuth(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
            scope=settings.SPOTIFY_SCOPES
        )
        auth_url = sp_oauth.get_authorize_url()
        logger.info("Generated Spotify authorization URL")
        return {"auth_url": auth_url}
    except Exception as e:
        logger.error(f"Error generating auth URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating authorization URL")

@router.get("/callback")
async def callback(code: str) -> Dict[str, Any]:
    """Handle Spotify OAuth callback and exchange code for tokens."""
    try:
        # Initialize SpotifyOAuth
        sp_oauth = SpotifyOAuth(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
            scope=settings.SPOTIFY_SCOPES
        )
        
        # Exchange code for tokens
        token_info = sp_oauth.get_access_token(code)
        logger.info("Received token info from Spotify")
        
        if not token_info or (isinstance(token_info, dict) and token_info.get("error")):
            error_msg = token_info.get("error_description") if isinstance(token_info, dict) else "Failed to get access token"
            logger.error(f"Error getting access token: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg or "Failed to get access token")
            
        # Create JWT token
        access_token = create_access_token(
            data={
                "sub": token_info["access_token"],
                "refresh_token": token_info["refresh_token"]
            },
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Debug log to verify JWT payload
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"JWT payload after creation: {payload}")
        
        logger.info("Successfully created access token")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "spotify_access_token": token_info["access_token"],
            "spotify_refresh_token": token_info["refresh_token"],
            "expires_in": token_info["expires_in"]
        }
        
    except SpotifyException as e:
        logger.error(f"Spotify API error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in callback: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me")
async def get_current_user_info(current_user: str = Depends(get_current_user)) -> Dict[str, Any]:
    """Get information about the current user."""
    try:
        # Initialize Spotify client with the access token
        sp = spotipy.Spotify(auth=current_user)
        # Get user profile
        user_info = sp.current_user()
        logger.info(f"Successfully retrieved user info for user: {user_info.get('id')}")
        return user_info
    except Exception as e:
        logger.error(f"Error getting user info: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    """Logout the current user by invalidating their tokens."""
    try:
        # Validate token first
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            spotify_token = payload.get("sub")
            if spotify_token is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if token is already blacklisted
        if token in token_blacklist:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Add token to blacklist
        token_blacklist.add(token)
        logger.info("Successfully added token to blacklist")
        
        # Initialize Spotify client to close the session
        sp = spotipy.Spotify(auth=spotify_token)
        sp._session.close()
        logger.info("Successfully logged out user")
        return {"message": "Successfully logged out"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during logout") 