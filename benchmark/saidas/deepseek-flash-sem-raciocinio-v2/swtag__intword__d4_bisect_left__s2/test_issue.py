from alvo import intword


def test_googol():
    assert intword(10 ** 100) == "1.0 googol"


def test_negative_googol():
    assert intword(-(10 ** 100)) == "-1.0 googol"


def test_decillion_still_works():
    assert intword(10 ** 33) == "1.0 decillion"
