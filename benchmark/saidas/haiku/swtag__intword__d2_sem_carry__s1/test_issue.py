from alvo import intword


def test_intword_promotes_suffix_when_rounding_reaches_next_power():
    # 999999 / 1000 = 999.999, which "%.1f" rounds to "1000.0".
    # The suffix must move up to "million" instead of "1000.0 thousand".
    assert intword(999999) == "1.0 million"


def test_intword_promotes_suffix_at_billion_boundary():
    assert intword(999999999) == "1.0 billion"


def test_intword_promotes_suffix_at_trillion_boundary():
    assert intword(999999999999) == "1.0 trillion"


def test_intword_promotes_suffix_for_negative_values():
    assert intword(-999999) == "-1.0 million"


def test_intword_exact_power_boundary_is_unchanged():
    assert intword(1000000) == "1.0 million"
