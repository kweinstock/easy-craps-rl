"""Hop bets: every exact two-die combination."""

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
