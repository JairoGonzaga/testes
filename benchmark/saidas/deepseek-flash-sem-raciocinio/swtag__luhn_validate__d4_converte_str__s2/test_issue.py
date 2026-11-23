import pytest

from alvo import validate


def test_validate_returns_int_unchanged():
    number = 79927398713
    result = validate(number)
    assert result == number
    assert isinstance(result, int)
    assert not isinstance(result, str)


def test_validate_returns_str_unchanged():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)


def test_validate_identity_for_luhn_numbers():
    for number in (79927398713, 1234567812345670, 4111111111111111):
        result = validate(number)
        assert result == number
        assert type(result) is type(number)
