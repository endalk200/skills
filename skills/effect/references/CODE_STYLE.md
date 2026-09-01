# Code Style And Control Flow

This reference owns ordinary Effect composition and branching. Match the project's established style first, then use these defaults when the codebase has no stronger convention.

## Application Boundary

- Run a long-lived application with the platform runtime entrypoint: `NodeRuntime.runMain`, `BunRuntime.runMain`, or `BrowserRuntime.runMain`.
- Put resource acquisition, finalizers, and application teardown inside the main Effect. The platform runtime can then interrupt the application fiber and release scoped resources on shutdown.
- Reserve `Effect.runPromise` and `Effect.runSync` for tests, short scripts, REPL-style use, or embedding where another host owns lifecycle and shutdown.

## Explicit Calls And Dual APIs

Write callbacks explicitly instead of passing functions tacitly:

```ts
effect.pipe(Effect.map((value) => normalize(value)))
```

This preserves inference when the callback has optional parameters or overloads and keeps stack traces legible. Apply the same rule to `flow`: define an explicit named or arrow function when it is passed as behavior.

For a dual API, choose the form that makes the local expression easiest to read:

- Use data-last inside a pipeline: `effect.pipe(Effect.map((value) => f(value)))`.
- Use data-first for one direct operation: `Effect.map(effect, (value) => f(value))`.
- Follow the surrounding module when both forms are equally clear. Do not rewrite between equivalent forms without a readability or inference reason.

## Sequencing Without Nesting

- Use a shallow `pipe` for a linear chain of transformations over one value.
- Use `Effect.gen` when later steps depend on earlier results, or when the workflow contains local `if`, loops, early failure, or several named intermediate values.
- Use `Effect.Do` with `Effect.bind` for effectful fields and `Effect.let` for derived plain fields when the accumulated record is itself the useful shape. Prefer `Effect.gen` when do notation only adds record plumbing.
- Extract a named Effect operation when a generator or pipeline still hides a distinct domain step.

`Effect.gen` is linear syntax, not eager execution: yielded failures, service requirements, interruption, and finalization remain in the Effect model.

## Branching And Pattern Matching

Use ordinary `if` for a simple boolean branch, including inside `Effect.gen` or an Effect-returning function. Represent an expected invalid outcome deliberately as `Option` or a typed failure rather than throwing.

Use `Effect.when(effect, conditionEffect)` when the condition is itself an Effect and skipping the operation should be represented as `Option.none`. A failed condition remains a typed failure; a false condition skips the source effect.

Use `Match` when structural conditions or a closed union benefit from declarative, type-narrowed, exhaustive handling:

- `Match.type<T>()` builds a reusable matcher function; `Match.value(value)` matches one value immediately.
- Add cases with `Match.when`, `Match.not`, `Match.tag`, literal/object patterns, or built-in predicates such as `Match.string` and `Match.number`.
- Finish a closed union with `Match.exhaustive` by default.
- Use `Match.orElse` for a real fallback, `Match.option` when no match is expected absence, and `Match.result` when the unmatched input must remain available as failure data.
- Put `Match.withReturnType<T>()` first in the pipeline; later placement does not enforce every branch correctly.
- `Match.tag` requires the Effect `_tag` convention. For `Data.TaggedEnum` and `Schema.TaggedUnion`, prefer their owned exhaustive matchers described in `SCHEMA.md`.

## Combining And Traversing Effects

- Use `Effect.zip` for two results kept as a tuple and `Effect.zipWith` when the two results are immediately combined.
- Use `Effect.all` for a known tuple, iterable, struct, or record of Effects; the success value preserves that input shape.
- Use `Effect.forEach` to apply one effectful operation across an iterable. Collected results preserve input order.
- These operators are sequential by default. Enable concurrency only when operations are independent, ordering of execution is irrelevant, and the downstream system permits it. Use `{ concurrent: true }` for `zip` / `zipWith` and an explicit bounded `{ concurrency }` for `all` / `forEach`.
- Default collection behavior short-circuits on typed failure. Use `Effect.all(..., { mode: "result" })` when every typed outcome must be collected as `Result` instead.
- Set `{ discard: true }` when only execution matters; avoid allocating a result collection that will immediately be ignored.

## Loops

- Use a native `for` or `while` inside `Effect.gen` when the workflow needs local state, `break`, `continue`, or collected values.
- Use `Effect.forEach` for iterable traversal and `Schedule` with `Effect.repeat` for time-based repetition.
- Use `Effect.whileLoop` for a tight effectful loop whose condition and step live outside generator control flow. Inspect the pinned signature before use.

Pinned-source guard: in `effect@4.0.0-beta.102`, `Effect.whileLoop` accepts `{ while: () => boolean, body: () => Effect<A, E, R>, step: (value: A) => void }` and returns `Effect<void, E, R>`. The current code-style page's prose showing an `initial` argument and collected array does not match that source or current Effect `main`; do not copy that form.
