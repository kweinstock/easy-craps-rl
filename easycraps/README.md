# easycraps

The Easy Craps game engine as a plain, dependency-free Python library — no
Gym/Gymnasium, no HTTP required. Built so an RL agent (or a human script)
can play by calling methods, not by driving a UI:

```python
import easycraps

table = easycraps.Table(credit=200)
table.pass_line_bet(5)
table.field_bet(10)

result = table.roll()
print(result.ok, result.message)
print(table.credit, table.point, table.bets)
```

**For the full API reference — every class, every method, every
constant — open [`docs/api.html`](docs/api.html) in a browser.** This
README is just the orientation; that page is exhaustive.

Install it in editable mode from this directory:

```bash
pip install -e .
```

See [`../rl/GETTING_STARTED.md`](../rl/GETTING_STARTED.md) for a full
walkthrough and [`../docs/RULES.md`](../docs/RULES.md) for the rules every
method resolves against. This same engine (`easycraps.Game`, the lower-level
class `Table` wraps) also backs the `backend` HTTP/WebSocket API
that drives the live web UI — so a `Table` in a script and a browser tab
pointed at the cabinet are playing by identical rules.

## Folder structure

```
easycraps/
  pyproject.toml
  README.md            This file.
  docs/
    api.html            Full API reference — open in a browser.
  src/easycraps/
    __init__.py          Public exports: Table, Game, ActionResult, GameState,
                          RollResult, TriggerError, constants.

    constants/            "What are the rules?" — pure data, no logic.
      __init__.py         Re-exports everything flat (C.POINT_NUMBERS still works).
      points.py           Point numbers, Place bet payouts.
      field.py             Field / C / E / Any Craps / Any Seven.
      hardways.py           Hard way combos + payouts.
      horn.py                Horn number bets + the combined Horn bet.
      hop.py                  Every two-die combination + hop_key()/hop_pay_for().
      lucky.py                 Lucky Roller (Low/High/Roll'Em All) needed-sets.
      settings.py               DEFAULT_MIN_BET.

    engine/               "How does a trigger/roll actually resolve?" — the
                          low-level, dependency-free simulator.
      __init__.py         Re-exports Game, GameState, RollResult, TriggerError.
      errors.py           TriggerError.
      state.py            GameState + RollResult dataclasses (+ to_dict()).
      game.py             Game: the named-trigger dispatcher (apply()).
      resolution.py         resolve_roll(): settles every bet against one roll.

    table/                "How do I use this without thinking about triggers?"
                          — the friendly Pythonic wrapper most code should use.
      __init__.py         Re-exports Table, ActionResult, TriggerError.
      result.py           ActionResult dataclass.
      core.py             Table: __init__, trigger(), state properties.
      wagers.py             WagerMixin: every *_bet() method.
      controls.py            ControlsMixin: add_funds, roll, press, across, ...

  tests/
    test_engine.py        Tests against the raw Game/trigger API.
    test_table.py          Tests against the friendly Table API.
```

Nothing outside this package needs to know about that internal split —
`import easycraps` and everything in the Quickstart above works the same
regardless of which submodule a name actually lives in. `constants`,
`engine`, and `table` are each their own subpackage purely to keep every
file short enough to read in one sitting; the public API (what's exported
from `easycraps/__init__.py`) hasn't changed shape because of it.

## Tests

```bash
pip install -e ".[dev]"
pytest
```
