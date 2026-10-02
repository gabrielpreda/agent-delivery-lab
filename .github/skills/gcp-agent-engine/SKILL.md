---
name: gcp-agent-engine
description: Use when adapting, deploying, or operating the ADK agent on Google Cloud Agent Engine (currently documented by Google under Agent Runtime / Agent Platform terminology).
---

# Deploy the ADK agent to Agent Engine

Use this skill when the requested target is Google Cloud Agent Engine / Agent Runtime. Product names, APIs, SDKs, regions, and supported ADK features can change; check current official Google documentation and installed package versions before coding deployment calls.

## Check the architecture first

- This repository currently runs ADK inside a FastAPI service and creates a fresh in-memory session per HTTP request. Agent Engine hosts an ADK application as an agent resource; it is not automatically a drop-in host for this FastAPI API.
- Confirm whether the goal is to move agent execution to Agent Engine, keep FastAPI as a gateway to a remote agent, or expose the agent directly. Preserve the current HTTP contract only if that is part of the request.
- Check session behavior, streaming needs, authentication, supported ADK tools, and data residency requirements before selecting a design.

## Deployment practices

- Follow the current official ADK and Agent Engine deployment path and use pinned, compatible SDK dependencies. Keep local execution and tests independent from live cloud resources.
- Use explicit project, supported region, staging bucket, runtime identity, and least-privilege IAM. Never commit service account keys or credentials.
- Externalize model/provider credentials and other secrets using supported managed secret mechanisms. Do not bake secrets into package archives or images.
- Define how FastAPI reaches the remote agent, if it remains in the design, including authentication, timeouts, retries, streaming, and safe error mapping.
- Treat create/update/delete operations as cloud changes. Inspect the target resource and configuration before applying them.

## Validate and document

- Run local pytest tests with cloud calls mocked. Validate deployment configuration and SDK compatibility before creating a live resource.
- After deployment, verify resource readiness and invoke a non-sensitive smoke query using the supported SDK/API. Check logs and record the deployed resource identifier and region.
- Document cost-bearing resources, cleanup procedure, identity requirements, and rollback/update procedure.
- There is no Agent Engine-specific MCP server configured in this repository. Use the supported SDK/CLI or a verified Google Cloud MCP tool when available; do not assume the Cloud Run MCP manages Agent Engine resources.
