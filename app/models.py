from pydantic import BaseModel


class WorkspaceState(BaseModel):
    status: str
    module: str


class HealthResponse(BaseModel):
    status: str
    ready: bool
