"""easycraps — the Easy Craps game engine as a plain Python library.

    import easycraps

    table = easycraps.Table(credit=200)
    table.pass_line_bet(5)
    table.field_bet(10)
    result = table.roll()
    print(table.credit, table.point, result.message)

See the top-level rl/GETTING_STARTED.md for a full walkthrough, and
easy-craps/docs/RULES.md for what every bet actually pays and how a round
resolves. `Table` (this module) is the recommended interface; `Game` is the
lower-level named-trigger dispatcher it's built on, also used directly by
the web UI's HTTP API — both are exported here in case you want the raw
trigger interface instead of named methods.
"""
from . import constants
from .engine import Game, GameState, RollResult, TriggerError
from .table import ActionResult, Table

__all__ = [
    "Table",
    "ActionResult",
    "Game",
    "GameState",
    "RollResult",
    "TriggerError",
    "constants",
]
