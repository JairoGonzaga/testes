from alvo import intword


def test_negative_million():
    assert intword(-1000000) == "-1.0 million"


def test_negative_small():
    assert intword(-500) == "-500"


def test_negative_rounding():
    assert intword(-1500000000) == "-1.5 billion"
