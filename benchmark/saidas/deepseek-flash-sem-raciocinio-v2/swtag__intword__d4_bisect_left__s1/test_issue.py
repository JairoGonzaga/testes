from alvo import intword


def test_googol_is_one_googol():
    assert intword(10**100) == "1.0 googol"


def test_negative_googol():
    assert intword(-(10**100)) == "-1.0 googol"


def test_two_googols():
    assert intword(2 * 10**100) == "2.0 googol"
