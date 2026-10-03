"""HTTP API exposing health and query endpoints for the ADK agent."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.agent import run_agent_query, run_medical_note_parser

logger = logging.getLogger(__name__)
AgentQuery = Callable[[str], Awaitable[str]]
MedicalNoteParser = Callable[[str], Awaitable[str]]

app = FastAPI(title="Agent Delivery Lab", version="0.1.0")


class QueryRequest(BaseModel):
    """Request body for an agent query."""

    query: str = Field(min_length=1)

    @field_validator("query")
    @classmethod
    def query_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("query must contain non-whitespace characters")
        return value


class QueryResponse(BaseModel):
    """Response body returned after the agent completes a query."""

    response: str


class MedicalNoteRequest(BaseModel):
    """Request body containing a medical note as plain text."""

    medical_note: str = Field(min_length=1)

    @field_validator("medical_note")
    @classmethod
    def medical_note_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("medical_note must contain non-whitespace characters")
        return value


class MedicalNoteParseResponse(BaseModel):
    """Response body containing parsed note text for downstream normalization."""

    parsed_content: str


def get_agent_query() -> AgentQuery:
    """Provide the ADK query runner; tests can override this dependency."""
    return run_agent_query


def get_medical_note_parser() -> MedicalNoteParser:
    """Provide the ADK parser; tests can override this dependency."""
    return run_medical_note_parser


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Report that the HTTP service is running."""
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
async def query_agent(
    request: QueryRequest,
    agent_query: AgentQuery = Depends(get_agent_query),
) -> QueryResponse:
    """Send a query to the configured ADK agent."""
    try:
        response = await agent_query(request.query)
    except Exception as exc:
        logger.exception("ADK agent query failed")
        raise HTTPException(
            status_code=502,
            detail="Agent query failed",
        ) from exc
    return QueryResponse(response=response)


@app.post("/soap/parse", response_model=MedicalNoteParseResponse)
async def parse_medical_note(
    request: MedicalNoteRequest,
    note_parser: MedicalNoteParser = Depends(get_medical_note_parser),
) -> MedicalNoteParseResponse:
    """Parse a medical note and return text for downstream normalization."""
    try:
        parsed_content = await note_parser(request.medical_note)
    except Exception as exc:
        logger.exception("Medical note parsing failed")
        raise HTTPException(
            status_code=502,
            detail="Medical note parsing failed",
        ) from exc
    return MedicalNoteParseResponse(parsed_content=parsed_content)