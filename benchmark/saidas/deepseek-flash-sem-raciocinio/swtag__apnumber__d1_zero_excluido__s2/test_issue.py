import pytest

from alvo import apnumber


def test_apnumber_zero():
    assert apnumber(0) == "zero"


def test_apnumber_all_single_digits():
    words = ["zero", "one", "two", "three", "four",
             "five", "six", "seven", "eight", "nine"]
    for value, word in enumerate(words):
        assert apnumber(value) == word


def test_apnumber_other_values_unchanged():
    assert apnumber(5) == "five"
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"
