from alvo import naturalsize


def test_naturalsize_binary_uses_1024_base():
    # 3000000 / 1024**2 = 2.86..., expected '2.9 MiB' per the issue
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
