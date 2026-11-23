from alvo import ordinal


def test_111_is_111th():
    assert ordinal(111) == "111th"


def test_numbers_ending_in_11_12_13():
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"
    assert ordinal(1011) == "1011th"
    assert ordinal(1012) == "1012th"
    assert ordinal(1013) == "1013th"


def test_small_numbers_still_work():
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"
    assert ordinal(101) == "101st"
