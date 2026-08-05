# Skills

A common delivery workflow is:

`grill-with-docs` -> `to-spec` -> `to-tickets` -> `implement` -> `code-review`

`Manual` skills declare `disable-model-invocation: true` and are intended to be invoked explicitly. `Model or manual` skills may be selected by the agent or invoked directly.

## Agent Compatibility

| Agent       | Manual-skill policy                                               | Explicit invocation |
| ----------- | ----------------------------------------------------------------- | ------------------- |
| Claude Code | `disable-model-invocation: true` in `SKILL.md`                    | `/skill-name`       |
| Cursor      | `disable-model-invocation: true` in `SKILL.md`                    | `/skill-name`       |
| Codex       | `policy.allow_implicit_invocation: false` in `agents/openai.yaml` | `$skill-name`       |

The Agent Skills specification does not currently standardize manual-only invocation. The canonical frontmatter is retained for Claude Code and Cursor, while each manual skill carries Codex's companion metadata. OpenCode ignores the frontmatter field, so its configuration hides manual skills from the model-facing catalog and its command adapters inject the canonical `SKILL.md` only after explicit invocation.

OpenCode's paths and commands are relative to this repository root. When installing the collection elsewhere, copy or merge `opencode.json` and `.opencode/commands/` alongside the `skills/` directory. Claude Code users should note that manual-only frontmatter is supported for regular user and project skills, but some Claude Code versions have ignored it for plugin-provided skills.

| Skill                                                                     | Purpose                                                                                                            | Invocation      |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------- |
| [`babysit-pr`](babysit-pr/SKILL.md)                                       | Validate and triage PR review findings before addressing selected items.                                           | Manual          |
| [`code-review`](code-review/SKILL.md)                                     | Review changes against repository standards and the originating spec using parallel subagents.                     | Model or manual |
| [`codebase-design`](codebase-design/SKILL.md)                             | Apply deep-module vocabulary and principles to interfaces, seams, testability, and architecture.                   | Model or manual |
| [`conventional-commit`](conventional-commit/SKILL.md)                     | Create focused, safe commits using the Conventional Commits format.                                                | Model or manual |
| [`create-pr`](create-pr/SKILL.md)                                         | Publish the current branch as a review-ready pull or merge request.                                                 | Manual          |
| [`diagnosing-bugs`](diagnosing-bugs/SKILL.md)                             | Diagnose hard bugs and regressions through a tight, red-capable feedback loop.                                      | Model or manual |
| [`domain-modeling`](domain-modeling/SKILL.md)                             | Sharpen domain terminology, maintain `CONTEXT.md`, and record durable architectural decisions.                     | Model or manual |
| [`edit-article`](edit-article/SKILL.md)                                   | Restructure and tighten an article while preserving information dependencies.                                      | Manual          |
| [`effect`](effect/SKILL.md)                                               | Build production TypeScript applications with Effect v4 using source-backed patterns.                              | Model or manual |
| [`grill-me`](grill-me/SKILL.md)                                           | Start a relentless interview that sharpens a plan or design.                                                       | Manual          |
| [`grill-with-docs`](grill-with-docs/SKILL.md)                             | Grill a plan while maintaining its domain glossary and ADRs.                                                       | Manual          |
| [`grilling`](grilling/SKILL.md)                                           | Stress-test a design tree through dependency-aware frontier rounds.                                                 | Model or manual |
| [`handoff`](handoff/SKILL.md)                                             | Write a redacted handoff document so another agent can continue the session.                                       | Manual          |
| [`implement`](implement/SKILL.md)                                         | Implement a spec or ticket set, verify it, and review the result without committing it.                            | Manual          |
| [`improve-codebase-architecture`](improve-codebase-architecture/SKILL.md) | Find deepening opportunities and present them in a visual architecture report.                                     | Manual          |
| [`investigate-library-upgrade`](investigate-library-upgrade/SKILL.md)     | Trace an upgrade's upstream changes to repository usage before implementation.                                     | Model or manual |
| [`prototype`](prototype/SKILL.md)                                         | Build shareable logic or UI prototypes that answer a focused design question.                                      | Model or manual |
| [`research`](research/SKILL.md)                                           | Investigate a question through primary sources and save cited findings in the repository.                          | Model or manual |
| [`setup-skills`](setup-skills/SKILL.md)                                   | Configure issue tracking, triage and Wayfinder labels, and domain-document conventions for the engineering skills. | Manual          |
| [`source-context`](source-context/SKILL.md)                               | Fetch dependency source code for implementation-level and version-specific investigation.                          | Model or manual |
| [`tdd`](tdd/SKILL.md)                                                     | Develop behavior through deliberate seams using a red-green-refactor cycle.                                        | Model or manual |
| [`teach`](teach/SKILL.md)                                                 | Maintain a stateful teaching workspace with missions, lessons, resources, and learning records.                    | Manual          |
| [`to-spec`](to-spec/SKILL.md)                                             | Synthesize the current discussion into a spec and publish it to the configured tracker.                            | Manual          |
| [`to-tickets`](to-tickets/SKILL.md)                                       | Split a spec or plan into dependency-aware vertical-slice tickets and publish them.                                | Manual          |
| [`triage`](triage/SKILL.md)                                               | Move incoming issues and external pull requests through category and state roles into durable outcomes.            | Manual          |
| [`wait-what`](wait-what/SKILL.md)                                         | Re-pitch the previous response with missing context and simpler language.                                           | Manual          |
| [`wayfinder`](wayfinder/SKILL.md)                                         | Navigate large uncertain efforts through a shared map of decision tickets.                                         | Manual          |
| [`writing-for-agents`](writing-for-agents/SKILL.md)                       | Write predictable skills, agent instructions, and documents reached by context pointers.                           | Model or manual |
