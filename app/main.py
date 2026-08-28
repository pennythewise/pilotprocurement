from __future__ import annotations

import uuid

from fastapi import FastAPI
from pydantic import BaseModel, Field


class ReconciliationTriggerRequest(BaseModel):
    transaction_ids: list[str] = Field(..., min_length=1)


app = FastAPI(title="Reconciliation Service")


@app.post("/reconciliation-trigger")
def reconciliation_trigger(payload: ReconciliationTriggerRequest) -> dict[str, str]:
    return {"job_id": str(uuid.uuid4())}
