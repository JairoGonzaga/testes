from alvo import intword


def test_intword_exactly_one_thousand():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_one_thousand():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_above_and_below_1000():
    assert intword(999) == "999"
    assert intword(1001) == "1.0 thousand"


def test_intword_one_thousand_int_format():
    assert intword(1000, format="%d") == "1 thousand"
