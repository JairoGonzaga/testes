from alvo import intword


def test_negative_million_keeps_minus_sign():
    assert intword(-1000000) == "-1.0 million"


def test_negative_thousand_keeps_minus_sign():
    assert intword(-1234) == "-1.2 thousand"


def test_negative_small_number_keeps_minus_sign():
    assert intword(-999) == "-999"


def test_negative_googol_keeps_minus_sign():
    assert intword(-(10**100)) == "-1.0 googol"


def test_negative_sign_is_never_dropped():
    # Every negative input must come back with a leading minus sign.
    for value in (-1, -12, -999, -1000, -1234567, -10**9, -10**12, -(10**100)):
        result = intword(value)
        assert result.startswith("-"), f"sign dropped for {value}: {result!r}"


def test_positive_values_unaffected():
    assert intword(0) == "0"
    assert intword(999) == "999"
    assert intword(1234) == "1.2 thousand"
    assert intword(1000000) == "1.0 million"
    assert intword(10**100) == "1.0 googol"
