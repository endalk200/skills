# Writing Agent Briefs

An agent brief is a structured comment posted on an issue or pull request when it moves to `ready-for-agent`. It is the authoritative specification that an AFK agent will work from. The original body and discussion are context; the agent brief is the contract.

The brief states **what the agent should do**. For an issue, that means building the change from nothing. For a pull request, it means what remains to finish or correct the existing diff.

## Principles

### Durability over precision

The item may sit in `ready-for-agent` for days or weeks while the codebase changes.

- Describe interfaces, types, and behavioral contracts.
- Name specific types, function signatures, or config shapes that the agent should find or modify.
- Describe code by domain and interface rather than file path or line number.
- Write so the brief survives implementation refactors.

### Behavioral, not procedural

Describe **what** the system should do, not **how** to implement it. The agent will explore the codebase fresh and make its own implementation decisions.

- **Good:** "The `SkillConfig` type should accept an optional `schedule` field of type `CronExpression`."
- **Weak:** "Open the skill types file and add a schedule field."
- **Good:** "Running triage without arguments should show a summary of issues needing attention."
- **Weak:** "Add a switch statement in the main handler."

### Complete acceptance criteria

Every brief must have concrete, independently verifiable acceptance criteria. The list is complete when satisfying every criterion establishes the desired behavior, including relevant error and boundary cases.

### Explicit scope boundaries

State what is out of scope so the agent does not gold-plate the issue or absorb adjacent work.

## Template

```markdown
## Agent Brief

**Category:** bug / enhancement
**Summary:** one-line description of what needs to happen

**Current behavior:**
Describe what happens now. For bugs, this is the broken behavior.
For enhancements, this is the status quo the feature builds on.

**Desired behavior:**
Describe what should happen after the work is complete.
Include relevant edge cases and error conditions.

**Key interfaces:**
- `TypeName`: what needs to change and why
- `functionName()` return type: what it currently returns and what it should return
- Config shape: any new configuration options

**Acceptance criteria:**
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3

**Out of scope:**
- Thing that should not be changed
- Adjacent feature that belongs in separate work
```

## Example: bug

```markdown
## Agent Brief

**Category:** bug
**Summary:** Description truncation should preserve word boundaries

**Current behavior:**
When a skill description exceeds 1024 characters, it is truncated at exactly
1024 characters and can end in the middle of a word.

**Desired behavior:**
Truncation should break at the last word boundary before the limit and append
"..." without exceeding the maximum length.

**Key interfaces:**
- `SkillMetadata.description` remains a string with the current size limit
- The description extraction and validation behavior changes

**Acceptance criteria:**
- [ ] Descriptions under 1024 characters are unchanged
- [ ] Longer descriptions break at the last word boundary
- [ ] Truncated descriptions end with "..."
- [ ] The result, including "...", does not exceed 1024 characters

**Out of scope:**
- Changing the length limit
- Adding multiline description support
```

## Example: enhancement

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** Add `.out-of-scope/` directory support for tracking rejected feature requests

**Current behavior:**
When a feature request is rejected, the issue is closed with a `wontfix` label
and a comment. There is no persistent record of the decision or reasoning.
Future similar requests require the maintainer to recall or search for the
prior discussion.

**Desired behavior:**
Rejected feature requests should be documented in `.out-of-scope/<concept>.md`
files that capture the decision, reasoning, and links to all issues that
requested the feature. When triaging new issues, these files should be
checked for matches.

**Key interfaces:**
- Markdown file format in `.out-of-scope/`: each file should have a
  `# Concept Name` heading, a `**Decision:**` line, a `**Reason:**` line,
  and a `**Prior requests:**` list with issue links
- The triage workflow should read all `.out-of-scope/*.md` files early
  and match incoming issues against them by concept similarity

**Acceptance criteria:**
- [ ] Closing a feature as wontfix creates/updates a file in `.out-of-scope/`
- [ ] The file includes the decision, reasoning, and link to the closed issue
- [ ] If a matching `.out-of-scope/` file already exists, the new issue is
      appended to its "Prior requests" list rather than creating a duplicate
- [ ] During triage, existing `.out-of-scope/` files are checked and surfaced
      when a new issue matches a prior rejection

**Out of scope:**
- Automated matching (human confirms the match)
- Reopening previously rejected features
- Bug reports (only enhancement rejections go to `.out-of-scope/`)
```

## Example: pull request

For a pull request, "Current behavior" describes the state of the diff and the brief asks the agent to finish or fix it.

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** Finish JSON error output in the proposed triage command

**Current behavior:**
The pull request serializes successful output as JSON, but errors still use
human-readable text and the new mode has no test coverage.

**Desired behavior:**
With JSON output selected, both success and error output should be valid JSON.
The existing human-readable behavior should remain unchanged otherwise.

**Key interfaces:**
- The command error path emits `{ "error": string }` in JSON mode
- The serializer already introduced by the pull request remains the single path

**Acceptance criteria:**
- [ ] Success and error cases emit valid JSON in JSON mode
- [ ] Exit codes remain unchanged
- [ ] Tests cover one success and one error case
- [ ] Default output remains unchanged

**Out of scope:**
- Adding JSON output to other commands
- Redesigning the successful payload
```

## Example: bad brief

```markdown
## Agent Brief

**Summary:** Fix the triage bug

**What to do:**
The triage thing is broken. Look at the main file and fix it.
The function around line 150 has the issue.

**Files to change:**
- src/triage/handler.ts (line 150)
- src/types.ts (line 42)
```

This is bad because:
- No category
- Vague description ("the triage thing is broken")
- References file paths and line numbers that will go stale
- No acceptance criteria
- No scope boundaries
- No description of current vs desired behavior
