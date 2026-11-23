"""Pytest suite for alvo.py (Brazilian CPF normalisation and validation)."""

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


# ---------------------------------------------------------------------------
# Independent reference for the CPF check digits.
# Written in the textbook form (remainder < 2 -> 0, else 11 - remainder) so the
# tests do not simply mirror the arithmetic inside alvo.py.
# ---------------------------------------------------------------------------

def _reference_check_digits(body):
    digits = [int(c) for c in body]
    s1 = sum(d * w for d, w in zip(digits, range(10, 1, -1)))
    r1 = s1 % 11
    d1 = 0 if r1 < 2 else 11 - r1
    s2 = sum(d * w for d, w in zip(digits + [d1], range(11, 1, -1)))
    r2 = s2 % 11
    d2 = 0 if r2 < 2 else 11 - r2
    return f"{d1}{d2}"


def _make_cpf(body):
    return body + _reference_check_digits(body)


def _format_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def _pseudo_random_bodies(count, seed=20240601):
    """Deterministic 9-digit strings (simple LCG) so runs are reproducible."""
    state = seed
    bodies = []
    for _ in range(count):
        digits = []
        for _ in range(9):
            state = (state * 1103515245 + 12345) & 0x7FFFFFFF
            digits.append(str((state >> 16) % 10))
        bodies.append("".join(digits))
    return bodies


KNOWN_VALID = [
    ("11144477735", "111.444.777-35"),
    ("52998224725", "529.982.247-25"),
    ("12345678909", "123.456.789-09"),
]

VALID_BODIES = [
    "123456789",
    "111444777",
    "529982247",
    "100000000",
    "000000001",
    "000000006",
    "000000010",
    "012345678",
    "246813579",
    "500000000",
    "987654321",
    "999999998",
]

RANDOM_BODIES = [b for b in _pseudo_random_bodies(60) if set(b) != {"0"}]

SINGLE_DIGIT_BODIES = [
    "0" * i + str(d) + "0" * (8 - i) for i in range(9) for d in range(1, 10)
]


class TestExceptionHierarchy:
    def test_validation_error_is_a_value_error(self):
        assert issubclass(ValidationError, ValueError)
        assert isinstance(ValidationError("x"), ValueError)

    def test_format_and_checksum_errors_are_validation_errors(self):
        assert issubclass(InvalidFormat, ValidationError)
        assert issubclass(InvalidChecksum, ValidationError)

    def test_length_error_is_a_format_error(self):
        assert issubclass(InvalidLength, InvalidFormat)
        assert issubclass(InvalidLength, ValidationError)

    def test_checksum_error_is_not_a_format_error(self):
        assert not issubclass(InvalidChecksum, InvalidFormat)
        assert not issubclass(InvalidChecksum, InvalidLength)

    def test_format_error_is_not_a_length_error(self):
        assert not issubclass(InvalidFormat, InvalidLength)


class TestClean:
    @pytest.mark.parametrize("value", ["", "abc", "123", "a b-c.d"])
    def test_without_deletechars_nothing_is_removed(self, value):
        assert clean(value) == value

    def test_removes_each_listed_character(self):
        assert clean("a-b.c", "-.") == "abc"

    def test_removes_every_occurrence(self):
        assert clean("1-1-1-1", "-") == "1111"

    def test_each_deletechar_is_removed_individually(self):
        assert clean("abcabc", "ab") == "cc"

    def test_only_listed_characters_are_removed(self):
        assert clean("hello world", "lo") == "he wrd"

    def test_space_is_kept_unless_listed(self):
        assert clean("1 2") == "1 2"
        assert clean("1 2", " ") == "12"

    def test_empty_deletechars_removes_nothing(self):
        assert clean("-.", "") == "-."

    def test_removing_all_characters_gives_empty_string(self):
        assert clean("---", "-") == ""

    def test_does_not_strip_whitespace(self):
        assert clean("  a  ") == "  a  "

    def test_accepts_list_of_characters(self):
        assert clean(["1", "-", "2"], "-") == "12"

    def test_accepts_list_of_strings(self):
        assert clean(["ab", "c"]) == "abc"

    def test_accepts_tuple(self):
        assert clean(("1", "2")) == "12"

    def test_accepts_generator(self):
        assert clean((c for c in "1-2"), "-") == "12"

    def test_empty_iterable_gives_empty_string(self):
        assert clean([]) == ""

    @pytest.mark.parametrize("bad", [None, 123, 12.5, object()])
    def test_non_iterable_raises_invalid_format(self, bad):
        with pytest.raises(InvalidFormat) as info:
            clean(bad)
        assert type(info.value) is InvalidFormat

    def test_non_string_items_raise_invalid_format(self):
        with pytest.raises(InvalidFormat) as info:
            clean([1, 2, 3])
        assert type(info.value) is InvalidFormat

    def test_bytes_raise_invalid_format(self):
        with pytest.raises(InvalidFormat):
            clean(b"123")


