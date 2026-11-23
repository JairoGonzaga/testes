def test_c2_r1_negatives_and_rounding_up():
    # [R1/normal]
    assert intword(-1234) == "-1.2 thousand"
    assert intword(-1000) == "-1.0 thousand"
    assert intword(-999) == "-999"
    assert intword(999999999) == "1.0 billion"
