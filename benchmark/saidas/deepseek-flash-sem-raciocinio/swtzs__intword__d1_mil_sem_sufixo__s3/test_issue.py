import pytest

from alvo import intword


def test_intword_1000_exact():
    assert intword(1000) == "1.0 thousand"


def test_intword_thousand_range():
    assert intword(1001) == "1.0 thousand"
    assert intword(1500) == "1.5 thousand"
    assert intword(999_999) == "1000.0 thousand"
