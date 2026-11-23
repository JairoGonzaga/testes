from alvo import naturalsize


def test_decimal_rounding_up_promotes_to_next_unit():
    # 999999 B is 999.999 kB, which rounds to 1000.0 kB; the unit must become MB.
    assert naturalsize(999999) == "1.0 MB"


def test_decimal_rounding_up_promotes_to_next_unit_gb():
    # 999999999 B is 999.999999 MB, which rounds to 1000.0 MB; the unit must become GB.
    assert naturalsize(999999999) == "1.0 GB"


def test_binary_rounding_up_promotes_to_next_unit():
    # 1048575 B is 1023.999 KiB, which rounds to 1024.0 KiB; the unit must become MiB.
    assert naturalsize(1048575, binary=True) == "1.0 MiB"


def test_gnu_rounding_up_promotes_to_next_unit():
    # 1048575 B is 1023.999 KiB in GNU style, which rounds to 1024.0K; the unit must become M.
    assert naturalsize(1048575, gnu=True) == "1.0M"
