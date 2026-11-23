import pytest

from alvo import validate, checksum, InvalidChecksum


def test_textbook_luhn_number_is_valid():
    # 79927398713 is the canonical Luhn example with a valid check digit
    assert checksum("79927398713") == 0
    assert validate("79927398713") == "79927398713"


def test_other_valid_luhn_numbers():
    for number in ("79927398713", "4111111111111111", "5500005555555559"):
        assert validate(number) == number
        assert checksum(number) == 0


def test_invalid_checksum_detected():
    with pytest.raises(InvalidChecksum):
        validate("79927398710")
