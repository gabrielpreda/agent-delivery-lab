"""Google ADK agent configuration and query execution."""

from __future__ import annotations

import os
from uuid import uuid4

from dotenv import load_dotenv
from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.exit_loop_tool import exit_loop
from google.genai import types

load_dotenv()

APP_NAME = "agent_delivery_lab"
USER_ID = "api-user"
MODEL = os.getenv("ADK_MODEL", "gemini-flash-latest")

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
    output_key="parsed_content",
)

medical_note_normalizer_agent = Agent(
    name="medical_note_normalizer",
    model=MODEL,
    description="Normalizes parsed medical-note facts before SOAP conversion.",
    instruction=(
        "Normalize the parsed medical-note content into a concise, consistent "
        "factual representation for SOAP conversion. Preserve all clinically "
        "relevant facts, uncertainty, and omissions. Do not infer, diagnose, or "
        "add facts that are not present. Do not assign SOAP sections yet.\n\n"
        "Parsed content:\n{parsed_content}\n\n"
        "If a previous validation result is present, address its issues while "
        "normalizing:\n{check_result?}"
    ),
    output_key="normalized_content",
)

medical_note_soap_converter_agent = Agent(
    name="medical_note_soap_converter",
    model=MODEL,
    description="Converts normalized medical-note facts into structured SOAP JSON.",
    instruction=(
        "Convert the normalized medical-note content into a SOAP note. Return "
        "only valid JSON with exactly four string-or-null fields named "
        "subjective, objective, assessment, and plan. Use null for any section "
        "that is not documented. Preserve uncertainty and do not invent facts, "
        "diagnoses, or recommendations. Do not include markdown fences or text "
        "outside the JSON object.\n\n"
        "Normalized content:\n{normalized_content}\n\n"
        "If this is a retry, correct the previous checker issues:\n"
        "{check_result?}"
    ),
    output_key="soap_note",
)

medical_note_soap_checker_agent = Agent(
    name="medical_note_soap_checker",
    model=MODEL,
    description="Checks SOAP structure and fidelity to normalized note facts.",
    instruction=(
        "Validate the generated SOAP JSON against the normalized source. Check "
        "that it has the four SOAP sections, that documented facts are not "
        "invented or contradicted, and that undocumented sections remain null. "
        "Return only valid JSON with a boolean field named passed and a list of "
        "string issues. Set passed to true only when the SOAP note is valid. "
        "Do not rewrite the SOAP note or include markdown fences. Call the "
        "exit_loop tool when the note passes. If this is the second check and "
        "it still fails, call exit_loop to stop; otherwise leave the loop "
        "running for its single retry.\n\n"
        "Normalized content:\n{normalized_content}\n\n"
        "SOAP note:\n{soap_note}\n\n"
        "Previous validation result (empty on the first check):\n"
        "{check_result?}"
    ),
    output_key="check_result",
    tools=[exit_loop],
)

soap_conversion_and_check_loop = LoopAgent(
    name="soap_conversion_and_check_loop",
    description=(
        "Converts and validates SOAP output, retrying conversion once when "
        "validation fails."
    ),
    sub_agents=[medical_note_soap_converter_agent, medical_note_soap_checker_agent],
    max_iterations=2,
)

root_agent = SequentialAgent(
    name="medical_note_workflow",
    description=(
        "Orchestrates parsing and normalization followed by bounded SOAP "
        "conversion and validation."
    ),
    sub_agents=[
        medical_note_parser_agent,
        medical_note_normalizer_agent,
        soap_conversion_and_check_loop,
    ],
)

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def _run_agent(input_text: str) -> dict[str, str]:
    """Run the root workflow in a fresh session and return SOAP/check output."""
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

    async for _event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):
        pass

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )
    if session is not None:
        soap_note = session.state.get("soap_note")
        check_result = session.state.get("check_result")
        if (
            isinstance(soap_note, str)
            and soap_note.strip()
            and isinstance(check_result, str)
            and check_result.strip()
        ):
            return {
                "soap_note": soap_note,
                "check_result": check_result,
            }

    raise RuntimeError("The ADK workflow completed without a checked SOAP note.")


async def run_medical_note_parser(medical_note: str) -> dict[str, str]:
    """Run the note through parsing, normalization, conversion, and checking."""
    return await _run_agent(medical_note)