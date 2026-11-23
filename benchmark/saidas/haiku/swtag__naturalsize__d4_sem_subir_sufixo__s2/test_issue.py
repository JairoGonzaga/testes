from alvo import naturalsize


def test_decimal_rounding_up_promotes_unit():
    # 999999 bytes is 999.999 kB, which rounds to "1000.0" at one decimal
    # place. The unit must be promoted to MB, giving "1.0 MB".
    assert naturalsize(999999) == "1.0 MB"


def test_binary_rounding_up_promotes_unit():
    # 1048575 bytes is 1023.999 KiB, which rounds to "1024.0" at one decimal
    # place. The unit must be promoted to MiB, giving "1.0 MiB".
    assert naturalsize(1048575, binary=True) == "1.0 MiB"


def test_no_promotion_when_rounding_stays_below_next_unit():
    # 999949 bytes is 999.949 kB, which rounds to "999.9" and must stay in kB.
    assert naturalsize(999949) == "999.9 kB"
