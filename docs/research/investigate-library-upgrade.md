# Research: a stronger `investigate-library-upgrade` skill

## Question

How can the existing [`investigate-library-upgrade` skill](https://raw.githubusercontent.com/pauldambra/dotfiles/refs/heads/main/ai/skills/investigate-library-upgrade/SKILL.md) be improved by applying this repository's primary-source research approach?

## Conclusion

Keep its most important boundary: investigate, write an assessment, and stop before changing the project. Replace its changelog-led classification with an **evidence-led compatibility investigation**. The key question should become:

> What changes between the resolved current and proposed target states, which of those changes intersect with this repository's actual use, and how could that impact be verified?

The strongest workflow uses four independent evidence streams:

1. resolved dependency state and package metadata;
2. upstream migration guidance, release notes, and source/tag diffs;
3. repository usage, configuration, and runtime-context evidence;
4. the repository's existing verification and deployment machinery.

## Findings

### 1. A version number and changelog are useful signals, not proof of compatibility

Semantic Versioning only works when a project declares a precise public API and follows the specification. It explicitly treats `0.y.z` and prereleases as unstable, and even its own guidance says consumers should verify upgrades. Therefore the skill should use SemVer to set an initial risk prior, never to conclude safety. ([SemVer 2.0.0](https://semver.org/))

The current skill's rule that an API absent from the changelog's breaking-change list is **Safe** is too strong. A better category is **No known impact found**, accompanied by the evidence searched and its coverage. Missing documentation is uncertainty, not evidence of compatibility.

### 2. Establish both declared intent and the complete resolved state

The current skill is right to prefer lockfiles for exact versions, but it should retain both views:

- the manifest expresses the project's requested range, features/extras, source, aliases, overrides, and workspace intent;
- the lockfile expresses the resolved dependency graph used for reproducible installation.

This distinction is explicit across ecosystems: npm says `package-lock.json` describes the exact generated tree; uv distinguishes broad `pyproject.toml` requirements from exact, cross-platform `uv.lock` resolutions; and Cargo says `Cargo.toml` is broad while `Cargo.lock` contains exact dependency information. ([npm lockfile](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/), [uv lockfile](https://docs.astral.sh/uv/concepts/projects/layout/#the-lockfile), [Cargo lockfile](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html))

The assessment should record, per workspace and dependency edge:

- declared constraint and dependency kind (runtime, development, peer, optional);
- resolved version and source (registry, Git revision, fork, alias, local replacement);
- enabled features/extras and platform markers;
- whether multiple resolved versions exist and why;
- the proposed target-selection rule (exact version, stable channel, explicit registry tag, or prerelease).

For Go specifically, `go.sum` is a checksum record and can contain versions no longer selected; it should not be treated as the installed-version authority. The module graph/tool output and `go.mod` directives—including `replace` and `retract`—must be interpreted together. ([Go Modules Reference](https://go.dev/ref/mod#go-mod-file))

### 3. Compare the compatibility envelope and the artifact, not only APIs named in prose

An upgrade can fail before an application calls an API. The skill should compare current and target package metadata for:

- supported runtime/toolchain versions;
- operating system, CPU, libc, and Python environment markers;
- peer dependencies and their satisfiability in the whole graph;
- default and optional features/extras;
- entry points, module format, exported subpaths, binaries, plugins, and generated types;
- direct/transitive dependency graph changes and native/build requirements;
- withdrawn, deprecated, yanked, or retracted releases.

These fields carry real compatibility constraints. npm documents that peer dependencies express host compatibility and can make graph resolution fail, while `engines`, `os`, `cpu`, and `libc` describe environment constraints. Python package metadata similarly exposes `Requires-Python`, conditional `Requires-Dist`, and extras. Cargo features control conditional compilation and optional dependencies, and `rust-version` states the required toolchain. ([npm `package.json`](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/), [Python core metadata](https://packaging.python.org/en/latest/specifications/core-metadata/), [Cargo features](https://doc.rust-lang.org/cargo/reference/features.html), [Cargo Rust version](https://doc.rust-lang.org/cargo/reference/rust-version.html))

For Node packages, changes to `exports` deserve explicit treatment: Node documents that introducing or restricting `exports` can make previously working subpath imports fail, even if the named JavaScript API appears unchanged. ([Node package entry points](https://nodejs.org/api/packages.html#package-entry-points))

Where tooling permits, compare the actual published artifacts. For example, `npm diff --diff=pkg@old --diff=pkg@new` compares the registry tarballs for two package versions. Artifact/API diffs can reveal removed files, exports, declarations, or generated assets omitted from release prose. ([`npm diff`](https://docs.npmjs.com/cli/v11/commands/npm-diff))

### 4. Make upstream research a triangulation step

Use a source hierarchy, but do not stop after the first source:

1. official migration or upgrade guide;
2. official changelog and release notes;
3. package registry metadata and published artifacts;
4. source and public-API diff between the exact version tags/commits;
5. relevant upstream tests, issues, or pull requests only when they explain an observed change.

Release discovery needs explicit completeness checks. GitHub's Releases API excludes ordinary Git tags that have no associated release, so “all GitHub releases between X and Y” is not necessarily “all shipped versions.” Compare exact tags/commits and reconcile them with registry versions; record any version-to-tag mapping gaps. ([GitHub Releases API](https://docs.github.com/en/rest/releases/releases#list-releases), [GitHub tag/commit comparison](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/viewing-and-comparing-commits/comparing-commits))

Every upstream claim in the assessment should link to its owning source. Inference should be labeled as inference, separate from upstream statements.

### 5. Discover usage beyond imports, then reason by unique usage shape

Import search is only the first pass. The skill should also inspect:

- deep/subpath and dynamic imports;
- re-exports and wrapper modules;
- type-only use, annotations, generated code, macros, derive/procedural use;
- configuration files, package scripts, command-line invocations, plugins and framework conventions;
- serialized/persisted values, network contracts, snapshots, fixtures, and environment variables;
- mocks, test helpers, examples, and build/deployment definitions.

For Python, distribution names and import names are not reliably identical, and namespace packages may map one import name to multiple distributions; the standard library exposes this mapping but notes limitations for some editable installs. This is a concrete reason not to generate grep patterns directly from a registry name. ([Python `importlib.metadata`](https://docs.python.org/3/library/importlib.metadata.html#mapping-import-to-distribution-packages))

Replace the hard “more than 200 files: sample and stop” rule with bounded, coverage-oriented analysis:

1. enumerate all candidate sites mechanically;
2. group them by import path, API, call/configuration shape, and execution context;
3. inspect every unique high-risk shape;
4. sample only repeated equivalent shapes;
5. report counts, exclusions, sampled groups, and uncovered areas.

This scales better without allowing a rare but critical usage to disappear in a convenience sample.

### 6. Classify claims, not files, and preserve uncertainty

A file can contain several usages with different risks. Use one row per **usage/change intersection**, with these categories:

- **No known impact found** — searched evidence did not identify an intersecting change;
- **Mechanical migration** — required edit is explicit and locally checkable;
- **Behavioral or verification risk** — code may compile but semantics, defaults, timing, serialization, or output may change;
- **Design decision required** — removed capability or changed semantics require choosing an approach;
- **Unknown** — evidence is absent, contradictory, inaccessible, or the usage cannot be resolved confidently.

Attach an evidence link and confidence to each claim. Report confidence as a vector rather than one vague score:

| Dimension | What lowers confidence |
| --- | --- |
| Version/source identity | aliases, forks, mutable Git refs, ambiguous tags |
| Upstream change coverage | missing releases/tags, incomplete migration docs |
| Artifact/API coverage | unavailable artifacts, generated or dynamic interfaces |
| Repository usage coverage | reflection, code generation, conventions, broad exclusions |
| Compatibility inference | undocumented behavior or contradictory evidence |
| Verification coverage | missing tests, unavailable platforms/services, weak CI |

The final conclusion should state what was not inspected and what evidence would raise confidence.

### 7. Derive a verification plan from this repository

Even though the investigation must not perform the upgrade, it should inspect the repository's actual scripts, CI workflows, test configuration, runtime matrix, deployment checks, and ownership boundaries. Then map each identified risk to an exact verification step.

A useful plan distinguishes:

- install/resolution checks;
- compile, type-check, lint, and public-API checks;
- focused tests for affected usage shapes;
- full regression/build checks;
- platform/runtime matrix checks;
- smoke, integration, migration, and rollback checks where behavior or persisted data changes.

List commands already present in the repository and clearly label newly proposed commands. Do not claim that a check passed unless it was actually run against the target state. SemVer itself advises consumers to verify that upgrades function as advertised. ([SemVer 2.0.0](https://semver.org/#why-use-semantic-versioning))

## Recommended skill shape

Use these phases:

1. **Frame scope** — package identity, target policy, workspaces, environments, investigation-only boundary.
2. **Capture baseline** — manifest intent plus exact resolved graph and source.
3. **Resolve target** — stable/prerelease policy, withdrawn versions, runtime constraints, version/tag mapping.
4. **Build upstream evidence set** — migration docs, releases, changelog, metadata/artifact and tag/API diffs.
5. **Map repository usage** — code, config, CLI, generated/conventional use; group by unique shape.
6. **Intersect and classify** — one evidence-backed claim per change/usage intersection.
7. **Plan verification and rollout** — derive exact checks from repository machinery and map them to risks.
8. **Write assessment and stop** — include evidence, coverage, uncertainties, estimates, and decision points; make no project changes.

The output should include an evidence ledger, resolved-state delta, compatibility-envelope delta, impacted usage table, verification matrix, uncertainty/coverage section, and recommended next decision. Avoid “reply go ahead” as automatic authorization language; implementation should begin only when the user's next request unambiguously asks for it.

## Suggested acceptance criteria for the rewritten skill

- It never labels an upgrade or usage “safe” solely because a changelog is silent.
- It distinguishes manifest constraints from resolved versions and graph state.
- It reconciles registry versions, tags, releases, and exact source identity.
- It compares runtime, peer, feature/extra, export/entry-point, and dependency-graph metadata.
- It searches code and non-code integration surfaces and reports measurable coverage.
- Every material upstream claim has a primary-source citation; inferences are labeled.
- Every identified risk maps to a repository-specific verification step.
- Confidence is multidimensional and all important unknowns are explicit.
- Large repositories use grouping and stratified coverage instead of an arbitrary stop.
- It writes an assessment and performs no upgrade unless separately and explicitly authorized.
