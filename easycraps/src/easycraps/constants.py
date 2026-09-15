"""Static game data for Easy Craps. See docs/RULES.md (in the parent easy-craps
project) for the rules these encode."""

POINT_NUMBERS = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]

POINT_LABEL = {
    2: "2", 3: "3", 4: "4", 5: "5", 6: "SIX",
    8: "8", 9: "NINE", 10: "10", 11: "11", 12: "12",
}

# number -> (a, b) meaning the number pays (a-b):b, i.e. a/b is the total
# return multiplier (win + stake) on a winning bet.
PLACE_PAY = {
    2: (13, 2), 3: (15, 4), 4: (14, 5), 5: (12, 5), 6: (13, 6),
    8: (13, 6), 9: (12, 5), 10: (14, 5), 11: (15, 4), 12: (13, 2),
}


def place_return_multiplier(number: int) -> float:
    a, b = PLACE_PAY[number]
    return a / b


# Hard ways: number -> (die combo, total-return multiplier)
HARDS = {
    4: {"combo": (2, 2), "pay_for": 8},
    6: {"combo": (3, 3), "pay_for": 10},
    8: {"combo": (4, 4), "pay_for": 10},
    10: {"combo": (5, 5), "pay_for": 8},
}

# Horn single-number bets: number -> (combo, total-return multiplier)
HORN_NUMBERS = {
    2: {"combo": (1, 1), "pay_for": 31},
    3: {"combo": (1, 2), "pay_for": 16},
    11: {"combo": (5, 6), "pay_for": 16},
    12: {"combo": (6, 6), "pay_for": 31},
}

HORN_BET_PAY_FOR = 4  # flat combined "horn" bet, 3:1
HORN_BET_WINNERS = (2, 3, 11, 12)

FIELD_WINNERS = (2, 3, 4, 9, 10, 11, 12)
FIELD_DOUBLE_WINNERS = (2, 12)
FIELD_PAY_FOR = 2  # 1:1 total return
FIELD_DOUBLE_PAY_FOR = 3  # 2:1 total return
LOW_FIELD_WINNERS = (2, 3, 4)
HIGH_FIELD_WINNERS = (10, 11, 12)
LOW_FIELD_PAY_FOR = 5
HIGH_FIELD_PAY_FOR = 5

C_WINNERS = (2, 3, 12)
C_PAY_FOR = 8
E_WINNERS = (11,)
E_PAY_FOR = 15
ANY_CRAPS_WINNERS = (2, 3, 12)
ANY_CRAPS_PAY_FOR = 8
ANY_SEVEN_PAY_FOR = 5

# All 21 unique two-die combinations for Hop bets.
HOP_COMBOS = []
for _d1 in range(1, 7):
    for _d2 in range(_d1, 7):
        HOP_COMBOS.append((_d1, _d2))


def hop_key(a: int, b: int) -> str:
    lo, hi = sorted((a, b))
    return f"hop_{lo}{hi}"


def hop_pay_for(a: int, b: int) -> int:
    return 31 if a == b else 16  # 30:1 doubles, 15:1 non-doubles


LUCKY_LOW_NEEDED = frozenset({2, 3, 4, 5, 6})
LUCKY_HIGH_NEEDED = frozenset({8, 9, 10, 11, 12})
LUCKY_ALL_NEEDED = frozenset({2, 3, 4, 5, 6, 8, 9, 10, 11, 12})
LUCKY_PAY_FOR = {"lowrolls": 31, "highrolls": 31, "rollemall": 156}

DEFAULT_MIN_BET = 3.0
