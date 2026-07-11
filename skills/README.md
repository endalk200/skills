# Skills

A common delivery workflow is:

`grill-with-docs` -> `to-spec` -> `to-tickets` -> `implement` -> `code-review`

`Manual` skills declare `disable-model-invocation: true` and are intended to be invoked explicitly. `Model or manual` skills may be selected by the agent or invoked directly.

| Skill | Purpose | Invocation |
| --- | --- | --- |
| [`code-review`](code-review/SKILL.md) | Review changes against repository standards and the originating spec using parallel subagents. | Model or manual |
| [`codebase-design`](codebase-design/SKILL.md) | Apply deep-module vocabulary and principles to interfaces, seams, testability, and architecture. | Model or manual |
| [`conventional-commit`](conventional-commit/SKILL.md) | Create focused, safe commits using the Conventional Commits format. | Model or manual |
| [`domain-modeling`](domain-modeling/SKILL.md) | Sharpen domain terminology, maintain `CONTEXT.md`, and record durable architectural decisions. | Model or manual |
| [`edit-article`](edit-article/SKILL.md) | Restructure and tighten an article while preserving information dependencies. | Manual |
| [`grill-me`](grill-me/SKILL.md) | Start a relentless interview that sharpens a plan or design. | Manual |
| [`grill-with-docs`](grill-with-docs/SKILL.md) | Grill a plan while maintaining its domain glossary and ADRs. | Manual |
| [`grilling`](grilling/SKILL.md) | Stress-test a plan one decision at a time until shared understanding is reached. | Model or manual |
| [`handoff`](handoff/SKILL.md) | Write a redacted handoff document so another agent can continue the session. | Manual |
| [`implement`](implement/SKILL.md) | Implement a spec or ticket set, verify it, and review the result without committing it. | Manual |
| [`improve-codebase-architecture`](improve-codebase-architecture/SKILL.md) | Find deepening opportunities and present them in a visual architecture report. | Manual |
| [`investigate-library-upgrade`](investigate-library-upgrade/SKILL.md) | Trace an upgrade's upstream changes to repository usage before implementation. | Model or manual |
| [`prototype`](prototype/SKILL.md) | Build throwaway logic or UI prototypes that answer a focused design question. | Model or manual |
| [`research`](research/SKILL.md) | Investigate a question through primary sources and save cited findings in the repository. | Model or manual |
| [`setup-skills`](setup-skills/SKILL.md) | Configure issue tracking, triage and Wayfinder labels, and domain-document conventions for the engineering skills. | Manual |
| [`source-context`](source-context/SKILL.md) | Fetch dependency source code for implementation-level and version-specific investigation. | Model or manual |
| [`tdd`](tdd/SKILL.md) | Develop behavior through deliberate seams using a red-green-refactor cycle. | Model or manual |
| [`teach`](teach/SKILL.md) | Maintain a stateful teaching workspace with missions, lessons, resources, and learning records. | Manual |
| [`to-spec`](to-spec/SKILL.md) | Synthesize the current discussion into a spec and publish it to the configured tracker. | Manual |
| [`to-tickets`](to-tickets/SKILL.md) | Split a spec or plan into dependency-aware vertical-slice tickets and publish them. | Manual |
| [`wayfinder`](wayfinder/SKILL.md) | Navigate large uncertain efforts through a shared map of investigation tickets. | Manual |
| [`writing-great-skills`](writing-great-skills/SKILL.md) | Provide principles and vocabulary for writing predictable, maintainable skills. | Manual |
