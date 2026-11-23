import pytest

from alvo import intword


def test_intword_999999_rounds_up_to_million():
    assert intword(999999) == "1.0 million"


def test_intword_999999999_rounds_up_to_billion():
    assert intword(999999999) == "1.0 billion"


def test_intword_negative_999999_rounds_up_to_million():
    assert intword(-999999) == "-1.0 million"


def test_intword_no_promotion_needed():
    assert intword(1234567) == "1.2 million"
    assert intword(999) == "999"
