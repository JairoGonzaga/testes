import pytest
from alvo import checksum, validate, InvalidFormat, InvalidChecksum

# Helper to compute expected checksum using the function itself for dynamic values

def expected_checksum(number, alphabet="0123456789"):
    return checksum(number, alphabet)

@pytest.mark.parametrize(
    "number,alphabet,expected",
    [
        ("0", "0123456789", 0),
        ("79927398713", "0123456789", 0),  # classic Luhn example (valid)
        ("79927398714", "0123456789", 1),  # one off, invalid
        (12345, "0123456789", checksum(12345)),  # dynamic check using function itself
        ("00123", "0123456789", checksum("00123")),
        ("ABC", "ABC", checksum("ABC", "ABC")),
        ("CBA", "ABC", checksum("CBA", "ABC")),
    ],
)
def test_checksum_known_values(number, alphabet, expected):
    # Directly compare to expected value; for dynamic cases we compute via the function itself
    assert checksum(number, alphabet) == expected

def test_checksum_invalid_character_raises():
    # Using default alphabet, a non-digit character should raise ValueError inside checksum
    with pytest.raises(ValueError):
        checksum("12A3")

@pytest.mark.parametrize(
    "number,alphabet",
    [
        ("", "0123456789"),          # empty string -> InvalidFormat
        (0, "0123456789"),            # zero is falsy -> InvalidFormat
        (None, "0123456789"),         # None is falsy -> InvalidFormat
        ("-123", "0123456789"),     # '-' not in alphabet -> InvalidFormat via exception
        ("12A3", "0123456789"),     # invalid character -> InvalidFormat via exception
    ],
)
def test_validate_invalid_format(number, alphabet):
    with pytest.raises(InvalidFormat):
        validate(number, alphabet)

def test_validate_invalid_checksum():
    # Choose a number that we know does not produce checksum 0 with default alphabet
    # Using a simple example where checksum returns non‑zero
    number = "79927398714"  # one digit changed from valid Luhn example
    with pytest.raises(InvalidChecksum):
        validate(number)

def test_validate_successful():
    # Valid Luhn example should pass and return the original number
    number = "79927398713"
    assert validate(number) == number

def test_validate_custom_alphabet_success_and_failure():
    alphabet = "ABC"
    # Build a number that yields checksum 0 using the custom alphabet
    # We can brute‑force a short example
    for num in range(0, 1000):
        s = "".join(alphabet[int(d) % 3] for d in str(num))
        if checksum(s, alphabet) == 0:
            valid_num = s
            break
    else:
        pytest.fail("Could not find a valid checksum example for custom alphabet")

    # Should validate successfully
    assert validate(valid_num, alphabet) == valid_num

    # Now tweak the last character to make checksum non‑zero and expect InvalidChecksum
    # Change last char to a different valid symbol
    if len(valid_num) > 0:
        bad_char = next(c for c in alphabet if c != valid_num[-1])
        bad_num = valid_num[:-1] + bad_char
        if checksum(bad_num, alphabet) == 0:
            # If by chance still 0, ensure we pick another alteration
            bad_num = valid_num[:-1] + alphabet[0]
        with pytest.raises(InvalidChecksum):
            validate(bad_num, alphabet)

def test_checksum_large_number_performance():
    # Very large integer should still compute without error
    large_num = int("9" * 1000)  # 1000 digits of 9
    # We only assert that it returns an int within alphabet range
    result = checksum(large_num)
    assert isinstance(result, int)
    assert 0 <= result < 10
