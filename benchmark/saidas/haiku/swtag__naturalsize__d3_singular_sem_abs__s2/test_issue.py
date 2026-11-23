from alvo import naturalsize


def test_negative_one_byte_uses_singular_decimal():
    # naturalsize(-1) currently returns '-1 Bytes'; the singular form is expected.
    assert naturalsize(-1) == "-1 Byte"


def test_negative_one_byte_uses_singular_binary():
    # Same bug for the binary (base 1024) code path.
    assert naturalsize(-1, binary=True) == "-1 Byte"
