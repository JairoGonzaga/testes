from alvo import naturalsize


def test_naturalsize_promotes_unit_after_rounding():
    assert naturalsize(999999) == "1.0 MB"


def test_naturalsize_promotes_binary_unit_after_rounding():
    assert naturalsize(1024 * 1023.99, binary=True) == "1.0 MiB"
