"""Unit tests for alvo.py: Luhn-style mod-N checksum and validation."""

import random

import pytest

from alvo import (
    InvalidChecksum,
    InvalidFormat,
    ValidationError,
    checksum,
    validate,
)

DECIMAL = "0123456789"
HEX = "0123456789abcdef"
SMALL = "abc"

VALID_DECIMAL = [
    "0",
    "00",
    "18",
    "59",
    "79927398713",
    "4111111111111111",
    "5555555555554444",
    "378282246310005",
]


def reference_checksum(text, alphabet=DECIMAL):
    base = len(alphabet)
    total = 0
    for position, symbol in enumerate(reversed(text)):
        value = alphabet.index(symbol)
        if position % 2 == 1:
            doubled = value * 2
            value = doubled // base + doubled % base
        total += value
    return total % base


def random_texts(seed, alphabet, count=200, max_len=30):
    rng = random.Random(seed)
    texts = []
    for _ in range(count):
        length = rng.randint(1, max_len)
        texts.append("".join(rng.choice(alphabet) for _ in range(length)))
    return texts


class _UnprintableTruthy:
    def __bool__(self):
        return True

    def __str__(self):
        raise RuntimeError("cannot be rendered as text")


class _EmptyTextTruthy:
    def __bool__(self):
        return True

    def __str__(self):
        return ""


class TestErrorHierarchy:
    def test_validation_error_is_value_error(self):
        assert issubclass(ValidationError, ValueError)

    @pytest.mark.parametrize("error_type", [InvalidFormat, InvalidChecksum])
    def test_specific_errors_derive_from_validation_error(self, error_type):
        assert issubclass(error_type, ValidationError)
        assert issubclass(error_type, ValueError)

    def test_format_and_checksum_errors_are_siblings(self):
        assert not issubclass(InvalidFormat, InvalidChecksum)
        assert not issubclass(InvalidChecksum, InvalidFormat)

    def test_errors_can_be_raised_without_arguments(self):
        with pytest.raises(InvalidFormat):
            raise InvalidFormat()
        with pytest.raises(InvalidChecksum):
            raise InvalidChecksum()


class TestChecksumDecimal:
    @pytest.mark.parametrize(
        "number, expected",
        [
            ("0", 0),
            ("00", 0),
            ("1", 1),
            ("5", 5),
            ("10", 2),
            ("17", 9),
            ("18", 0),
            ("59", 0),
            ("50", 1),
            ("95", 4),
            ("79927398713", 0),
            ("79927398710", 7),
            ("4111111111111111", 0),
            ("4111111111111112", 1),
            ("5555555555554444", 0),
            ("378282246310005", 0),
        ],
    )
    def test_known_values(self, number, expected):
        assert checksum(number) == expected

    def test_default_alphabet_is_decimal(self):
        assert checksum("79927398713") == checksum("79927398713", DECIMAL) == 0
        assert checksum("17") == checksum("17", DECIMAL) == 9

    def test_integer_input_is_converted_with_str(self):
        assert checksum(79927398713) == 0
        assert checksum(4111111111111112) == 1
        assert checksum(18) == 0
        assert checksum(10) == 2

    def test_empty_string_has_zero_checksum(self):
        assert checksum("") == 0

    @pytest.mark.parametrize(
        "number",
        [-18, 1.5, True, "1.8", "1 8", "1a", "[1]", "１８"],
    )
    def test_symbols_outside_alphabet_raise_value_error(self, number):
        with pytest.raises(ValueError):
            checksum(number)

    def test_result_is_within_alphabet_range(self):
        for text in random_texts(seed=1, alphabet=DECIMAL):
            assert 0 <= checksum(text) <= 9

    def test_matches_reference_on_random_inputs(self):
        for text in random_texts(seed=2, alphabet=DECIMAL):
            assert checksum(text) == reference_checksum(text)


class TestChecksumCustomAlphabet:
    @pytest.mark.parametrize(
        "number, expected",
        [("0", 0), ("f", 15), ("0f", 15), ("1f", 1), ("8f", 0)],
    )
    def test_hex_known_values(self, number, expected):
        assert checksum(number, HEX) == expected

    @pytest.mark.parametrize(
        "number, expected",
        [("a", 0), ("aa", 0), ("bb", 0), ("cb", 0), ("ab", 1), ("ca", 2)],
    )
    def test_three_symbol_known_values(self, number, expected):
        assert checksum(number, SMALL) == expected

    def test_modulus_follows_alphabet_length(self):
        # A reduction modulo 10 would not agree with these expected values.
        assert checksum("8f", HEX) == 0
        assert checksum("1f", HEX) == 1

    def test_single_symbol_alphabet_always_sums_to_zero(self):
        assert checksum("a", "a") == 0
        assert checksum("aaa", "a") == 0

    def test_empty_alphabet_rejects_symbols(self):
        with pytest.raises(ValueError):
            checksum("1", alphabet="")

    def test_empty_alphabet_with_empty_number_divides_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            checksum("", alphabet="")

    def test_symbol_missing_from_alphabet_raises(self):
        with pytest.raises(ValueError):
            checksum("8g", HEX)
        with pytest.raises(ValueError):
            checksum("1", SMALL)

    def test_non_sequence_alphabet_raises_type_error(self):
        with pytest.raises(TypeError):
            checksum("18", None)

    @pytest.mark.parametrize("alphabet", [DECIMAL, HEX, SMALL])
    def test_matches_reference_on_random_inputs(self, alphabet):
        for text in random_texts(seed=7, alphabet=alphabet):
            assert checksum(text, alphabet) == reference_checksum(text, alphabet)


