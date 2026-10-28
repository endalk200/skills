---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker (see `docs/agents/issue-tracker.md`) and state its title before starting. If the reference is ambiguous, ask.

Read the `tdd` skill completely and apply it where possible, at seams selected within the accepted scope and repository conventions.

Run affected checks during implementation and complete the checks required by the accepted task and repository CI before declaring readiness. Reuse passing results while the code and environment they cover remain unchanged; rerun affected checks after relevant edits or failures. Report required checks as passed, failed, or not run.

When the work is ready, ask the user to run the `code-review` skill, which has a second model review the uncommitted work. It is manual-only, so do not start it yourself. Do not commit unless the user asks.
