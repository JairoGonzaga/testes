from alvo import intword


def test_googol():
    assert intword(10**100) == "1.0 googol"


def test_googol_negative():
    assert intword(-(10**100)) == "-1.0 googol"


def test_googol_larger():
    assert intword(5 * 10**100) == "5.0 googol"


def test_googol_boundary_below():
    # Largest value still using decillion should not be googol
    assert intword(10**99).endswith("googol") is False


def test_decillion_still_works():
    assert intword(10**33) == "1.0 decillion"
