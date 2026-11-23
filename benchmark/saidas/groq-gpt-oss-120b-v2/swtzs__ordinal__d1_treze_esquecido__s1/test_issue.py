import pytest
from alvo import ordinal


@pytest.mark.parametrize(
    "value,expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),  # the bug: currently returns "13rd"
    ],
)
def test_ordinal_teens(value, expected):
    """11, 12 and 13 should always have the 'th' suffix."""
    assert ordinal(value) == expected
