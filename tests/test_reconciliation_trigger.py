from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_reconciliation_trigger_returns_job_id_for_valid_transaction_ids():
    response = client.post(
        "/reconciliation-trigger",
        json={"transaction_ids": ["txn-001", "txn-002", "txn-003"]},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "job_id" in payload
    assert isinstance(payload["job_id"], str)
    assert payload["job_id"]


def test_reconciliation_trigger_rejects_empty_transaction_list():
    response = client.post(
        "/reconciliation-trigger",
        json={"transaction_ids": []},
    )

    assert response.status_code == 422
