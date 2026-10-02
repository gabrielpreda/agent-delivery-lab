import asyncio
from types import SimpleNamespace
from typing import Any

from google.genai import types

from app import agent


def test_run_agent_query_uses_a_fresh_session_and_returns_final_text(
    monkeypatch: Any,
) -> None:
    calls: dict[str, Any] = {}

    async def create_session(**kwargs: Any) -> None:
        calls["session"] = kwargs

    async def run_async(**kwargs: Any) -> Any:
        calls["run"] = kwargs
        yield SimpleNamespace(
            is_final_response=lambda: True,
            content=types.Content(parts=[types.Part(text="Agent response")]),
        )

    monkeypatch.setattr(agent.session_service, "create_session", create_session)
    monkeypatch.setattr(agent.runner, "run_async", run_async)

    response = asyncio.run(agent.run_agent_query("Test query"))

    assert response == "Agent response"
    assert calls["session"]["app_name"] == agent.APP_NAME
    assert calls["session"]["user_id"] == agent.USER_ID
    assert calls["session"]["session_id"]
    assert calls["run"]["user_id"] == agent.USER_ID
    assert calls["run"]["session_id"] == calls["session"]["session_id"]
    assert calls["run"]["new_message"].parts[0].text == "Test query"