from alvo import naturalsize


def test_binary_uses_powers_of_1024():
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_kib():
    assert naturalsize(10240, binary=True) == "10.0 KiB"
