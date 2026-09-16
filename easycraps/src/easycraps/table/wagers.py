"""Bet-placement methods — one per named bet, all wrapping `Table.bet()`.

Mixed into `Table` (see `core.py`); every method here assumes `self` has
the `.trigger()` method `Table` provides. See ../../docs/RULES.md for what
each of these bets pays and how it resolves.
"""
from __future__ import annotations

from .. import constants as C
from .result import ActionResult


class WagerMixin:
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
