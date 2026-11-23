from alvo import apnumber


def test_apnumber_zero_is_word():
    # Issue: apnumber(0) should return 'zero', not '0'.
    assert apnumber(0) == "zero"


def test_apnumber_five_is_word():
    # Issue states apnumber(5) -> 'five' works fine.
    assert apnumber(5) == "five"
