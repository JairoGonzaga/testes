import pytest

from alvo import validate


@pytest.mark.parametrize("number", [79927398713, 4111111111111111])
def test_validate_int_returns_the_int_unchanged(number):
    result = validate(number)
    assert result == number
    assert type(result) is int


def test_validate_str_returns_the_str_unchanged():
    number = "79927398713"
    result = validate(number)
    assert result == number
    assert type(result) is str
