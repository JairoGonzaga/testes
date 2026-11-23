from alvo import intword


def test_negative_million_keeps_sign():
    assert intword(-1000000) == "-1.0 million"


def test_positive_million_still_works():
    assert intword(1000000) == "1.0 million"


def test_negative_thousand_keeps_sign():
    assert intword(-2000) == "-2.0 thousand"


def test_negative_small_number_keeps_sign():
    assert intword(-42) == "-42"


def test_negative_billion_keeps_sign():
    assert intword(-1500000000) == "-1.5 billion"


def test_negative_with_custom_format():
    assert intword(-1234567, "%.2f") == "-1.23 million"


def test_negative_rounding_rollover_keeps_sign():
    assert intword(-999999) == "-1.0 million"
