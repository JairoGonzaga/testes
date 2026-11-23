from alvo import naturalsize


def test_naturalsize_minus_one_uses_singular_byte():
    assert naturalsize(-1) == "-1 Byte"


def test_naturalsize_minus_two_uses_plural_bytes():
    assert naturalsize(-2) == "-2 Bytes"


def test_naturalsize_one_uses_singular_byte():
    assert naturalsize(1) == "1 Byte"
