from alvo import intword


def test_intword_999999_promotes_to_million():
    assert intword(999999) == "1.0 million"
