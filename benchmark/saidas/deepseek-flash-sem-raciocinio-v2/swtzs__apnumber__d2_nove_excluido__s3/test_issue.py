from alvo import apnumber


def test_apnumber_nine_is_spelled_out():
    # Issue: apnumber(9) must be 'nine', not '9'.
    assert apnumber(9) == "nine"


def test_apnumber_zero_is_spelled_out():
    # Sanity: in-range single digit still uses the word table.
    assert apnumber(0) == "zero"
