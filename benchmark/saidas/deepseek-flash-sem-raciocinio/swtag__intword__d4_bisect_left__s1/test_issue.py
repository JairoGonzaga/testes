from alvo import intword


def test_googol():
    assert intword(10**100) == "1.0 googol"


def test_googol_with_decimals():
    assert intword(10**100, "%.2f") == "1.00 googol"


def test_values_just_below_googol_still_use_decillion():
    assert intword(10**99) == "1.0 decillion"


def test_negative_googol():
    assert intword(-(10**100)) == "-1.0 googol"


def test_decillion_still_works():
    assert intword(10**33) == "1.0 decillion"
    assert intword(10**34) == "10.0 decillion"
