import pytest

from alvo import intword


def test_intword_negative_million_keeps_minus():
    assert intword(-1000000) == "-1.0 million"


def test_intword_negative_thousand_keeps_minus():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_negative_small_keeps_minus():
    assert intword(-5) == "-5"
