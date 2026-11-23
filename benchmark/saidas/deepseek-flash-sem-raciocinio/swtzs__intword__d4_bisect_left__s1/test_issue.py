import pytest

from alvo import intword


def test_googol():
    assert intword(10**100) == "1.0 googol"


def test_googol_negative():
    assert intword(-(10**100)) == "-1.0 googol"


def test_googol_multiple():
    assert intword(2 * 10**100) == "2.0 googol"


def test_decillion_still_works():
    assert intword(10**33) == "1.0 decillion"


def test_just_below_googol_is_not_googol():
    result = intword(10**99)
    assert "googol" not in result
