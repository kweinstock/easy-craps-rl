# Easy Craps — Backend

FastAPI HTTP/WebSocket API over the `easycraps` game engine. This is the
network-facing layer: it powers the React frontend, and it's how any
non-Python (or out-of-process) agent plays the table. A Python agent
running in-process should instead use the `easycraps` library directly —
see [`../../easycraps`](../../easycraps) and
[`../../rl/GETTING_STARTED.md`](../../rl/GETTING_STARTED.md). Both paths
dispatch through the exact same named triggers, so a script using `Table`
and a browser tab hitting this API play by identical rules.

To run this alongside the frontend with one command, use
[`../run.py`](../run.py) instead of the steps below.

## Install

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate   # or `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt   # installs easycraps (editable, from ../../easycraps) + FastAPI
```

## Run the API (used by the React frontend, or any HTTP-capable agent)

```bash
uvicorn app.api.main:app --reload --port 8000
```

## Run tests

```bash
pytest
```

## Trigger reference

Every trigger is fired as `POST /sessions/{id}/trigger` with body
`{"trigger": "<name>", "payload": {...}}`, or the equivalent JSON message
over `WS /sessions/{id}/ws`. Full rules for what each trigger resolves are
in [../../docs/RULES.md](../../docs/RULES.md); the same names map 1:1 to
`easycraps.Table` methods (e.g. `place_bet` + `spot="field"` ==
`table.field_bet(amount)`).

| Trigger | Payload | Notes |
|---|---|---|
| `add_funds` | `{amount}` | Deposit credit. |
| `place_bet` | `{spot, amount}` | `spot` is one of the bet keys below. |
| `clear_last_bet` | `{}` | Undo the most recent `place_bet` this turn. |
| `clear_all_bets` | `{}` | Return every active bet's stake to credit. |
| `double_bet` | `{}` | Double every active bet. |
| `repeat_last_bet` | `{}` | Re-place last round's bets. |
| `toggle_set_bets` | `{}` | Toggle whether Place/Hard Way bets work next roll. |
| `press` | `{spot?}` | Re-bet current stake onto `spot` (defaults to the Point's Place bet). |
| `across` | `{amount}` | One unit of `amount` on every point number but the Point. |
| `toggle_puck` | `{}` | Cosmetic manual OFF, only with no Point established. |
| `cashout` | `{}` | Zero out credit (must have no bets active). |
| `set_min_bet` | `{amount}` | Table-config only; not a player action. |
| `roll` | `{d1?, d2?}` | Resolves the roll. Omit `d1`/`d2` for random dice, or pass them for deterministic tests/replays. |
| `reset` | `{keep_credit?}` | Starts a fresh session, optionally keeping some credit. |

### Bet spot keys

`pass`, `field`, `lowfield`, `highfield`, `c`, `e`, `ce`, `anycraps`,
`seven`, `horn`, `place_<2|3|4|5|6|8|9|10|11|12>`, `hard_<4|6|8|10>`,
`horn_<2|3|11|12>`, `hop_<two digits, e.g. hop_16>`, `lowrolls`,
`rollemall`, `highrolls`.
