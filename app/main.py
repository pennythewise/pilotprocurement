from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from app.models import HealthResponse, WorkspaceState

app = FastAPI(title="Pilot Procurement Finance API")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint that returns service status."""
    return HealthResponse(status="healthy", ready=True)


@app.get("/finance/workspace", response_model=WorkspaceState)
async def get_finance_workspace():
    """Get the finance workspace state.
    
    Requires authentication.
    """
    return WorkspaceState(status="ready", module="finance")


@app.get("/", tags=["landing"])
async def landing_page():
    """Landing page that lists available workspaces."""
    return {
        "message": "Pilot Procurement API",
        "workspaces": [
            {"name": "finance", "path": "/finance/workspace"}
        ]
    }


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