class TestIsDigits:
    @pytest.mark.parametrize("value", ["0", "7", "10", "0123456789", "000", "9" * 50])
    def test_digit_strings_are_true(self, value):
        assert isdigits(value) is True

    @pytest.mark.parametrize("value", [
        "", " ", "\n", "\t1", " 1", "1 ", "1 2", "1\n2", "12\n\n",
        "12a", "a12", "-1", "+1", "1.0", "1,0", "1e3", "١٢",
    ])
    def test_non_digit_strings_are_false(self, value):
        assert isdigits(value) is False

    def test_trailing_newline_is_accepted_because_of_dollar_anchor(self):
        # '$' also matches just before a final newline; this documents that behaviour.
        assert isdigits("1\n") is True

    @pytest.mark.parametrize("bad", [None, 123, b"123"])
    def test_non_string_input_raises_type_error(self, bad):
        with pytest.raises(TypeError):
            isdigits(bad)


class TestCompact:
    @pytest.mark.parametrize("raw, expected", [
        ("", ""),
        ("123", "123"),
        ("123.456.789-09", "12345678909"),
        ("1-2", "12"),
        ("1.2", "12"),
        ("1 2", "12"),
        (" 1 2 ", "12"),
        ("1-.- 2", "12"),
        (" - . ", ""),
        ("   ", ""),
    ])
    def test_removes_dash_dot_and_space(self, raw, expected):
        assert compact(raw) == expected

    def test_strips_outer_whitespace(self):
        assert compact("\t123\n") == "123"
        assert compact("\r\n 123 \t") == "123"

    def test_keeps_interior_tabs_and_newlines(self):
        assert compact("12\t34") == "12\t34"
        assert compact("12\n34") == "12\n34"

    def test_keeps_other_punctuation(self):
        assert compact("1/2") == "1/2"
        assert compact("1_2") == "1_2"
        assert compact("1,2") == "1,2"

    def test_accepts_list_of_characters(self):
        assert compact(["1", "-", "2", " "]) == "12"

    @pytest.mark.parametrize("bad", [None, 123, b"12"])
    def test_invalid_input_raises_invalid_format(self, bad):
        with pytest.raises(InvalidFormat) as info:
            compact(bad)
        assert type(info.value) is InvalidFormat


class TestCalcCheckDigits:
    @pytest.mark.parametrize("body, expected", [
        ("111444777", "35"),
        ("529982247", "25"),
        ("123456789", "09"),
        ("000000000", "00"),
        ("000000006", "04"),
        ("000000001", "91"),
    ])
    def test_known_check_digits(self, body, expected):
        assert _calc_check_digits(body) == expected

    def test_reference_oracle_agrees_with_known_cpfs(self):
        for cpf, _ in KNOWN_VALID:
            assert _reference_check_digits(cpf[:9]) == cpf[9:]

    @pytest.mark.parametrize("body", VALID_BODIES + RANDOM_BODIES + SINGLE_DIGIT_BODIES)
    def test_matches_reference_algorithm(self, body):
        assert _calc_check_digits(body) == _reference_check_digits(body)

    def test_only_first_nine_digits_are_used(self):
        assert _calc_check_digits("11144477735") == "35"
        assert _calc_check_digits("11144477799") == "35"

    def test_returns_two_digit_string(self):
        result = _calc_check_digits("123456789")
        assert isinstance(result, str)
        assert len(result) == 2
        assert result.isdigit()

    def test_non_digit_body_raises_value_error(self):
        with pytest.raises(ValueError):
            _calc_check_digits("abcdefghi")


