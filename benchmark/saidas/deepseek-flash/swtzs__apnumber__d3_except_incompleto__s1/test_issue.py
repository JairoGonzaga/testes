import pytest

from alvo import apnumber


def test_apnumber_none_is_returned_as_string():
    assert apnumber(None) == "None"


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, "None"),
        ("abc", "abc"),
        ("", ""),
    ],
)
def test_apnumber_returns_non_numeric_values_as_strings(value, expected):
    assert apnumber(value) == expected
