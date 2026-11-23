from alvo import intword


def test_negative_million():
    assert intword(-1000000) == "-1.0 million"


def test_negative_thousand():
    assert intword(-1500) == "-1.5 thousand"


def test_negative_billion():
    assert intword(-2000000000) == "-2.0 billion"


def test_negative_googol_scale():
    assert intword(-10**100) == "-1.0 googol"


def test_negative_small():
    assert intword(-999) == "-999"


def test_positive_unchanged():
    assert intword(1000000) == "1.0 million"
    assert intword(999) == "999"
