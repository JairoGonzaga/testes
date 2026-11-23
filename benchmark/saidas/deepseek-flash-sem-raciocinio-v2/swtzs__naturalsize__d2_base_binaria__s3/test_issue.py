from alvo import naturalsize


def test_naturalsize_binary_uses_1024():
    # From issue: 3000000 / 1024**2 = 2.86... -> '2.9 MiB'
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
