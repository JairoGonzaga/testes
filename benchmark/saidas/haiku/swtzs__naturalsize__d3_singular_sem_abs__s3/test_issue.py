from alvo import naturalsize


def test_positive_one_byte_is_singular():
    assert naturalsize(1) == "1 Byte"


def test_negative_one_byte_is_singular():
    assert naturalsize(-1) == "-1 Byte"
