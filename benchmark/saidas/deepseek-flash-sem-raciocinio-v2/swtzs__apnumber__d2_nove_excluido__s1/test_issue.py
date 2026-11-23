from alvo import apnumber


def test_apnumber_nine_is_spelled_out():
    assert apnumber(9) == "nine"


def test_apnumber_eight_is_spelled_out():
    assert apnumber(8) == "eight"


def test_apnumber_zero_is_spelled_out():
    assert apnumber(0) == "zero"
