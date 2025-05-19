from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.auth import router as auth_router
from app.api.spotify import router as spotify_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI backend for the SpotifEye application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(spotify_router, prefix="/api/v1/spotify")


@app.get("/")
async def root() -> dict:
    """Root endpoint to verify API is running."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "status": "operational",
        "version": "1.0.0",
    }


@app.get("/callback")
async def root_callback(request: Request) -> RedirectResponse:
    """Handle callback requests directly."""
    return RedirectResponse(url=f"/auth/callback{request.url.query}")


@app.options("/{full_path:path}")
async def options_route(full_path: str) -> dict:
    """Handle OPTIONS requests for CORS preflight."""
    return {}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True
    )
