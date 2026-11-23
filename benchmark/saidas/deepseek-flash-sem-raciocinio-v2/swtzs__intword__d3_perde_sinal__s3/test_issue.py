from alvo import intword


def test_intword_negative_million_keeps_sign():
    assert intword(-1000000) == "-1.0 million"
