import pytest


@pytest.mark.django_db
class TestHealthcheck:
    def test_healthcheck_endpoint(self, api_client):
        response = api_client.get("/api/healthcheck/")
        assert response.status_code == 200
