"""Reproduction tests for the Luhn validation bug described in ISSUE.md.

The checksum implementation doubles every second digit but folds the result
with ``(digit * 2) % 10`` instead of summing the *digits* of the doubled
value.  As soon as a doubled digit is 5 or greater (5*2 = 10, 6*2 = 12, ...)
the carried tens are lost, so perfectly valid Luhn numbers are rejected with
``InvalidChecksum``.

All assertions below only use the public ``validate`` API, so they hold for
any correct implementation of the Luhn algorithm.
"""

import pytest

from alvo import InvalidChecksum, InvalidFormat, validate


def _luhn_ok(number):
    """Reference (correct) Luhn implementation used to build expectations."""
    digits = [int(c) for c in reversed(str(number))]
    total = sum(digits[::2])
    total += sum(sum(divmod(d * 2, 10)) for d in digits[1::2])
    return total % 10 == 0


def _completa(payload):
    """Append the check digit that makes ``payload`` a valid Luhn number."""
    for candidate in "0123456789":
        number = payload + candidate
        if _luhn_ok(number):
            return number
    raise AssertionError("no check digit found for %r" % (payload,))


def test_reference_helper_agrees_with_known_luhn_values():
    # Sanity check of the helper itself (no library code involved).
    assert _luhn_ok("79927398713")
    assert _luhn_ok("4111111111111111")
    assert not _luhn_ok("79927398710")


def test_standard_luhn_example_is_accepted():
    """The exact case from the issue report: '79927398713' must be valid."""
    assert validate("79927398713") == "79927398713"


@pytest.mark.parametrize(
    "number",
    [
        "79927398713",  # issue example (doubled digit 9 -> 18)
        "59",           # 5 -> 10, 9 -> total 10 (multiple of 10)
        "18",           # regression guard: already worked before the fix
        "1234567812345670",
        "5555555555554444",
        "4012888888881881",
        "4111111111111111",  # regression guard: already worked before the fix
    ],
)
def test_valid_numbers_are_accepted(number):
    assert _luhn_ok(number)  # the fixture really is a valid Luhn number
    assert validate(number) == number


@pytest.mark.parametrize("payload", ["7992739871", "4", "5", "9", "799273987", "37828224631000"])
def test_generated_valid_numbers_are_accepted(payload):
    """Every properly computed check digit must be accepted."""
    number = _completa(payload)
    assert validate(number) == number


@pytest.mark.parametrize(
    "number",
    [
        "79927398710",
        "79927398711",
        "79927398712",
        "79927398714",
        "1234567812345671",
        "60",
        "9",
    ],
)
def test_invalid_checksums_are_still_rejected(number):
    assert not _luhn_ok(number)
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_wrong_check_digit_of_the_issue_example_is_rejected():
    # Same digits, last one changed: must not be silently accepted.
    assert validate("79927398713") == "79927398713"
    with pytest.raises(InvalidChecksum):
        validate("79927398714")


def test_integer_input_is_supported():
    assert validate(79927398713) == 79927398713


def test_empty_input_still_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("")
