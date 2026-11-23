from alvo import naturalsize


def test_binary_uses_powers_of_1024():
    # 3000000 / 1024**2 = 2.861... -> '2.9 MiB'
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_kib():
    # 3000 / 1024 = 2.929... -> '2.9 KiB'
    assert naturalsize(3000, binary=True) == "2.9 KiB"


def test_decimal_still_uses_powers_of_1000():
    assert naturalsize(3000000) == "3.0 MB"
