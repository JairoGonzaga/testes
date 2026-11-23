from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    # Directly reproduces the reported bug: zero must be a word, not a digit string.
    assert apnumber(0) == "zero"


def test_apnumber_single_digit_is_spelled_out():
    # Working case cited in the issue (5 -> 'five').
    assert apnumber(5) == "five"
