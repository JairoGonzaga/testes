import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value",
    ["something else", "abc", "twelve", None],
)
def test_non_numeric_input_is_returned_as_str(value):
    assert ordinal(value) == str(value)


def test_issue_example_returns_the_original_text():
    assert ordinal('something else') == 'something else'


@pytest.mark.parametrize(
    ("value", "expected"),
    [(1, "1st"), (2, "2nd"), (3, "3rd"), (11, "11th"), (21, "21st"), ("22", "22nd")],
)
def test_numeric_input_is_unaffected(value, expected):
    assert ordinal(value) == expected
