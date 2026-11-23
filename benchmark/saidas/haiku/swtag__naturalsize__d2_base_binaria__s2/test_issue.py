from alvo import naturalsize


def test_binary_issue_example_uses_powers_of_1024():
    # 3000000 / 1024**2 = 2.86... so the expected output is '2.9 MiB'.
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_mebibyte_value_uses_base_1024():
    # 1536 * 1024 bytes is exactly 1.5 MiB when binary units use 1024.
    assert naturalsize(1536 * 1024, binary=True) == "1.5 MiB"


def test_binary_value_below_1024_is_shown_in_bytes():
    # 1000 bytes is below one KiB when KiB means 1024 bytes.
    assert naturalsize(1000, binary=True) == "1000 Bytes"
