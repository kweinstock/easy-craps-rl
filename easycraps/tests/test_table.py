from easycraps import Table


def make_table(credit=100.0):
    table = Table(credit=credit, seed=0)
    table.set_min_bet(1)
    return table


def test_table_starts_with_credit():
    table = Table(credit=50)
    assert table.credit == 50


def test_named_bet_methods_place_bets():
    table = make_table(100)
    result = table.pass_line_bet(10)
    assert result.ok
    assert table.credit == 90
    assert table.bets["pass"] == 10


def test_field_bet_and_roll():
    table = make_table(100)
    table.field_bet(5)
    before = table.credit
    result = table.roll(d1=1, d2=1)  # total 2, field pays double
    assert result.ok
    assert table.credit == before + 15  # win 10 + stake 5


def test_hard_way_bet_via_named_method():
    table = make_table(100)
    table.hard_way_bet(6, 1)
    before = table.credit
    table.roll(d1=3, d2=3)
    assert table.credit == before + 10


def test_hop_bet_via_named_method():
    table = make_table(100)
    table.hop_bet(4, 3, 1)
    before = table.credit
    table.roll(d1=4, d2=3)
    assert table.credit == before + 16  # non-double pays 15:1, total return 16


def test_bad_spot_raises_trigger_error():
    from easycraps import TriggerError

    table = make_table(100)
    try:
        table.bet("not_a_real_spot", 1)
        assert False, "expected TriggerError"
    except TriggerError:
        pass


def test_result_is_falsy_when_rejected():
    table = make_table(0)
    result = table.pass_line_bet(10)  # no credit
    assert not result
    assert not result.ok


def test_deterministic_seed_reproducible():
    a = Table(credit=100, seed=42)
    b = Table(credit=100, seed=42)
    a.set_min_bet(1)
    b.set_min_bet(1)
    a.field_bet(1)
    b.field_bet(1)
    ra = a.roll()
    rb = b.roll()
    assert ra.state["last_roll"]["dice"] == rb.state["last_roll"]["dice"]
