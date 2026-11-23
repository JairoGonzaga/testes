from alvo import naturalsize


def test_decimal_rounding_up_promotes_unit():
    # 999999 bytes is 999.999 kB, which "%.1f" rounds to "1000.0"; the unit must move up to MB.
    assert naturalsize(999999) == "1.0 MB"


def test_binary_rounding_up_promotes_unit():
    # 1048575 bytes is 1023.999 KiB, which "%.1f" rounds to "1024.0"; the unit must move up to MiB.
    assert naturalsize(1024**2 - 1, binary=True) == "1.0 MiB"


def test_gnu_rounding_up_promotes_unit():
    # Same rounding overflow in GNU style: "1024.0K" must become "1.0M".
    assert naturalsize(1024**2 - 1, gnu=True) == "1.0M"


def test_values_that_do_not_round_up_keep_their_unit():
    assert naturalsize(999000) == "999.0 kB"
    assert naturalsize(1000) == "1.0 kB"
