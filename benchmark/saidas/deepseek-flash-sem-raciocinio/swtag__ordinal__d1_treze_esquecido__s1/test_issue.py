import pytest

from alvo import ordinal


def test_ordinal_13_is_th():
    # Core case from the issue report.
    assert ordinal(13) == "13th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (-13, "-13th"),
        (1013, "1013th"),
    ],
)
def test_teens_always_take_th(value, expected):
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
        (100, "100th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
    ],
)
def test_regular_ordinals_unchanged(value, expected):
    assert ordinal(value) == expected


def test_non_finite_and_invalid_values_unchanged():
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
    assert ordinal("abc") == "abc"
