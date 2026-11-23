import string

import pytest

from alvo import InvalidChecksum, InvalidFormat, ValidationError, checksum, validate

DIGITS = "0123456789"
HEX = "0123456789abcdef"
UPPER = string.ascii_uppercase
BINARY = "01"
REVERSED_DIGITS = "9876543210"


# ---------------------------------------------------------------------------
# Independent reference implementations (oracles), written without alvo.py.
# ---------------------------------------------------------------------------


def _luhn_valid(s):
    """Standard decimal Luhn check."""
    total = 0
    for k, ch in enumerate(reversed(s)):
        d = int(ch)
        if k % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def _mod_n_valid(s, alphabet):
    """Generalised Luhn check modulo len(alphabet)."""
    n = len(alphabet)
    total = 0
    for k, ch in enumerate(reversed(s)):
        v = alphabet.index(ch)
        if k % 2 == 1:
            v *= 2
            total += v // n + v % n
        else:
            total += v
    return total % n == 0


def _check_char(payload, alphabet):
    """Return the single symbol that makes payload + symbol valid."""
    return next(c for c in alphabet if _mod_n_valid(payload + c, alphabet))


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------


def test_validation_error_derives_from_value_error():
    assert issubclass(ValidationError, ValueError)


@pytest.mark.parametrize("exc", [InvalidFormat, InvalidChecksum])
def test_specific_errors_derive_from_validation_error(exc):
    assert issubclass(exc, ValidationError)
    assert issubclass(exc, ValueError)


def test_specific_errors_are_not_subclasses_of_each_other():
    assert not issubclass(InvalidFormat, InvalidChecksum)
    assert not issubclass(InvalidChecksum, InvalidFormat)


# ---------------------------------------------------------------------------
# checksum: default decimal alphabet
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "number, expected",
    [
        ("0", 0),
        ("1", 1),
        ("5", 5),
        ("9", 9),
        ("10", 2),
        ("12", 4),
        ("21", 5),
        ("18", 0),
        ("50", 1),
        ("55", 6),
        ("59", 0),
        ("000012", 4),
        ("1234567890", 3),
        ("4111111111111111", 0),
        ("49927398716", 0),
        ("79927398713", 0),
        ("79927398710", 7),
    ],
)
def test_checksum_default_alphabet_known_values(number, expected):
    assert checksum(number) == expected


def test_checksum_default_alphabet_is_decimal_digits():
    assert checksum("12") == checksum("12", DIGITS) == checksum("12", alphabet=DIGITS)


def test_checksum_accepts_integers_via_their_string_form():
    assert checksum(12) == 4
    assert checksum(79927398713) == 0
    assert checksum(79927398710) == 7


def test_checksum_of_empty_string_is_zero():
    assert checksum("") == 0


def test_checksum_returns_int_within_alphabet_range():
    assert type(checksum("79927398713")) is int
    for n in range(0, 500):
        assert 0 <= checksum(str(n)) < 10


# ---------------------------------------------------------------------------
# checksum: custom alphabets
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "number, alphabet, expected",
    [
        ("0", HEX, 0),
        ("f", HEX, 15),
        ("8f", HEX, 0),
        ("1f", HEX, 1),
        ("ff", HEX, 14),
        ("A", UPPER, 0),
        ("B", UPPER, 1),
        ("NZ", UPPER, 0),
        ("NA", UPPER, 1),
        ("AZ", UPPER, 25),
        ("0", BINARY, 0),
        ("1", BINARY, 1),
        ("10", BINARY, 1),
        ("11", BINARY, 0),
    ],
)
def test_checksum_custom_alphabet_known_values(number, alphabet, expected):
    assert checksum(number, alphabet) == expected


def test_checksum_single_symbol_alphabet_is_always_zero():
    assert checksum("0", "0") == 0
    assert checksum("000", "0") == 0


def test_checksum_depends_on_alphabet_order():
    assert checksum("0", REVERSED_DIGITS) == 9
    assert checksum("9", REVERSED_DIGITS) == 0


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("12a", DIGITS),
        ("-1", DIGITS),
        ("A", DIGITS),
        ("8g", HEX),
        ("1", ""),
    ],
)
def test_checksum_symbol_outside_alphabet_raises_value_error(number, alphabet):
    with pytest.raises(ValueError):
        checksum(number, alphabet)


def test_checksum_empty_number_with_empty_alphabet_divides_by_zero():
    with pytest.raises(ZeroDivisionError):
        checksum("", "")


def test_checksum_non_sequence_alphabet_raises_type_error():
    with pytest.raises(TypeError):
        checksum("1", None)


# ---------------------------------------------------------------------------
# validate: accepted inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "number",
    [
        "0",
        "00",
        "18",
        "59",
        "12345678903",
        "49927398716",
        "79927398713",
        "4111111111111111",
    ],
)
def test_validate_returns_valid_string_unchanged(number):
    assert validate(number) is number


