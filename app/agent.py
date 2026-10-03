"""Google ADK agent configuration and query execution."""

from __future__ import annotations

import os
from uuid import uuid4

from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

APP_NAME = "agent_delivery_lab"
USER_ID = "api-user"
MODEL = os.getenv("ADK_MODEL", "gemini-flash-latest")

root_agent = Agent(
    name="assistant",
    model=MODEL,
    description="A general-purpose assistant exposed through a small HTTP API.",
    instruction="Answer the user's query clearly and concisely.",
)

medical_note_parser_agent = Agent(
    name="medical_note_parser",
    model=MODEL,
    description="Extracts information from medical notes for later normalization.",
    instruction=(
        "Extract and organize information explicitly stated in the medical note "
        "for subsequent normalization into a SOAP note. Do not invent or infer "
        "facts, diagnoses, medications, dates, or findings. Preserve uncertainty "
        "and omissions. Return concise plain text; do not create SOAP sections."
    ),
)

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)
medical_note_parser_runner = Runner(
    agent=medical_note_parser_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def _run_agent(runner: Runner, input_text: str) -> str:
    """Run input in a fresh ADK session and return the final text response."""
    session_id = uuid4().hex
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )
    message = types.Content(
        role="user",
        parts=[types.Part(text=input_text)],
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):
        if not event.is_final_response() or event.content is None:
            continue
        response_parts = [
            part.text for part in event.content.parts or [] if part.text
        ]
        if response_parts:
            return "\n".join(response_parts)

    raise RuntimeError("The ADK agent completed without a text response.")


async def run_agent_query(query: str) -> str:
    """Run one general query in a fresh ADK session."""
    return await _run_agent(runner, query)


async def run_medical_note_parser(medical_note: str) -> str:
    """Parse one medical note in a fresh ADK session."""
    return await _run_agent(medical_note_parser_runner, medical_note)