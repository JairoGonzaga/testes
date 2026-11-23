from alvo import intword


def test_googol_is_humanized_as_one_point_zero_googol():
    assert intword(10**100) == "1.0 googol"


def test_negative_googol_is_humanized_as_negative_one_point_zero_googol():
    assert intword(-(10**100)) == "-1.0 googol"


def test_decillion_is_still_humanized_as_one_point_zero_decillion():
    assert intword(10**33) == "1.0 decillion"
