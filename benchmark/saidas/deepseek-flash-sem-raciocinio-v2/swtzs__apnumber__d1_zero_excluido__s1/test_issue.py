from alvo import apnumber


def test_apnumber_zero_is_word():
    # Issue: zero comes back as digit string; expected 'zero'.
    assert apnumber(0) == "zero"


def test_apnumber_five_is_word():
    # Issue explicitly says single digits like 5 already work.
    assert apnumber(5) == "five"


def test_apnumber_nine_is_word():
    # "0 to 9" range: nine is the upper bound of the word range.
    assert apnumber(9) == "nine"
