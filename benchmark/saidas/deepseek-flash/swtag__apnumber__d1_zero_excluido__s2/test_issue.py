import pytest

from alvo import apnumber


def test_apnumber_zero_returns_word():
    assert apnumber(0) == "zero"


def test_apnumber_all_single_digits_spelled_out():
    words = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    ]
    for digit, word in enumerate(words):
        assert apnumber(digit) == word, f"apnumber({digit}) != {word!r}"
