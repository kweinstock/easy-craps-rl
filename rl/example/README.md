# Example: a very basic RL agent

The smallest possible agent that actually learns, built on
[`easycraps`](../../easycraps) — meant to be read top to bottom as a
template for your own agent in a sibling `rl/<your-name>/` folder.

[`q_learning_agent.py`](q_learning_agent.py) is tabular Q-learning with:

- **2 states**: `"come_out"` (no Point established) or `"point_on"`.
- **2 actions**: bet one unit on the Pass Line, or bet one unit on the
  Field, then roll.
- **Reward**: the change in bankroll (`credit + total_bet`) after that
  roll — i.e. did that action make or lose money.

That's the entire interface to the game: `easycraps.Table` for placing
bets and rolling, `table.credit` / `table.total_bet` / `table.point` for
observing what happened. No Gym, no fixed observation vector — you decide
what state and action space fit your algorithm (see
[`../GETTING_STARTED.md`](../GETTING_STARTED.md) for the full method list).

## Run it

```bash
pip install -r requirements.txt   # installs easycraps in editable mode
python q_learning_agent.py
```

It trains for a few thousand short episodes (epsilon-greedy, decaying
exploration), then prints the learned Q-values for both states and the
average final bankroll over 200 greedy (no-exploration) evaluation
episodes.

## Where to go from here

This example's state space is intentionally tiny so the whole Q-table
prints on two lines. A stronger agent would want more of what
`table.state` already gives you for free: the actual Point number, current
bankroll, what's already on the table, hard-way "rolls since last hit"
counters, Lucky Roller progress — plus a larger action set (the full bet
list in [`../GETTING_STARTED.md`](../GETTING_STARTED.md)). Swap in a
bigger state encoding, more actions, and/or a real function approximator
(a small neural net instead of a dict-based Q-table) as needed — the
`easycraps.Table` interface underneath doesn't change.
