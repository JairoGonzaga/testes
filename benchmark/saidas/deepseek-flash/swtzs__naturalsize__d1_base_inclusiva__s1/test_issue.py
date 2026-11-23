from alvo import naturalsize


def test_naturalsize_one_kilobyte():
    assert naturalsize(1000) == "1.0 kB"


def test_naturalsize_just_below_one_kilobyte():
    assert naturalsize(999) == "999 Bytes"
