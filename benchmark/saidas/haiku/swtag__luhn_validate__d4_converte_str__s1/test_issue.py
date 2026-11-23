import pytest

from alvo import validate


VALID_INTS = [
    18,
    79927398713,
]


@pytest.mark.parametrize("number", VALID_INTS)
def test_validate_returns_int_unchanged(number):
    result = validate(number)
    assert result == number
    assert isinstance(result, int)
    assert not isinstance(result, str)


def test_issue_example_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


@pytest.mark.parametrize("number", ["18", "79927398713"])
def test_validate_string_input_is_returned_unchanged(number):
    result = validate(number)
    assert result == number
    assert isinstance(result, str)
