import pytest
from alvo import validate, InvalidChecksum


def test_validate_int_returns_int():
    """When a valid integer is given, validate should return the same integer."""
    number = 79927398713
    result = validate(number)
    # Current buggy implementation returns a string, so this will fail.
    assert isinstance(result, int)
    assert result == number


def test_validate_invalid_checksum_raises():
    """An invalid number should raise InvalidChecksum."""
    with pytest.raises(InvalidChecksum):
        validate(1)  # 1 is not a valid Luhn number and triggers checksum failure.
