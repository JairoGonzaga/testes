from alvo import naturalsize


def test_naturalsize_promotes_unit_when_rounding_crosses_boundary():
    assert naturalsize(999999) == "1.0 MB"


def test_naturalsize_promotes_unit_for_larger_decimal_boundary():
    assert naturalsize(999999999) == "1.0 GB"
