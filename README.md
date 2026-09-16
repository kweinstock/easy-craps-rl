# Easy Craps RL

A single-player "Easy Craps" cabinet, plus a plain Python library so RL
agents can play it — split so there's one shared source of truth for the
rules instead of one implementation for the UI and a second for training.
See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full breakdown
of why it's split this way.

Originally the whole cabinet was a single static HTML file
([assets/easy-craps-display.html](assets/easy-craps-display.html), kept for
reference). It's been split up so that:

- one plain Python library (`easycraps`) implements every rule as a named
  **trigger**, callable directly by a Python agent or wrapped by friendly
  methods like `table.field_bet(10)`,
- the same triggers are exposed over HTTP/WebSocket so any language (or an
  out-of-process agent) can drive a table too, and
- the UI is a thin renderer over engine state, not where the rules live.

## Layout

```
easy-craps-rl/
  docs/
    RULES.md             The rulebook — read this first.
    ARCHITECTURE.md       Why it's split this way.
  easycraps/              Python: the game engine as an installable library.
    src/easycraps/        Game, Table (the friendly API), constants. No I/O, no deps.
    tests/
  cabinet/                The live, playable table.
    run.py                Runs backend + frontend together, prints the URL.
    backend/              FastAPI HTTP + WebSocket server over easycraps.
      app/api/
      tests/
    frontend/              React + TypeScript (Vite) cabinet UI.
      src/components/      One file per button/betting area.
      src/pages/           GamePage (the table) and RulesPage (help -> rulebook).
      src/hooks/useGame.ts WebSocket session hook every component reads from.
  assets/                 Original static prototype + art, kept for reference.
  rl/                     RL agents (one subfolder per person) built on easycraps.
```

## Running the cabinet

```bash
pip install -r cabinet/backend/requirements.txt   # also installs easycraps (editable)
npm install --prefix cabinet/frontend

cd cabinet
python run.py
```

`run.py` starts the backend (`http://localhost:8000`) and the frontend dev
server together and prints the frontend URL once it's ready. Ctrl+C stops
both. (To run them in separate terminals instead, see
[`cabinet/README.md`](cabinet/README.md).)

Open the printed URL. The HELP button opens `/rules`, which renders
[docs/RULES.md](docs/RULES.md) straight from the backend.

## Playing with a Python agent

```python
import easycraps

table = easycraps.Table(credit=200)
table.pass_line_bet(5)
result = table.roll()
print(result.message, table.credit, table.point)
```

See [`rl/GETTING_STARTED.md`](rl/GETTING_STARTED.md) for a walkthrough,
[`easycraps/docs/api.html`](easycraps/docs/api.html) for the exhaustive API
reference (every class, method, and constant), and
[`docs/RULES.md`](docs/RULES.md) for the payouts those methods resolve.
A non-Python agent (or one that must run out-of-process)
drives the exact same triggers over HTTP instead — `POST /sessions`, then
`POST /sessions/{id}/trigger` against the cabinet backend — see
[`cabinet/backend/README.md`](cabinet/backend/README.md).
