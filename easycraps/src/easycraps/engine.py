"""Easy Craps game engine — the low-level trigger dispatcher.

Every player/dealer action is implemented as a named "trigger" dispatched
through `Game.apply()`. Most code should use the friendlier `Table` class in
`easycraps.table` instead; `Game` is the one integration point everything
else (the web UI's HTTP API, `Table`, any other language's agent talking
over HTTP) calls through, so behavior never drifts between "playing the
game" and "training on the game".
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Callable

from . import constants as C


class TriggerError(ValueError):
    """Raised when a trigger is called with an invalid name or payload."""


@dataclass
class RollResult:
    d1: int
    d2: int
    total: int
    winnings: float
    resolved: dict[str, float]  # bet key -> net credit change (win incl. stake, or 0)
    lost_keys: list[str]
    point_before: int | None
    point_after: int | None
    message: str


@dataclass
class GameState:
    credit: float = 0.0
    bets: dict[str, float] = field(default_factory=dict)
    last_bets: dict[str, float] = field(default_factory=dict)
    bet_log: list[tuple[str, float]] = field(default_factory=list)
    point: int | None = None
    min_bet: float = C.DEFAULT_MIN_BET
    set_bets_on: bool = True
    puck_manual_off: bool = False
    hard_since: dict[int, int] = field(default_factory=lambda: {4: 4, 6: 2, 8: 80, 10: 94})
    lucky_hits: dict[str, set[int]] = field(
        default_factory=lambda: {"lowrolls": set(), "rollemall": set(), "highrolls": set()}
    )
    history: list[tuple[int, int]] = field(default_factory=list)
    last_roll: RollResult | None = None
    message: str = "Place your Pass Line bet to start the come-out roll."
    rolling: bool = False

    def total_bets(self) -> float:
        return sum(self.bets.values())

    def to_dict(self) -> dict[str, Any]:
        return {
            "credit": round(self.credit, 2),
            "bets": {k: round(v, 2) for k, v in self.bets.items()},
            "total_bets": round(self.total_bets(), 2),
            "point": self.point,
            "min_bet": self.min_bet,
            "set_bets_on": self.set_bets_on,
            "puck_manual_off": self.puck_manual_off,
            "hard_since": dict(self.hard_since),
            "lucky_hits": {k: sorted(v) for k, v in self.lucky_hits.items()},
            "history": self.history[-20:],
            "bet_log_count": len(self.bet_log),
            "message": self.message,
            "last_roll": None
            if self.last_roll is None
            else {
                "dice": [self.last_roll.d1, self.last_roll.d2],
                "total": self.last_roll.total,
                "winnings": round(self.last_roll.winnings, 2),
                "resolved": {k: round(v, 2) for k, v in self.last_roll.resolved.items()},
                "lost_keys": self.last_roll.lost_keys,
                "point_before": self.last_roll.point_before,
                "point_after": self.last_roll.point_after,
            },
        }


class Game:
    """A single-table, single-player Easy Craps session."""

    def __init__(self, rng: random.Random | None = None):
        self.state = GameState()
        self.rng = rng or random.Random()
        self._triggers: dict[str, Callable[[dict], Any]] = {
            "add_funds": self._t_add_funds,
            "place_bet": self._t_place_bet,
            "clear_last_bet": self._t_clear_last_bet,
            "clear_all_bets": self._t_clear_all_bets,
            "double_bet": self._t_double_bet,
            "repeat_last_bet": self._t_repeat_last_bet,
            "toggle_set_bets": self._t_toggle_set_bets,
            "press": self._t_press,
            "across": self._t_across,
            "toggle_puck": self._t_toggle_puck,
            "cashout": self._t_cashout,
            "set_min_bet": self._t_set_min_bet,
            "roll": self._t_roll,
            "reset": self._t_reset,
        }

    @property
    def trigger_names(self) -> list[str]:
        return list(self._triggers.keys())

    def apply(self, trigger: str, payload: dict | None = None) -> dict[str, Any]:
        """Dispatch a named trigger. Returns {ok, message, state}."""
        payload = payload or {}
        handler = self._triggers.get(trigger)
        if handler is None:
            raise TriggerError(f"Unknown trigger: {trigger!r}. Valid: {self.trigger_names}")
        ok, message = handler(payload)
        if message:
            self.state.message = message
        return {"ok": ok, "message": self.state.message, "state": self.state.to_dict()}

    # ---------------------------------------------------------------- utils
    def _is_valid_spot(self, key: str) -> bool:
        if key in ("pass", "field", "lowfield", "highfield", "c", "e", "ce",
                   "anycraps", "seven", "horn", "lowrolls", "rollemall", "highrolls"):
            return True
        if key.startswith("place_"):
            return int(key.split("_")[1]) in C.POINT_NUMBERS
        if key.startswith("hard_"):
            return int(key.split("_")[1]) in C.HARDS
        if key.startswith("horn_"):
            return int(key.split("_")[1]) in C.HORN_NUMBERS
        if key.startswith("hop_"):
            digits = key.split("_")[1]
            return len(digits) == 2 and digits[0].isdigit() and digits[1].isdigit()
        return False

    def _refresh_after_bet_mutation(self) -> None:
        self.state.bets = {k: v for k, v in self.state.bets.items() if v > 0}

    # ------------------------------------------------------------- triggers
    def _t_add_funds(self, payload: dict) -> tuple[bool, str]:
        amount = float(payload.get("amount", 0))
        if amount <= 0:
            return False, "No funds added — enter a positive number."
        self.state.credit += amount
        return True, f"${amount:.2f} added to credit."

    def _t_place_bet(self, payload: dict) -> tuple[bool, str]:
        if self.state.rolling:
            return False, "Wait for the roll to finish."
        spot = payload.get("spot")
        amount = float(payload.get("amount", 0))
        if not spot or not self._is_valid_spot(spot):
            raise TriggerError(f"Invalid bet spot: {spot!r}")
        if amount <= 0:
            raise TriggerError("Bet amount must be positive.")
        if self.state.credit < amount:
            return False, "Not enough credit for that bet — add funds."
        self.state.credit -= amount
        self.state.bets[spot] = self.state.bets.get(spot, 0) + amount
        self.state.bet_log.append((spot, amount))
        return True, f"${amount:.2f} on {spot}."

    def _t_clear_last_bet(self, payload: dict) -> tuple[bool, str]:
        if self.state.rolling:
            return False, "Wait for the roll to finish."
        if not self.state.bet_log:
            return False, "No bet to clear this turn."
        key, amount = self.state.bet_log.pop()
        self.state.bets[key] = self.state.bets.get(key, 0) - amount
        self.state.credit += amount
        self._refresh_after_bet_mutation()
        return True, f"Removed ${amount:.2f} from {key}."

    def _t_clear_all_bets(self, payload: dict) -> tuple[bool, str]:
        if self.state.rolling:
            return False, "Wait for the roll to finish."
        total = self.state.total_bets()
        if total <= 0:
            return False, "No bets on the table."
        self.state.credit += total
        self.state.bets = {}
        self.state.bet_log = []
        return True, f"Cleared all bets (${total:.2f} returned to credit)."

    def _t_double_bet(self, payload: dict) -> tuple[bool, str]:
        if self.state.rolling:
            return False, "Wait for the roll to finish."
        need = self.state.total_bets()
        if need <= 0:
            return False, "Place a bet before doubling it."
        if need > self.state.credit:
            return False, "Not enough credit to double."
        self.state.credit -= need
        for key in list(self.state.bets):
            self.state.bets[key] *= 2
            self.state.bet_log.append((key, self.state.bets[key] / 2))
        return True, "Bets doubled."

    def _t_repeat_last_bet(self, payload: dict) -> tuple[bool, str]:
        if self.state.rolling:
            return False, "Wait for the roll to finish."
        if not self.state.last_bets:
            return False, "No previous bet to repeat yet."
        need = sum(self.state.last_bets.values())
        if need > self.state.credit:
            return False, "Not enough credit to repeat last bet."
        self.state.credit -= need
        for key, amount in self.state.last_bets.items():
            self.state.bets[key] = self.state.bets.get(key, 0) + amount
            self.state.bet_log.append((key, amount))
        return True, "Repeated last bet."

    def _t_toggle_set_bets(self, payload: dict) -> tuple[bool, str]:
        self.state.set_bets_on = not self.state.set_bets_on
        return True, (
            "Place & Hard Way bets are back ON."
            if self.state.set_bets_on
            else "Place & Hard Way bets are OFF for the next roll."
        )

    def _t_press(self, payload: dict) -> tuple[bool, str]:
        if self.state.rolling:
            return False, "Wait for the roll to finish."
        spot = payload.get("spot")
        if spot is None:
            if self.state.point is None:
                return False, "Press applies to the established Point bet."
            spot = f"place_{self.state.point}"
        current = self.state.bets.get(spot)
        if not current:
            return False, "No bet on that spot to press yet."
        if self.state.credit < current:
            return False, "Not enough credit to press that bet."
        self.state.credit -= current
        self.state.bets[spot] += current
        self.state.bet_log.append((spot, current))
        return True, f"Pressed {spot} to ${self.state.bets[spot]:.2f}."

    def _t_across(self, payload: dict) -> tuple[bool, str]:
        if self.state.rolling:
            return False, "Wait for the roll to finish."
        amount = float(payload.get("amount", 0))
        if amount <= 0:
            raise TriggerError("Across amount must be positive.")
        placed = []
        for n in C.POINT_NUMBERS:
            if n == self.state.point:
                continue
            key = f"place_{n}"
            if self.state.credit < amount:
                break
            self.state.credit -= amount
            self.state.bets[key] = self.state.bets.get(key, 0) + amount
            self.state.bet_log.append((key, amount))
            placed.append(n)
        return True, f"Placed bets across {len(placed)} numbers."

    def _t_toggle_puck(self, payload: dict) -> tuple[bool, str]:
        if self.state.point is not None:
            return False, "The puck can only be reset when no Point is established."
        self.state.puck_manual_off = not self.state.puck_manual_off
        return True, (
            "Marker puck manually set to OFF."
            if self.state.puck_manual_off
            else "Marker puck restored."
        )

    def _t_cashout(self, payload: dict) -> tuple[bool, str]:
        if self.state.total_bets() > 0:
            return False, "Clear your bets before cashing out."
        if self.state.credit <= 0:
            return False, "No credit to cash out."
        amount = self.state.credit
        self.state.credit = 0
        return True, f"Ticket printed for ${amount:.2f}."

    def _t_set_min_bet(self, payload: dict) -> tuple[bool, str]:
        amount = float(payload.get("amount", 0))
        if amount <= 0:
            raise TriggerError("Minimum bet must be positive.")
        self.state.min_bet = amount
        return True, f"Minimum total bet set to ${amount:.2f}."

    def _t_reset(self, payload: dict) -> tuple[bool, str]:
        keep_credit = float(payload.get("keep_credit", 0))
        self.state = GameState(credit=keep_credit)
        return True, "New session started."

    def _t_roll(self, payload: dict) -> tuple[bool, str]:
        s = self.state
        if s.rolling:
            return False, "Roll already in progress."
        total = s.total_bets()
        if total <= 0:
            return False, "Place a bet before rolling."
        if total < s.min_bet:
            return False, f"Minimum total bet is ${s.min_bet:.2f} — add more chips."

        d1 = payload.get("d1")
        d2 = payload.get("d2")
        if d1 is None or d2 is None:
            d1, d2 = self.rng.randint(1, 6), self.rng.randint(1, 6)
        d1, d2 = int(d1), int(d2)
        total_pips = d1 + d2

        result = self._resolve_roll(d1, d2, total_pips)
        s.last_roll = result
        s.history.append((d1, d2))
        s.last_bets = dict(s.bets)
        s.bet_log = []
        return True, result.message

    # ------------------------------------------------------------ resolving
    def _resolve_roll(self, d1: int, d2: int, total: int) -> RollResult:
        s = self.state
        resolved: dict[str, float] = {}
        lost: list[str] = []
        winnings = 0.0

        def settle(key: str, won: bool, pay_for: int) -> None:
            nonlocal winnings
            amt = s.bets.get(key)
            if not amt:
                return
            if won:
                payout = amt * pay_for
                s.credit += payout
                winnings += payout
                resolved[key] = payout
            else:
                lost.append(key)
            del s.bets[key]

        settle(
            "field",
            total in C.FIELD_WINNERS,
            C.FIELD_DOUBLE_PAY_FOR if total in C.FIELD_DOUBLE_WINNERS else C.FIELD_PAY_FOR,
        )
        settle("lowfield", total in C.LOW_FIELD_WINNERS, C.LOW_FIELD_PAY_FOR)
        settle("highfield", total in C.HIGH_FIELD_WINNERS, C.HIGH_FIELD_PAY_FOR)
        settle("c", total in C.C_WINNERS, C.C_PAY_FOR)
        settle("e", total in C.E_WINNERS, C.E_PAY_FOR)
        settle("anycraps", total in C.ANY_CRAPS_WINNERS, C.ANY_CRAPS_PAY_FOR)
        settle("seven", total == 7, C.ANY_SEVEN_PAY_FOR)
        settle("horn", total in C.HORN_BET_WINNERS, C.HORN_BET_PAY_FOR)
        for n, info in C.HORN_NUMBERS.items():
            settle(f"horn_{n}", total == n, info["pay_for"])

        ce_amt = s.bets.get("ce")
        if ce_amt:
            half = ce_amt // 2 if ce_amt == int(ce_amt) else ce_amt / 2
            won = 0.0
            if total in C.C_WINNERS:
                won = half * C.C_PAY_FOR
            elif total in C.E_WINNERS:
                won = half * C.E_PAY_FOR
            if won > 0:
                s.credit += won
                winnings += won
                resolved["ce"] = won
            else:
                lost.append("ce")
            del s.bets["ce"]

        for a, b in C.HOP_COMBOS:
            key = C.hop_key(a, b)
            hit = (d1, d2) in ((a, b), (b, a))
            settle(key, hit, C.hop_pay_for(a, b))

        for n, info in C.HARDS.items():
            key = f"hard_{n}"
            amt = s.bets.get(key)
            hit_hard = (d1, d2) == info["combo"] or (d2, d1) == info["combo"]
            if not amt:
                if not hit_hard:
                    s.hard_since[n] += 1
                else:
                    s.hard_since[n] = 0
                continue
            if hit_hard:
                payout = amt * info["pay_for"]
                s.credit += payout
                winnings += payout
                resolved[key] = payout
                del s.bets[key]
                s.hard_since[n] = 0
            elif total == 7 or total == n:
                lost.append(key)
                del s.bets[key]
                s.hard_since[n] += 1
            else:
                s.hard_since[n] += 1

        if s.set_bets_on:
            for n in C.POINT_NUMBERS:
                key = f"place_{n}"
                amt = s.bets.get(key)
                if not amt:
                    continue
                if total == n:
                    payout = amt * C.place_return_multiplier(n)
                    s.credit += payout
                    winnings += payout
                    resolved[key] = payout
                    del s.bets[key]
                elif total == 7:
                    lost.append(key)
                    del s.bets[key]

        for name, needed in (
            ("lowrolls", C.LUCKY_LOW_NEEDED),
            ("rollemall", C.LUCKY_ALL_NEEDED),
            ("highrolls", C.LUCKY_HIGH_NEEDED),
        ):
            amt = s.bets.get(name)
            if not amt:
                continue
            if total == 7:
                lost.append(name)
                del s.bets[name]
                s.lucky_hits[name] = set()
                continue
            if total in needed:
                s.lucky_hits[name].add(total)
            if needed.issubset(s.lucky_hits[name]):
                payout = amt * C.LUCKY_PAY_FOR[name]
                s.credit += payout
                winnings += payout
                resolved[name] = payout
                del s.bets[name]
                s.lucky_hits[name] = set()
        if total == 7:
            for name in ("lowrolls", "rollemall", "highrolls"):
                s.lucky_hits[name] = set()

        point_before = s.point
        pass_amt = s.bets.get("pass", 0)
        if s.point is None:
            if total == 7:
                if pass_amt:
                    payout = pass_amt * 2
                    s.credit += payout
                    winnings += payout
                    resolved["pass"] = payout
                    del s.bets["pass"]
                message = "7 on the come-out — Pass Line wins! Place a new Pass Line bet."
            else:
                s.point = total
                s.puck_manual_off = False
                message = f"Point is {C.POINT_LABEL[total]}. Anything but 7 keeps it alive."
        else:
            if total == s.point:
                if pass_amt:
                    payout = pass_amt * 2
                    s.credit += payout
                    winnings += payout
                    resolved["pass"] = payout
                    del s.bets["pass"]
                message = f"Point {C.POINT_LABEL[s.point]} repeats — Pass Line wins! New come-out roll."
                s.point = None
            elif total == 7:
                if pass_amt:
                    lost.append("pass")
                    del s.bets["pass"]
                message = "Seven out. Pass Line & Place bets lose. New come-out roll."
                s.point = None
            else:
                message = f"Point is still {C.POINT_LABEL[s.point]} — roll again."

        return RollResult(
            d1=d1, d2=d2, total=total, winnings=winnings, resolved=resolved,
            lost_keys=lost, point_before=point_before, point_after=s.point,
            message=message,
        )
