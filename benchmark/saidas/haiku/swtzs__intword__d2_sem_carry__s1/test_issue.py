from alvo import intword


def test_rounding_up_to_next_power_promotes_suffix():
    # Issue: intword(999999) returned '1000.0 thousand' instead of '1.0 million'.
    assert intword(999999) == "1.0 million"


def test_rounding_up_to_billion_promotes_suffix():
    # Same bug one power higher: 999999999 rounds to '1000.0 million'.
    assert intword(999999999) == "1.0 billion"


def test_negative_rounding_up_promotes_suffix():
    assert intword(-999999) == "-1.0 million"


def test_no_promotion_when_rounding_stays_below_next_power():
    # Control case: 999.0 does not reach the next power, so the suffix must stay.
    assert intword(999000) == "999.0 thousand"
