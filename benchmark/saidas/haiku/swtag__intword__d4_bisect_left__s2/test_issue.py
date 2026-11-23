from alvo import intword


def test_googol_is_humanized_as_one_googol():
    # intword(10**100) used to return a 67-digit number with the "decillion"
    # suffix instead of "1.0 googol".
    assert intword(10**100) == "1.0 googol"


def test_negative_googol_is_humanized_as_one_googol():
    assert intword(-(10**100)) == "-1.0 googol"
