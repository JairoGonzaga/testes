from alvo import naturalsize


def test_negative_one_byte_singular():
    assert naturalsize(-1) == "-1 Byte"


def test_positive_one_byte_singular():
    assert naturalsize(1) == "1 Byte"


def test_negative_one_byte_gnu():
    assert naturalsize(-1, gnu=True) == "-1B"


def test_negative_small_values_plural():
    assert naturalsize(-2) == "-2 Bytes"
    assert naturalsize(-512) == "-512 Bytes"


def test_negative_large_value():
    assert naturalsize(-1000) == "-1.0 kB"
