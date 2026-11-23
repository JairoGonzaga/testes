from alvo import naturalsize


def test_naturalsize_binary_uses_powers_of_1024():
    # From the issue: 3000000 / 1024**2 = 2.86..., formatted as '2.9' with 'MiB'.
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
