from alvo import apnumber


def test_zero_is_spelled_out():
    assert apnumber(0) == "zero"


def test_zero_float_is_spelled_out():
    assert apnumber(0.0) == "zero"


def test_other_single_digits_still_work():
    assert apnumber(5) == "five"
    assert apnumber(9) == "nine"


def test_out_of_range_returns_digits():
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
