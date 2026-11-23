from alvo import intword


def test_intword_999999_promotes_to_million():
    assert intword(999999) == "1.0 million"


def test_intword_999999_negative():
    assert intword(-999999) == "-1.0 million"


def test_intword_999999999_promotes_to_billion():
    assert intword(999999999) == "1.0 billion"


def test_intword_no_promotion_below_threshold():
    assert intword(999949) == "999.9 thousand"