def test_validate_returns_valid_integer_unchanged():
    number = 79927398713
    assert validate(number) is number


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("8f", HEX),
        ("NZ", UPPER),
        ("11", BINARY),
        ("0", "0"),
        ("000", "0"),
        ("9", REVERSED_DIGITS),
    ],
)
def test_validate_custom_alphabet_returns_valid_number(number, alphabet):
    assert validate(number, alphabet=alphabet) is number


# ---------------------------------------------------------------------------
# validate: format errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("number", [0, 0.0, False, "", None, [], (), {}])
def test_falsy_input_is_invalid_format_even_when_checksum_would_pass(number):
    with pytest.raises(InvalidFormat) as excinfo:
        validate(number)
    assert type(excinfo.value) is InvalidFormat


def test_empty_number_with_empty_alphabet_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("", "")


@pytest.mark.parametrize(
    "number",
    [
        "12a",
        "1 2",
        "+1",
        "-1",
        "1.5",
        "a",
        "[1]",
        -79927398713,
        1.5,
        True,
        (1,),
    ],
)
def test_symbols_outside_alphabet_are_invalid_format(number):
    with pytest.raises(InvalidFormat) as excinfo:
        validate(number)
    assert type(excinfo.value) is InvalidFormat


def test_bad_symbol_is_chained_from_original_value_error():
    with pytest.raises(InvalidFormat) as excinfo:
        validate("12a")
    assert isinstance(excinfo.value.__context__, ValueError)


def test_unprintable_object_is_invalid_format_chained_from_runtime_error():
    class Unprintable:
        def __bool__(self):
            return True

        def __str__(self):
            raise RuntimeError("no string form")

    with pytest.raises(InvalidFormat) as excinfo:
        validate(Unprintable())
    assert isinstance(excinfo.value.__context__, RuntimeError)


def test_non_sequence_alphabet_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("1", None)


def test_empty_alphabet_makes_nonempty_number_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("12", "")


def test_digit_missing_from_custom_alphabet_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("1", "0")


# ---------------------------------------------------------------------------
# validate: checksum errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "number, alphabet",
    [
        ("1", DIGITS),
        ("5", DIGITS),
        ("12", DIGITS),
        ("1234567890", DIGITS),
        ("79927398710", DIGITS),
        ("1f", HEX),
        ("12", HEX),
        ("NA", UPPER),
        ("10", BINARY),
    ],
)
def test_wrong_checksum_raises_invalid_checksum(number, alphabet):
    with pytest.raises(InvalidChecksum) as excinfo:
        validate(number, alphabet)
    assert type(excinfo.value) is InvalidChecksum
    assert excinfo.value.__context__ is None


def test_invalid_checksum_is_a_validation_error():
    with pytest.raises(ValidationError):
        validate("1")


def test_invalid_format_is_a_validation_error():
    with pytest.raises(ValidationError):
        validate("x")


# ---------------------------------------------------------------------------
# Round-trip properties built from independent oracles
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "payload",
    ["0", "1", "7", "12", "123", "9999", "4111111111111", "7992739871", "1234567890"],
)
def test_decimal_payload_with_computed_check_digit_is_valid(payload):
    full = payload + _check_char(payload, DIGITS)
    assert _luhn_valid(full)
    assert checksum(full) == 0
    assert validate(full) is full


def test_sweep_of_generated_decimal_numbers_round_trip():
    for i in range(0, 3000, 7):
        payload = str(i)
        full = payload + _check_char(payload, DIGITS)
        assert validate(full) == full
        assert checksum(full) == 0


@pytest.mark.parametrize("payload", ["7992739871", "5", "123456789", "0"])
def test_every_wrong_decimal_check_digit_is_rejected(payload):
    good = _check_char(payload, DIGITS)
    for d in DIGITS:
        candidate = payload + d
        if d == good:
            assert validate(candidate) is candidate
        else:
            with pytest.raises(InvalidChecksum):
                validate(candidate)


@pytest.mark.parametrize(
    "alphabet, payload",
    [
        (HEX, "8"),
        (HEX, "1a2b3c"),
        (HEX, "deadbeef"),
        (UPPER, "Q"),
        (UPPER, "HELLO"),
        (BINARY, "1011"),
        (REVERSED_DIGITS, "123"),
    ],
)
def test_custom_alphabet_round_trip_and_wrong_symbol_rejected(alphabet, payload):
    full = payload + _check_char(payload, alphabet)
    assert _mod_n_valid(full, alphabet)
    assert checksum(full, alphabet) == 0
    assert validate(full, alphabet) is full

    wrong = alphabet[(alphabet.index(full[-1]) + 1) % len(alphabet)]
    with pytest.raises(InvalidChecksum):
        validate(payload + wrong, alphabet)
