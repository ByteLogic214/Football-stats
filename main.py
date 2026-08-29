from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import get_settings
from app.api import api_router
from app.services.thestatsapi import stats_client
import os

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Football Statistics Analyzer powered by TheStatsAPI - Real-time stats & betting odds comparison",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix="/api")

@app.get("/api/health")
async def health():
    """Backend health check + TheStatsAPI connectivity"""
    try:
        api_health = await stats_client.health_check()
        return {
            "status": "healthy",
            "api_connected": True,
            "api_status": api_health,
            "version": settings.APP_VERSION
        }
    except Exception as e:
        return {
            "status": "healthy",
            "api_connected": False,
            "error": str(e),
            "version": settings.APP_VERSION
        }

# Serve frontend static files if built
frontend_build = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
if os.path.exists(frontend_build):
    app.mount("/", StaticFiles(directory=frontend_build, html=True), name="static")

    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        if full_path.startswith("api/"):
            return {"detail": "Not found"}
        return FileResponse(os.path.join(frontend_build, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
