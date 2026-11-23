from alvo import apnumber


def test_apnumber_nine():
    assert apnumber(9) == "nine"


def test_apnumber_one():
    assert apnumber(1) == "one"


def test_apnumber_zero():
    assert apnumber(0) == "zero"
