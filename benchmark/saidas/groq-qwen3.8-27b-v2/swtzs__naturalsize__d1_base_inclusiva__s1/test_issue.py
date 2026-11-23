from alvo import naturalsize


def test_naturalsize_decimal_kilobyte():
    # Issue: 1000 (exactly one decimal kilobyte) must be converted to the next unit.
    assert naturalsize(1000) == "1.0 kB"
