from alvo import naturalsize


def test_naturalsize_999999_returns_1_mb():
    # Reported in the issue: rounding to 1000.0 must promote to the next unit.
    assert naturalsize(999999) == "1.0 MB"
