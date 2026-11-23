import pytest

from alvo import InvalidChecksum, checksum, validate


def luhn_is_valid(number):
    """Reference Luhn check (base 10), used as an oracle."""
    total = 0
    for pos, ch in enumerate(reversed(number)):
        digit = int(ch)
        if pos % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def luhn_check_digit(prefix):
    for candidate in "0123456789":
        if luhn_is_valid(prefix + candidate):
            return candidate
    raise AssertionError("no valid check digit exists")


def test_issue_example_is_accepted():
    assert validate('79927398713') == '79927398713'


def test_issue_example_checksum_is_zero():
    assert checksum('79927398713') == 0


def test_doubled_digit_of_five_is_accepted():
    # Doubling 5 gives 10, whose digit sum is 1; 1 + 9 = 10 is valid Luhn.
    assert validate('59') == '59'


@pytest.mark.parametrize("prefix", [
    "7992739871",
    "5",
    "55",
    "59",
    "555555",
    "9876543215",
    "4539148803436",
    "1234567895",
])
def test_valid_numbers_with_large_doubled_digits_are_accepted(prefix):
    number = prefix + luhn_check_digit(prefix)
    assert luhn_is_valid(number)
    assert validate(number) == number


@pytest.mark.parametrize("prefix", [
    "7992739871",
    "5",
    "55",
    "555555",
    "4539148803436",
])
def test_wrong_check_digit_is_rejected(prefix):
    valid_digit = luhn_check_digit(prefix)
    wrong_digit = "0" if valid_digit != "0" else "1"
    with pytest.raises(InvalidChecksum):
        validate(prefix + wrong_digit)
note>The test file reproduces the bug: on the current alvo.py the issue example and the other valid-number tests fail with InvalidChecksum, and with a corrected checksum (patched in-process, alvo.py untouched) all 16 tests pass.
