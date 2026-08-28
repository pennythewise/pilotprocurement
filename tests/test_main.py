import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_endpoint_returns_200(self, client):
        """Test that the health endpoint returns a 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_ready_response(self, client):
        """Test that the health endpoint returns a successful ready response."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert data["ready"] is True

    def test_health_endpoint_response_schema(self, client):
        """Test that the health endpoint response matches the expected schema."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "ready" in data


class TestFinanceWorkspace:
    def test_finance_workspace_endpoint_returns_200(self, client):
        """Test that the finance workspace endpoint returns a 200 status code."""
        response = client.get("/finance/workspace")
        assert response.status_code == 200

    def test_finance_workspace_endpoint_returns_correct_state(self, client):
        """Test that the finance workspace endpoint returns the correct workspace state."""
        response = client.get("/finance/workspace")
        data = response.json()
        assert data["status"] == "ready"
        assert data["module"] == "finance"

    def test_finance_workspace_response_schema(self, client):
        """Test that the finance workspace response matches the expected schema."""
        response = client.get("/finance/workspace")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "module" in data


class TestLandingPage:
    def test_landing_page_returns_200(self, client):
        """Test that the landing page returns a 200 status code."""
        response = client.get("/")
        assert response.status_code == 200

    def test_landing_page_has_workspaces(self, client):
        """Test that the landing page lists available workspaces."""
        response = client.get("/")
        data = response.json()
        assert "workspaces" in data
        assert len(data["workspaces"]) > 0

    def test_landing_page_has_finance_workspace(self, client):
        """Test that the finance workspace is listed on the landing page."""
        response = client.get("/")
        data = response.json()
        workspaces = data["workspaces"]
        finance_workspace = next(
            (w for w in workspaces if w["name"] == "finance"), None
        )
        assert finance_workspace is not None
        assert finance_workspace["path"] == "/finance/workspace"


class TestAppLoading:
    def test_app_loads_without_errors(self, client):
        """Test that the app loads without blank state or broken layout."""
        # Make a simple request to verify the app is functional
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
