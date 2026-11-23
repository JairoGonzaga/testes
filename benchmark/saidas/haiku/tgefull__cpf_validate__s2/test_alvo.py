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

TAB = chr(9)
NL = chr(10)


# ---------------------------------------------------------------------------
# Helpers and reference data
# ---------------------------------------------------------------------------


def raises_exactly(exc_type, func, *args):
    """Assert that func raises exc_type itself, not merely a subclass of it."""
    with pytest.raises(exc_type) as info:
        func(*args)
    assert type(info.value) is exc_type, (
        f"expected exactly {exc_type.__name__}, got {type(info.value).__name__}"
    )
    return info.value


def reference_check_digits(base9):
    """Independent implementation of the CPF check-digit rule for nine base digits."""
    assert len(base9) == 9 and base9.isdigit()
    digits = [int(c) for c in base9]
    s1 = sum(w * d for w, d in zip(range(10, 1, -1), digits))
    r1 = 11 - s1 % 11
    d1 = 0 if r1 >= 10 else r1
    s2 = sum(w * d for w, d in zip(range(11, 2, -1), digits)) + 2 * d1
    r2 = 11 - s2 % 11
    d2 = 0 if r2 >= 10 else r2
    return f"{d1}{d2}"


def _random_bases(count, seed):
    rng = random.Random(seed)
    bases = []
    for _ in range(count):
        first = str(rng.randint(1, 9))  # non-zero lead keeps the number positive
        rest = "".join(str(rng.randint(0, 9)) for _ in range(8))
        bases.append(first + rest)
    return bases


RANDOM_BASES = _random_bases(120, seed=20240601)

# Hand-verified valid numbers (check digits worked out against the algorithm).
VALID_CPFS = [
    "12345678909",  # first remainder is 1, so first check digit is 0
    "11144477735",
    "52998224725",  # exercises the 2 * d1 term in the second check digit
    "10000004006",  # first remainder is 0, so first check digit is 0
    "60000000060",  # second remainder is 1, so second check digit is 0
]

INVALID_FORMAT_STRINGS = [
    "",
    " ",
    "   ",
    "-",
    ".-. ",
    "abc",
    "1234567890a",
    "12345678909x",
    "x12345678909",
    "+12345678909",
    "12/34567890",
    "123" + TAB + "45678909",
    "12" + NL + "345678909",
    "12a45678909",
    "0",
    "00",
    "0000000000",
    "00000000000",
    "0000000000000",
]

INVALID_LENGTH_STRINGS = [
    "1",
    "-1",
    "12",
    "1234567890",
    "123456789090",
    "1234567890123",
    "123.456.789",
    "123.456.789-0",
    "9" * 20,
]

INVALID_CHECKSUM_STRINGS = [
    "12345678900",
    "12345678919",
    "12345678999",
    "11144477736",
    "11144477705",
    "52998224736",
    "60000000050",
    "00000000001",
    "123.456.789-10",
]

NON_STRING_INPUTS = [None, 12345678909, 1.5, b"12345678909", ["1", 2]]


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------


class TestExceptionHierarchy:
    def test_validation_error_is_a_value_error(self):
        assert issubclass(ValidationError, ValueError)

    def test_invalid_format_is_a_validation_error(self):
        assert issubclass(InvalidFormat, ValidationError)

    def test_invalid_checksum_is_a_validation_error(self):
        assert issubclass(InvalidChecksum, ValidationError)

    def test_invalid_length_is_an_invalid_format(self):
        assert issubclass(InvalidLength, InvalidFormat)
        assert issubclass(InvalidLength, ValidationError)

    def test_checksum_error_is_not_a_format_or_length_error(self):
        assert not issubclass(InvalidChecksum, InvalidFormat)
        assert not issubclass(InvalidChecksum, InvalidLength)

    def test_format_error_is_not_a_length_error(self):
        assert not issubclass(InvalidFormat, InvalidLength)


# ---------------------------------------------------------------------------
# clean()
# ---------------------------------------------------------------------------


