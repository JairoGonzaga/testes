import pytest

from alvo import ordinal


def test_ordinal_returns_string_for_non_numeric_input():
    assert ordinal("something else") == "something else"


def test_ordinal_returns_string_for_unconvertible_object():
    assert ordinal(None) == "None"
