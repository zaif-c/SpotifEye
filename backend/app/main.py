from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, spotify
from app.core.config import settings

app = FastAPI(title="SpotifEye API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes
app.include_router(auth.router, tags=["auth"])
app.include_router(spotify.router, prefix="/spotify", tags=["spotify"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to SpotifEye API",
        "status": "operational",
        "version": "1.0.0"
    } 