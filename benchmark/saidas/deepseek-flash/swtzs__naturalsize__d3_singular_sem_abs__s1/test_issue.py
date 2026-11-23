from alvo import naturalsize


def test_naturalsize_negative_one_uses_singular_byte():
    assert naturalsize(-1) == "-1 Byte"
