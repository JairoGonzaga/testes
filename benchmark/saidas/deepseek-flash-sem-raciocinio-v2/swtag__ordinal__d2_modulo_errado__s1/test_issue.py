from alvo import ordinal


def test_ordinal_11():
    assert ordinal(11) == "11th"


def test_ordinal_12():
    assert ordinal(12) == "12th"


def test_ordinal_13():
    assert ordinal(13) == "13th"


def test_ordinal_111():
    assert ordinal(111) == "111th"
