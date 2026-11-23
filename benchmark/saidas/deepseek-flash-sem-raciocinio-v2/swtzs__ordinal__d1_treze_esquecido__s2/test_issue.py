from alvo import ordinal


def test_ordinal_13_is_th():
    assert ordinal(13) == "13th"


def test_ordinal_11_is_th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_th():
    assert ordinal(12) == "12th"
