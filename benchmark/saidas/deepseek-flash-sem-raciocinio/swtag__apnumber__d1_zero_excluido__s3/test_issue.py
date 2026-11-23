import pytest

from alvo import apnumber


def test_apnumber_zero():
    assert apnumber(0) == "zero"


def test_apnumber_zero_float():
    assert apnumber(0.0) == "zero"


def test_apnumber_single_digits():
    expected = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }
    for value, word in expected.items():
        assert apnumber(value) == word


def test_apnumber_out_of_range_unchanged():
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
