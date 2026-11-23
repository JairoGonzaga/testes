"""Reproduction tests for: naturalsize(binary=True) gives wrong values.

With ``binary=True`` the size must be scaled by powers of 1024 (KiB, MiB, ...).
The buggy implementation always uses base 1000 unless ``gnu=True``, so binary
results are computed with powers of 1000.
"""

import pytest

from alvo import naturalsize

KIB = 1024
MIB = 1024 ** 2
GIB = 1024 ** 3
TIB = 1024 ** 4


def test_issue_example_from_report():
    # 3_000_000 / 1024**2 = 2.86... -> "2.9 MiB"
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


@pytest.mark.parametrize(
    "value, expected",
    [
        # below one kibibyte: still bytes (and NOT scaled by 1000)
        (0, "0 Bytes"),
        (1, "1 Byte"),
        (2, "2 Bytes"),
        (1000, "1000 Bytes"),
        (1023, "1023 Bytes"),
        # exact powers of 1024
        (KIB, "1.0 KiB"),
        (2 * KIB, "2.0 KiB"),
        (MIB, "1.0 MiB"),
        (GIB, "1.0 GiB"),
        (TIB, "1.0 TiB"),
        # non-round values
        (int(1.5 * MIB), "1.5 MiB"),
        (int(KIB ** 2 * 1.5 * 2), "3.0 MiB"),
        (int(2.5 * GIB), "2.5 GiB"),
        (3000000, "2.9 MiB"),
        (1023 * MIB, "1023.0 MiB"),
        (int(1023.96 * KIB), "1.0 MiB"),
        # negative values
        (-3000000, "-2.9 MiB"),
        (-KIB, "-1.0 KiB"),
    ],
)
def test_binary_uses_powers_of_1024(value, expected):
    assert naturalsize(value, binary=True) == expected


def test_binary_base_is_1024():
    # If the base were 1000, 1024 would be reported as "1.0 kB"-style scaling;
    # with the correct base it stays a plain byte count below 1024.
    assert naturalsize(1023, binary=True) == "1023 Bytes"
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    # The classic tell-tale: MiB must be value / 1024**2.
    assert naturalsize(10 * MIB, binary=True) == "10.0 MiB"


def test_binary_respects_format_argument():
    assert naturalsize(KIB, binary=True, format="%.0f") == "1 KiB"
    assert naturalsize(int(2.25 * MIB), binary=True, format="%.2f") == "2.25 MiB"


def test_decimal_mode_unchanged():
    assert naturalsize(3000000) == "3.0 MB"
    assert naturalsize(1024) == "1.0 kB"
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1) == "1 Byte"


def test_gnu_mode_unchanged():
    assert naturalsize(1024, gnu=True) == "1.0K"
    assert naturalsize(1024 ** 2, gnu=True) == "1.0M"
    assert naturalsize(1023, gnu=True) == "1023B"
