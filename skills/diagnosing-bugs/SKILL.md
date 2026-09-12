---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the cause remains unclear after initial inspection, or when explicitly requested.
---

# Diagnosing Bugs

A discipline for hard bugs. Use the phases that advance the investigation, and state when missing evidence limits a phase.

Before starting, preserve the user's requested outcome. If they asked only for diagnosis, establish and report the cause with evidence, clean up temporary instrumentation, and stop before changing production behavior. Continue through the fix and regression-test phase only when fixing is in scope.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Phase 1 — Build a feedback loop

A **tight** pass/fail signal that goes red on this bug makes bisection, hypothesis testing, and instrumentation more useful. Prefer building that signal; when it is unavailable, use the evidence-based investigation path below.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one — try them in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is tight — a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not — keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Report what you tried and which evidence is missing. Continue investigating available source, logs, traces, and other artifacts with explicitly tentative hypotheses. Ask for the specific artifact or environment access needed while continuing independent authorized work. Obtain permission before accessing production or adding production instrumentation unless that action is already authorized. Distinguish inferred causes from reproduced ones and report verification limits.

### Completion criterion — a tight loop that goes red

When reproduction is available, Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** — a script path, a test invocation, a curl — that you have **already run at least once** (paste the invocation and its output), and that is:

- [ ] **Red-capable** — it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring" — it must be able to _catch this specific bug_.
- [ ] **Deterministic** — same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast** — seconds, not minutes.
- [ ] **Agent-runnable** — you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

Prefer a red-capable loop for testing a causal theory. If reproduction is unavailable, record the evidence gap and proceed with the available evidence; a hypothesis alone does not establish the cause.

## Phase 2 — Reproduce + minimise

Run the loop. Watch it go red — the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut — keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing** — removing any one of them makes the loop go green.

When a reproduction is available, use the minimised case to test hypotheses. Otherwise continue with available evidence and retain the reproduction gap in the findings.

## Phase 3 — Hypothesise

Rank the hypotheses supported by the evidence and consider plausible alternatives. Test the strongest discriminating prediction first; do not invent alternatives to meet a quota.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the environment supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the seams that distinguish hypotheses.
3. Never "log everything and search".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes one repository search. Untagged logs survive; tagged logs die.

**Performance branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

Phase 4 is done when discriminating evidence supports a causal explanation, or further progress requires unavailable evidence or access. Rule out plausible alternatives where the evidence permits. If the requested outcome is diagnosis only, remove temporary instrumentation and report the cause or tentative explanation, evidence, and remaining uncertainty, then stop.

## Phase 5 — Fix + regression test

Enter this phase only when fixing is in scope.

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Run the Phase 1 feedback loop against the original, un-minimised scenario when available; otherwise run the strongest available affected checks and report the reproduction gap.

## Phase 6 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces, or the unavailable reproduction and verification limits are documented
- [ ] Regression test passes (or absence of seam is documented)
- [ ] Required task and CI checks are accounted for; reuse passing results only while the covered code and environment are unchanged, and rerun affected checks after relevant cleanup edits or failures
- [ ] All `[DEBUG-...]` instrumentation removed (search the unique prefix)
- [ ] Throwaway prototypes deleted or moved to a clearly marked debug location
- [ ] The hypothesis that proved correct is included in the handoff, commit, or PR description if one is produced

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling), hand off the specifics to the `improve-codebase-architecture` skill. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.
