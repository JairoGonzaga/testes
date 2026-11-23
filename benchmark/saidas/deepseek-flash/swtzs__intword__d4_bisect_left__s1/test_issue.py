from alvo import intword


def test_intword_exact_googol():
    assert intword(10**100) == "1.0 googol"


def test_intword_negative_exact_googol():
    assert intword(-(10**100)) == "-1.0 googol"


def test_intword_exact_googol_with_custom_format():
    assert intword(10**100, format="%.0f") == "1 googol"
