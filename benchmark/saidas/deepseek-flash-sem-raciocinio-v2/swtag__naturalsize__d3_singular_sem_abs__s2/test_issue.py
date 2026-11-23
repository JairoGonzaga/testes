from alvo import naturalsize


def test_naturalsize_negative_one_is_singular():
    assert naturalsize(-1) == "-1 Byte"


def test_naturalsize_singular_one():
    assert naturalsize(1) == "1 Byte"
