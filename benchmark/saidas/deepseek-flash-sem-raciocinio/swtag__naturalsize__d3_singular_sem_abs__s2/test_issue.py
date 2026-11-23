from alvo import naturalsize


def test_negative_one_is_singular():
    assert naturalsize(-1) == "-1 Byte"


def test_positive_one_is_singular():
    assert naturalsize(1) == "1 Byte"


def test_zero_and_plural():
    assert naturalsize(0) == "0 Bytes"
    assert naturalsize(2) == "2 Bytes"


def test_binary_negative_one():
    assert naturalsize(-1, binary=True) == "-1 Byte"
