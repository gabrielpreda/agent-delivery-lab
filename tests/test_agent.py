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

    async def run_async(**kwargs: Any) -> Any:
        calls["run"] = kwargs
        yield SimpleNamespace(
            is_final_response=lambda: True,
            content=types.Content(parts=[types.Part(text="Parsed note facts")]),
        )

    monkeypatch.setattr(agent.session_service, "create_session", create_session)
    monkeypatch.setattr(agent.runner, "run_async", run_async)

    response = asyncio.run(agent.run_medical_note_parser("Medical note text"))

    assert isinstance(agent.root_agent, SequentialAgent)
    assert agent.root_agent.sub_agents == [agent.medical_note_parser_agent]
    assert agent.runner.agent is agent.root_agent
    assert not hasattr(agent, "medical_note_parser_runner")
    assert response == "Parsed note facts"
    assert calls["session"]["app_name"] == agent.APP_NAME
    assert calls["session"]["user_id"] == agent.USER_ID
    assert calls["session"]["session_id"]
    assert calls["run"]["user_id"] == agent.USER_ID
    assert calls["run"]["session_id"] == calls["session"]["session_id"]
    assert calls["run"]["new_message"].parts[0].text == "Medical note text"