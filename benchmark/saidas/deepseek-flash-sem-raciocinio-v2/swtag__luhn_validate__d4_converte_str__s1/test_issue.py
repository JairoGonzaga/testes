import pytest

from alvo import validate, InvalidChecksum


def test_validate_int_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_str_returns_str():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)


def test_validate_invalid_int_raises():
    with pytest.raises(InvalidChecksum):
        validate(79927398714)
