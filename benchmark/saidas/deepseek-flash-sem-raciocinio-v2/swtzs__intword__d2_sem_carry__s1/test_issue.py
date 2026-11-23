from alvo import intword


def test_intword_999999_promotes_to_million():
    # Issue: intword(999999) returns '1000.0 thousand', expected '1.0 million'.
    assert intword(999999) == "1.0 million"
