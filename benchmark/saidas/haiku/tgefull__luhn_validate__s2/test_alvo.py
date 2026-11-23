import itertools

import pytest

from alvo import InvalidChecksum, InvalidFormat, ValidationError, checksum, validate

DIGITS = "0123456789"
HEX = "0123456789abcdef"
BINARY = "01"
CARD_16 = "4" + "1" * 15


def reference_checksum(text, alphabet):
    """Independent Luhn-style oracle: every second digit from the right is doubled."""
    base = len(alphabet)
    total = 0
    for position, char in enumerate(reversed(text)):
        value = alphabet.index(char)
        if position % 2 == 1:
            doubled = 2 * value
            value = doubled if doubled < base else doubled - base + 1
        total += value
    return total % base


def is_valid(text, alphabet=DIGITS):
    try:
        validate(text, alphabet)
    except InvalidChecksum:
        return False
    return True


class Unprintable:
    def __str__(self):
        raise RuntimeError("no text form")


# Exception hierarchy

def test_validation_error_is_a_value_error():
    assert issubclass(ValidationError, ValueError)


def test_invalid_format_is_a_validation_error():
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidFormat, ValueError)


def test_invalid_checksum_is_a_validation_error():
    assert issubclass(InvalidChecksum, ValidationError)
    assert issubclass(InvalidChecksum, ValueError)


def test_format_and_checksum_errors_are_siblings():
    assert not issubclass(InvalidFormat, InvalidChecksum)
    assert not issubclass(InvalidChecksum, InvalidFormat)


# checksum: default alphabet

@pytest.mark.parametrize(
    "text, expected",
    [
        ("", 0),
        ("0", 0),
        ("9", 9),
        ("01", 1),
        ("10", 2),
        ("50", 1),
        ("90", 9),
        ("18", 0),
        ("59", 0),
        ("79927398713", 0),
        ("79927398710", 7),
        (CARD_16, 0),
        (CARD_16[:-1] + "2", 1),
    ],
)
def test_checksum_default_alphabet_known_values(text, expected):
    assert checksum(text) == expected


def test_checksum_defaults_to_decimal_digits():
    assert checksum("79927398710") == checksum("79927398710", DIGITS) == 7


def test_checksum_converts_non_string_numbers_with_str():
    assert checksum(79927398710) == 7
    assert checksum(0) == 0


def test_checksum_of_bool_fails_because_text_is_not_in_alphabet():
    with pytest.raises(ValueError):
        checksum(True)


# checksum: custom alphabets

@pytest.mark.parametrize(
    "text, alphabet, expected",
    [
        ("f1", HEX, 0),
        ("ff", HEX, 14),
        ("1f", HEX, 1),
        ("a", HEX, 10),
        ("f", HEX, 15),
        ("80", HEX, 1),
        ("11", BINARY, 0),
        ("10", BINARY, 1),
        ("0", "10", 1),
        ("0", "01", 0),
        ("aaa", "a", 0),
        ("xz", "xyz", 2),
    ],
)
def test_checksum_custom_alphabet_known_values(text, alphabet, expected):
    assert checksum(text, alphabet) == expected


def test_checksum_accepts_alphabet_as_keyword():
    assert checksum("f1", alphabet=HEX) == 0


@pytest.mark.parametrize(
    "text, alphabet",
    [
        ("abc", DIGITS),
        ("12a", DIGITS),
        ("-1", DIGITS),
        ("2", BINARY),
        ("1", ""),
    ],
)
def test_checksum_rejects_characters_outside_alphabet(text, alphabet):
    with pytest.raises(ValueError):
        checksum(text, alphabet)


def test_checksum_with_empty_alphabet_has_no_modulus():
    with pytest.raises(ZeroDivisionError):
        checksum("", "")


@pytest.mark.parametrize(
    "alphabet, max_length",
    [(DIGITS, 3), (HEX, 2), (BINARY, 6), ("xyz", 3), ("ab", 4)],
)
def test_checksum_matches_reference_for_every_short_string(alphabet, max_length):
    for length in range(max_length + 1):
        for chars in itertools.product(alphabet, repeat=length):
            text = "".join(chars)
            result = checksum(text, alphabet)
            assert result == reference_checksum(text, alphabet), text
            assert 0 <= result < len(alphabet)


# validate: accepted inputs

