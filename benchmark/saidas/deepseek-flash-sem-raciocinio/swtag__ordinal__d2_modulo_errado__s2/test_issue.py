from alvo import ordinal


def test_ordinal_eleven():
    assert ordinal(11) == "11th"


def test_ordinal_teens_suffix_th():
    for value in (11, 12, 13):
        assert ordinal(value) == f"{value}th"


def test_ordinal_teens_with_hundreds():
    for value in (111, 112, 113):
        assert ordinal(value) == f"{value}th"


def test_ordinal_basic_suffixes_still_ok():
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(21) == "21st"
