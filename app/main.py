import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from app.api.endpoints import router as api_router
from app.core.simulation import run_simulation

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the background simulation task
    task = asyncio.create_task(run_simulation())
    yield
    # Shutdown: Cancel the task
    task.cancel()

app = FastAPI(
    title="FlowSync AI",
    description="AI-powered crowd management system for large sporting venues.",
    version="1.0.0",
    lifespan=lifespan
)

# Include the REST API routes
app.include_router(api_router, prefix="/api")

# Mount static files for the dashboard
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_dashboard():
    """
    Serves the simple HTML dashboard.
    """
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "FlowSync AI API is running. Dashboard not found."}
