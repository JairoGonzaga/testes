"""Testes de apnumber."""

import math

import pytest

from alvo import apnumber


def test_c1_r1():
    # [R1/fronteira]
    assert apnumber(0) == 'zero'


import math
import pytest

@pytest.mark.parametrize(
    "inp,expected",
    [
        (5, "five"),                     # simple integer within range
        ("3", "three"),                  # numeric string
        (2.9, "two"),                    # float truncated to int
        (-1, "-1"),                      # negative integer out of range
        (10, "10"),                      # integer equal to upper bound, out of range
        (math.nan, "NaN"),               # NaN value
        (float("inf"), "+Inf"),          # positive infinity
        (float("-inf"), "-Inf"),         # negative infinity
        (None, "None"),                  # non-convertible type raises TypeError
        ("foo", "foo"),                  # non-convertible string raises ValueError
    ],
)
def test_c2_r1(inp, expected):
    assert apnumber(inp) == expected
