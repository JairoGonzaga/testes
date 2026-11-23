from alvo import naturalsize


def test_binary_issue_example_uses_powers_of_1024():
    # 3000000 / 1024**2 = 2.86..., so the expected output is '2.9 MiB'
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_mebibytes_are_not_computed_with_powers_of_1000():
    # 1500000 / 1024**2 = 1.43..., not 1500000 / 1000**2 = 1.5
    assert naturalsize(1500000, binary=True) == "1.4 MiB"


def test_binary_negative_value_uses_powers_of_1024():
    assert naturalsize(-3000000, binary=True) == "-2.9 MiB"


def test_binary_values_below_1024_are_shown_in_bytes():
    # 1000 and 1023 are below 1 KiB, so they must not be shown as KiB
    assert naturalsize(1000, binary=True) == "1000 Bytes"
    assert naturalsize(1023, binary=True) == "1023 Bytes"


def test_binary_one_kib_boundary():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_gnu_still_uses_powers_of_1024():
    assert naturalsize(3000000, gnu=True) == "2.9M"


def test_decimal_default_still_uses_powers_of_1000():
    assert naturalsize(3000000) == "3.0 MB"
