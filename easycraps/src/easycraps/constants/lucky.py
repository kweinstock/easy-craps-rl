"""Lucky Roller progressive side bets (Low Rolls / High Rolls / Roll'Em All)."""

LUCKY_LOW_NEEDED = frozenset({2, 3, 4, 5, 6})
LUCKY_HIGH_NEEDED = frozenset({8, 9, 10, 11, 12})
LUCKY_ALL_NEEDED = frozenset({2, 3, 4, 5, 6, 8, 9, 10, 11, 12})
LUCKY_PAY_FOR = {"lowrolls": 31, "highrolls": 31, "rollemall": 156}
