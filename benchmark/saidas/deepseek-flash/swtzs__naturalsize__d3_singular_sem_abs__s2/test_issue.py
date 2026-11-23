from alvo import naturalsize


def test_naturalsize_negative_one_uses_singular_byte():
    assert naturalsize(-1) == "-1 Byte"


def test_naturalsize_positive_one_still_uses_singular_byte():
    assert naturalsize(1) == "1 Byte"


def test_naturalsize_negative_one_binary_uses_singular_byte():
    assert naturalsize(-1, binary=True) == "-1 Byte"
