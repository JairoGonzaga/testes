import pytest

from alvo import validate, checksum, InvalidChecksum


def test_textbook_luhn_number_is_accepted():
    assert validate('79927398713') == '79927398713'


def test_textbook_luhn_number_checksum_is_zero():
    assert checksum('79927398713') == 0
