from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    assert apnumber(0) == "zero"


def test_apnumber_five_still_spelled_out():
    assert apnumber(5) == "five"
