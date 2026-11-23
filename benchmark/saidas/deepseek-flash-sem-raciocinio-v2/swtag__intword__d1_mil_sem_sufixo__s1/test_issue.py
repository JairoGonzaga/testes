from alvo import intword


def test_intword_1000_is_humanized():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_1000_is_humanized():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_just_below_1000_unchanged():
    assert intword(999) == "999"


def test_intword_above_1000_still_humanized():
    assert intword(1001) == "1.0 thousand"
    assert intword(1500) == "1.5 thousand"
