```python
import math

import pytest

from alvo import _APNUMBER_WORDS, _format_not_finite, apnumber


EXPECTED_WORDS = (
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
)


def test_apnumber_word_table_is_exact():
    assert _APNUMBER_WORDS == EXPECTED_WORDS
    assert len(_APNUMBER_WORDS) == 10


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "zero"),
        (1, "one"),
        (2, "two"),
        (3, "three"),
        (4, "four"),
        (5, "five"),
        (6, "six"),
        (7, "seven"),
        (8, "eight"),
        (9, "nine"),
        (0.0, "zero"),
        (1.0, "one"),
        (2.0, "two"),
        (8.0, "eight"),
        (9.0, "nine"),
        (True, "one"),
        (False, "zero"),
        ("0", "zero"),
        ("1", "one"),
        ("2", "two"),
        ("5", "five"),
        ("8", "eight"),
        ("9", "nine"),
    ],
)
def test_apnumber_maps_single_digits(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.1, "zero"),
        (0.5, "zero"),
        (0.999, "zero"),
        (1.1, "one"),
        (1.9, "one"),
        (2.5, "two"),
        (3.7, "three"),
        (4.99, "four"),
        (8.1, "eight"),
        (9.999, "nine"),
        (-0.0, "zero"),
        (-0.1, "zero"),
        (-0.5, "zero"),
        (-0.999, "zero"),
        (-1.0, "-1"),
        (-1.1, "-1"),
        (-1.9, "-1"),
        (10.0, "10"),
        (10.1, "10"),
        (10.9, "10"),
        (11.0, "11"),
        (11.9, "11"),
        (-10.0, "-10"),
        (-10.9, "-10"),
        (10, "10"),
        (11, "11"),
        (100, "100"),
        (-1, "-1"),
        (-10, "-10"),
    ],
)
def test_apnumber_truncates_to_int_and_stringifies_out_of_range_values(
    value, expected
):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("0", "zero"),
        ("1", "one"),
        ("2", "two"),
        ("5", "five"),
        ("8", "eight"),
        ("9", "nine"),
        (" 3 ", "three"),
        ("+2", "two"),
        ("03", "three"),
        ("-0", "zero"),
        ("10", "10"),
        ("11", "11"),
        ("-1", "-1"),
        (" 10 ", "10"),
        ("-01", "-1"),
        ("3.7", "3.7"),
        ("10.0", "10.0"),
        ("1e1", "1e1"),
        (" 3.0 ", " 3.0 "),
    ],
)
def test_apnumber_handles_numeric_strings(value, expected):
    assert apnumber(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (math.nan, "NaN"),
        (float("nan"), "NaN"),
        ("nan", "NaN"),
        ("NaN", "NaN"),
        (math.inf, "+Inf"),
        (float("inf"), "+Inf"),
        ("inf", "+Inf"),
        ("Infinity", "+Inf"),
        (-math.inf, "-Inf