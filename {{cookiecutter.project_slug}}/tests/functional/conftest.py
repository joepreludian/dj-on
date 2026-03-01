import pytest
from django.test import Client


@pytest.fixture(scope="session")
def api_client():
    return Client()