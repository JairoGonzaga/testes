import math

import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (1111, "1111th"),
        (1112, "1112th"),
        (1113, "1113th"),
        (11.0, "11th"),
        ("11", "11th"),
    ],
)
def test_teens_get_th(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
    ],
)
def test_non_teens_unchanged(value, expected):
    assert ordinal(value) == expected
