from alvo import ordinal


def test_111_is_111th():
    assert ordinal(111) == "111th"


def test_112_is_112th():
    assert ordinal(112) == "112th"


def test_113_is_113th():
    assert ordinal(113) == "113th"


def test_1011_is_1011th():
    assert ordinal(1011) == "1011th"


def test_nearby_values_still_correct():
    assert ordinal(114) == "114th"
    assert ordinal(121) == "121st"
    assert ordinal(22) == "22nd"
    assert ordinal(13) == "13th"
