# Copilot instructions

- Establish the repository's current purpose, stack, and architecture from its README, manifests, source, and tests before proposing changes. Do not infer them from the repository name or ignore-file patterns.
- This repository currently has minimal project documentation. If a request depends on product behavior or a technology choice that the repository does not establish, ask for clarification rather than inventing requirements or scaffolding a speculative design.
- Check the project’s own manifests and documentation for build, lint, and test commands; do not assume a toolchain or claim validation that was not run.
- Keep changes focused, and add or update tests and user-facing documentation when implementing an agreed behavior.
- For bootstrap work in a sparse or undocumented repository, follow [the repository discovery skill](skills/repository-discovery/SKILL.md).
