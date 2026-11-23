import pytest

from alvo import InvalidChecksum, checksum, validate


def test_textbook_luhn_number_is_valid():
    """The issue: '79927398713' has a valid Luhn check digit."""
    assert validate("79927398713") == "79927398713"


def test_textbook_luhn_number_does_not_raise():
    try:
        validate("79927398713")
    except InvalidChecksum:
        pytest.fail("valid Luhn number '79927398713' was rejected")


def test_checksum_of_textbook_luhn_number_is_zero():
    assert checksum("79927398713") == 0
