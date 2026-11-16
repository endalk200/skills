# Agent Skills Repository

This repository contains agent skills I use in my daily work. Some are original; others are adapted to fit my workflows and use cases.

## Skills

The collection currently contains 33 published skills under [`skills/`](skills/).

A common delivery workflow is:

`grill-with-docs` -> `to-spec` -> `to-tickets` -> `implement` or `implement-spec` -> `code-review` -> verify in the running app

In a repository set up with `setup-verification`, that last step follows `docs/agents/verification/README.md`.

`Manual` skills declare `disable-model-invocation: true` and are intended to be invoked explicitly. `Model or manual` skills may be selected by the agent or invoked directly.

## Agent Compatibility

| Agent       | Manual-skill policy                                               | Explicit invocation |
| ----------- | ----------------------------------------------------------------- | ------------------- |
| Claude Code | `disable-model-invocation: true` in `SKILL.md`                    | `/skill-name`       |
| Cursor      | `disable-model-invocation: true` in `SKILL.md`                    | `/skill-name`       |
| Codex       | `policy.allow_implicit_invocation: false` in `agents/openai.yaml` | `$skill-name`       |

The Agent Skills specification does not currently standardize manual-only invocation. The canonical frontmatter is retained for Claude Code and Cursor, while each manual skill carries Codex's companion metadata. Agents that support neither, such as OpenCode, may offer manual skills to the model; this repository ships no adapter for them.

Claude Code users should note that manual-only frontmatter is supported for regular user and project skills, but some Claude Code versions have ignored it for plugin-provided skills.

| Skill                                                                            | Purpose                                                                                                            | Invocation      |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------- |
| [`code-review`](skills/code-review/SKILL.md)                                     | Triage and fix findings from a GPT-6.1 Sol review of the change, or from reviewers on an open PR.                  | Manual          |
| [`codebase-design`](skills/codebase-design/SKILL.md)                             | Apply deep-module vocabulary and principles to interfaces, seams, testability, and architecture.                   | Model or manual |
| [`commit`](skills/commit/SKILL.md)                                               | Create focused, safe commits using the Conventional Commits format.                                                | Manual          |
| [`create-pr`](skills/create-pr/SKILL.md)                                         | Publish the current branch as a review-ready pull or merge request.                                                | Model or manual |
| [`diagnosing-bugs`](skills/diagnosing-bugs/SKILL.md)                             | Diagnose hard bugs and regressions through a tight, red-capable feedback loop.                                     | Model or manual |
| [`domain-modeling`](skills/domain-modeling/SKILL.md)                             | Sharpen domain terminology, maintain `GLOSSARY.md`, and record durable architectural decisions.                    | Model or manual |
| [`effect`](skills/effect/SKILL.md)                                               | Build production TypeScript applications with Effect v4 using source-backed patterns.                              | Model or manual |
| [`grill-me`](skills/grill-me/SKILL.md)                                           | Start a relentless interview that sharpens a plan or design.                                                       | Manual          |
| [`grill-with-docs`](skills/grill-with-docs/SKILL.md)                             | Grill a plan while maintaining its domain glossary and ADRs.                                                       | Manual          |
| [`grilling`](skills/grilling/SKILL.md)                                           | Stress-test a design tree through dependency-aware frontier rounds.                                                | Model or manual |
| [`handoff`](skills/handoff/SKILL.md)                                             | Write a redacted handoff document so another agent can continue the session.                                       | Manual          |
| [`implement`](skills/implement/SKILL.md)                                         | Implement a spec or ticket set and verify it without committing, then review it with `code-review`.                | Manual          |
| [`implement-spec`](skills/implement-spec/SKILL.md)                               | Implement a ticketed spec on one integration branch with parallel implementer subagents, then review it.           | Manual          |
| [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md) | Find deepening opportunities and present them in a visual architecture report.                                     | Manual          |
| [`investigate-library-upgrade`](skills/investigate-library-upgrade/SKILL.md)     | Trace an upgrade's upstream changes to repository usage before implementation.                                     | Manual          |
| [`maintain-verification`](skills/maintain-verification/SKILL.md)                 | Audit the verification runbook and feature map against source and the running app, then ship fixes.                | Manual          |
| [`prototype`](skills/prototype/SKILL.md)                                         | Build shareable logic or UI prototypes that answer a focused design question.                                      | Model or manual |
| [`research`](skills/research/SKILL.md)                                           | Investigate a question through primary sources and save cited findings in the repository.                          | Model or manual |
| [`retro`](skills/retro/SKILL.md)                                                 | Review a coding session and suggest improvements to the agent environment.                                         | Manual          |
| [`setup-skills`](skills/setup-skills/SKILL.md)                                   | Configure issue tracking, triage and Wayfinder labels, and domain-document conventions for the engineering skills. | Manual          |
| [`setup-verification`](skills/setup-verification/SKILL.md)                       | Write a runbook and feature map that let any agent launch, drive, and prove the running app.                       | Manual          |
| [`source-context`](skills/source-context/SKILL.md)                               | Fetch dependency source code for implementation-level and version-specific investigation.                          | Model or manual |
| [`tdd`](skills/tdd/SKILL.md)                                                     | Develop behavior through deliberate seams using a red-green-refactor cycle.                                        | Model or manual |
| [`teach`](skills/teach/SKILL.md)                                                 | Maintain a stateful teaching workspace with missions, lessons, resources, and learning records.                    | Manual          |
| [`technical-writing`](skills/technical-writing/SKILL.md)                         | Apply a layered writing standard to technical documentation.                                                       | Model or manual |
| [`to-questionnaire`](skills/to-questionnaire/SKILL.md)                           | Turn a decision you can't answer alone into a Markdown questionnaire for someone who can.                          | Manual          |
| [`to-spec`](skills/to-spec/SKILL.md)                                             | Synthesize the current discussion into a spec and publish it to the configured tracker.                            | Manual          |
| [`to-tickets`](skills/to-tickets/SKILL.md)                                       | Split a spec or plan into dependency-aware vertical-slice tickets and publish them.                                | Manual          |
| [`triage`](skills/triage/SKILL.md)                                               | Move incoming issues and external pull requests through category and state roles into durable outcomes.            | Manual          |
| [`wait-what`](skills/wait-what/SKILL.md)                                         | Re-pitch the previous response with missing context and simpler language.                                          | Manual          |
| [`wayfinder`](skills/wayfinder/SKILL.md)                                         | Navigate large uncertain efforts through a shared map of decision tickets.                                         | Manual          |
| [`wizard`](skills/wizard/SKILL.md)                                               | Generate an interactive bash wizard for setup steps only a human can perform.                                      | Model or manual |
| [`writing-for-agents`](skills/writing-for-agents/SKILL.md)                       | Write predictable skills, agent instructions, and documents reached by context pointers.                           | Model or manual |

## Validation

Run `python3 scripts/validate-skills.py` after adding, removing, or changing skill metadata. The validator keeps the active skill directories, catalog, Claude plugin manifest, Codex metadata, and invocation policies synchronized.

## Attribution

Some of the skills in this repo are adopted from [Matt Pocock's skills](https://github.com/mattpocock/skills) and have been customized for my use cases and also adopted to work with other coding agent. Matt's skills are too dependent on claude code specific things.

`setup-verification` and `maintain-verification` are adapted from the `create-verification-skill` and `maintain-verification-skill` skills in [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT). They write agent-neutral docs under `docs/agents/` instead of a Cursor skill, and run without subagents.
