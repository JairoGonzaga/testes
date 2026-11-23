def test_round_up_promotes_unit():
    # when rounding reaches the next power of a thousand, promote to the larger unit
    assert intword(999_950) == "1.0 million"
    assert intword(1_999_950_000) == "2.0 billion"
