from alvo import naturalsize


def test_exactly_one_kilobyte():
    # Issue: naturalsize(1000) must be '1.0 kB', not '1000 Bytes'
    assert naturalsize(1000) == "1.0 kB"
