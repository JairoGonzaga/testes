from alvo import naturalsize


def test_binary_uses_1024_base():
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_kib():
    assert naturalsize(2048, binary=True) == "2.0 KiB"


def test_binary_gib():
    assert naturalsize(1024 ** 3 * 3, binary=True) == "3.0 GiB"
