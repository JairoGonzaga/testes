from alvo import naturalsize


def test_naturalsize_exactly_one_kilobyte():
    assert naturalsize(1000) == '1.0 kB'


def test_naturalsize_exactly_one_kibibyte():
    assert naturalsize(1024, binary=True) == '1.0 KiB'
