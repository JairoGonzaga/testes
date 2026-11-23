import pytest

from alvo import ordinal


def test_ordinal_11_is_11th():
    assert ordinal(11) == "11th"


def test_ordinal_12_and_13_are_teens():
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"


def test_ordinal_111_and_112_are_teens():
    assert ordinal(111) == "111th"
    assert ordinal(112) == "112th"
