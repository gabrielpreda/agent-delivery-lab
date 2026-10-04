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
- `miro-jira-story-generation` defines how to read Miro evidence, check Jira for duplicates, draft stories, and gate Jira writes on approval.
- `fastapi-adk` captures the service and agent conventions in this repository.
- `gcp-cloud-run` covers deployment and operations on Cloud Run.
- `gcp-agent-engine` covers architecture and deployment considerations for Agent Engine.
- `container-deployment` covers local Docker, Kubernetes, and other managed container targets.
- `generate-pytest-suite`, `repository-discovery`, `pandas-data-cleaning`, and `gcp-document-ai-batch` are also present; the last two support unrelated project types.

The VS Code MCP configuration in `.vscode/mcp.json` includes Jira, Miro, Figma, GitHub's hosted MCP server, Google's hosted Cloud Run MCP server, and Google Developer Knowledge for official ADK/GCP documentation. Jira credentials must be supplied as `JIRA_USERNAME` and `JIRA_API_TOKEN`; the Jira MCP server is launched with `uvx mcp-atlassian`, so install `uv` and make it available on `PATH`. Miro and Figma use their MCP server OAuth sign-in flows in VS Code; access follows the authorized account, team, and board/file permissions. The Developer Knowledge key is requested by VS Code and is not stored in the checked-in file. The GitHub and Cloud Run endpoints require the corresponding sign-in and IAM permissions in the MCP host. Cloud Run MCP can modify cloud resources, so use a least-privilege identity and verify the target project and region before deployment. No Agent Engine-specific MCP server is configured; follow current Google SDK/CLI guidance for that target.

### Generate Jira stories from a Miro board

1. Open this repository in VS Code and start the Jira and Miro MCP servers from the Chat tools/customizations UI. Complete Jira credentials and the Miro OAuth sign-in if prompted. Confirm the `jira` and `miro` tools are available; the configuration alone does not authenticate either service.
2. In Copilot Chat, choose **Miro to Jira Delivery** from the agent picker. Provide the full Miro board URL and the Jira project key, for example: `Review this Miro board and draft Jira stories for project ABC: <board URL>`.
3. The agent reads relevant diagrams, frames, notes, and comments; records board evidence; searches Jira for related stories and duplicates; and checks the project's issue types and required fields. It then presents the proposed stories, acceptance criteria, dependencies, evidence, and unresolved questions.
4. Review the proposal. Jira issues are created only after you explicitly approve the displayed story batch. The agent reports the Jira keys and links returned by Jira. Story generation does not start implementation; request implementation separately by Jira key.

If a board name finds multiple results, choose the correct board. If Miro cannot find a board, check that the Miro OAuth session uses a team with access and that the user has board permission. For an unavailable or stale tool list, inspect **Chat: Open Customizations → Tools** and restart or reconnect the relevant MCP server. See the [Miro MCP setup guide](https://developers.miro.com/docs/connecting-miro-mcp-to-ai-coding-tools) and [VS Code MCP documentation](https://code.visualstudio.com/docs/agent-customization/mcp-servers) for client setup details.
