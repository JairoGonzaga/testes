from alvo import ordinal


def test_ordinal_13_is_th():
    assert ordinal(13) == "13th"


def test_ordinal_11_and_12_are_th():
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
