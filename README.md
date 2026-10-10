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

- `delivery-lifecycle` describes Jira-backed work from Miro/Figma discovery through implementation, review, deployment, and delivery status updates.
- `miro-jira-story-generation` defines how to read Miro/Figma evidence, check Jira for duplicates, draft stories, and gate Jira writes on approval.
- `fastapi-adk` captures the service and agent conventions in this repository.
- `gcp-cloud-run` covers deployment and operations on Cloud Run.
- `gcp-agent-engine` covers architecture and deployment considerations for Agent Engine.
- `gcp-deployment-lifecycle` coordinates GCP preflight, identity/secrets/build readiness, approval, deployment, verification, and rollback with the target-specific skills.
- `container-deployment` covers local Docker, Kubernetes, and other managed container targets.
- `generate-pytest-suite`, `repository-discovery`, `pandas-data-cleaning`, and `gcp-document-ai-batch` are also present; the last two support unrelated project types.

The VS Code MCP configuration in `.vscode/mcp.json` includes Jira, the official hosted Miro MCP server, a local token-based Figma MCP server, GitHub's hosted MCP server, Google's hosted Cloud Run MCP server, and Google Developer Knowledge for official ADK/GCP documentation. Jira credentials must be supplied as `JIRA_USERNAME` and `JIRA_API_TOKEN`; the Jira MCP server is launched with `uvx mcp-atlassian`, so install `uv` and make it available on `PATH`. Miro uses the official hosted server and its OAuth sign-in flow in VS Code; authorize the Miro account/team that can access the required boards. No Miro token is needed in `.env`. The Figma server is [Framelink's figma-developer-mcp](https://github.com/GLips/Figma-Context-MCP), launched with `npx` at the version pinned in `.vscode/mcp.json`. Add `FIGMA_API_KEY` from a Figma personal access token to your ignored local `.env`; VS Code loads it for the local Figma MCP process. Use read-only file scopes where possible. `.env` is gitignored and must not be copied into a container image. The Developer Knowledge key is requested by VS Code and is not stored in the checked-in file. The GitHub and Cloud Run endpoints require the corresponding sign-in and IAM permissions in the MCP host. Cloud Run MCP can modify cloud resources, so use a least-privilege identity and verify the target project and region before deployment. No Agent Engine-specific MCP server is configured; follow current Google SDK/CLI guidance for that target. The [Delivery Lifecycle agent](.github/agents/delivery-lifecycle.agent.md) enables the configured provider tools subject to its tool allowlist and active-session authentication/permissions.

### Generate Jira stories from product discovery

1. Start the Jira server and the relevant source MCP server (Miro or Figma) from the Chat tools/customizations UI. Complete Jira credentials, Miro OAuth authorization, and/or add `FIGMA_API_KEY` to your ignored `.env` as applicable. Confirm the tools start and can read the requested resource; configuration alone does not grant resource access.
2. In Copilot Chat, choose **Delivery Lifecycle** from the agent picker. Provide the Miro board or Figma file URL and Jira project key, for example: `Review this Figma file and draft Jira stories for project ABC: <file URL>`.
3. The agent reads relevant frames, flows, notes, comments, and design context using the actual tools exposed by the selected server; records source evidence; searches Jira for related stories and duplicates; and checks the project's issue types and required fields. It then presents proposed stories, acceptance criteria, dependencies, evidence, and unresolved questions.
4. Review the proposal. Jira issues are created only after you explicitly approve the displayed story batch. The agent reports the Jira keys and links returned by Jira. Story generation does not start implementation; request implementation separately by Jira key.

If a source is ambiguous or unavailable, choose the correct file/board and verify OAuth or token scopes plus resource permissions. For an unavailable or stale tool list, inspect **Chat: Open Customizations → Tools** and restart the relevant MCP server. See the [Miro MCP setup guide](https://developers.miro.com/docs/connecting-to-miro-mcp), [Framelink Figma MCP](https://github.com/GLips/Figma-Context-MCP), and [VS Code MCP documentation](https://code.visualstudio.com/docs/agent-customization/mcp-servers) for setup details.

### Deploy to GCP

Use **Delivery Lifecycle** for the approved delivery path. Copilot follows `gcp-deployment-lifecycle` plus `gcp-cloud-run` or `gcp-agent-engine`, checks the target and current state, prepares a concrete rollout and rollback plan, and requests approval for the exact cloud changes before applying them. Cloud Run operations are available through the configured `cloud_run` MCP server when authenticated and authorized. Agent Engine currently has no configured dedicated MCP server, so execution requires a verified authorized SDK/CLI path or another available GCP tool. See those skills for preflight, verification, and reporting requirements.
