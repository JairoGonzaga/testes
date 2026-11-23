import pytest

from alvo import validate, checksum, InvalidChecksum, InvalidFormat


def test_standard_luhn_example_is_valid():
    assert validate("79927398713") == "79927398713"


def test_checksum_of_standard_luhn_example_is_zero():
    assert checksum("79927398713") == 0


@pytest.mark.parametrize(
    "number",
    [
        "79927398713",
        "49927398716",
        "1234567812345670",
        "0",
        "18",
        "26",
    ],
)
def test_valid_numbers_pass(number):
    assert validate(number) == number


@pytest.mark.parametrize(
    "number",
    [
        "79927398710",
        "79927398711",
        "49927398717",
        "1234567812345678",
    ],
)
def test_invalid_numbers_raise_checksum_error(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_invalid_characters_raise_format_error():
    with pytest.raises(InvalidFormat):
        validate("7992739871a")