class TestCheckDigit:
    @pytest.mark.parametrize(
        "body, check_digit",
        [
            ("7992739871", "3"),
            ("411111111111111", "1"),
            ("1", "8"),
            ("5", "9"),
            ("", "0"),
        ],
    )
    def test_exactly_one_check_digit_closes_the_number(self, body, check_digit):
        valid_digits = [digit for digit in DECIMAL if checksum(body + digit) == 0]
        assert valid_digits == [check_digit]

    @pytest.mark.parametrize("number", VALID_DECIMAL)
    def test_every_single_digit_error_is_detected(self, number):
        for index, original in enumerate(number):
            for replacement in DECIMAL:
                if replacement == original:
                    continue
                mutated = number[:index] + replacement + number[index + 1 :]
                assert checksum(mutated) != 0
                with pytest.raises(InvalidChecksum):
                    validate(mutated)


class TestValidateAccepts:
    @pytest.mark.parametrize("number", VALID_DECIMAL)
    def test_returns_valid_string_unchanged(self, number):
        result = validate(number)
        assert result == number
        assert type(result) is str

    def test_returns_the_same_object(self):
        number = "79927398713"
        assert validate(number) is number

    def test_integer_input_is_accepted_and_returned_as_is(self):
        value = 79927398713
        result = validate(value)
        assert result is value
        assert isinstance(result, int)

    def test_default_alphabet_is_decimal(self):
        assert validate("18") == "18"
        assert validate("18", DECIMAL) == "18"

    def test_custom_alphabet_valid_values(self):
        assert validate("8f", HEX) == "8f"
        assert validate("bb", SMALL) == "bb"
        assert validate("cb", alphabet=SMALL) == "cb"
        assert validate("a", "a") == "a"

    @pytest.mark.parametrize("alphabet", [DECIMAL, HEX, SMALL])
    def test_random_inputs_agree_with_reference(self, alphabet):
        for text in random_texts(seed=11, alphabet=alphabet):
            if reference_checksum(text, alphabet) == 0:
                assert validate(text, alphabet) is text
            else:
                with pytest.raises(InvalidChecksum):
                    validate(text, alphabet)


class TestValidateChecksumFailures:
    @pytest.mark.parametrize(
        "number",
        ["10", "17", "19", "95", "4111111111111112", "79927398710", "378282246310006"],
    )
    def test_wrong_check_digit_raises_invalid_checksum(self, number):
        with pytest.raises(InvalidChecksum) as info:
            validate(number)
        assert type(info.value) is InvalidChecksum

    def test_hex_and_small_alphabet_checksum_failures(self):
        with pytest.raises(InvalidChecksum):
            validate("0f", HEX)
        with pytest.raises(InvalidChecksum):
            validate("f", HEX)
        with pytest.raises(InvalidChecksum):
            validate("ab", SMALL)


class TestValidateFormatFailures:
    @pytest.mark.parametrize("value", ["", 0, 0.0, None, False, [], (), {}])
    def test_falsy_values_are_invalid_format(self, value):
        with pytest.raises(InvalidFormat) as info:
            validate(value)
        assert type(info.value) is InvalidFormat

    @pytest.mark.parametrize(
        "value",
        [
            -18,
            1.5,
            18.0,
            True,
            [1, 8],
            ("1", "8"),
            "abc",
            "1 8",
            " 18",
            "18\n",
            "4111-1111-1111-1111",
            "1a",
            "１８",
        ],
    )
    def test_non_decimal_text_is_invalid_format(self, value):
        with pytest.raises(InvalidFormat) as info:
            validate(value)
        assert type(info.value) is InvalidFormat

    def test_symbol_outside_custom_alphabet_is_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("8g", HEX)
        with pytest.raises(InvalidFormat):
            validate("18", SMALL)

    def test_falsy_check_runs_before_checksum(self):
        # Falsy input is rejected even when the alphabet is unusable.
        with pytest.raises(InvalidFormat):
            validate("", alphabet=None)
        with pytest.raises(InvalidFormat):
            validate(0, alphabet=None)

    def test_checksum_exceptions_are_wrapped_as_invalid_format(self):
        with pytest.raises(InvalidFormat):
            validate("18", alphabet=None)
        with pytest.raises(InvalidFormat):
            validate("5", alphabet="")
        with pytest.raises(InvalidFormat):
            validate(_EmptyTextTruthy(), alphabet="")
        with pytest.raises(InvalidFormat):
            validate(_UnprintableTruthy())

    def test_wrapped_error_is_not_a_checksum_error(self):
        with pytest.raises(InvalidFormat) as info:
            validate(_UnprintableTruthy())
        assert type(info.value) is InvalidFormat

    @pytest.mark.parametrize("value", ["", "abc", "17"])
    def test_all_failures_are_validation_errors(self, value):
        with pytest.raises(ValidationError):
            validate(value)
