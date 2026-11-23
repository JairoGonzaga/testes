from alvo import apnumber


def test_zero_spelled_out():
    assert apnumber(0) == "zero"


def test_five_spelled_out():
    assert apnumber(5) == "five"


def test_nine_spelled_out():
    assert apnumber(9) == "nine"


def test_out_of_range_stays_digit():
    assert apnumber(10) == "10"


def test_negative_stays_digit():
    assert apnumber(-1) == "-1"