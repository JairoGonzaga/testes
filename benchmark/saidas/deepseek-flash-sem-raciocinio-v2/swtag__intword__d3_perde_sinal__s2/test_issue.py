from alvo import intword


def test_negative_million():
    assert intword(-1000000) == "-1.0 million"


def test_negative_thousand():
    assert intword(-1000) == "-1.0 thousand"


def test_negative_below_powers():
    assert intword(-999) == "-999"


def test_negative_non_integer_value():
    assert intword(-2500000) == "-2.5 million"


def test_positive_still_works():
    assert intword(1000000) == "1.0 million"
