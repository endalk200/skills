# Effect Atom

Use this when building reactive frontend state with `@effect-atom/atom` or a framework adapter such as `@effect-atom/atom-react`.

Effect Atom is versioned independently from Effect. Check the project-pinned package before using APIs that are absent from these core patterns. This reference owns Atom-specific composition; read `SERVICES_LAYERS.md`, `STREAMS.md`, and `SCHEMA.md` for the underlying Effect concerns.

## State And Hooks

Define shared atoms at module scope so their identity is stable. Keep transient form and component-only state local to the component.

```tsx
import { Atom, useAtomSet, useAtomValue } from "@effect-atom/atom-react"

const countAtom = Atom.make(0)
const doubledAtom = Atom.make((get) => get(countAtom) * 2)

function Count() {
  const count = useAtomValue(countAtom)
  const setCount = useAtomSet(countAtom)
  return <button onClick={() => setCount((n) => n + 1)}>{count}</button>
}
```

Hook chooser:

- Read only: `useAtomValue(atom)`.
- Write or dispatch only: `useAtomSet(atom)`.
- Read and write/dispatch: `useAtom(atom)`.

`get(atom)` records a dependency. A derived atom reruns only when one of the atoms it read changes.

## Lifecycle

Atoms are lazy and automatically dispose when unused. Components reading the same atom reference share its state and effect; `Atom.family` provides that stable identity per key.

- Reset and release resources after the last subscriber unmounts: keep the default.
- Retain an unused atom briefly: `atom.pipe(Atom.setIdleTTL(duration))`.
- Retain shared state for the application lifetime: `atom.pipe(Atom.keepAlive)`.
- Mount a resource-owning atom without reading its value: `useAtomMount(atom)`.
- Refresh from an explicit UI event: `useAtomRefresh(atom)`.
- Refresh when the page regains focus: `atom.pipe(Atom.refreshOnWindowFocus)`.

An Effect returned by an atom runs in the atom's scope. Acquire resources with `Effect.acquireRelease`; releasing the final mount runs their finalizers.

Endpoint results have no implicit freshness policy. Choose retention and refresh triggers from the endpoint's semantics.

## Effectful Atoms And Result

Returning an `Effect` from `Atom.make` produces an atom of `Result.Result`. Read reactive inputs before the asynchronous work so a change interrupts/rebuilds the computation with the new input.

```ts
import { Effect } from "effect"

const userIdAtom = Atom.make("user-1")

const userAtom = Atom.make((get) =>
  Effect.gen(function* () {
    const userId = get(userIdAtom)
    return yield* loadUser(userId)
  })
)
```

Render every `Result` state. Use `Result.builder` to exhaustively distinguish expected tagged errors from defects. A successful result can have `waiting: true` while a dependency-triggered refresh is running, allowing stale-while-refresh UI.

```tsx
import { Result, useAtomValue } from "@effect-atom/atom-react"

function User() {
  const result = useAtomValue(userAtom)

  return Result.builder(result)
    .onInitial(() => <p>Loading…</p>)
    .onErrorTag("UserNotFound", ({ id }) => <p>User {id} was not found.</p>)
    .onDefect(() => <p>Unexpected failure.</p>)
    .onSuccess((user, { waiting }) => (
      <article aria-busy={waiting} style={{ opacity: waiting ? 0.6 : 1 }}>
        {user.name}
      </article>
    ))
    .render()
}
```

Compose effectful atoms with `get.result`. It unwraps success into the Effect channel and propagates failure.

```ts
const profileAtom = Atom.make((get) =>
  Effect.gen(function* () {
    const user = yield* get.result(userAtom, { suspendOnWaiting: true })
    const permissions = yield* get.result(permissionsAtom, {
      suspendOnWaiting: true,
    })
    return { user, permissions }
  })
)
```

Use `suspendOnWaiting: true` when the derived value requires fresh dependencies. Use `false` only when continuing from the current successful value during refresh is semantically valid.

## Actions

Use `Atom.fn` for explicit operations rather than encoding a command as a writable value atom. Use `runtime.fn` when the operation requires services.

```ts
const refreshUsersAtom = Atom.fn(
  Effect.fn("Users.refresh")(function* () {
    yield* refreshUsers()
  })
)

function RefreshButton() {
  const refresh = useAtomSet(refreshUsersAtom)
  return <button onClick={() => refresh()}>Refresh</button>
}
```

Use `useAtom(actionAtom)` when the UI also renders the action `Result` or disables controls from its `waiting` state. Use promise mode when the event handler needs the exact `Exit`.

