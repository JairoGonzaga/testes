from alvo import intword


def test_intword_exactly_one_thousand_is_humanized():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_exactly_one_thousand_is_humanized():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_below_one_thousand_is_unchanged():
    assert intword(999) == "999"
