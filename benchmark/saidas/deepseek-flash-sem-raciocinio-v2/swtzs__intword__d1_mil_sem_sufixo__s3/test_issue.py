from alvo import intword


def test_intword_1000_is_thousand():
    assert intword(1000) == "1.0 thousand"
