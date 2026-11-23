from alvo import naturalsize


def test_naturalsize_negative_one_is_singular_byte():
    assert naturalsize(-1) == "-1 Byte"


def test_naturalsize_positive_one_is_singular_byte():
    assert naturalsize(1) == "1 Byte"


def test_naturalsize_zero_is_plural_bytes():
    assert naturalsize(0) == "0 Bytes"


def test_naturalsize_negative_two_is_plural_bytes():
    assert naturalsize(-2) == "-2 Bytes"
