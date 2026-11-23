import pytest

from alvo import validate


def test_validate_returns_int_unchanged():
    result = validate(79927398713)
    assert result == 79927398713


def test_validate_returns_int_type_for_int_input():
    result = validate(79927398713)
    assert isinstance(result, int)
    assert type(result) is int
