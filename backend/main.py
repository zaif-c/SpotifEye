from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI backend for the SpotifEye application",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Uses configured frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "status": "operational",
        "version": "1.0.0"
    }

@app.options("/{full_path:path}")
async def options_route(full_path: str):
    """Handle OPTIONS requests for CORS preflight."""
    return {}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.BACKEND_HOST, 
        port=settings.BACKEND_PORT, 
        reload=True
    ) 