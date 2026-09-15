# Easy Craps — Rulebook

Easy Craps is a simplified craps variant designed for a single-player cabinet.
It removes several bets found at a standard craps table and adds a few
cabinet-only side bets. This document is the single source of truth for the
rules — the [game engine](../easycraps/src/easycraps/engine.py) implements
exactly what's described here, and both the web UI and Python agents are
built on top of it.

## What's different from standard craps

- **Every number except 7 can be the Point**: 2, 3, 4, 5, 6, 8, 9, 10, 11, 12.
  (Standard craps only uses 4, 5, 6, 8, 9, 10 as points.)
- **No Don't Pass, Don't Come, or Come bets.**
- **No Buy or Lay bets.**
- **No Big 6 / Big 8.**
- Place bets are available on every point number, including 2, 3, 11, and 12
  (not offered at a standard table).
- Two cabinet-exclusive side bets: **Lucky Roller** (multi-roll progressive)
  and a flat **Horn Bet** / **C&E** split bet.

## Round structure

1. **Come-out roll.** No Point is established (the puck is OFF).
   - Roll **7** → Pass Line wins (paid 1:1), the shooter stays on a new
     come-out roll.
   - Roll anything else (2,3,4,5,6,8,9,10,11,12) → that number becomes the
     **Point** (the puck turns ON and moves to that number).
2. **Point phase.** The puck is ON a number.
   - Roll the **Point** again → Pass Line wins (1:1), puck goes OFF, back to
     a come-out roll.
   - Roll a **7** ("seven-out") → Pass Line and all Place/Hard Way bets on
     the table lose, puck goes OFF, back to a come-out roll.
   - Roll anything else → no resolution for the Pass Line; Place, Field,
     Hard Way, and one-roll bets still resolve normally on every roll.

One-roll bets (Field, C, E, Any Craps, Seven, Horn, Hop) and multi-roll side
bets (Lucky Roller) resolve on **every** roll regardless of come-out/point
phase.

## Bets

All payouts below are written as **win : stake**. "Total return" is what the
engine actually credits back (win + original stake), since the stake is
deducted from credit the moment the bet is placed.

### Pass Line
- Bet before the come-out roll (or add to it any time the puck is off).
- Pays **1 : 1**.
- Wins when the come-out roll is 7, or when an established Point repeats
  before a 7.
- Loses on seven-out.

### Place Bets (one per point number: 2,3,4,5,6,8,9,10,11,12)
- Can be made any time; working by default.
- Wins whenever its number is rolled (not just as the Point), loses on 7,
  otherwise stays up.
- Payouts:

  | Number | Pays |
  |---|---|
  | 2, 12 | 11 : 2 |
  | 3, 11 | 11 : 4 |
  | 4, 10 | 9 : 5 |
  | 5, 9  | 7 : 5 |
  | 6, 8  | 7 : 6 |

- **Press**: re-bet the current winnings-sized amount onto the Place bet
  on the active Point, doubling it in place.
- **Across**: place one unit on every point number except the current
  Point in a single action.
- **Set Bets On/Off**: toggles whether Place and Hard Way bets are
  "working" on the next come-out roll. When off, they neither win nor lose
  on that roll's resolution.

### Field (one roll)
- Wins on 2, 3, 4, 9, 10, 11, 12.
- Pays **1 : 1**, except **2 and 12 pay double (2 : 1)**.
- Loses on 5, 6, 7, 8.
- *(Note: the original cabinet HTML prototype had a bug that returned only
  the stake — no actual winnings — on a regular Field win. The engine here
  implements the correct 1:1 / 2:1 payouts described above.)*

### Low Field / High Field (one roll)
- **Low Field**: wins on 2, 3, 4. Pays **4 : 1**.
- **High Field**: wins on 10, 11, 12. Pays **4 : 1**.

### C (Craps) and E (Eleven) — one roll
- **C**: wins on 2, 3, 12. Pays **7 : 1**.
- **E**: wins on 11. Pays **14 : 1**.
- **C&E**: a single bet split in half between C and E (odd amounts round the
  half down); each half resolves independently at the odds above.

### Any Craps (one roll)
- Wins on 2, 3, 12. Pays **7 : 1**. (Functionally identical to "C".)

### Any Seven (one roll)
- Wins on 7. Pays **4 : 1**.

### Horn numbers (one roll, bet individually on 2, 3, 11, or 12)
- 2 or 12 pay **30 : 1**.
- 3 or 11 pay **15 : 1**.

### Horn Bet (one roll, the combined center bet)
- A single flat bet that wins if the roll is 2, 3, 11, or 12.
- Pays a flat **3 : 1** on the whole wager (this is a simplified "quick
  horn," not four separate sub-bets).

### Hop Bets (one roll, bet on an exact dice combination)
- Bet that the next roll is an exact two-die combination, e.g. 4-3 or 2-2.
- **Doubles** (1-1, 2-2, 3-3, 4-4, 5-5, 6-6) pay **30 : 1**.
- **Non-doubles** (e.g. 1-3, 2-6, 4-5, …) pay **15 : 1** and win on either
  die order.

### Hard Ways (multi-roll, stays up until it resolves)
- **Hard 4** (2-2) and **Hard 10** (5-5) pay **7 : 1**.
- **Hard 6** (3-3) and **Hard 8** (4-4) pay **9 : 1**.
- Wins when the number comes up as an exact pair (e.g. 3-3 for Hard 6).
- Loses if the same number comes up "easy" (any other combination that
  sums to it, e.g. 4-2 for Hard 6) or if a 7 is rolled.
- The cabinet tracks and displays **rolls since last hit** for each number.

### Lucky Roller (multi-roll progressive side bets)
Bet before any roll; the bet stays active across multiple rolls until it
resolves. A 7 at any point busts all three Lucky Roller bets.

- **Low Rolls**: every one of {2,3,4,5,6} must appear (in any order, across
  any number of rolls) before a 7. Pays **30 : 1**.
- **High Rolls**: every one of {8,9,10,11,12} must appear before a 7. Pays
  **30 : 1**.
- **Roll'Em All**: every non-7 total (2,3,4,5,6,8,9,10,11,12) must appear
  before a 7. Pays **155 : 1**.

## Table controls (not gameplay bets)

- **Add Funds**: deposit more credit.
- **Cashout**: convert all remaining credit to a payout ticket; only
  allowed with no bets on the table.
- **Minimum Total Bet**: a table-level setting (gear icon) for the smallest
  total wager the Roll button will accept. This is a dealer/operator
  control, not a player action, and is excluded from the RL action space.
- **Clear Last Bet / Clear All Bets**: undo the most recent bet placement,
  or (pressed again with nothing left to undo) return every active bet's
  stake to credit.
- **Double Bet**: doubles every currently active bet, in place.
- **Repeat Last Bet**: re-places whatever was on the table for the previous
  resolved roll.
- **Puck manual OFF**: cosmetic toggle only available when no Point is
  established.

## Triggers

Every action above is implemented as a named **trigger** on the game engine
(`Game.apply(trigger, payload)`), the same call the web UI's buttons make
over HTTP/WebSocket and the same call any agent makes to interact with the
table. See [backend/README.md](../cabinet/backend/README.md) for the full trigger
list and HTTP details, or [easycraps](../easycraps) for the plain-Python
library (`Table`) that wraps these triggers in named methods like
`table.field_bet(10)` for in-process Python agents — see
[`../rl/GETTING_STARTED.md`](../rl/GETTING_STARTED.md) for a
walkthrough.
