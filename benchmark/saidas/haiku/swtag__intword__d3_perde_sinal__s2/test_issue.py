from alvo import intword


def test_negative_million_keeps_minus_sign():
    assert intword(-1000000) == "-1.0 million"


def test_negative_thousand_keeps_minus_sign():
    assert intword(-1000) == "-1.0 thousand"


def test_negative_fractional_million_keeps_minus_sign():
    assert intword(-1500000) == "-1.5 million"


def test_negative_rounding_to_next_unit_keeps_minus_sign():
    assert intword(-999999) == "-1.0 million"


def test_negative_small_value_keeps_minus_sign():
    assert intword(-5) == "-5"


def test_positive_values_are_unchanged():
    assert intword(1000000) == "1.0 million"
    assert intword(1000) == "1.0 thousand"
    assert intword(5) == "5"
