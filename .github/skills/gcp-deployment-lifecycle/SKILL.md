---
name: gcp-deployment-lifecycle
description: Prepare, deploy, verify, and document this application on Google Cloud using the selected runtime skill.
---

# GCP deployment lifecycle

Use this skill to prepare and carry out an authorized deployment to Google Cloud. Pair it with [Cloud Run](../gcp-cloud-run/SKILL.md) or [Agent Engine](../gcp-agent-engine/SKILL.md) for target-specific behavior. This repository currently has Cloud Run and Google Developer Knowledge MCP servers configured; it has no Agent Engine-specific MCP server. Configuration does not prove the tools are connected, authenticated, or authorized.

## 1. Establish the release target

- Inspect the app, dependency lock, tests, Docker/build configuration, CI workflow, and existing infrastructure before selecting a deployment path.
- Confirm environment, GCP project, region, service/resource name, runtime target, desired access policy, source commit or immutable image digest, and who is authorizing deployment. Do not infer a production target from local gcloud defaults.
- Use current official Google documentation for changing APIs, flags, IAM roles, supported regions, and runtime requirements. Prefer Google Developer Knowledge MCP when connected; otherwise use official documentation and report any unresolved uncertainty.
- If target choices are missing, prepare a concrete deployment plan and identify only the choices that block a safe deployment.

## 2. Prepare and preflight

- Check the active identity and its least-privilege permissions. Prefer workload identity / service identity; do not create or download long-lived service-account keys.
- Identify required Google APIs, Artifact Registry or source-build path, runtime service account, Secret Manager entries and access bindings, network/ingress policy, and logging/monitoring needs. Enable APIs or change IAM only when required and explicitly included in the approved scope.
- Keep secret values out of source, shell history, build args, logs, and tool output. Bind secret references to the runtime identity; never print secret contents to verify them.
- Build reproducibly from the checked-in lock/configuration. Inspect the build context for `.env`, credentials, caches, tests, and other unintended files. Use an immutable image digest for promotion when an image workflow exists.
- Run repository release checks when requested or required by its workflow. State the exact commands and outcomes. Do not make live cloud writes as a substitute for local validation.
- Inspect the existing target before update. Capture the current revision/configuration needed for rollback and identify whether the change is additive, destructive, or may cause downtime.

## 3. Gate cloud changes

Before any cloud mutation, present the exact project, region, environment, resource, source revision/image digest, access mode, IAM/secret/API changes, rollout strategy, checks, and rollback route. Obtain explicit approval for that scope. Approval to edit code, create a pull request, or merge does not authorize cloud changes. Renew approval if target or material configuration changes.

If using Cloud Run MCP, use only tools exposed by the active `cloud_run` server and confirm the selected project/resource before each write. If using `gcloud`, inspect `gcloud config` and use explicit project/region flags; never rely on an implicit active project. Do not silently fall back to shell commands if the required MCP operation is unavailable or vice versa.

## 4. Deploy and verify

- Apply only the approved deployment plan. Prefer a repeatable checked-in configuration or documented command. Record the source commit, image digest, deployment command/tool operation, project, region, and returned revision/resource ID.
- Confirm rollout readiness and the expected runtime identity, ingress/access policy, secret references, and health configuration. Review startup/runtime logs for failures without exposing sensitive input.
- Call the documented health endpoint (currently `/healthz` for the FastAPI service). Run a functional smoke request only when its input is non-sensitive and within the approved scope.
- If deployment or verification fails, stop rollout/promotion, capture the error and current state, and report the recovery options. Roll back only when rollback is covered by the approval; otherwise ask for approval before that cloud write.

## 5. Record the result

Report the environment, project/region, service/resource, revision or image digest, access mode, health/smoke checks and outcomes, relevant logs, remaining risks, and tested rollback route. Update Jira only after approval of the exact status/comment update. Never claim a deployment succeeded based solely on a successful command response; verify the live resource state.

## Tool boundaries

- The repository's `cloud_run` MCP endpoint is the Cloud Run operations integration. Use its currently advertised tools, not guessed tool names. It does not deploy Agent Engine resources.
- `google_developer_knowledge` supplies documentation context, not deployment authority.
- Agent Engine deployment requires a verified current SDK/CLI path or a separately configured, authorized tool. If none is available, prepare the deployment artifacts and exact operator steps, and state that execution is blocked by missing capability.
- GitHub MCP is for repository/PR operations; it does not establish GCP IAM or deployment permission.
