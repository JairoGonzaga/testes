import pytest
from alvo import validate, ValidationError


def test_validate_int_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_str_returns_str():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)


def test_validate_invalid_checksum_raises():
    from alvo import InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate(79927398714)
