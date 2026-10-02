---
name: repository-discovery
description: Use when bootstrapping, planning a first feature, or choosing architecture in a sparse or undocumented repository; verify project facts and clarify unresolved requirements before committing to a stack or design.
---

# Repository Discovery

Use this workflow when the repository does not yet establish its purpose, implementation stack, or development workflow.

1. Inspect the README, tracked files, manifests, CI configuration, tests, and existing documentation. Treat these as evidence; do not infer a stack from the repository name or ignore rules.
2. Summarize what is established and what remains unknown. Look for documented goals, runtime/dependency declarations, scripts, and test conventions.
3. If the requested work depends on unresolved product behavior or a consequential technology choice, ask a concise clarifying question before scaffolding or implementing it. For decisions that do not affect the request, choose the smallest conventional option consistent with verified repository evidence.
4. Once scope is clear, make the smallest coherent change that fits the existing project structure. Avoid introducing frameworks, dependencies, or architecture without a demonstrated need.
5. Validate with commands declared by the project’s manifests or documentation. If no suitable command exists, report that limitation and use relevant checks that can be justified by the repository; never imply an unrun check passed.
6. When an implementation adds durable project facts or workflows, update the relevant project documentation so later work can rely on it.
