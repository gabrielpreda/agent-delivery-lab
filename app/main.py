"""HTTP API exposing health and query endpoints for the ADK agent."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.agent import run_medical_note_parser

logger = logging.getLogger(__name__)
MedicalNoteParser = Callable[[str], Awaitable[dict[str, str]]]

app = FastAPI(title="Agent Delivery Lab", version="0.1.0")


class MedicalNoteRequest(BaseModel):
    """Request body containing a medical note as plain text."""

    medical_note: str = Field(min_length=1)

    @field_validator("medical_note")
    @classmethod
    def medical_note_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("medical_note must contain non-whitespace characters")
        return value


class SOAPNote(BaseModel):
    """The four SOAP sections; undocumented sections are represented as null."""

    subjective: str | None
    objective: str | None
    assessment: str | None
    plan: str | None


class SOAPCheckResult(BaseModel):
    """Checker outcome; retry orchestration is implemented by the next story."""

    passed: bool
    issues: list[str]


class MedicalNoteParseResponse(BaseModel):
    """Response body containing SOAP conversion and checker output."""

    soap_note: SOAPNote
    validation: SOAPCheckResult


def get_medical_note_parser() -> MedicalNoteParser:
    """Provide the ADK parser; tests can override this dependency."""
    return run_medical_note_parser


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Report that the HTTP service is running."""
    return {"status": "ok"}


@app.post("/soap/parse", response_model=MedicalNoteParseResponse)
async def parse_medical_note(
    request: MedicalNoteRequest,
    note_parser: MedicalNoteParser = Depends(get_medical_note_parser),
) -> MedicalNoteParseResponse:
    """Run the note through parsing, normalization, conversion, and checking."""
    try:
        result = await note_parser(request.medical_note)
        soap_json = result["soap_note"]
        check_json = result["check_result"]
        soap_note = SOAPNote.model_validate_json(soap_json)
        validation = SOAPCheckResult.model_validate_json(check_json)
    except Exception as exc:
        logger.exception("Medical note parsing failed")
        raise HTTPException(
            status_code=502,
            detail="Medical note parsing failed",
        ) from exc
    return MedicalNoteParseResponse(soap_note=soap_note, validation=validation)