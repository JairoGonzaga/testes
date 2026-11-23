from alvo import naturalsize


def test_rounding_up_promotes_unit():
    assert naturalsize(999999) == "1.0 MB"


def test_rounding_up_promotes_unit_binary():
    assert naturalsize(1024 * 1024 - 1, binary=True) == "1.0 MiB"


def test_no_change_for_in_range_values():
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(1500) == "1.5 kB"
    assert naturalsize(1536, binary=True) == "1.5 KiB"
