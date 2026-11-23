import pytest

from alvo import ordinal


def test_ordinal_11_is_11th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_12th():
    assert ordinal(12) == "12th"


def test_ordinal_13_is_13th():
    assert ordinal(13) == "13th"


def test_ordinal_111_is_111th():
    assert ordinal(111) == "111th"


def test_ordinal_regular_cases():
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"
    assert ordinal(101) == "101st"
