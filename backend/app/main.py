from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from app.api import auth, spotify
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="SpotifEye API")

@app.on_event("startup")
async def startup_event():
    # Log the API prefix
    logger.info(f"API V1 prefix: {settings.API_V1_STR}")
    
    # Log all registered routes
    for route in app.routes:
        logger.info(f"Registered route: {route.path} [{route.methods}]")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Use frontend URL from settings
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include routers with prefixes
app.include_router(auth.router, tags=["auth"])
app.include_router(spotify.router, prefix="/spotify", tags=["spotify"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to SpotifEye API",
        "status": "operational",
        "version": "1.0.0",
    }
