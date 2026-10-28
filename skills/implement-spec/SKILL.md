---
name: implement-spec
description: Implement a whole spec and its tickets on one integration branch, running implementer subagents in parallel across the ticket frontier, then review the result.
disable-model-invocation: true
---

You have been provided a spec. It should have tickets, produced by `to-tickets`, describing how to implement it. For a single ticket or a spec without tickets, use `implement` instead.

The issue tracker should have been provided to you. If not, tell the user to run `setup-skills` first.

The goal is the entire spec implemented on a single **integration branch**. Invoking this skill authorizes local branches, worktrees, and commits for that goal. Push, open a pull request, or change ticket state only when the user has authorized publishing.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them, so there is always a **frontier** of tickets that are ready to be worked.

Run subagents with the host's subagent mechanism, each **implementer subagent** in an isolated worktree, in the background where possible for maximum concurrency. If the host cannot run isolated or background subagents, work the frontier yourself one ticket at a time, in the same order, on branches off the integration branch.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: the spec, the tickets, exploration notes, and previous commits. Don't duplicate information already available through a pointer.

## Steps

1. Read the spec and tickets to understand the task graph.

2. (Optional) Use an **exploration subagent** for any exploration the tickets need: relevant codebase files or external documentation. It saves its notes as markdown in a directory outside the repo (the OS temp directory) that every later subagent can read, so **implementer subagents** can focus on implementation.

3. Create the integration branch from the default branch. If the issue tracker closes work through pull requests and the user authorized publishing, open a draft pull request after the first merge in step 5 (a branch with no commits ahead of the default branch can't open one), marked as closing the spec and tickets.

4. Start one **implementer subagent** per frontier ticket, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - reads the `tdd` skill completely and applies it to build the ticket;
   - merges the integration branch tip into its own branch before reporting done.

5. When an **implementer subagent** completes, merge its branch into the integration branch with a **merger subagent**.

6. If the merge changes the **frontier**, start **implementer subagents** for the newly ready tickets.

7. Once every ticket is merged, read the `code-review` skill completely and follow it on the integration branch, using the default branch as the fixed point. Invoking `implement-spec` is the user's request for that review. Its reviewer runs on a provider the user picks, so ask for it at the start of this skill unless the user named one, rather than stalling here.

8. If a draft pull request exists, mark it ready for review. Otherwise, if the user authorized tracker updates, resolve each ticket the way the issue tracker closes work. Report the integration branch, the checks run and their results, and any ticket left unresolved.

9. Remove every **implementer subagent** worktree.
