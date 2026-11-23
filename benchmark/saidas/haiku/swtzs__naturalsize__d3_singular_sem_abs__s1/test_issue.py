from alvo import naturalsize


def test_negative_one_byte_uses_singular():
    # Issue: naturalsize(-1) returns '-1 Bytes' instead of '-1 Byte'.
    assert naturalsize(-1) == "-1 Byte"


def test_positive_one_byte_uses_singular():
    # Control case: already correct, must keep passing.
    assert naturalsize(1) == "1 Byte"


def test_negative_one_byte_binary_uses_singular():
    # Same bug in binary mode: abs value is below the 1024 base.
    assert naturalsize(-1, binary=True) == "-1 Byte"


def test_negative_multiple_bytes_stays_plural():
    # Only exactly one byte should use the singular form.
    assert naturalsize(-2) == "-2 Bytes"
