# Copilot instructions

- Establish the repository's current purpose, stack, and architecture from its README, manifests, source, and tests before proposing changes. Do not infer them from the repository name or ignore-file patterns.
- This repository currently has minimal project documentation. If a request depends on product behavior or a technology choice that the repository does not establish, ask for clarification rather than inventing requirements or scaffolding a speculative design.
- Check the project’s own manifests and documentation for build, lint, and test commands; do not assume a toolchain or claim validation that was not run.
- Keep changes focused, and add or update tests and user-facing documentation when implementing an agreed behavior.
- For bootstrap work in a sparse or undocumented repository, follow [the repository discovery skill](skills/repository-discovery/SKILL.md).
- For Jira-backed feature delivery, follow [the delivery lifecycle skill](skills/delivery-lifecycle/SKILL.md); keep review approval with an authorized reviewer.
- For Miro-to-Jira product discovery in VS Code, select the [Miro to Jira Delivery agent](agents/miro-jira-delivery.agent.md); use its explicitly enabled MCP tools and tool map. Never guess provider tool names or claim access without verifying the tools are available.
- For application changes, use the relevant stack guidance, including [FastAPI and ADK](skills/fastapi-adk/SKILL.md), [Cloud Run](skills/gcp-cloud-run/SKILL.md), [Agent Engine](skills/gcp-agent-engine/SKILL.md), or [portable container deployment](skills/container-deployment/SKILL.md).
- Prefer the narrowest applicable skill. Do not apply unrelated data-cleaning or Document AI guidance to this FastAPI/ADK service.
