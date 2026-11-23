from alvo import ordinal


def test_ordinal_111_is_111th():
    assert ordinal(111) == "111th"


def test_ordinal_112_and_113_are_th():
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"


def test_small_teens_still_work():
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
