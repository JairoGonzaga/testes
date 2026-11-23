from alvo import intword


def test_negative_million_keeps_minus_sign():
    assert intword(-1000000) == "-1.0 million"


def test_negative_million_with_fraction_keeps_minus_sign():
    assert intword(-1500000) == "-1.5 million"


def test_negative_billion_keeps_minus_sign():
    assert intword(-1000000000) == "-1.0 billion"


def test_negative_thousand_keeps_minus_sign():
    assert intword(-1000) == "-1.0 thousand"


def test_negative_small_value_keeps_minus_sign():
    assert intword(-5) == "-5"


def test_negative_rounding_carry_keeps_minus_sign():
    assert intword(-999999999) == "-1.0 billion"


def test_negative_custom_format_keeps_minus_sign():
    assert intword(-1000000, format="%.2f") == "-1.00 million"


def test_negative_string_input_keeps_minus_sign():
    assert intword("-1000000") == "-1.0 million"


def test_positive_value_unchanged():
    assert intword(1000000) == "1.0 million"
