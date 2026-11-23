from alvo import naturalsize


def test_binary_issue_example_uses_powers_of_1024():
    # 3000000 / 1024**2 = 2.86... -> '2.9 MiB' (the buggy code gives '3.0 MiB')
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_two_million_bytes_is_1_9_mib():
    assert naturalsize(2000000, binary=True) == "1.9 MiB"


def test_binary_five_gib_uses_1024_cubed():
    assert naturalsize(5 * 1024**3, binary=True) == "5.0 GiB"


def test_binary_values_below_1024_stay_in_bytes():
    assert naturalsize(1000, binary=True) == "1000 Bytes"


def test_decimal_still_uses_powers_of_1000():
    assert naturalsize(3000000) == "3.0 MB"


def test_gnu_still_uses_powers_of_1024():
    assert naturalsize(3000000, gnu=True) == "2.9M"
