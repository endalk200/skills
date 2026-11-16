---
name: source-context
description: Use when writing code against a dependency whose installed version is newer than you know (a new major, or an API you don't recognize), when asked how a dependency works internally, when debugging unexpected library behavior, when a fix or recommendation needs source-backed evidence, or when opensrc is mentioned.
---

# Source Context

Fetches dependency source code so agents can read implementations, not just types. Clones repositories at the correct version tag and caches them globally at `~/.opensrc/`.

For anything beyond a quick one-file lookup, prefer running this work in a dedicated subagent.

Use a dedicated subagent by default when you need to:

- Inspect multiple files
- Trace call paths across a library
- Compare runtime code and tests
- Verify edge-case behavior
- Investigate version-specific behavior
- Summarize findings without dumping raw source into the main thread

Have the subagent:

1. Resolve the correct source tree with `opensrc path ...`
2. Read the repository's agent-facing docs first when it ships them: `LLMS.md`, `llms.txt`, `ai-docs/`, migration guides. They sit at the repository root, which for a monorepo package is above the printed path (two levels up from `.../packages/effect`). Search long migration guides rather than reading them whole.
3. Inspect the fetched code with normal search and read tools
4. Return only the relevant files, symbols, and conclusions

Prompt the subagent with the full target and question, including any version or cwd constraints.

## Usage Examples

```bash
rg "parse" $(opensrc path zod)
cat $(opensrc path zod)/src/types.ts
find $(opensrc path zod) -name "*.test.ts"

# Specific versions
opensrc path zod@3.22.0
opensrc path pypi:flask@3.0.0
```

`opensrc path <pkg>` prints the absolute path to downloaded source.

### Version Resolution

Pin the version the project actually installs. For npm packages, `opensrc` resolves it from lockfiles such as `package-lock.json`, `bun.lock`, `pnpm-lock.yaml`, and `yarn.lock` when run from the project root; use `--cwd` when the lockfiles are elsewhere, and `<pkg>@<version>` otherwise:

```bash
opensrc path zod --cwd /path/to/project/lock-file
```

## When Not to Use It

Do not fetch source for:

- API usage of a dependency version you already know
- Setup or installation questions
- Cases where docs or types already answer the question
- Broad research that does not require implementation details
