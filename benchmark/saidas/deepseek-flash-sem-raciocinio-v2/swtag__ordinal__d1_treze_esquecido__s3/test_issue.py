from alvo import ordinal


def test_ordinal_13_is_th():
    assert ordinal(13) == "13th"


def test_ordinal_11_12_13_are_th():
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"


def test_ordinal_hundreds_ending_in_13():
    assert ordinal(113) == "113th"