class TestClean:
    def test_default_deletes_nothing(self):
        assert clean("a-b.c d") == "a-b.c d"

    def test_empty_string(self):
        assert clean("") == ""

    @pytest.mark.parametrize(
        "number, deletechars, expected",
        [
            ("1-2.3", "-.", "123"),
            ("a b c", " ", "abc"),
            ("aaa", "a", ""),
            ("abc", "abc", ""),
            ("3-2-1", "-", "321"),
            ("x1y", "xy", "1"),
            ("a" + NL + "b", "", "a" + NL + "b"),
            ("a" + NL + "b", NL, "ab"),
            ("ação-1", "-", "ação1"),
        ],
    )
    def test_removes_only_listed_characters(self, number, deletechars, expected):
        assert clean(number, deletechars) == expected

    def test_deletechars_as_keyword(self):
        assert clean("1-2", deletechars="-") == "12"

    def test_deletechars_can_be_a_set(self):
        assert clean("a-b", {"-"}) == "ab"

    def test_preserves_order(self):
        assert clean("9-8-7-6", "-") == "9876"

    def test_is_case_sensitive(self):
        assert clean("aA", "a") == "A"

    def test_accepts_list_of_characters(self):
        assert clean(["1", "-", "2"], "-") == "12"

    def test_accepts_tuple(self):
        assert clean(("4", "5")) == "45"

    def test_accepts_generator(self):
        assert clean((c for c in "7-8"), "-") == "78"

    @pytest.mark.parametrize("bad", NON_STRING_INPUTS)
    def test_non_iterable_or_non_string_items_raise_invalid_format(self, bad):
        raises_exactly(InvalidFormat, clean, bad)

    def test_invalid_format_raised_even_with_deletechars(self):
        raises_exactly(InvalidFormat, clean, 123, "-")

    def test_any_exception_while_iterating_becomes_invalid_format(self):
        def exploding():
            yield "1"
            raise RuntimeError("boom")

        raises_exactly(InvalidFormat, clean, exploding())


# ---------------------------------------------------------------------------
# isdigits()
# ---------------------------------------------------------------------------


class TestIsDigits:
    @pytest.mark.parametrize("text", ["0", "5", "0123456789", "12345678909", "9" * 50])
    def test_accepts_ascii_digit_strings(self, text):
        assert isdigits(text) is True

    @pytest.mark.parametrize(
        "text",
        [
            "",
            " ",
            " 1",
            "1 ",
            "1 2",
            "12a",
            "a12",
            "1.2",
            "1,2",
            "-1",
            "+1",
            "1/2",
            TAB + "1",
            "1" + TAB,
        ],
    )
    def test_rejects_anything_but_ascii_digits(self, text):
        assert isdigits(text) is False

    def test_rejects_non_ascii_digits(self):
        assert isdigits(chr(0x661) + chr(0x662) + chr(0x663)) is False  # Arabic-Indic
        assert isdigits(chr(0xFF11) + chr(0xFF12)) is False  # fullwidth

    def test_rejects_embedded_newline(self):
        assert isdigits("12" + NL + "3") is False

    def test_pinned_quirk_dollar_matches_before_trailing_newline(self):
        # re's `$` also matches just before a final newline. This documents the
        # current behaviour; validate() is unaffected because compact() strips it.
        assert isdigits("123" + NL) is True

    def test_returns_bool(self):
        assert type(isdigits("1")) is bool
        assert type(isdigits("x")) is bool

    @pytest.mark.parametrize("bad", NON_STRING_INPUTS)
    def test_non_string_raises_type_error(self, bad):
        with pytest.raises(TypeError):
            isdigits(bad)


# ---------------------------------------------------------------------------
# compact()
# ---------------------------------------------------------------------------


class TestCompact:
    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("123.456.789-09", "12345678909"),
            ("111.444.777-35", "11144477735"),
            ("1 2 3", "123"),
            ("1-2-3", "123"),
            ("1.2.3", "123"),
            ("  1 . 2 - 3  ", "123"),
            ("12/34", "12/34"),
            ("a-b", "ab"),
            ("", ""),
            ("-.- ", ""),
        ],
    )
    def test_removes_spaces_dots_and_hyphens(self, raw, expected):
        assert compact(raw) == expected

    def test_strips_surrounding_tabs_and_newlines(self):
        assert compact(TAB + "12345678909" + NL) == "12345678909"

    def test_keeps_inner_tab(self):
        assert compact("1" + TAB + "2") == "1" + TAB + "2"

    def test_list_input_is_joined_then_cleaned(self):
        assert compact(["1", ".", "2", "-", "3"]) == "123"

    @pytest.mark.parametrize("bad", NON_STRING_INPUTS)
    def test_non_string_input_raises_invalid_format(self, bad):
        raises_exactly(InvalidFormat, compact, bad)


# ---------------------------------------------------------------------------
# _calc_check_digits()
# ---------------------------------------------------------------------------


class TestCalcCheckDigits:
    @pytest.mark.parametrize(
        "base, expected",
        [
            ("123456789", "09"),
            ("111444777", "35"),
            ("529982247", "25"),
            ("100000040", "06"),
            ("600000000", "60"),
            ("000000000", "00"),
        ],
    )
    def test_known_vectors(self, base, expected):
        assert _calc_check_digits(base) == expected

    def test_only_first_nine_digits_contribute(self):
        assert _calc_check_digits("12345678999") == "09"

    def test_result_is_two_decimal_digits(self):
        result = _calc_check_digits("529982247")
        assert isinstance(result, str)
        assert len(result) == 2
        assert result.isdigit()


