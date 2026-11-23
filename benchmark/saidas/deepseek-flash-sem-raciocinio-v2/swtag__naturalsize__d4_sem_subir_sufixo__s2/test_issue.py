from alvo import naturalsize


def test_promotes_unit_when_rounding_overflows_decimal():
    assert naturalsize(999999) == "1.0 MB"


def test_promotes_unit_when_rounding_overflows_decimal_mid():
    assert naturalsize(999999999) == "1.0 GB"


def test_promotes_unit_when_rounding_overflows_binary():
    assert naturalsize(1024 * 1024 - 1, binary=True) == "1.0 MiB"


def test_promotes_unit_when_rounding_overflows_gnu():
    assert naturalsize(1024 * 1024 - 1, gnu=True) == "1.0M"


def test_no_promotion_when_rounding_does_not_overflow():
    assert naturalsize(999949) == "999.9 kB"
    assert naturalsize(1000) == "1.0 kB"
