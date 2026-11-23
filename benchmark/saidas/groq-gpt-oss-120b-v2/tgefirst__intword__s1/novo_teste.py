def test_c2_r1_rounding_bump():
    # When the format rounds the chopped value up to exactly 1000,
    # the function should promote to the next unit.
    assert intword(999500, format="%.0f") == "1 million"
    # With the default format (one decimal), it stays in the original unit.
    assert intword(999500) == "999.5 thousand"