# ---------------------------------------------------------------------------
# validate(): accepted inputs
# ---------------------------------------------------------------------------


class TestValidateAccepts:
    @pytest.mark.parametrize("cpf", VALID_CPFS)
    def test_known_valid_numbers_are_returned_unchanged(self, cpf):
        assert validate(cpf) == cpf

    @pytest.mark.parametrize(
        "raw, expected",
        [
            ("123.456.789-09", "12345678909"),
            ("111.444.777-35", "11144477735"),
            ("529.982.247-25", "52998224725"),
            ("100.000.040-06", "10000004006"),
            ("600.000.000-60", "60000000060"),
            ("123 456 789 09", "12345678909"),
            ("123-456-789-09", "12345678909"),
            ("  123.456.789-09  ", "12345678909"),
            (TAB + "123.456.789-09" + NL, "12345678909"),
            ("12345678909" + NL, "12345678909"),
        ],
    )
    def test_formatted_input_is_normalised(self, raw, expected):
        assert validate(raw) == expected

    def test_returns_a_str(self):
        assert type(validate("12345678909")) is str

    def test_accepts_list_of_characters(self):
        assert validate(list("123.456.789-09")) == "12345678909"

    def test_repeated_digits_pass_when_check_digits_match(self):
        # Only the check-digit rule is applied; repeated digits are not rejected.
        assert validate("11111111111") == "11111111111"


# ---------------------------------------------------------------------------
# validate(): error paths
# ---------------------------------------------------------------------------


class TestValidateFormatErrors:
    @pytest.mark.parametrize("raw", INVALID_FORMAT_STRINGS)
    def test_bad_characters_or_zero_value_raise_invalid_format(self, raw):
        raises_exactly(InvalidFormat, validate, raw)

    @pytest.mark.parametrize("bad", NON_STRING_INPUTS)
    def test_non_string_input_raises_invalid_format(self, bad):
        raises_exactly(InvalidFormat, validate, bad)

    def test_all_zeros_is_format_error_not_checksum_error(self):
        # All zeros satisfy the checksum but fail the positive-number rule.
        raises_exactly(InvalidFormat, validate, "00000000000")

    def test_zero_is_rejected_before_length_is_checked(self):
        raises_exactly(InvalidFormat, validate, "0")

    def test_format_error_takes_precedence_over_length(self):
        # Eleven characters, but not all digits.
        raises_exactly(InvalidFormat, validate, "1234567890a")


class TestValidateLengthErrors:
    @pytest.mark.parametrize("raw", INVALID_LENGTH_STRINGS)
    def test_wrong_digit_count_raises_invalid_length(self, raw):
        raises_exactly(InvalidLength, validate, raw)

    def test_length_error_is_also_an_invalid_format(self):
        err = raises_exactly(InvalidLength, validate, "1234567890")
        assert isinstance(err, InvalidFormat)
        assert isinstance(err, ValidationError)


class TestValidateChecksumErrors:
    @pytest.mark.parametrize("raw", INVALID_CHECKSUM_STRINGS)
    def test_wrong_check_digits_raise_invalid_checksum(self, raw):
        raises_exactly(InvalidChecksum, validate, raw)

    def test_checksum_error_is_a_validation_error(self):
        err = raises_exactly(InvalidChecksum, validate, "12345678900")
        assert isinstance(err, ValidationError)
        assert not isinstance(err, InvalidFormat)


# ---------------------------------------------------------------------------
# Generated numbers (differential checks against the reference rule)
# ---------------------------------------------------------------------------


class TestGeneratedNumbers:
    @pytest.mark.parametrize("base", RANDOM_BASES)
    def test_calc_check_digits_matches_reference(self, base):
        assert _calc_check_digits(base) == reference_check_digits(base)

    @pytest.mark.parametrize("base", RANDOM_BASES)
    def test_generated_number_is_accepted(self, base):
        full = base + reference_check_digits(base)
        assert validate(full) == full

    @pytest.mark.parametrize("base", RANDOM_BASES)
    def test_generated_number_is_accepted_when_formatted(self, base):
        check = reference_check_digits(base)
        formatted = f"{base[:3]}.{base[3:6]}.{base[6:]}-{check}"
        assert validate(formatted) == base + check

    @pytest.mark.parametrize("base", RANDOM_BASES[:40])
    def test_generated_number_with_wrong_check_digits_is_rejected(self, base):
        check = reference_check_digits(base)
        wrong = f"{(int(check) + 1) % 100:02d}"
        raises_exactly(InvalidChecksum, validate, base + wrong)
