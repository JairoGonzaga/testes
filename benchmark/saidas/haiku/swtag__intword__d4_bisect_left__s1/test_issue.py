from alvo import intword


def test_googol_is_humanized_as_googol():
    # intword(10**100) must read '1.0 googol', not a huge number
    # with the 'decillion' suffix.
    assert intword(10**100) == "1.0 googol"


def test_googol_does_not_fall_back_to_decillion():
    assert "decillion" not in intword(10**100)


def test_decillion_still_humanized_as_decillion():
    # Guard: the boundary just below the googol keeps working.
    assert intword(10**33) == "1.0 decillion"
