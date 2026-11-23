from alvo import intword


def test_rounding_up_promotes_suffix_thousand_to_million():
    assert intword(999999) == "1.0 million"


def test_rounding_up_promotes_suffix_million_to_billion():
    assert intword(999999999) == "1.0 billion"


def test_rounding_up_promotes_suffix_negative():
    assert intword(-999999) == "-1.0 million"


def test_no_promotion_needed_still_works():
    assert intword(1234567) == "1.2 million"
    assert intword(999) == "999"
    assert intword(1000) == "1.0 thousand"
