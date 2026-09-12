---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Use `tdd` where possible, at seams selected within the accepted scope and repository conventions.

Run affected checks during implementation and complete the checks required by the accepted task and repository CI before declaring readiness. Reuse passing results while the code and environment they cover remain unchanged; rerun affected checks after relevant edits or failures. Report required checks as passed, failed, or not run.
