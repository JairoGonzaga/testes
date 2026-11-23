from alvo import intword


def test_intword_exactly_one_thousand():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_one_thousand():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_just_below_thousand_unchanged():
    assert intword(999) == "999"
