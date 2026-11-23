import pytest

from alvo import validate, checksum, InvalidChecksum, InvalidFormat


def test_validate_standard_luhn_example():
    assert validate("79927398713") == "79927398713"


def test_checksum_standard_luhn_example():
    assert checksum("79927398713") == 0


def test_validate_other_valid_luhn_numbers():
    for number in ["79927398713", "4242424242424242", "4111111111111111",
                   "5555555555554444", "378282246310005", "6011111111111117"]:
        assert validate(number) == number


def test_validate_checksum_agrees_with_doubling_rule():
    # Independent reference implementation of Luhn.
    def ref(number):
        digits = [int(c) for c in reversed(str(number))]
        total = 0
        for i, d in enumerate(digits):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        return total % 10

    for number in ["79927398713", "4242424242424242", "4111111111111111",
                   "5555555555554444", "378282246310005", "6011111111111117"]:
        assert checksum(number) == ref(number) == 0


def test_invalid_number_still_rejected():
    with pytest.raises(InvalidChecksum):
        validate("79927398710")


def test_empty_number_rejected():
    with pytest.raises(InvalidFormat):
        validate("")
