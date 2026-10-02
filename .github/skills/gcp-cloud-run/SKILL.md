---
name: gcp-cloud-run
description: Use when preparing or deploying this FastAPI and ADK service to Google Cloud Run.
---

# Deploy the FastAPI service to Cloud Run

Use this skill for Cloud Run deployment design, implementation, and operation. First inspect the current app, dependency manifest, and any existing Docker or CI files. This repository currently has no checked-in container or deployment configuration, so choose a minimal deployment path that satisfies the request.

## Container and runtime

- Bind the HTTP server to `0.0.0.0` and the port provided by the `PORT` environment variable. Keep the ASGI target `app.main:app` unless the application structure changes.
- Include only runtime dependencies and application files in the image. Do not copy `.env`, local credentials, caches, or tests into a production image.
- Set resource limits, concurrency, minimum instances, ingress, and public/private access only from stated requirements. Explain cost or availability implications when they materially affect the choice.
- Read API keys from Secret Manager or another approved secret store, not from image layers or checked-in files. Prefer workload identity and a least-privilege service identity for Google Cloud API access.
- Configure the service to handle termination and request timeouts. Keep health checks aligned with the service’s `/healthz` endpoint.

## Deployment and verification

- Confirm project, region, service name, access policy, and secret names before a real deployment. Inspect the target service before updating it.
- Prefer repeatable source-controlled deployment configuration or a documented `gcloud run deploy` command. Use current Google Cloud documentation for flags because deployment interfaces can change.
- After deployment, verify the Cloud Run revision is ready, inspect logs for startup/runtime failures, and call `/healthz`. Exercise `/query` only with an approved test query and avoid exposing credentials or sensitive prompts in logs.
- Report the deployed service, revision, URL/access mode, verification performed, and rollback route. Do not claim deployment succeeded without checking service state.

## MCP use

When the official Cloud Run MCP server is available, use it for service inspection and deployment operations within the configured identity’s permissions. Keep the target project and region explicit and follow any configured approval controls. The Cloud Run MCP server does not replace the application runtime’s service identity or secret configuration.
