---
name: container-deployment
description: Use when packaging this Python service for a Docker-compatible host or a non-GCP container platform.
---

# Portable container deployment

Use this skill when the deployment target is not specified or is outside the GCP-specific Cloud Run and Agent Engine skills. First check whether the repository already defines a container image, CI pipeline, or infrastructure. Keep platform-specific setup in a small adapter layer and verify details against the selected provider’s current documentation.

## Application contract

- Run the ASGI application as `app.main:app` unless the application structure changes.
- Listen on `0.0.0.0` and the port supplied by the host (commonly `PORT`); avoid hard-coded host ports in production.
- Build a reproducible image from the declared Python dependencies. Use a supported Python version, a non-root runtime user where practical, and a minimal runtime image.
- Keep secrets out of the image, source control, build arguments, and logs. Use the target platform’s secret manager or runtime secret injection.
- Add health and readiness checks that match actual startup and dependency behavior. The current service exposes `/healthz` for process health; do not report external dependencies as healthy unless they are checked.
- Set resource, request timeout, concurrency, and replica limits based on expected model latency and provider quotas. Avoid hard-coded assumptions about one vendor’s limits.

## Platform adapters

- For local Docker or Compose, provide a clear build/run path and a safe environment-variable example without real secret values.
- For Kubernetes, define deployment, service, probes, resource requests/limits, and secret references. Do not commit kubeconfig files or cluster credentials.
- For managed container platforms, follow their port, health, identity, scaling, and logging contracts. Cloud Run has its dedicated skill.
- For CI/CD, build once and promote the same immutable image digest between environments. Pin or constrain dependencies and use the platform’s workload identity/OIDC support where available.

## Release checks

- Run the project’s configured tests and static checks before release when requested by the task or repository workflow.
- Inspect the final image configuration for included secrets and unnecessary files.
- After release, verify deployment readiness, health endpoint behavior, logs, and rollback instructions. State the exact environment and image digest/revision verified.
