# Getting started: building an agent with `easycraps`

This folder is where RL agents live (one subfolder per person — `Gavin/`,
`Keagan/`, add your own). The game itself is a plain Python library called
`easycraps`, not a Gym/Gymnasium environment — you call methods on a
`Table` object, the same way a player would push buttons.

## 1. Install the library

`easycraps` lives at [`../easycraps`](../easycraps).
Install it in editable mode so your agent always sees the latest rules:

```bash
pip install -e ../easycraps
```

(Path is relative to wherever you run the command from — adjust `..` to
however deep your agent script is under `rl/`.)

## 2. Play a round

```python
import easycraps

table = easycraps.Table(credit=200)

table.pass_line_bet(5)          # bet before the come-out roll
result = table.roll()           # random dice
print(result.message)           # e.g. "Point is SIX. Anything but 7 keeps it alive."
print(table.credit, table.point, table.bets)
```

Every betting/action method returns an `ActionResult` with `.ok` (did it
happen), `.message` (human-readable, same text the web UI shows), and
`.state` (the full state snapshot as a dict, same shape the HTTP API
returns). `ActionResult` is also truthy/falsy based on `.ok`, so
`if not table.field_bet(10): ...` works for "that bet was rejected".

## 3. The methods available

Table setup / bankroll:

| Method | Same as |
|---|---|
| `table.add_funds(amount)` | tapping "+ Add Funds" |
| `table.cashout()` | tapping "CASHOUT" (only with no bets active) |
| `table.set_min_bet(amount)` | the gear icon (table config, not a player action) |
| `table.reset(keep_credit=0)` | starting a brand new session |

Placing bets — every one of these takes a dollar amount and returns an
`ActionResult`:

| Method | Bet |
|---|---|
| `table.pass_line_bet(amt)` | Pass Line |
| `table.field_bet(amt)` | Field (2,3,4,9,10,11,12; 2 & 12 pay double) |
| `table.low_field_bet(amt)` | Low Field (2,3,4) |
| `table.high_field_bet(amt)` | High Field (10,11,12) |
| `table.place_number_bet(number, amt)` | Place bet on `number` (2,3,4,5,6,8,9,10,11,12) |
| `table.hard_way_bet(number, amt)` | Hard way on `number` (4,6,8,10) |
| `table.craps_bet(amt)` | "C" (2,3,12) |
| `table.eleven_bet(amt)` | "E" (11) |
| `table.craps_eleven_bet(amt)` | "C&E" split bet |
| `table.any_craps_bet(amt)` | Any Craps (2,3,12) |
| `table.seven_bet(amt)` | Any Seven |
| `table.horn_number_bet(number, amt)` | Single horn number (2,3,11,12) |
| `table.horn_bet(amt)` | Combined horn bet |
| `table.hop_bet(d1, d2, amt)` | Exact combo, e.g. `table.hop_bet(4, 3, 1)` |
| `table.lucky_low_bet(amt)` | Lucky Roller — Low Rolls |
| `table.lucky_high_bet(amt)` | Lucky Roller — High Rolls |
| `table.lucky_all_bet(amt)` | Lucky Roller — Roll'Em All |

Managing bets already on the table:

| Method | Same as |
|---|---|
| `table.clear_last_bet()` | undo the most recent bet this turn |
| `table.clear_all_bets()` | return every active bet's stake to credit |
| `table.double_bet()` | double every active bet |
| `table.repeat_last_bet()` | re-place last round's bets |
| `table.toggle_set_bets()` | toggle whether Place/Hard Way bets work next roll |
| `table.press(spot=None)` | re-bet current stake onto `spot` (defaults to the Point's Place bet) |
| `table.across(amount)` | one unit on every point number but the Point |
| `table.toggle_puck()` | cosmetic manual OFF, only with no Point established |

Rolling:

```python
table.roll()               # random dice
table.roll(d1=3, d2=4)     # deterministic — great for unit tests / replaying a scenario
```

Reading state (all read-only properties, no method calls needed):

```python
table.credit       # float
table.bets         # {spot_key: amount}
table.total_bet     # sum of table.bets.values()
table.point        # None or the established point number
table.min_bet      # current table minimum
table.message      # last message, same text the UI shows
table.history      # list of (d1, d2) tuples, oldest first
table.last_roll    # the RollResult dataclass from the most recent roll, or None
table.state        # everything above as one dict (same JSON the HTTP API returns)
```

## 4. Escape hatch: raw triggers

If you ever need a bet spot or action that doesn't have a named method yet,
every one of the methods above is a thin wrapper over one call:

```python
table.trigger("place_bet", spot="place_6", amount=5)
table.bet("place_6", 5)  # equivalent, shorter
```

The full list of raw trigger names and bet-spot keys is in
[`../cabinet/backend/README.md`](../cabinet/backend/README.md#trigger-reference)
(the HTTP API and this library both dispatch through the exact same
trigger names).

## 5. The rules

Read [`../docs/RULES.md`](../docs/RULES.md) before
you design a policy — Easy Craps allows Place bets on 2, 3, 11, and 12
(non-standard), has no Don't Pass/Come, and includes cabinet-only bets
(Lucky Roller, Horn Bet, C&E) that a standard-craps strategy guide won't
mention.

## 6. Why not Gymnasium?

`easycraps.Table` deliberately isn't a Gym/Gymnasium `Env`. There's no
fixed observation vector or Discrete action space forced on you — pick
whatever state representation and action framing suit your algorithm,
using `table.state` (or the individual properties) as your source of
truth, and any subset of the methods above as your action set. If your
algorithm specifically needs a Gym-style `reset()`/`step()` loop, it's
straightforward to build a thin Env around `Table` yourself in your own
subfolder — `Table` is the stable layer underneath, and it doesn't require
you to.

## 7. Non-Python agents

If your agent isn't in Python, it doesn't use this library at all — it
drives the same triggers over HTTP against `backend`'s FastAPI
server instead (`POST /sessions`, then `POST /sessions/{id}/trigger`). See
[`../cabinet/backend/README.md`](../cabinet/backend/README.md).
