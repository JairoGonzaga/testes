import pytest

from alvo import InvalidChecksum, validate


def _reference_luhn_ok(number):
    """Standard Luhn check: a doubled digit >= 10 contributes its digit sum."""
    total = 0
    for position, char in enumerate(reversed(number)):
        digit = int(char)
        if position % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def _with_check_digit(payload):
    for check in "0123456789":
        candidate = payload + check
        if _reference_luhn_ok(candidate):
            return candidate
    raise AssertionError("no valid check digit found")


def test_issue_example_is_accepted():
    assert validate("79927398713") == "79927398713"


def test_doubled_digit_five_is_accepted():
    # "59": the doubled 5 gives 10 -> 1 + 0 = 1, and 9 + 1 = 10, which is valid.
    assert validate("59") == "59"


@pytest.mark.parametrize(
    "payload", ["5", "6", "7", "8", "9", "1234567", "4539", "79927398"]
)
def test_numbers_with_doubled_digits_five_or_more_are_accepted(payload):
    number = _with_check_digit(payload)
    assert _reference_luhn_ok(number)
    assert validate(number) == number


def test_invalid_number_with_doubled_digit_five_or_more_is_rejected():
    # Last digit of the valid example changed from 3 to 4: checksum no longer 0.
    invalid = "79927398714"
    with pytest.raises(InvalidChecksum):
        validate(invalid)
