# Copilot instructions

- Establish the repository's current purpose, stack, and architecture from its README, manifests, source, and tests before proposing changes. Do not infer them from the repository name or ignore-file patterns.
- This repository currently has minimal project documentation. If a request depends on product behavior or a technology choice that the repository does not establish, ask for clarification rather than inventing requirements or scaffolding a speculative design.
- Check the project’s own manifests and documentation for build, lint, and test commands; do not assume a toolchain or claim validation that was not run.
- Keep changes focused, and add or update tests and user-facing documentation when implementing an agreed behavior.
- For bootstrap work in a sparse or undocumented repository, follow [the repository discovery skill](skills/repository-discovery/SKILL.md).
- For Jira-backed feature delivery, follow [the delivery lifecycle skill](skills/delivery-lifecycle/SKILL.md); keep review approval with an authorized reviewer.
- For Miro or Figma discovery and Jira-backed delivery in VS Code, select the [Delivery Lifecycle agent](agents/delivery-lifecycle.agent.md) and follow the [delivery lifecycle skill](skills/delivery-lifecycle/SKILL.md). For drafting Jira stories, also follow the [Miro/Jira story generation skill](skills/miro-jira-story-generation/SKILL.md). Discover the active provider tools, ground requirements in source evidence, check Jira for duplicates, and get approval for the exact batch before Jira writes. Never guess provider tool names or claim access without verifying the tools are available.
- For GCP deployment, follow the [GCP deployment lifecycle skill](skills/gcp-deployment-lifecycle/SKILL.md) and the relevant target skill: [Cloud Run](skills/gcp-cloud-run/SKILL.md) or [Agent Engine](skills/gcp-agent-engine/SKILL.md). Deployment requires an explicit target and approval for the specific cloud changes; code or merge approval alone does not authorize production deployment.
- For application changes, use the [FastAPI and ADK](skills/fastapi-adk/SKILL.md) guidance and relevant deployment guidance, or [portable container deployment](skills/container-deployment/SKILL.md) for other hosts.
- Prefer the narrowest applicable skill. Do not apply unrelated data-cleaning or Document AI guidance to this FastAPI/ADK service.
