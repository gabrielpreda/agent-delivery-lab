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
- `POST /soap/parse` accepts `{"medical_note":"..."}` and returns the final
	`soap_note` only when validation passes. If validation fails after the one
	retry, `soap_note` is `null` and the validation issues are returned. The root
	ADK workflow parses and normalizes the note, then runs SOAP conversion and
	checking in a loop with at most two attempts. Undocumented SOAP sections are
	`null`; blank input returns HTTP 422 and workflow failures return HTTP 502.
- Interactive API documentation is available at `/docs`.

Each medical note workflow runs in a new in-memory ADK session; conversation
history is not retained between requests or process restarts.

## Tests

```sh
pytest
```

## Agent development skills and MCP tools

Repository-specific GitHub Copilot skills live in `.github/skills/`:

- `delivery-lifecycle` describes Jira-backed work from triage through review and merge.
- `fastapi-adk` captures the service and agent conventions in this repository.
- `gcp-cloud-run` covers deployment and operations on Cloud Run.
- `gcp-agent-engine` covers architecture and deployment considerations for Agent Engine.
- `container-deployment` covers local Docker, Kubernetes, and other managed container targets.
- `generate-pytest-suite`, `repository-discovery`, `pandas-data-cleaning`, and `gcp-document-ai-batch` are also present; the last two support unrelated project types.

The VS Code MCP configuration in `.vscode/mcp.json` includes Jira, GitHub's hosted MCP server, Google's hosted Cloud Run MCP server, and Google Developer Knowledge for official ADK/GCP documentation. Jira credentials must be supplied as `JIRA_USERNAME` and `JIRA_API_TOKEN`; the Developer Knowledge key is requested by VS Code and is not stored in the checked-in file. The GitHub and Cloud Run endpoints require the corresponding sign-in and IAM permissions in the MCP host. Cloud Run MCP can modify cloud resources, so use a least-privilege identity and verify the target project and region before deployment. No Agent Engine-specific MCP server is configured; follow current Google SDK/CLI guidance for that target.
