"""The friendly, Pythonic surface of the library.

`Game.apply("place_bet", {"spot": "field", "amount": 10})` is how the engine
works internally (and how the web UI talks to it over HTTP), but it's not a
pleasant way to write an agent. `Table` wraps a `Game` and gives every bet
and action its own named method, so an agent reads like:

    import easycraps

    table = easycraps.Table(credit=200)
    table.pass_line_bet(5)
    table.field_bet(10)
    result = table.roll()
    print(table.credit, table.point, result.message)

Every method returns the same `RollResult`/dict-ish info the underlying
trigger produced, and raises `TriggerError` for programmer errors (bad spot
name, negative amount, unknown trigger) exactly like `Game.apply()` does.
Rejected-but-valid actions (not enough credit, rolling before the minimum
bet is met, etc.) don't raise — they come back with `.ok is False` and a
human-readable `.message`, same as a player would see on screen.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from . import constants as C
from .engine import Game, TriggerError

__all__ = ["Table", "ActionResult", "TriggerError"]


@dataclass(frozen=True)
class ActionResult:
    """What every Table method returns."""

    ok: bool
    message: str
    state: dict[str, Any]

    def __bool__(self) -> bool:
        return self.ok


class Table:
    """One Easy Craps table/session, with one named method per button."""

    def __init__(self, credit: float = 0.0, rng: random.Random | None = None, seed: int | None = None):
        if seed is not None:
            rng = random.Random(seed)
        self._game = Game(rng=rng)
        if credit:
            self._game.apply("add_funds", {"amount": credit})

    # ------------------------------------------------------------ raw escape hatch
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

    # ------------------------------------------------------------------ table controls
    def add_funds(self, amount: float) -> ActionResult:
        return self.trigger("add_funds", amount=amount)

    def cashout(self) -> ActionResult:
        return self.trigger("cashout")

    def set_min_bet(self, amount: float) -> ActionResult:
        return self.trigger("set_min_bet", amount=amount)

    def reset(self, keep_credit: float = 0.0) -> ActionResult:
        return self.trigger("reset", keep_credit=keep_credit)

    # ------------------------------------------------------------------ bet placement
    def bet(self, spot: str, amount: float) -> ActionResult:
        """Place `amount` on any raw bet-spot key (see docs/RULES.md)."""
        return self.trigger("place_bet", spot=spot, amount=amount)

    def pass_line_bet(self, amount: float) -> ActionResult:
        return self.bet("pass", amount)

    def field_bet(self, amount: float) -> ActionResult:
        return self.bet("field", amount)

    def low_field_bet(self, amount: float) -> ActionResult:
        return self.bet("lowfield", amount)

    def high_field_bet(self, amount: float) -> ActionResult:
        return self.bet("highfield", amount)

    def place_number_bet(self, number: int, amount: float) -> ActionResult:
        """Place bet on `number` (one of docs/RULES.md's point numbers: 2,3,4,5,6,8,9,10,11,12)."""
        return self.bet(f"place_{number}", amount)

    def hard_way_bet(self, number: int, amount: float) -> ActionResult:
        """Hard way bet on `number` (4, 6, 8, or 10)."""
        return self.bet(f"hard_{number}", amount)

    def craps_bet(self, amount: float) -> ActionResult:
        """"C" — wins on 2, 3, or 12."""
        return self.bet("c", amount)

    def eleven_bet(self, amount: float) -> ActionResult:
        """"E" — wins on 11."""
        return self.bet("e", amount)

    def craps_eleven_bet(self, amount: float) -> ActionResult:
        """"C&E" — half on craps, half on eleven."""
        return self.bet("ce", amount)

    def any_craps_bet(self, amount: float) -> ActionResult:
        return self.bet("anycraps", amount)

    def seven_bet(self, amount: float) -> ActionResult:
        """Any-seven, one roll."""
        return self.bet("seven", amount)

    def horn_number_bet(self, number: int, amount: float) -> ActionResult:
        """Single horn number (2, 3, 11, or 12)."""
        return self.bet(f"horn_{number}", amount)

    def horn_bet(self, amount: float) -> ActionResult:
        """The combined horn bet (wins flat on any of 2, 3, 11, 12)."""
        return self.bet("horn", amount)

    def hop_bet(self, d1: int, d2: int, amount: float) -> ActionResult:
        """Exact-combo bet on the next roll, e.g. hop_bet(4, 3, 1)."""
        return self.bet(C.hop_key(d1, d2), amount)

    def lucky_low_bet(self, amount: float) -> ActionResult:
        """Lucky Roller: every of 2,3,4,5,6 before a 7."""
        return self.bet("lowrolls", amount)

    def lucky_high_bet(self, amount: float) -> ActionResult:
        """Lucky Roller: every of 8,9,10,11,12 before a 7."""
        return self.bet("highrolls", amount)

    def lucky_all_bet(self, amount: float) -> ActionResult:
        """Lucky Roller: every non-7 total before a 7 ("Roll'Em All")."""
        return self.bet("rollemall", amount)

    # ------------------------------------------------------------------ bet management
    def clear_last_bet(self) -> ActionResult:
        return self.trigger("clear_last_bet")

    def clear_all_bets(self) -> ActionResult:
        return self.trigger("clear_all_bets")

    def double_bet(self) -> ActionResult:
        return self.trigger("double_bet")

    def repeat_last_bet(self) -> ActionResult:
        return self.trigger("repeat_last_bet")

    def toggle_set_bets(self) -> ActionResult:
        return self.trigger("toggle_set_bets")

    def press(self, spot: str | None = None) -> ActionResult:
        """Re-bet the current stake onto `spot` (defaults to the Point's Place bet)."""
        return self.trigger("press", spot=spot)

    def across(self, amount: float) -> ActionResult:
        """One unit of `amount` on every point number except the current Point."""
        return self.trigger("across", amount=amount)

    def toggle_puck(self) -> ActionResult:
        return self.trigger("toggle_puck")

    # ------------------------------------------------------------------ the roll
    def roll(self, d1: int | None = None, d2: int | None = None) -> ActionResult:
        """Resolve a roll. Omit d1/d2 for random dice, or pass them for
        deterministic/replayable rolls (handy for tests and evals)."""
        payload: dict[str, Any] = {}
        if d1 is not None:
            payload["d1"] = d1
        if d2 is not None:
            payload["d2"] = d2
        return self.trigger("roll", **payload)
