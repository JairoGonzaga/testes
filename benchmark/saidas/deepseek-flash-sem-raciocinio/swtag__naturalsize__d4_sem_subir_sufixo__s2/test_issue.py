import pytest

from alvo import naturalsize


def test_issue_example():
    # 999999 bytes formats as 1000.0, so the unit must be promoted to MB.
    assert naturalsize(999999) == "1.0 MB"


def test_no_unit_overflow_decimal():
    # 999999999 bytes -> 1000.0 MB must be promoted to 1.0 GB
    assert naturalsize(999999999) == "1.0 GB"
    # just below the promotion point, unit stays kB
    assert naturalsize(999949) == "999.9 kB"
    # 999950 rounds to 1000.0 kB -> promote to 1.0 MB
    assert naturalsize(999950) == "1.0 MB"


def test_no_unit_overflow_binary():
    assert naturalsize(1048575, binary=True) == "1.0 MiB"
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1024 * 1024, binary=True) == "1.0 MiB"


def test_no_unit_overflow_gnu():
    assert naturalsize(1024, gnu=True) == "1.0K"
    assert naturalsize(1024 * 1024 - 1, gnu=True) == "1.0M"


def test_negative_values_promote():
    assert naturalsize(-999999) == "-1.0 MB"


def test_regular_values_unchanged():
    assert naturalsize(0) == "0 Bytes"
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(1000000) == "1.0 MB"
    assert naturalsize(1536) == "1.5 kB"
