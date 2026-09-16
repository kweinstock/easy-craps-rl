"""Roll resolution: settles every bet category against one dice roll.

`resolve_roll()` is the only function here — it mutates `state` in place
(removing resolved bets, crediting winnings, updating hard-way/Lucky Roller
counters and the Pass Line point) and returns a `RollResult` summarizing
what happened. `engine.game.Game` is the only caller; this is split out
purely so "how a roll resolves" isn't buried inside the trigger
dispatcher — see docs/RULES.md for what each of these bets actually pays.
"""
from __future__ import annotations

from .. import constants as C
from .state import GameState, RollResult


def resolve_roll(state: GameState, d1: int, d2: int, total: int) -> RollResult:
    s = state
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
