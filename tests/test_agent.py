import asyncio
from types import SimpleNamespace
from typing import Any

from google.adk.agents import SequentialAgent
from google.genai import types

from app import agent


def test_root_agent_orchestrates_parser_and_pipeline_uses_root_runner(
    monkeypatch: Any,
) -> None:
    calls: dict[str, Any] = {}

    async def create_session(**kwargs: Any) -> None:
        calls["session"] = kwargs

    async def get_session(**kwargs: Any) -> Any:
        calls["get_session"] = kwargs
        return SimpleNamespace(
            state={
                "parsed_content": "Parsed note facts",
                "normalized_content": "Normalized note facts",
                "soap_note": (
                    '{"subjective":"Headache","objective":null,'
                    '"assessment":null,"plan":null}'
                ),
                "check_result": '{"passed":true,"issues":[]}',
            }
        )

    async def run_async(**kwargs: Any) -> Any:
        calls["run"] = kwargs
        for output in (
            "Parsed note facts",
            "Normalized note facts",
            '{"subjective":"Headache","objective":null,'
            '"assessment":null,"plan":null}',
        ):
            yield SimpleNamespace(
                is_final_response=lambda: True,
                content=types.Content(parts=[types.Part(text=output)]),
            )

    monkeypatch.setattr(agent.session_service, "create_session", create_session)
    monkeypatch.setattr(agent.session_service, "get_session", get_session)
    monkeypatch.setattr(agent.runner, "run_async", run_async)

    response = asyncio.run(agent.run_medical_note_parser("Medical note text"))

    assert isinstance(agent.root_agent, SequentialAgent)
    assert agent.root_agent.sub_agents == [
        agent.medical_note_parser_agent,
        agent.medical_note_normalizer_agent,
        agent.medical_note_soap_converter_agent,
        agent.medical_note_soap_checker_agent,
    ]
    assert agent.runner.agent is agent.root_agent
    assert agent.medical_note_parser_agent.output_key == "parsed_content"
    assert agent.medical_note_normalizer_agent.output_key == "normalized_content"
    assert "{parsed_content}" in agent.medical_note_normalizer_agent.instruction
    assert agent.medical_note_soap_converter_agent.output_key == "soap_note"
    assert "{normalized_content}" in agent.medical_note_soap_converter_agent.instruction
    assert agent.medical_note_soap_checker_agent.output_key == "check_result"
    assert "{soap_note}" in agent.medical_note_soap_checker_agent.instruction
    assert response == {
        "soap_note": (
            '{"subjective":"Headache","objective":null,'
            '"assessment":null,"plan":null}'
        ),
        "check_result": '{"passed":true,"issues":[]}',
    }
    assert calls["session"]["app_name"] == agent.APP_NAME
    assert calls["session"]["user_id"] == agent.USER_ID
    assert calls["session"]["session_id"]
    assert calls["run"]["user_id"] == agent.USER_ID
    assert calls["run"]["session_id"] == calls["session"]["session_id"]
    assert calls["run"]["new_message"].parts[0].text == "Medical note text"
    assert calls["get_session"]["session_id"] == calls["session"]["session_id"]