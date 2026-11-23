"""Pytest suite for alvo.py (Brazilian CPF validation helpers)."""

import random

import pytest

from alvo import (
    InvalidChecksum,
    InvalidFormat,
    InvalidLength,
    ValidationError,
    _calc_check_digits,
    clean,
    compact,
    isdigits,
    validate,
)

# Known CPF numbers (check digits computed by the official algorithm).
VALID_CPF = "12345678909"  # 123.456.789-09
VALID_CPF_B = "11144477735"  # 111.444.777-35
VALID_CPF_C = "52998224725"  # 529.982.247-25
# Check digits that hit the "remainder 0 or 1 -> digit 0" rule.
ZERO_FIRST_DIGIT_CPF = "00000000604"  # first check digit is 0 (remainder 1)
ZERO_SECOND_DIGIT_CPF = "00000009300"  # second check digit is 0 (remainder 1)
REPEATED_DIGITS_CPF = "11111111111"  # accepted: module has no repeated-digit rule


def _error_type(func, *args):
    """Return the exact exception class raised by func(*args)."""
    with pytest.raises(ValidationError) as excinfo:
        func(*args)
    return type(excinfo.value)


def _ref_dv(digits, top):
    """Independent oracle for one check digit (weights top, top-1, ..., 2)."""
    total = sum(d * w for d, w in zip(digits, range(top, 1, -1)))
    rest = total % 11
    return 0 if rest < 2 else 11 - rest


def _ref_check(prefix9):
    digits = [int(c) for c in prefix9]
    d1 = _ref_dv(digits, 10)
    d2 = _ref_dv(digits + [d1], 11)
    return f"{d1}{d2}"


# --- exception hierarchy ---------------------------------------------------

def test_exception_hierarchy():
    assert issubclass(ValidationError, ValueError)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidChecksum, ValidationError)
    assert issubclass(InvalidLength, InvalidFormat)
    assert issubclass(InvalidLength, ValidationError)
    assert not issubclass(InvalidChecksum, InvalidFormat)
    assert not issubclass(InvalidFormat, InvalidLength)


def test_validation_errors_are_value_errors():
    with pytest.raises(ValueError):
        validate("")


# --- clean -----------------------------------------------------------------

def test_clean_without_deletechars_keeps_everything():
    assert clean("a-b.c 1") == "a-b.c 1"


def test_clean_removes_each_listed_char():
    assert clean("1.2-3 4", " -.") == "1234"


def test_clean_keeps_order_of_remaining_chars():
    assert clean("a1b2c3", "b") == "a12c3"


def test_clean_deletechars_can_be_a_list():
    assert clean("1.2-3", [".", "-"]) == "123"


def test_clean_empty_input():
    assert clean("") == ""
    assert clean("", " -.") == ""


def test_clean_can_delete_everything():
    assert clean("...", ".") == ""


def test_clean_accepts_any_iterable_of_strings():
    assert clean(["1", "2", "3"]) == "123"
    assert clean(iter("4-5"), "-") == "45"


def test_clean_returns_str():
    assert isinstance(clean("123"), str)


@pytest.mark.parametrize("bad", [None, 123, 1.5, b"123", ["1", 2]])
def test_clean_rejects_non_iterables_and_non_string_items(bad):
    assert _error_type(clean, bad) is InvalidFormat


# --- isdigits --------------------------------------------------------------

@pytest.mark.parametrize("value", ["0", "7", "123", "0000", "12345678909"])
def test_isdigits_accepts_ascii_digit_strings(value):
    assert isdigits(value) is True


@pytest.mark.parametrize(
    "value",
    ["", " ", "12a", "a12", "1 2", " 12", "12 ", "1.2", "-1", "+1", "1,000",
     "١٢", "²"],
)
def test_isdigits_rejects_everything_else(value):
    assert isdigits(value) is False


def test_isdigits_dollar_matches_before_trailing_newline():
    # The regex uses '$', which also matches just before a final newline.
    assert isdigits("123\n") is True


def test_isdigits_rejects_none():
    with pytest.raises(TypeError):
        isdigits(None)


# --- compact ---------------------------------------------------------------

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("111.444.777-35", "11144477735"),
        ("123 456 789 09", "12345678909"),
        (" 123.456.789-09 ", "12345678909"),
        ("1-2.3 4", "1234"),
        ("   ", ""),
        ("", ""),
        (" - . ", ""),
        ("\t123\n", "123"),
        ("1/2/3", "1/2/3"),
        ("abc", "abc"),
    ],
)
def test_compact(raw, expected):
    assert compact(raw) == expected


def test_compact_strips_only_outer_whitespace():
    assert compact("1\t2") == "1\t2"


def test_compact_rejects_none_and_non_iterables():
    assert _error_type(compact, None) is InvalidFormat
    assert _error_type(compact, 12345678909) is InvalidFormat


