import pytest
from alvo import (
    clean,
    isdigits,
    compact,
    validate,
    InvalidFormat,
    InvalidLength,
    InvalidChecksum,
    _calc_check_digits,
)

def test_clean_basic_removal():
    # remove hyphen and space
    assert clean("12-34 5", deletechars=" -") == "12345"
    # without deletechars, only iterable conversion occurs
    assert clean("abc", deletechars="") == "abc"

def test_clean_non_iterable_raises():
    # Passing a non-iterable (int) should raise InvalidFormat
    with pytest.raises(InvalidFormat):
        clean(12345)

def test_isdigits_true_and_false():
    assert isdigits("012345") is True
    assert isdigits("00123a") is False
    # empty string does not match the regex
    assert isdigits("") is False

def test_compact_strips_and_deletes():
    # compact should delete spaces, hyphens, dots and strip surrounding whitespace
    raw = "  12.34-5 6 7 8 9 "
    # After cleaning, should be "123456789"
    assert compact(raw) == "123456789"

def _make_valid_number(first9: str) -> str:
    """Return an 11‑digit number with correct check digits for the given first 9 digits."""
    check = _calc_check_digits(first9)
    return first9 + check

def test_calc_check_digits_known():
    # Using the algorithm directly on a known base should give expected check digits
    base = "123456789"
    expected = _calc_check_digits(base)
    # The algorithm yields '09' for this base
    assert expected == "09"
    # Verify that the full number passes validation
    full = base + expected
    assert validate(full) == full

def test_validate_success_and_normalisation():
    base = "987654321"
    full = _make_valid_number(base)
    # Insert formatting characters that should be ignored by compact/validate
    formatted = f" {full[:3]}.{full[3:6]}-{full[6:]} "
    # validate should return the compacted, clean version
    assert validate(formatted) == full

def test_validate_invalid_format_non_digit():
    # Contains a letter
    with pytest.raises(InvalidFormat):
        validate("12345A78901")

def test_validate_invalid_length():
    # Too short (10 digits after compaction)
    short = "1234567890"
    with pytest.raises(InvalidLength):
        validate(short)
    # Too long (12 digits)
    long = "123456789012"
    with pytest.raises(InvalidLength):
        validate(long)

def test_validate_invalid_checksum():
    base = "111111111"
    valid = _make_valid_number(base)
    # Corrupt the last check digit
    corrupted = valid[:-1] + ("0" if valid[-1] != "0" else "1")
    with pytest.raises(InvalidChecksum):
        validate(corrupted)

def test_validate_zero_or_negative():
    # All zeros should be rejected as int(number) <= 0
    zeros = "0" * 11
    with pytest.raises(InvalidFormat):
        validate(zeros)
    # Leading minus is stripped by compact, resulting in a checksum error
    with pytest.raises(InvalidChecksum):
        validate("-12345678901")
