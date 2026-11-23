from alvo import intword


def test_rounding_promotes_suffix():
    assert intword(999999) == "1.0 million"


def test_rounding_promotes_suffix_million():
    assert intword(999999999) == "1.0 billion"


def test_rounding_promotes_suffix_negative():
    assert intword(-999999) == "-1.0 million"


def test_no_promotion_when_not_rounded():
    assert intword(999) == "999"
    assert intword(1000) == "1.0 thousand"
    assert intword(999499) == "999.5 thousand"
