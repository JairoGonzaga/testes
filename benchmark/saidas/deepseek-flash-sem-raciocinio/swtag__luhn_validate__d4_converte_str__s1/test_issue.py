import pytest

from alvo import validate, InvalidChecksum, InvalidFormat


def test_validate_int_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_int_identity():
    value = 79927398713
    assert validate(value) is value


def test_validate_str_returns_str():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)


def test_validate_invalid_checksum_still_raises():
    with pytest.raises(InvalidChecksum):
        validate(79927398714)


def test_validate_empty_still_raises():
    with pytest.raises(InvalidFormat):
        validate(0)
