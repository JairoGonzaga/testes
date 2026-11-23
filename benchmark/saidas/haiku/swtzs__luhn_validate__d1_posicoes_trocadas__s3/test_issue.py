import pytest

from alvo import checksum, validate


VALID_LUHN_NUMBERS = [
    "79927398713",       # textbook example from the issue
    "4111111111111111",  # Visa test number
    "4012888888881881",  # Visa test number
]


def test_textbook_example_is_accepted():
    assert validate("79927398713") == "79927398713"


@pytest.mark.parametrize("number", VALID_LUHN_NUMBERS)
def test_valid_luhn_numbers_are_accepted(number):
    assert validate(number) == number


@pytest.mark.parametrize("number", VALID_LUHN_NUMBERS)
def test_checksum_of_valid_luhn_number_is_zero(number):
    assert checksum(number) == 0
