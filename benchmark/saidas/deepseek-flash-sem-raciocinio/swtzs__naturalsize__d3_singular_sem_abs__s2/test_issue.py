from alvo import naturalsize


def test_naturalsize_positive_one_byte():
    assert naturalsize(1) == "1 Byte"


def test_naturalsize_negative_one_byte():
    assert naturalsize(-1) == "-1 Byte"
