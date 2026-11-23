from alvo import naturalsize


def test_naturalsize_promotes_unit_when_rounding_reaches_next_unit():
    assert naturalsize(999999) == "1.0 MB"
