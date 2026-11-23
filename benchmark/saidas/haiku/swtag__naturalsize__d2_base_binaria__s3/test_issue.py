from alvo import naturalsize


def test_binary_issue_example_uses_powers_of_1024():
    # ISSUE.md: 3000000 / 1024**2 = 2.86..., so the result must be '2.9 MiB'.
    # The buggy code divides by 1000**2 and returns '3.0 MiB'.
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_gibibytes_use_powers_of_1024():
    # 2 * 1024**3 bytes is exactly 2.0 GiB. The buggy code divides by 1000**3
    # and returns '2.1 GiB'.
    assert naturalsize(2 * 1024**3, binary=True) == "2.0 GiB"


def test_binary_1000_bytes_is_plain_bytes():
    # 1000 bytes is below 1 KiB (1024 bytes), so it must be shown as bytes.
    # The buggy code treats 1000 as 1 KiB and returns '1.0 KiB'.
    assert naturalsize(1000, binary=True) == "1000 Bytes"


def test_binary_1023_bytes_is_plain_bytes():
    # 1023 bytes is still below 1 KiB, so it must not be shown as KiB.
    assert naturalsize(1023, binary=True) == "1023 Bytes"


def test_decimal_default_is_unchanged():
    # Regression guard: the default (decimal) mode must keep powers of 1000.
    assert naturalsize(3000000) == "3.0 MB"


def test_gnu_mode_is_unchanged():
    # Regression guard: GNU mode already uses powers of 1024.
    assert naturalsize(3000000, gnu=True) == "2.9M"
