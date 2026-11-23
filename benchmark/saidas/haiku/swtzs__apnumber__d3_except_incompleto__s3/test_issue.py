import pytest

from alvo import apnumber


def test_none_returns_string_none():
    assert apnumber(None) == "None"


@pytest.mark.parametrize(
    "value",
    [None, [], {}, (1, 2), object()],
    ids=["None", "list", "dict", "tuple", "object"],
)
def test_unconvertible_values_return_str(value):
    assert apnumber(value) == str(value)
