from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

from .notifications import InMemoryNotificationProvider, NotificationService


class NotificationRequest(BaseModel):
    recipient: str = Field(..., min_length=1)
    template: str = Field(..., min_length=1)


app = FastAPI(title="Pilot Procurement")
notification_service = NotificationService(InMemoryNotificationProvider())


def require_authorization(authorization: str | None = Header(default=None)) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required",
        )
    return authorization


@app.post("/integrations/notifications/send")
def send_notification(
    payload: NotificationRequest,
    _: str = Depends(require_authorization),
) -> dict[str, str | bool]:
    return notification_service.send_or_defer(payload.recipient, payload.template)
