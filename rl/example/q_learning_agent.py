"""A minimal tabular Q-learning agent playing Easy Craps via `easycraps`.

This is deliberately small — it exists to show the shape of an RL loop
against the library, not to be a strong player. Two actions (bet Pass Line
vs bet Field, one unit each roll) and a two-state world (come-out vs
point-on) is enough to demonstrate state/action/reward, epsilon-greedy
exploration, and a Q-table update end to end.

Run:
    pip install -r requirements.txt   # installs easycraps in editable mode
    python q_learning_agent.py
"""
from __future__ import annotations

import random
from collections import defaultdict

import easycraps

UNIT = 1.0
STARTING_CREDIT = 200.0
ROLLS_PER_EPISODE = 60
TRAIN_EPISODES = 3000
EVAL_EPISODES = 200

ACTIONS = ["pass_line", "field"]

ALPHA = 0.1  # learning rate
GAMMA = 0.9  # discount factor
EPSILON_START = 1.0
EPSILON_END = 0.05


def new_table() -> easycraps.Table:
    table = easycraps.Table(credit=STARTING_CREDIT)
    table.set_min_bet(UNIT)  # so a single unit bet is enough to roll
    return table


def get_state(table: easycraps.Table) -> str:
    """The whole observation: is this a come-out roll, or is a Point on?

    A real agent would want more than this (bankroll, the actual Point
    number, what's already on the table, hard-way counters, ...) — see
    `table.state` for everything available. Two states keeps the Q-table
    small enough to read directly, which is the point of this example.
    """
    return "point_on" if table.point is not None else "come_out"


def take_action(table: easycraps.Table, action: str) -> float:
    """Place the chosen bet, roll, and return the bankroll change (reward)."""
    bankroll_before = table.credit + table.total_bet
    if action == "pass_line":
        table.pass_line_bet(UNIT)
    else:
        table.field_bet(UNIT)
    table.roll()
    bankroll_after = table.credit + table.total_bet
    return bankroll_after - bankroll_before


def epsilon_for(episode: int) -> float:
    frac = min(1.0, episode / TRAIN_EPISODES)
    return EPSILON_START + frac * (EPSILON_END - EPSILON_START)


def choose_action(q_table: dict, state: str, epsilon: float) -> str:
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    q_values = q_table[state]
    return max(ACTIONS, key=lambda a: q_values[a])


def run_episode(q_table: dict, episode: int, *, learn: bool) -> float:
    table = new_table()
    state = get_state(table)
    epsilon = epsilon_for(episode) if learn else 0.0

    for _ in range(ROLLS_PER_EPISODE):
        if table.credit + table.total_bet <= 0:
            break  # busted

        action = choose_action(q_table, state, epsilon)
        reward = take_action(table, action)
        next_state = get_state(table)

        if learn:
            best_next = max(q_table[next_state].values(), default=0.0)
            td_target = reward + GAMMA * best_next
            q_table[state][action] += ALPHA * (td_target - q_table[state][action])

        state = next_state

    return table.credit + table.total_bet  # final bankroll


def main() -> None:
    q_table: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))

    print(f"Training for {TRAIN_EPISODES} episodes...")
    for episode in range(TRAIN_EPISODES):
        run_episode(q_table, episode, learn=True)

    print("\nLearned action preference by state:")
    for state in ("come_out", "point_on"):
        values = dict(q_table[state])
        best = max(ACTIONS, key=lambda a: values.get(a, 0.0))
        print(f"  {state:10s} -> {best:10s}   Q={values}")

    print(f"\nEvaluating greedily over {EVAL_EPISODES} episodes...")
    bankrolls = [run_episode(q_table, TRAIN_EPISODES, learn=False) for _ in range(EVAL_EPISODES)]
    avg = sum(bankrolls) / len(bankrolls)
    print(f"Average final bankroll (started at ${STARTING_CREDIT:.2f}): ${avg:.2f}")


if __name__ == "__main__":
    main()
