import pytest

from alvo import validate


def test_validate_int_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_str_returns_str():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)
