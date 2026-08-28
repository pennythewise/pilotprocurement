from fastapi.testclient import TestClient

from app.main import app, notification_service
from app.notifications import NotificationProviderError

client = TestClient(app)


def test_send_notification_queues_message():
    response = client.post(
        "/integrations/notifications/send",
        headers={"Authorization": "Bearer test-token"},
        json={"recipient": "approver@example.com", "template": "approval-pending"},
    )

    assert response.status_code == 200
    assert response.json()["queued"] is True
    assert response.json()["deferred"] is False
    assert response.json()["message_id"].startswith("mock-")


def test_send_notification_requires_authorization():
    response = client.post(
        "/integrations/notifications/send",
        json={"recipient": "approver@example.com", "template": "approval-pending"},
    )

    assert response.status_code == 401


def test_send_notification_defers_provider_failure(monkeypatch):
    def fail_send(recipient: str, template: str) -> str:
        raise NotificationProviderError("provider rate limit")

    monkeypatch.setattr(notification_service.provider, "send", fail_send)
    response = client.post(
        "/integrations/notifications/send",
        headers={"Authorization": "Bearer test-token"},
        json={"recipient": "approver@example.com", "template": "approval-pending"},
    )

    assert response.status_code == 200
    assert response.json() == {"queued": False, "deferred": True}
    assert ("approver@example.com", "approval-pending") in notification_service.deferred


def test_send_notification_validates_required_fields():
    response = client.post(
        "/integrations/notifications/send",
        headers={"Authorization": "Bearer test-token"},
        json={"recipient": "", "template": "approval-pending"},
    )

    assert response.status_code == 422
