import pytest

from alvo import validate


def test_validate_int_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)
    assert not isinstance(result, str)


def test_validate_str_returns_same_str():
    assert validate("79927398713") == "79927398713"
