from alvo import intword


def test_negative_million_keeps_minus_sign():
    assert intword(-1000000) == "-1.0 million"


def test_negative_small_number_keeps_minus_sign():
    assert intword(-500) == "-500"


def test_negative_billion_keeps_minus_sign():
    assert intword(-2000000000) == "-2.0 billion"


def test_positive_values_unchanged():
    assert intword(1000000) == "1.0 million"
    assert intword(500) == "500"
