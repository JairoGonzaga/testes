from alvo import intword


def test_intword_1000():
    assert intword(1000) == "1.0 thousand"


def test_intword_1000_negative():
    assert intword(-1000) == "-1.0 thousand"
