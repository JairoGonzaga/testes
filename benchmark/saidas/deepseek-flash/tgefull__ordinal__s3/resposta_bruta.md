```python
import math

import pytest

from alvo import _SUFIXOS, _format_not_finite, ordinal


class _BadFloatValueError:
    def __float__(self):
        raise ValueError("bad float")

    def __str__(self):
        return "bad-float-value-error"


class _BadFloatTypeError:
    def __float__(self):
        raise TypeError("bad float")

    def __str__(self):
        return "bad-float-type-error"


class _BadIntValueError:
    def __float__(self):
        return 12.0

    def __int__(self):
        raise ValueError("bad int")

    def __str__(self):
        return "bad-int-value-error"


class _NoIntWithFloat:
    def __float__(self):
        return 13.0

    def __str__(self):
        return "no-int-with-float"


class _GoodCustomNumber:
    def __float__(self):
        return 2.0

    def __int__(self):
        return 2

    def __str__(self):
        return "good-custom-number"


class _NaNFloat:
    def __float__(self):
        return float("nan")

    def __str__(self):
        return "nan-float"


class _InfFloat:
    def __float__(self):
        return float("inf")

    def __str__(self):
        return "inf-float"


def test_suffix_table():
    assert _SUFIXOS == (
        "th",
        "st",
        "nd",
        "rd",
        "th",
        "th",
        "th",
        "th",
        "th",
        "th",
    )


@pytest.mark.parametrize(
    "value,expected",
    [
        (math.nan, "NaN"),
        (float("nan"), "NaN"),
        (-math.inf, "-Inf"),
        (float("-inf"), "-Inf"),
        (math.inf, "+Inf"),
        (float("inf"), "+Inf"),
        (0.0, ""),
        (1.0, ""),
        (-1.5, ""),
        (1.5, ""),
    ],
)
def test_format_not_finite(value, expected):
    assert _format_not_finite(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0th"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (5, "5th"),
        (6, "6th"),
        (7, "7th"),
        (8, "8th"),
        (9, "9th"),
        (10, "10th"),
        (11,