@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("0", DIGITS),
        ("00", DIGITS),
        ("18", DIGITS),
        ("59", DIGITS),
        ("79927398713", DIGITS),
        (CARD_16, DIGITS),
        ("f1", HEX),
        ("11", BINARY),
        ("bb", "ab"),
        ("xxx", "x"),
    ],
)
def test_validate_accepts_valid_numbers(number, alphabet):
    assert validate(number, alphabet) == number


def test_validate_returns_the_same_string_object():
    number = "79927398713"
    assert validate(number) is number


def test_validate_returns_the_same_integer_object():
    number = 79927398713
    assert validate(number) is number


def test_validate_accepts_alphabet_as_keyword():
    assert validate("f1", alphabet=HEX) == "f1"
    with pytest.raises(InvalidFormat):
        validate("f1")


# validate: format errors

@pytest.mark.parametrize("number", ["", 0, 0.0, None, False, [], (), {}])
def test_falsy_input_is_invalid_format(number):
    with pytest.raises(InvalidFormat):
        validate(number)


def test_empty_string_is_invalid_format_even_with_empty_alphabet():
    with pytest.raises(InvalidFormat):
        validate("", "")


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("abc", DIGITS),
        ("f1", DIGITS),
        ("12a", DIGITS),
        (" 1", DIGITS),
        ("1 2", DIGITS),
        ("-1", DIGITS),
        ("+1", DIGITS),
        ("1.5", DIGITS),
        ("2", BINARY),
        ("1", ""),
        ("1", "ab"),
    ],
)
def test_characters_outside_alphabet_are_invalid_format(number, alphabet):
    with pytest.raises(InvalidFormat):
        validate(number, alphabet)


@pytest.mark.parametrize("number", [True, 1.5, [1, 2], ("1",), object()])
def test_non_string_input_whose_text_is_not_in_alphabet_is_invalid_format(number):
    with pytest.raises(InvalidFormat):
        validate(number)


def test_error_while_converting_to_text_becomes_invalid_format():
    with pytest.raises(InvalidFormat) as excinfo:
        validate(Unprintable())
    assert isinstance(excinfo.value.__context__, RuntimeError)


def test_bad_character_error_is_chained_as_invalid_format():
    with pytest.raises(InvalidFormat) as excinfo:
        validate("abc")
    assert isinstance(excinfo.value.__context__, ValueError)


# validate: checksum errors

@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("1", DIGITS),
        ("9", DIGITS),
        ("10", DIGITS),
        ("01", DIGITS),
        ("79927398710", DIGITS),
        ("4111111111111112", DIGITS),
        ("1f", HEX),
        ("ff", HEX),
        ("10", BINARY),
        ("0", "10"),
    ],
)
def test_wrong_checksum_is_invalid_checksum(number, alphabet):
    with pytest.raises(InvalidChecksum):
        validate(number, alphabet)


def test_integers_with_wrong_checksum_are_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate(4)
    with pytest.raises(InvalidChecksum):
        validate(79927398710)


def test_invalid_checksum_is_not_an_invalid_format():
    with pytest.raises(InvalidChecksum) as excinfo:
        validate("1")
    assert not isinstance(excinfo.value, InvalidFormat)


# validate: exhaustive oracle and structural properties

@pytest.mark.parametrize(
    "alphabet, max_length",
    [(DIGITS, 3), (HEX, 2), (BINARY, 5), ("ab", 4)],
)
def test_validate_agrees_with_reference_for_every_short_string(alphabet, max_length):
    for length in range(1, max_length + 1):
        for chars in itertools.product(alphabet, repeat=length):
            text = "".join(chars)
            if reference_checksum(text, alphabet) == 0:
                assert validate(text, alphabet) == text
            else:
                with pytest.raises(InvalidChecksum):
                    validate(text, alphabet)


def test_exactly_one_check_digit_completes_the_known_prefix():
    assert [c for c in DIGITS if is_valid("7992739871" + c)] == ["3"]


@pytest.mark.parametrize("alphabet", [DIGITS, HEX, BINARY, "xyz"])
def test_exactly_one_final_character_completes_any_short_prefix(alphabet):
    prefixes = [
        "".join(chars)
        for length in (0, 1, 2)
        for chars in itertools.product(alphabet, repeat=length)
    ]
    for prefix in prefixes:
        completing = [c for c in alphabet if is_valid(prefix + c, alphabet)]
        assert len(completing) == 1, prefix
