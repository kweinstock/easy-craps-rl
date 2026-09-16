# Architecture

## The problem this is solving

The project started as one HTML file where the rules, the rendering, and
the button-click handling were all tangled together in a single
`<script>` block (still kept at
[`../assets/easy-craps-display.html`](../assets/easy-craps-display.html)
for reference). That's fine for a static display, but it doesn't work once
you want RL agents to play the same game:

- An agent can't "click a div" — it needs a programmatic way to act.
- If the rules get reimplemented a second time for the agent, the two
  implementations **will** drift: a payout gets fixed in one place and not
  the other, and a policy trained against one version plays worse (or
  exploits a bug) against the other.

So the whole design follows one rule: **there is exactly one place where
game logic lives, and everything else is a thin adapter around it.**

## The layers

```
easycraps/                    the rules, once
    │
    ├── used directly by ──►  rl/*                (Python agents, in-process)
    │
    └── wrapped by ────────►  cabinet/backend      (FastAPI HTTP/WebSocket)
                                    │
                                    ├── used by ──► cabinet/frontend  (React UI)
                                    └── used by ──► non-Python / out-of-process agents (HTTP)
```

### 1. `easycraps/` — the engine, as a library, not an app

[`easycraps/src/easycraps/engine/`](../easycraps/src/easycraps/engine)
holds a `Game` class with **zero I/O** — no HTTP, no sockets, no printing.
It tracks a `GameState` (credit, bets, point, hard-way counters, Lucky
Roller progress, history) and exposes exactly one entry point:

```python
game.apply("place_bet", {"spot": "field", "amount": 10})
```

**Why a named "trigger" instead of just mutating state directly** (e.g.
`game.bets["field"] += 10`)? Because a trigger is a verb with validation
and resolution attached — the same unit of action a button click or a
network request naturally is. `apply()` always returns the same shape
(`{ok, message, state}`). That means the UI's "Field" spot's `onClick`, an
HTTP `POST /trigger`, and a Python agent's `table.field_bet(10)` are all,
underneath, the exact same function call. There's no second code path to
fall out of sync with the first.

Payout tables and which numbers are points live in
[`constants/`](../easycraps/src/easycraps/constants), separate from the
resolution logic in `engine/resolution.py`'s `resolve_roll()` — so the
*data* (what [`RULES.md`](RULES.md) documents) isn't interleaved with the
*mechanics* (iterate bets, settle, mutate credit). Both `constants` and
`engine` are themselves small subpackages (one file per bet category, one
file per concern) rather than single monolithic modules — see
[`easycraps/README.md`](../easycraps/README.md#folder-structure) for the
full breakdown, or [`easycraps/docs/api.html`](../easycraps/docs/api.html)
for the exhaustive method-by-method reference.

[`table/`](../easycraps/src/easycraps/table) (`Table`) sits on top of
`Game` purely for ergonomics — `table.field_bet(10)` instead of
`game.apply("place_bet", {"spot": "field", "amount": 10})`. It adds **no**
new behavior; every method is a one-line call into `Game.apply()`. That
distinction matters: `Game` is the contract every consumer relies on,
`Table` is just a friendlier name for the same triggers, safe to extend
with more convenience methods without ever becoming a second place a rule
could be implemented differently.

This is a plain `pip install -e .` package with no dependency on a web
framework or a specific RL library. In particular, it does **not** depend
on Gymnasium: there's no fixed observation vector or Discrete action space
forced on any agent. Pick whatever state representation and action framing
your algorithm wants (`table.state` and the individual properties are the
raw material), and build any Gym-style wrapper you personally need on top,
in your own `rl/<name>/` folder — the library itself stays unopinionated.

### 2. `cabinet/backend/` — the network adapter, not a second engine

[`cabinet/backend/app/api/main.py`](../cabinet/backend/app/api/main.py) is
FastAPI wrapping `easycraps.Game` in HTTP/WebSocket sessions
(`POST /sessions`, `POST /sessions/{id}/trigger`,
`WS /sessions/{id}/ws`). It does session bookkeeping (a dict of `Game`
instances) and nothing else — no rules logic lives here. This layer exists
for two reasons:

- The **frontend** needs live, shared, network-reachable game state — a
  browser can't `import easycraps` itself, and a WebSocket lets the server
  push resolved-roll state back after `roll` instead of the UI guessing.
- A **non-Python agent**, or one that must run out-of-process (a different
  machine, a different language), can't `pip install` a Python library,
  but it can speak HTTP. It fires the identical trigger names/payloads
  `Table` uses.

It also serves `/rules` — reading `docs/RULES.md` off disk and handing it
to the frontend — so the rulebook has one copy, not one embedded in the UI
and one duplicated in the API.

### 3. `cabinet/frontend/` — a thin renderer, deliberately dumb

Every component (`PointsRow`, `FieldBlock`, `Hardways`, …) reads server
state and calls `fire(trigger, payload)` over the WebSocket; none of them
compute payouts or decide win/loss. `BetSpot` is the one generic building
block every clickable betting area wraps, so adding a new bet spot means
"give it a key," not "write new click logic." If the UI ever computed
anything about whether a bet won, it would be a second rules
implementation — exactly what this whole structure exists to avoid.

### 4. `cabinet/run.py` — one command for local dev

Starts the backend and frontend dev servers together, streams both logs,
and prints the frontend URL once it's ready. It's a dev convenience, not
an architectural layer — the two processes are still fully independent
(you can run them separately; see
[`../cabinet/README.md`](../cabinet/README.md)).

### 5. `rl/` — where the drift-free property pays off

[`rl/GETTING_STARTED.md`](../rl/GETTING_STARTED.md) is documentation, not
code — there's no adapter layer here by design. Agents `pip install -e
../easycraps` and call `Table` methods directly, in-process, at full
Python speed. Each person works in their own `rl/<name>/` subfolder and
picks whatever framing suits their algorithm (tabular Q-learning, a custom
Gym wrapper, a bandit, whatever) without the library imposing a shape on
them.

## Why this specific split (not one monolith, or the engine inside the backend)

- **Engine separate from backend** — so "play the game" (a script, a
  notebook, a training loop) doesn't require standing up a web server, and
  so the rules can be tested/versioned/installed independently of the
  API's own concerns (sessions, CORS, whatever comes later).
- **Backend separate from frontend** — so the rules are reachable from
  *any* client, browser or otherwise, over one protocol, rather than the
  browser being the only thing that can play.
- **`Table` separate from `Game`** — so the "nice API for humans/agents"
  layer can grow without ever becoming a second place a rule could be
  implemented differently than `Game` does.
- **`cabinet/` grouping backend + frontend** — they're always deployed and
  run together as "the live table," so they get their own folder (and
  `run.py`) instead of sitting as loose siblings next to the library and
  the docs.

The net effect: there is one function, `Game.apply()`, and every
consumer — a button click, a WebSocket message, an HTTP POST, or
`table.field_bet(10)` in a training loop — eventually calls it with the
same trigger name and payload. A bug fix or rule change happens in exactly
one place (`engine/resolution.py` or the relevant `constants/` file) and
is instantly correct everywhere else.
