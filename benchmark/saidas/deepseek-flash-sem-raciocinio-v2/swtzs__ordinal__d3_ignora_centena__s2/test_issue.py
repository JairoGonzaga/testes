from alvo import ordinal


def test_ordinal_111_is_111th():
    assert ordinal(111) == "111th"


def test_ordinal_11_still_works():
    assert ordinal(11) == "11th"
