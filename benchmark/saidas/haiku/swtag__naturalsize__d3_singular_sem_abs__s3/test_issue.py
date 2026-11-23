"""Reproduces the issue: naturalsize(-1) must use the singular 'Byte'."""

from alvo import naturalsize


def test_negative_one_byte_uses_singular():
    # The bug: naturalsize(-1) returns '-1 Bytes' instead of '-1 Byte'.
    assert naturalsize(-1) == "-1 Byte"


def test_positive_one_byte_uses_singular():
    # Already correct today; guards against a fix that breaks the positive case.
    assert naturalsize(1) == "1 Byte"


def test_negative_multiple_bytes_stays_plural():
    # Only exactly one byte (either sign) should use the singular form.
    assert naturalsize(-2) == "-2 Bytes"
