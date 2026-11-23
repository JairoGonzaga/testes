import pytest
from alvo import ordinal


def test_ordinal_non_numeric_returns_original():
    # Non‑numeric input should be returned unchanged.
    assert ordinal("something else") == "something else"


def test_ordinal_numeric_values():
    # Verify that normal numeric handling follows the implementation.
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    # Edge cases for the teens (11, 12, 13) all use "th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    # Larger numbers
    assert ordinal(21) == "21st"
    assert ordinal(112) == "112th"
