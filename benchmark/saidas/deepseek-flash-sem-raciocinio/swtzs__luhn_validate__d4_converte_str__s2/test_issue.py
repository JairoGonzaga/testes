import pytest

from alvo import validate


def test_validate_returns_int_unchanged():
    number = 79927398713
    result = validate(number)
    assert result == number
    assert isinstance(result, int)


def test_validate_returns_str_unchanged():
    number = "79927398713"
    result = validate(number)
    assert result == number
    assert isinstance(result, str)


def test_validate_preserves_type_for_valid_int():
    result = validate(79927398713)
    assert type(result) is int
