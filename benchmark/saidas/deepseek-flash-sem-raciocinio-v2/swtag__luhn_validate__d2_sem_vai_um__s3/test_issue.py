import pytest

from alvo import validate, InvalidChecksum


def test_standard_luhn_example_is_valid():
    """79927398713 is the standard valid Luhn example (digits >= 5 doubled)."""
    assert validate("79927398713") == "79927398713"


@pytest.mark.parametrize("number", ["183", "1234567812345674"])
def test_other_valid_numbers_with_doubled_digits_ge_5(number):
    assert validate(number) == number


def test_invalid_check_digit_still_rejected():
    # same digits as the standard valid example, but last digit changed
    with pytest.raises(InvalidChecksum):
        validate("79927398710")
