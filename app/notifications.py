from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class NotificationProviderError(Exception):
    """Raised when the external notification provider cannot accept a message."""


class NotificationProvider(Protocol):
    def send(self, recipient: str, template: str) -> str:
        """Send a notification and return the provider message ID."""


@dataclass
class InMemoryNotificationProvider:
    """Mock provider used until a real email/SMS integration is configured."""

    def send(self, recipient: str, template: str) -> str:
        return f"mock-{abs(hash((recipient, template)))}"


class NotificationService:
    def __init__(self, provider: NotificationProvider):
        self.provider = provider
        self.deferred: list[tuple[str, str]] = []

    def send_or_defer(self, recipient: str, template: str) -> dict[str, str | bool]:
        try:
            message_id = self.provider.send(recipient, template)
        except NotificationProviderError:
            self.deferred.append((recipient, template))
            return {"queued": False, "deferred": True}
        return {"queued": True, "deferred": False, "message_id": message_id}
