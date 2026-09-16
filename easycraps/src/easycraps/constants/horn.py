"""Horn number bets and the combined "horn" bet."""

# Horn single-number bets: number -> (combo, total-return multiplier)
HORN_NUMBERS = {
    2: {"combo": (1, 1), "pay_for": 31},
    3: {"combo": (1, 2), "pay_for": 16},
    11: {"combo": (5, 6), "pay_for": 16},
    12: {"combo": (6, 6), "pay_for": 31},
}

HORN_BET_PAY_FOR = 4  # flat combined "horn" bet, 3:1
HORN_BET_WINNERS = (2, 3, 11, 12)
