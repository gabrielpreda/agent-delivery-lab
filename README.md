# Agent Delivery Lab

Minimal FastAPI wrapper for a Google Agent Development Kit (ADK) assistant.

## Setup

Use Python 3.10 or later. Install the project and its test dependencies:

```sh
python -m pip install -e '.[dev]'
```

Set `GOOGLE_API_KEY` in the process environment or in a local `.env` file. The
agent model can be changed with `ADK_MODEL`; it defaults to
`gemini-flash-latest`.

## Run

```sh
uvicorn app.main:app --reload
```

## API

- `GET /healthz` returns `{"status":"ok"}`.
- `POST /query` accepts `{"query":"..."}` and returns `{"response":"..."}`.
	Empty and whitespace-only queries are rejected with HTTP 422. Agent execution
	failures return HTTP 502.
- Interactive API documentation is available at `/docs`.

Each query runs in a new in-memory ADK session; conversation history is not
retained between requests or process restarts. The initial agent is a generic
assistant because SCRUM-1 does not specify domain instructions, tools, or
persistent conversation behavior.

## Tests

```sh
pytest
```
