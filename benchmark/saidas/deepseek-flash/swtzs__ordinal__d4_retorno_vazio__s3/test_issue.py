import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value, expected",
    [
        ("something else", "something else"),
        ("abc", "abc"),
        (None, "None"),
        ([1, 2], "[1, 2]"),
    ],
)
def test_ordinal_returns_str_for_non_convertible_values(value, expected):
    assert ordinal(value) == expected
