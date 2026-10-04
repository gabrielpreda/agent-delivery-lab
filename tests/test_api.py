from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_medical_note_parser


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_healthz_returns_service_status(client: TestClient) -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_legacy_query_route_is_removed(client: TestClient) -> None:
    response = client.post("/query", json={"query": "Hello"})

    assert response.status_code == 404


def test_parse_medical_note_returns_structured_soap_note(client: TestClient) -> None:
    async def fake_parser(medical_note: str) -> dict[str, str]:
        assert medical_note == "Patient reports a headache."
        return {
            "soap_note": (
                '{"subjective":"Headache","objective":null,'
                '"assessment":null,"plan":null}'
            ),
            "check_result": '{"passed":true,"issues":[]}',
        }

    app.dependency_overrides[get_medical_note_parser] = lambda: fake_parser

    response = client.post(
        "/soap/parse",
        json={"medical_note": "Patient reports a headache."},
    )

    assert response.status_code == 200
    assert response.json() == {
        "soap_note": {
            "subjective": "Headache",
            "objective": None,
            "assessment": None,
            "plan": None,
        },
        "validation": {"passed": True, "issues": []},
    }


def test_parse_medical_note_rejects_invalid_soap_json(
    client: TestClient,
) -> None:
    async def invalid_parser(_: str) -> dict[str, str]:
        return {
            "soap_note": "This is not SOAP JSON",
            "check_result": '{"passed":true,"issues":[]}',
        }

    app.dependency_overrides[get_medical_note_parser] = lambda: invalid_parser

    response = client.post("/soap/parse", json={"medical_note": "Note text"})

    assert response.status_code == 502
    assert response.json() == {"detail": "Medical note parsing failed"}


def test_parse_medical_note_does_not_deliver_failed_validation(
    client: TestClient,
) -> None:
    async def failed_validation(_: str) -> dict[str, str]:
        return {
            "soap_note": "Unvalidated note must not be delivered",
            "check_result": '{"passed":false,"issues":["Missing plan"]}',
        }

    app.dependency_overrides[get_medical_note_parser] = lambda: failed_validation

    response = client.post("/soap/parse", json={"medical_note": "Note text"})

    assert response.status_code == 200
    assert response.json() == {
        "soap_note": None,
        "validation": {
            "passed": False,
            "issues": ["Missing plan"],
        },
    }


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