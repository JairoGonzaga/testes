from alvo import apnumber


def test_apnumber_zero_is_word():
    assert apnumber(0) == "zero"


def test_apnumber_zero_float_is_word():
    assert apnumber(0.0) == "zero"


def test_apnumber_other_digits_still_ok():
    assert apnumber(5) == "five"
    assert apnumber(9) == "nine"
    assert apnumber(10) == "10"
