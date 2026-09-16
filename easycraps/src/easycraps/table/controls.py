"""Table controls, bet management, and the roll itself.

Mixed into `Table` (see `core.py`); every method here assumes `self` has
the `.trigger()` method `Table` provides.
"""
from __future__ import annotations

from typing import Any

from .result import ActionResult


class ControlsMixin:
    # ------------------------------------------------------------- bankroll
    def add_funds(self, amount: float) -> ActionResult:
        return self.trigger("add_funds", amount=amount)

    def cashout(self) -> ActionResult:
        return self.trigger("cashout")

    def set_min_bet(self, amount: float) -> ActionResult:
        return self.trigger("set_min_bet", amount=amount)

    def reset(self, keep_credit: float = 0.0) -> ActionResult:
        return self.trigger("reset", keep_credit=keep_credit)

    # -------------------------------------------------------- bet management
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

    # ------------------------------------------------------------- the roll
    def roll(self, d1: int | None = None, d2: int | None = None) -> ActionResult:
        """Resolve a roll. Omit d1/d2 for random dice, or pass them for
        deterministic/replayable rolls (handy for tests and evals)."""
        payload: dict[str, Any] = {}
        if d1 is not None:
            payload["d1"] = d1
        if d2 is not None:
            payload["d2"] = d2
        return self.trigger("roll", **payload)
