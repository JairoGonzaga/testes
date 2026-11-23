import pytest

from alvo import InvalidChecksum, checksum, validate


def test_classic_luhn_number_is_valid():
    # 79927398713 is the textbook valid Luhn number from the issue.
    assert validate('79927398713') == '79927398713'


def test_classic_luhn_checksum_is_zero():
    assert checksum('79927398713') == 0


def test_invalid_luhn_number_still_rejected():
    # Same digit string with the check digit changed must still fail.
    with pytest.raises(InvalidChecksum):
        validate('79927398714')
