from alvo import apnumber


def test_apnumber_nine_spelled_out():
    # Issue: apnumber(9) returned '9' instead of 'nine'.
    assert apnumber(9) == 'nine'
