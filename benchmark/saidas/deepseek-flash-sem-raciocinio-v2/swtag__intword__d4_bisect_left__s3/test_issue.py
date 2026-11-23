from alvo import intword


def test_googol():
    assert intword(10**100) == "1.0 googol"


def test_negative_googol():
    assert intword(-(10**100)) == "-1.0 googol"


def test_small_values_still_work():
    assert intword(1234) == "1.2 thousand"
    assert intword(10**33) == "1.0 decillion"
