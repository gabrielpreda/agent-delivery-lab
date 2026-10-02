---
name: fastapi-adk
description: Use when implementing or reviewing this FastAPI service and its Google Agent Development Kit (ADK) agent.
---

# FastAPI and ADK project conventions

Use this skill for API, agent, configuration, and test changes in this repository.

## Establish the current design

- Confirm behavior in `README.md`, `app/main.py`, `app/agent.py`, and `tests/` before changing it.
- Keep the HTTP API boundary in FastAPI and agent execution behind the `get_agent_query` dependency so API tests can substitute a fake.
- The current `/query` endpoint creates a fresh in-memory ADK session for each request. Do not introduce persistent conversation state or a different session model without an explicit requirement.
- Load credentials from the environment or supported Google authentication. Never commit `.env`, API keys, access tokens, service account keys, or secret values.

## Implementation

- Use async route and agent calls where the underlying operation is asynchronous.
- Keep request and response schemas explicit with Pydantic. Validate blank input and return stable, non-sensitive client errors.
- Log backend exceptions server-side, but do not expose provider errors or credentials in API responses.
- Keep the agent’s model configurable through `ADK_MODEL`; check the installed ADK APIs and project lockfile before adopting a new API or dependency.
- Keep cloud-specific deployment and authentication configuration out of request handlers.

## Verification and documentation

- Add pytest coverage for API success, validation, dependency failures, and ADK session/event behavior affected by the change. Mock external model and cloud calls.
- Use the repository’s declared `pytest` command and report whether it was run.
- Update README behavior and configuration notes when the public API, session semantics, required environment, or deployment process changes.
