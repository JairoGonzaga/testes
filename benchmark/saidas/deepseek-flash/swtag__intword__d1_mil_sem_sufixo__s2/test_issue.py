import pytest

from alvo import intword


def test_exactly_one_thousand_is_humanized():
    # Core of the issue report: 1000 must be rendered with a word suffix.
    assert intword(1000) == "1.0 thousand"


def test_negative_one_thousand_is_humanized():
    assert intword(-1000) == "-1.0 thousand"


def test_one_thousand_with_float_value():
    assert intword(1000.0) == "1.0 thousand"


def test_one_thousand_with_string_value():
    assert intword("1000") == "1.0 thousand"


def test_one_thousand_with_custom_format():
    assert intword(1000, "%.0f") == "1 thousand"
    assert intword(1000, "%.2f") == "1.00 thousand"


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "0"),
        (1, "1"),
        (999, "999"),
        (-999, "-999"),
        (1001, "1.0 thousand"),
        (1500, "1.5 thousand"),
        (1000000, "1.0 million"),
    ],
)
def test_neighbouring_values_still_work(value, expected):
    # Guard: values at or above the first power must be humanized, while
    # values below it must stay untouched.
    assert intword(value) == expected
