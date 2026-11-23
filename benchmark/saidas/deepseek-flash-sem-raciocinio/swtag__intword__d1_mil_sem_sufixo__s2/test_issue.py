from alvo import intword


def test_intword_exactly_one_thousand():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_one_thousand():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_boundary_values():
    assert intword(999) == "999"
    assert intword(1001) == "1.0 thousand"
    assert intword(10**6) == "1.0 million"