```ts
const save = useAtomSet(saveUserAtom, { mode: "promiseExit" })
const exit = await save(input)
```

## Endpoint-Backed UI, Families, And Reactivity

Keep transport, status handling, and response decoding in an Effect service adapter. Create one runtime from its application layer, then expose endpoint reads with `runtime.atom` and writes with `runtime.fn`; the UI receives typed domain values and errors rather than raw responses.

```ts
const appRuntime = Atom.runtime(UserRepo.layer)

const usersAtom = appRuntime.atom(
  Effect.gen(function* () {
    const repo = yield* UserRepo.Service
    return yield* repo.list()
  })
).pipe(Atom.withReactivity(["users"]))

const saveUserAtom = appRuntime.fn(
  Effect.fn("User.save")(function* (input: UserInput) {
    const repo = yield* UserRepo.Service
    return yield* repo.save(input)
  }),
  { reactivityKeys: ["users"] }
)
```

Use `Atom.family` for parameterized query or action atoms. It returns the stable atom identity for a key instead of allocating a new atom during render. A family of action atoms gives each key an independent action `Result`, including `waiting` and failure state.

Connect reads and mutations with matching reactivity keys. Prefer the narrowest stable key that represents the data changed; use a collection key when a mutation can change membership.

```ts
const userAtom = Atom.family((id: UserId) =>
  appRuntime.atom(
    Effect.gen(function* () {
      const repo = yield* UserRepo.Service
      return yield* repo.get(id)
    })
  ).pipe(Atom.withReactivity({ users: [id] }))
)

const toggleUserAtom = Atom.family((id: UserId) =>
  appRuntime.fn(
    Effect.fn("User.toggle")(function* () {
      const repo = yield* UserRepo.Service
      yield* repo.toggle(id)
    }),
    { reactivityKeys: { users: [id] } }
  )
)
```

When an API is modeled with Effect HTTP API or RPC, prefer `AtomHttpApi.query` / `AtomHttpApi.mutation` or `AtomRpc.query` / `AtomRpc.mutation`. They preserve `Result`, runtime, and reactivity integration without a hand-written atom wrapper.

Keep one authoritative cache for each endpoint. When another data layer already owns freshness and retention, run the Effect client inside that owner instead of mirroring the same server state in an independent atom cache.

## Optimistic Mutations

Build optimistic state from the authoritative query atom. Keep the reducer pure and derive the next state from its `current` argument so overlapping mutations compose correctly.

```ts
const optimisticUsersAtom = Atom.optimistic(usersAtom)

const renameUserAtom = Atom.optimisticFn(optimisticUsersAtom, {
  reducer: (current, input: { id: UserId; name: string }) =>
    Result.map(current, (users) =>
      users.map((user) =>
        user.id === input.id ? { ...user, name: input.name } : user
      )
    ),
  fn: appRuntime.fn(
    Effect.fn("User.rename")(function* (input: {
      id: UserId
      name: string
    }) {
      const repo = yield* UserRepo.Service
      yield* repo.rename(input)
    })
  ),
})
```

`Atom.optimisticFn` applies the reducer immediately and reconciles with the mutation result. Keep the confirmed query as the source of truth and surface mutation failures instead of adding a second manual rollback state.

## Streams

Choose the atom shape from the UI consumption pattern:

- Latest emitted value: `Atom.make(stream)`.
- Progressive accumulated result: `Atom.fn` returning `Stream.scan(...)`.
- Explicit chunked “load more”: `Atom.pull(stream.pipe(Stream.rechunk(size)))`.
- Chunked streams requiring runtime services: `runtime.pull(stream)`.
- Polling: `Atom.make(Stream.fromEffect(query).pipe(Stream.repeat(schedule)))`.
- Custom multi-atom reducer semantics: an action atom using `get.set(...)`.

```ts
const searchAtom = Atom.fn((query: string) =>
  searchStream(query).pipe(
    Stream.scan([] as ReadonlyArray<SearchResult>, (results, item) => [
      ...results,
      item,
    ])
  )
)

const pageAtom = Atom.pull(
  searchStream("effect").pipe(Stream.rechunk(20))
)

const servicePageAtom = appRuntime.pull(serviceBackedPageStream)
```

`Atom.pull` accumulates emitted chunks. Its setter pulls the next chunk, and its successful value exposes `items` plus `done`; disable or remove “load more” when `done` is true.

Keep stream acquisition, interruption, error policy, and backpressure in the stream itself. Model ordinary polling as one scheduled stream so refresh or unmount interrupts and rebuilds a single producer. Use the atom to expose its reactive lifecycle to the UI.