class TestValidateAccepts:
    @pytest.mark.parametrize("cpf, formatted", KNOWN_VALID)
    def test_plain_digits(self, cpf, formatted):
        assert validate(cpf) == cpf

    @pytest.mark.parametrize("cpf, formatted", KNOWN_VALID)
    def test_formatted_input_returns_plain_digits(self, cpf, formatted):
        assert validate(formatted) == cpf

    def test_spaces_as_separators(self):
        assert validate("529 982 247 25") == "52998224725"
        assert validate("1 1 1 4 4 4 7 7 7 3 5") == "11144477735"

    def test_outer_whitespace_is_removed_from_result(self):
        assert validate("  123.456.789-09  ") == "12345678909"
        assert validate("52998224725\n") == "52998224725"

    def test_leading_zeros_are_kept(self):
        assert validate("00000000191") == "00000000191"
        assert validate("000.000.001-91") == "00000000191"

    def test_zero_first_check_digit_is_accepted(self):
        assert validate("00000000604") == "00000000604"

    def test_accepts_list_of_characters(self):
        assert validate(list("11144477735")) == "11144477735"

    @pytest.mark.parametrize("body", VALID_BODIES + RANDOM_BODIES)
    def test_generated_valid_numbers_round_trip(self, body):
        cpf = _make_cpf(body)
        assert validate(cpf) == cpf
        assert validate(_format_cpf(cpf)) == cpf


class TestValidateFormat:
    @pytest.mark.parametrize("raw", [
        "",
        "   ",
        "-.",
        "abc",
        "1234567890a",
        "a1234567890",
        "123456789O9",
        "529.982.247-2a",
        "1\t1144477735",
        "111444777 35x",
        "529982247\n25",
        "+11144477735",
        "111/444/777-35",
    ])
    def test_non_digit_characters_raise_invalid_format(self, raw):
        with pytest.raises(InvalidFormat) as info:
            validate(raw)
        assert type(info.value) is InvalidFormat

    @pytest.mark.parametrize("raw", [
        "0", "000", "00000000000", "000.000.000-00", " 0 ", "-0-",
    ])
    def test_all_zero_number_is_rejected_as_format_error(self, raw):
        with pytest.raises(InvalidFormat) as info:
            validate(raw)
        assert type(info.value) is InvalidFormat

    @pytest.mark.parametrize("raw", [None, 11144477735, 1.5, object()])
    def test_non_iterable_input_raises_invalid_format(self, raw):
        with pytest.raises(InvalidFormat):
            validate(raw)


class TestValidateLength:
    @pytest.mark.parametrize("raw", [
        "1",
        "12",
        "1234567890",
        "123456789012",
        "1" * 20,
        "12345678901234",
        "123.456.789-0",
        " 1234567890 ",
    ])
    def test_wrong_length_raises_invalid_length(self, raw):
        with pytest.raises(InvalidLength) as info:
            validate(raw)
        assert type(info.value) is InvalidLength


class TestValidateChecksum:
    @pytest.mark.parametrize("raw", [
        "11144477736",
        "11144477725",
        "11144477700",
        "11144478735",
        "52998224726",
        "52998224715",
        "12345678900",
        "12345678999",
        "111.444.777-36",
    ])
    def test_wrong_check_digits_raise_invalid_checksum(self, raw):
        with pytest.raises(InvalidChecksum) as info:
            validate(raw)
        assert type(info.value) is InvalidChecksum

    @pytest.mark.parametrize("body", VALID_BODIES + RANDOM_BODIES)
    def test_wrong_second_check_digit_is_rejected(self, body):
        cpf = _make_cpf(body)
        wrong = cpf[:10] + str((int(cpf[10]) + 1) % 10)
        with pytest.raises(InvalidChecksum):
            validate(wrong)

    @pytest.mark.parametrize("body", VALID_BODIES + RANDOM_BODIES)
    def test_wrong_first_check_digit_is_rejected(self, body):
        cpf = _make_cpf(body)
        wrong = cpf[:9] + str((int(cpf[9]) + 1) % 10) + cpf[10]
        with pytest.raises(InvalidChecksum):
            validate(wrong)

    @pytest.mark.parametrize("body", VALID_BODIES)
    def test_single_digit_body_change_is_detected(self, body):
        suffix = _reference_check_digits(body)
        for i in range(9):
            for digit in "0123456789":
                if digit == body[i]:
                    continue
                new_body = body[:i] + digit + body[i + 1:]
                candidate = new_body + suffix
                if set(candidate) == {"0"}:
                    continue
                if _reference_check_digits(new_body) == suffix:
                    assert validate(candidate) == candidate
                else:
                    with pytest.raises(InvalidChecksum):
                        validate(candidate)


class TestValidationErrorBase:
    @pytest.mark.parametrize("raw", ["", "abc", "1", "11144477736", "000"])
    def test_all_failures_are_validation_errors(self, raw):
        with pytest.raises(ValidationError):
            validate(raw)
