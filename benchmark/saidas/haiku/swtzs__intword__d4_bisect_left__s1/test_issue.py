from alvo import intword


def test_googol_is_humanized_as_one_googol():
    # Issue: intword(10**100) returns a huge number with 'decillion'
    # instead of '1.0 googol', because the float comparison against
    # powers[11] // power never matches.
    assert intword(10**100) == "1.0 googol"


def test_negative_googol_is_humanized_as_one_googol():
    # Same code path as the positive case, with the sign prefix kept.
    assert intword(-(10**100)) == "-1.0 googol"
