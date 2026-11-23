import pytest

from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_string_unchanged_still_works():
    assert apnumber("abc") == "abc"


def test_apnumber_still_converts_small_ints():
    assert apnumber(3) == "three"
