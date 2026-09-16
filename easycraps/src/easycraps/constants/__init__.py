"""Static game data for Easy Craps, split by bet category — see
docs/RULES.md (in the parent easy-craps project) for the rules these
encode. Everything is re-exported flat here so `from easycraps import
constants as C; C.POINT_NUMBERS` keeps working regardless of which
submodule a name actually lives in.
"""
from .field import (
    ANY_CRAPS_PAY_FOR,
    ANY_CRAPS_WINNERS,
    ANY_SEVEN_PAY_FOR,
    C_PAY_FOR,
    C_WINNERS,
    E_PAY_FOR,
    E_WINNERS,
    FIELD_DOUBLE_PAY_FOR,
    FIELD_DOUBLE_WINNERS,
    FIELD_PAY_FOR,
    FIELD_WINNERS,
    HIGH_FIELD_PAY_FOR,
    HIGH_FIELD_WINNERS,
    LOW_FIELD_PAY_FOR,
    LOW_FIELD_WINNERS,
)
from .hardways import HARDS
from .hop import HOP_COMBOS, hop_key, hop_pay_for
from .horn import HORN_BET_PAY_FOR, HORN_BET_WINNERS, HORN_NUMBERS
from .lucky import LUCKY_ALL_NEEDED, LUCKY_HIGH_NEEDED, LUCKY_LOW_NEEDED, LUCKY_PAY_FOR
from .points import PLACE_PAY, POINT_LABEL, POINT_NUMBERS, place_return_multiplier
from .settings import DEFAULT_MIN_BET

__all__ = [
    "POINT_NUMBERS", "POINT_LABEL", "PLACE_PAY", "place_return_multiplier",
    "FIELD_WINNERS", "FIELD_DOUBLE_WINNERS", "FIELD_PAY_FOR", "FIELD_DOUBLE_PAY_FOR",
    "LOW_FIELD_WINNERS", "HIGH_FIELD_WINNERS", "LOW_FIELD_PAY_FOR", "HIGH_FIELD_PAY_FOR",
    "C_WINNERS", "C_PAY_FOR", "E_WINNERS", "E_PAY_FOR",
    "ANY_CRAPS_WINNERS", "ANY_CRAPS_PAY_FOR", "ANY_SEVEN_PAY_FOR",
    "HARDS",
    "HORN_NUMBERS", "HORN_BET_PAY_FOR", "HORN_BET_WINNERS",
    "HOP_COMBOS", "hop_key", "hop_pay_for",
    "LUCKY_LOW_NEEDED", "LUCKY_HIGH_NEEDED", "LUCKY_ALL_NEEDED", "LUCKY_PAY_FOR",
    "DEFAULT_MIN_BET",
]
