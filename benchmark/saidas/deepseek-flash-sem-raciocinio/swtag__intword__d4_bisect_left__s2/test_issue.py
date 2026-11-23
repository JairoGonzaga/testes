from alvo import intword


def test_googol():
    assert intword(10**100) == "1.0 googol"


def test_negative_googol():
    assert intword(-(10**100)) == "-1.0 googol"


def test_just_below_googol():
    assert intword(10**100 - 1).endswith("decillion")


def test_just_above_googol():
    assert intword(10**100 * 2) == "2.0 googol"


def test_decillion():
    assert intword(10**33) == "1.0 decillion"
