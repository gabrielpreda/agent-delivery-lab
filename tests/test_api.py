from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_agent_query


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_healthz_returns_service_status(client: TestClient) -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query_returns_agent_response(client: TestClient) -> None:
    async def fake_query(query: str) -> str:
        assert query == "Hello"
        return "Hi there."

    app.dependency_overrides[get_agent_query] = lambda: fake_query

    response = client.post("/query", json={"query": "Hello"})

    assert response.status_code == 200
    assert response.json() == {"response": "Hi there."}


@pytest.mark.parametrize("query", ["", "   ", "\n\t"])
def test_query_rejects_blank_input(client: TestClient, query: str) -> None:
    response = client.post("/query", json={"query": query})

    assert response.status_code == 422


def test_query_hides_agent_exception_details(client: TestClient) -> None:
    async def failing_query(_: str) -> str:
        raise RuntimeError("private backend detail")

    app.dependency_overrides[get_agent_query] = lambda: failing_query

    response = client.post("/query", json={"query": "Hello"})

    assert response.status_code == 502
    assert response.json() == {"detail": "Agent query failed"}