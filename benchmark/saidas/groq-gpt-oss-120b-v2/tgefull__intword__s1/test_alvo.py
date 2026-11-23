import math
import pytest
from alvo import intword, _format_not_finite


def test_format_not_finite_cases():
    assert _format_not_finite(math.nan) == "NaN"
    assert _format_not_finite(float('-inf')) == "-Inf"
    assert _format_not_finite(float('inf')) == "+Inf"
    # Finite numbers return empty string
    assert _format_not_finite(0) == ""
    assert _format_not_finite(3.14) == ""


def test_intword_non_finite():
    assert intword(math.nan) == "NaN"
    assert intword(float('inf')) == "+Inf"
    assert intword(float('-inf')) == "-Inf"


def test_intword_non_numeric():
    # Value that cannot be converted to float should be returned as string
    assert intword("abc") == "abc"
    # None raises TypeError when float(None) is attempted, should return "None"
    assert intword(None) == "None"
    # Objects with __str__ but not numeric
    class Foo:
        def __str__(self):
            return "foo"
    assert intword(Foo()) == "foo"


def test_intword_small_and_negative():
    # Values below 1000 are returned as plain integers, preserving sign
    assert intword(0) == "0"
    assert intword(5) == "5"
    assert intword(-7) == "-7"
    # Float values are truncated via int()
    assert intword(5.9) == "5"
    assert intword(-5.9) == "-5"


def test_intword_thousand_and_million():
    # Exactly one thousand
    assert intword(1000) == "1.0 thousand"
    assert intword(-1000) == "-1.0 thousand"
    # Exactly one million
    assert intword(1_000_000) == "1.0 million"
    assert intword(-1_000_000) == "-1.0 million"


def test_intword_bump_to_next_unit():
    # 999,950 rounds to 1000.0 thousand, triggering a bump to million
    assert intword(999_950) == "1.0 million"
    assert intword(-999_950) == "-1.0 million"


def test_intword_custom_format_and_bump():
    # Using no decimal places, 1500 becomes 2 thousand
    assert intword(1500, format="%.0f") == "2 thousand"
    # With custom format, a value that rounds to 1000 triggers bump
    assert intword(999_500, format="%.0f") == "1 million"
    assert intword(-999_500, format="%.0f") == "-1 million"


def test_intword_huge_values():
    # Value exactly equal to the largest defined power (googol)
    googol = 10 ** 100
    assert intword(googol) == "1.0 googol"
    # Value larger than the largest power uses googol as the unit
    larger = googol * 10
    assert intword(larger) == "10.0 googol"
    # Negative large value
    assert intword(-larger) == "-10.0 googol"
