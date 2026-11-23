import pytest

from alvo import validate, InvalidChecksum, InvalidFormat


def test_validate_returns_int_unchanged():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)
    assert not isinstance(result, str)


def test_validate_int_identity_for_other_valid_number():
    # 18 is a valid Luhn number
    assert validate(18) == 18
    assert isinstance(validate(18), int)
    assert not isinstance(validate(18), str)


def test_validate_str_still_returns_str():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)


def test_validate_still_rejects_invalid_int():
    with pytest.raises(InvalidChecksum):
        validate(79927398710)


def test_validate_still_rejects_empty_int():
    with pytest.raises(InvalidFormat):
        validate(0)
