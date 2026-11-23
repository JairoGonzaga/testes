from alvo import intword


def test_negative_million_keeps_sign():
    assert intword(-1000000) == "-1.0 million"


def test_negative_thousand_keeps_sign():
    assert intword(-1234) == "-1.2 thousand"


def test_negative_billion_keeps_sign():
    assert intword(-2500000000) == "-2.5 billion"


def test_positive_unchanged():
    assert intword(1000000) == "1.0 million"


def test_negative_small_no_unit():
    assert intword(-999) == "-999"
