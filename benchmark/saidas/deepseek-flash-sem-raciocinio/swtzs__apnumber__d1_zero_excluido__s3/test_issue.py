import pytest

from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    assert apnumber(0) == "zero"


def test_apnumber_all_single_digits_are_spelled_out():
    expected = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    for n, word in enumerate(expected):
        assert apnumber(n) == word, f"apnumber({n}) should be {word!r}"
