from alvo import intword


def test_intword_negative_million():
    assert intword(-1000000) == "-1.0 million"


def test_intword_positive_million_unchanged():
    assert intword(1000000) == "1.0 million"


def test_intword_negative_below_thousand():
    assert intword(-12) == "-12"
