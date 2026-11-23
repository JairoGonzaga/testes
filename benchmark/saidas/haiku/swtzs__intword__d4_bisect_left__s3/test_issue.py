from alvo import intword


def test_googol_is_humanized_as_one_googol():
    assert intword(10**100) == "1.0 googol"


def test_negative_googol_keeps_sign():
    assert intword(-(10**100)) == "-1.0 googol"
