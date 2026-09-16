"""Table — the friendly, Pythonic surface of the library.

`Game.apply("place_bet", {"spot": "field", "amount": 10})` is how the engine
works internally (and how the web UI talks to it over HTTP), but it's not a
pleasant way to write an agent. `Table` wraps a `Game` and gives every bet
and action its own named method (see `wagers.py` and `controls.py`), so an
agent reads like:

    import easycraps

    table = easycraps.Table(credit=200)
    table.pass_line_bet(5)
    table.field_bet(10)
    result = table.roll()
    print(table.credit, table.point, result.message)

Every method returns the same `ActionResult` info the underlying trigger
produced, and raises `TriggerError` for programmer errors (bad spot name,
negative amount, unknown trigger) exactly like `Game.apply()` does.
Rejected-but-valid actions (not enough credit, rolling before the minimum
bet is met, etc.) don't raise — they come back with `.ok is False` and a
human-readable `.message`, same as a player would see on screen.
"""
from __future__ import annotations

import random
from typing import Any

from ..engine import Game
from .controls import ControlsMixin
from .result import ActionResult
from .wagers import WagerMixin


class Table(WagerMixin, ControlsMixin):
    """One Easy Craps table/session, with one named method per button."""

    def __init__(self, credit: float = 0.0, rng: random.Random | None = None, seed: int | None = None):
        if seed is not None:
            rng = random.Random(seed)
        self._game = Game(rng=rng)
        if credit:
            self._game.apply("add_funds", {"amount": credit})

    def trigger(self, name: str, **payload: Any) -> ActionResult:
        """Fire any trigger by name — the same power-user path the HTTP API uses."""
        result = self._game.apply(name, payload)
        return ActionResult(**result)

    # ------------------------------------------------------------------- state
    @property
    def state(self) -> dict[str, Any]:
        """Full JSON-serializable snapshot, same shape as the HTTP API returns."""
        return self._game.state.to_dict()

    @property
    def credit(self) -> float:
        return self._game.state.credit

    @property
    def bets(self) -> dict[str, float]:
        return dict(self._game.state.bets)

    @property
    def total_bet(self) -> float:
        return self._game.state.total_bets()

    @property
    def point(self) -> int | None:
        return self._game.state.point

    @property
    def min_bet(self) -> float:
        return self._game.state.min_bet

    @property
    def message(self) -> str:
        return self._game.state.message

    @property
    def history(self) -> list[tuple[int, int]]:
        return list(self._game.state.history)

    @property
    def last_roll(self):
        return self._game.state.last_roll
