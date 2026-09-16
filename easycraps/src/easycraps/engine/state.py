"""GameState and RollResult — the data a Game carries and returns."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..constants import DEFAULT_MIN_BET


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
    min_bet: float = DEFAULT_MIN_BET
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
