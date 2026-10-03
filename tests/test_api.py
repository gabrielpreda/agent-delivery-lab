from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_agent_query, get_medical_note_parser


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


def test_parse_medical_note_returns_parsed_content(client: TestClient) -> None:
    async def fake_parser(medical_note: str) -> str:
        assert medical_note == "Patient reports a headache."
        return "Reported symptom: headache"

    app.dependency_overrides[get_medical_note_parser] = lambda: fake_parser

    response = client.post(
        "/soap/parse",
        json={"medical_note": "Patient reports a headache."},
    )

    assert response.status_code == 200
    assert response.json() == {"parsed_content": "Reported symptom: headache"}


@pytest.mark.parametrize("medical_note", ["", "   ", "\n\t"])
def test_parse_medical_note_rejects_blank_input(
    client: TestClient,
    medical_note: str,
) -> None:
    response = client.post("/soap/parse", json={"medical_note": medical_note})

    assert response.status_code == 422


def test_parse_medical_note_hides_parser_exception_details(
    client: TestClient,
) -> None:
    async def failing_parser(_: str) -> str:
        raise RuntimeError("private backend detail")

    app.dependency_overrides[get_medical_note_parser] = lambda: failing_parser

    response = client.post("/soap/parse", json={"medical_note": "Note text"})

    assert response.status_code == 502
    assert response.json() == {"detail": "Medical note parsing failed"}