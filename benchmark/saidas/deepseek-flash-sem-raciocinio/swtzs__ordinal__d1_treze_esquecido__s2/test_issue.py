import pytest

from alvo import ordinal


def test_ordinal_13():
    assert ordinal(13) == "13th"


def test_ordinal_11_12_13():
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"


def test_ordinal_111_112_113():
    assert ordinal(111) == "111th"
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"


def test_ordinal_other_rd_still_works():
    assert ordinal(3) == "3rd"
    assert ordinal(23) == "23rd"
