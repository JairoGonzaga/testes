# test_issue.py
import pytest
from alvo import ordinal


def test_ordinal_111_should_be_th():
    # Bug causes 111 to incorrectly return '111st'.
    # After the fix this assertion will pass.
    assert ordinal(111) == '111th'


@pytest.mark.parametrize(
    "value,expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
    ],
)
def test_ordinal_small_numbers(value, expected):
    assert ordinal(value) == expected
