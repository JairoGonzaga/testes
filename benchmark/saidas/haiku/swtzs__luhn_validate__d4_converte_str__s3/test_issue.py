import pytest

from alvo import validate


@pytest.mark.parametrize("number", [79927398713, 4111111111111111])
def test_validate_returns_int_unchanged(number):
    result = validate(number)
    assert result == number
    assert isinstance(result, int)
    assert not isinstance(result, str)


def test_validate_int_example_from_issue():
    result = validate(79927398713)
    assert result == 79927398713
    assert type(result) is int
