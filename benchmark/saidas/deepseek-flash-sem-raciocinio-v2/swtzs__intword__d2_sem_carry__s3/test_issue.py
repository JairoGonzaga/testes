from alvo import intword


def test_intword_rounds_up_to_next_power():
    # Issue: rounding pushed 999999 to "1000.0 thousand"; expected "1.0 million".
    assert intword(999999) == '1.0 million'