# --- _calc_check_digits ----------------------------------------------------

@pytest.mark.parametrize(
    "prefix, expected",
    [
        ("123456789", "09"),
        ("111444777", "35"),
        ("529982247", "25"),
        ("000000006", "04"),  # first digit: remainder 1 -> 0
        ("000000093", "00"),  # second digit: remainder 1 -> 0
        ("000000000", "00"),
        ("111111111", "11"),
    ],
)
def test_calc_check_digits_known_values(prefix, expected):
    assert _calc_check_digits(prefix) == expected


def test_calc_check_digits_ignores_last_two_chars():
    assert _calc_check_digits("11144477799") == "35"


def test_calc_check_digits_returns_two_digit_string():
    result = _calc_check_digits("529982247")
    assert isinstance(result, str)
    assert len(result) == 2
    assert result.isdigit()


def test_calc_check_digits_needs_nine_digits():
    with pytest.raises(IndexError):
        _calc_check_digits("12345678")


def test_calc_check_digits_matches_reference_on_random_prefixes():
    rng = random.Random(20240601)
    for _ in range(2000):
        prefix = "".join(rng.choice("0123456789") for _ in range(9))
        assert _calc_check_digits(prefix) == _ref_check(prefix)


# --- validate: valid inputs ------------------------------------------------

@pytest.mark.parametrize(
    "raw, expected",
    [
        (VALID_CPF, VALID_CPF),
        ("123.456.789-09", VALID_CPF),
        ("123 456 789 09", VALID_CPF),
        (" 123.456.789-09\n", VALID_CPF),
        ("111.444.777-35", VALID_CPF_B),
        ("529.982.247-25", VALID_CPF_C),
        (ZERO_FIRST_DIGIT_CPF, ZERO_FIRST_DIGIT_CPF),
        (ZERO_SECOND_DIGIT_CPF, ZERO_SECOND_DIGIT_CPF),
    ],
)
def test_validate_returns_normalised_digits(raw, expected):
    assert validate(raw) == expected


def test_validate_returns_str():
    assert isinstance(validate("123.456.789-09"), str)


def test_validate_accepts_repeated_digits_as_this_module_does():
    # The module only checks the check digits; it has no repeated-digit rule.
    assert validate(REPEATED_DIGITS_CPF) == REPEATED_DIGITS_CPF


def test_validate_accepts_generated_valid_numbers():
    rng = random.Random(7)
    for _ in range(500):
        prefix = "".join(rng.choice("0123456789") for _ in range(9))
        if int(prefix) == 0:
            continue
        full = prefix + _ref_check(prefix)
        assert validate(full) == full
        formatted = f"{full[:3]}.{full[3:6]}.{full[6:9]}-{full[9:]}"
        assert validate(formatted) == full


# --- validate: format errors -----------------------------------------------

@pytest.mark.parametrize(
    "raw",
    [
        None,
        12345678909,
        b"12345678909",
        "",
        "   ",
        "-",
        "123a5678909",
        "123.456.789-0A",
        "123/456/789-09",  # '/' is not removed by compact
        "123\n456789-09",  # inner newline is not allowed
        "١" * 11,  # non-ASCII digits
    ],
)
def test_validate_rejects_bad_format(raw):
    assert _error_type(validate, raw) is InvalidFormat


@pytest.mark.parametrize(
    "raw", ["0", "00000000000", "000.000.000-00", "0000000000000"]
)
def test_validate_rejects_all_zeros_as_format_error(raw):
    assert _error_type(validate, raw) is InvalidFormat


# --- validate: length errors -----------------------------------------------

@pytest.mark.parametrize(
    "raw",
    ["1", "123", "123456789", "1234567890", "123456789012", "1" * 12,
     "111.444.777-3"],
)
def test_validate_rejects_wrong_length(raw):
    assert _error_type(validate, raw) is InvalidLength


def test_invalid_length_is_also_an_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("123")


def test_length_is_checked_before_checksum():
    assert _error_type(validate, "1234567891") is InvalidLength


# --- validate: checksum errors ---------------------------------------------

@pytest.mark.parametrize(
    "raw",
    [
        "12345678900",  # wrong second check digit
        "12345678919",  # wrong first check digit
        "12345678910",  # check digits are wrong
        "12345678908",
        "11144477736",
        "52998224724",
        "11144477700",
        "00000000605",
    ],
)
def test_validate_rejects_bad_checksum(raw):
    assert _error_type(validate, raw) is InvalidChecksum


@pytest.mark.parametrize("pos", [9, 10])
def test_every_wrong_check_digit_is_detected(pos):
    for d in "0123456789":
        if d == VALID_CPF[pos]:
            continue
        candidate = VALID_CPF[:pos] + d + VALID_CPF[pos + 1:]
        assert _error_type(validate, candidate) is InvalidChecksum
