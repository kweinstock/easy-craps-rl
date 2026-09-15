import random

from easycraps import Game


def make_game(credit=100.0):
    game = Game(rng=random.Random(0))
    game.apply("add_funds", {"amount": credit})
    game.apply("set_min_bet", {"amount": 1})
    return game


def test_place_bet_deducts_credit_and_tracks_spot():
    game = make_game(100)
    result = game.apply("place_bet", {"spot": "pass", "amount": 10})
    assert result["ok"]
    assert result["state"]["credit"] == 90
    assert result["state"]["bets"]["pass"] == 10


def test_come_out_seven_wins_pass_line():
    game = make_game(100)
    game.apply("place_bet", {"spot": "pass", "amount": 10})
    result = game.apply("roll", {"d1": 3, "d2": 4})  # 7
    assert result["state"]["point"] is None
    assert result["state"]["credit"] == 90 + 20  # stake back + 1:1 win


def test_non_seven_establishes_point():
    game = make_game(100)
    game.apply("place_bet", {"spot": "pass", "amount": 10})
    result = game.apply("roll", {"d1": 2, "d2": 2})  # 4
    assert result["state"]["point"] == 4


def test_seven_out_loses_pass_and_place():
    game = make_game(100)
    game.apply("place_bet", {"spot": "pass", "amount": 10})
    game.apply("roll", {"d1": 2, "d2": 2})  # point = 4
    game.apply("place_bet", {"spot": "place_6", "amount": 6})
    result = game.apply("roll", {"d1": 3, "d2": 4})  # 7, seven-out
    assert result["state"]["point"] is None
    assert "pass" not in result["state"]["bets"]
    assert "place_6" not in result["state"]["bets"]


def test_place_bet_pays_correct_multiplier():
    game = make_game(100)
    game.apply("place_bet", {"spot": "pass", "amount": 10})
    game.apply("roll", {"d1": 2, "d2": 2})  # point = 4, avoids immediately resolving place bet
    game.apply("place_bet", {"spot": "place_6", "amount": 6})
    before = game.state.credit
    result = game.apply("roll", {"d1": 2, "d2": 4})  # 6
    # 6 pays 7:6 total return multiplier 13/6 -> 6 * 13/6 = 13
    assert result["state"]["credit"] == before + 13
    assert "place_6" not in result["state"]["bets"]


def test_hard_way_wins_on_exact_pair():
    game = make_game(100)
    game.apply("place_bet", {"spot": "hard_6", "amount": 1})
    before = game.state.credit
    result = game.apply("roll", {"d1": 3, "d2": 3})
    assert result["state"]["credit"] == before + 10  # 9:1 total return multiplier 10
    assert game.state.hard_since[6] == 0


def test_hard_way_loses_on_easy_way():
    game = make_game(100)
    game.apply("place_bet", {"spot": "hard_6", "amount": 1})
    result = game.apply("roll", {"d1": 2, "d2": 4})  # 6 the easy way
    assert "hard_6" not in result["state"]["bets"]


def test_field_pays_double_on_two_and_twelve():
    game = make_game(100)
    game.apply("place_bet", {"spot": "field", "amount": 5})
    before = game.state.credit
    result = game.apply("roll", {"d1": 1, "d2": 1})  # 2
    assert result["state"]["credit"] == before + 15  # win 10 + stake 5


def test_lucky_lowrolls_needs_all_numbers_before_seven():
    game = make_game(100)
    game.apply("place_bet", {"spot": "lowrolls", "amount": 1})
    for d1, d2 in [(1, 1), (1, 2), (1, 3), (2, 2)]:  # 2,3,4,4 -- missing 5,6
        game.apply("roll", {"d1": d1, "d2": d2})
    assert "lowrolls" in game.state.bets
    before = game.state.credit
    game.apply("roll", {"d1": 1, "d2": 4})  # 5
    game.apply("roll", {"d1": 1, "d2": 5})  # 6 -> completes set {2,3,4,5,6}
    assert "lowrolls" not in game.state.bets
    assert game.state.credit == before + 31  # 30:1 total return multiplier 31


def test_invalid_trigger_raises():
    game = make_game(100)
    try:
        game.apply("not_a_trigger", {})
        assert False, "expected TriggerError"
    except Exception as exc:
        assert "Unknown trigger" in str(exc)
