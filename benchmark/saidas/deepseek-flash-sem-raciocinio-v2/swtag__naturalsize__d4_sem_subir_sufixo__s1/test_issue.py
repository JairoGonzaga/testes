from alvo import naturalsize


def test_rounding_up_promotes_to_next_unit():
    assert naturalsize(999999) == "1.0 MB"


def test_rounding_up_promotes_to_next_unit_larger():
    assert naturalsize(999999999) == "1.0 GB"


def test_rounding_up_promotes_to_next_unit_terabyte():
    assert naturalsize(999999999999) == "1.0 TB"


def test_no_premature_promotion_when_not_rounded_up():
    assert naturalsize(999949) == "999.9 kB"
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1) == "1 Byte"


def test_binary_and_gnu_unchanged_for_normal_values():
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1024, gnu=True) == "1.0K"
    assert naturalsize(999, gnu=True) == "999B"
