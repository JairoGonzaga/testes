from alvo import ordinal


# Small numbers keep working
def test_ordinal_basic():
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"


def test_ordinal_111():
    assert ordinal(111) == "111th"


def test_ordinal_112_113():
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"


def test_ordinal_larger_teens():
    assert ordinal(211) == "211th"
    assert ordinal(1011) == "1011th"
    assert ordinal(1113) == "1113th"


def test_ordinal_non_teen_suffixes_still_work():
    assert ordinal(101) == "101st"
    assert ordinal(102) == "102nd"
    assert ordinal(103) == "103rd"
    assert ordinal(121) == "121st"
    assert ordinal(122) == "122nd"
    assert ordinal(123) == "123rd"
    assert ordinal(1111) == "1111th"
