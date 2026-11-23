from alvo import naturalsize


def test_naturalsize_1000_bytes():
    assert naturalsize(1000) == "1.0 kB"
