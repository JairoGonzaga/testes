import pytest

from alvo import InvalidFormat, validate


def test_validate_rejects_empty_string():
    # An empty value has no digits to check, so it must be rejected as an
    # invalid format instead of being accepted as a valid checksum.
    with pytest.raises(InvalidFormat):
        validate('')


def test_validate_rejects_empty_string_with_custom_alphabet():
    with pytest.raises(InvalidFormat):
        validate('', alphabet='0123456789ABCDEF')


def test_validate_still_accepts_valid_number():
    # Regression guard: a well-formed number with a valid checksum is still accepted.
    assert validate('79927398713') == '79927398713'
