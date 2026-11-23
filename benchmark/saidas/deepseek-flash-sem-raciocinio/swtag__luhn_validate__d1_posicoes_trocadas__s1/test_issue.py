import pytest

from alvo import InvalidChecksum, InvalidFormat, checksum, validate


def luhn(number):
    """Reference Luhn check (doubling every second digit from the right)."""
    total = 0
    for i, ch in enumerate(reversed(str(number))):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total


VALID_LUHN = [
    "79927398713",  # textbook Luhn example from the issue
    "0",
    "18",
    "4111111111111111",
    "1234567812345670",
]

INVALID_LUHN = [
    "79927398711",
    "79927398712",
    "79927398714",
    "1234567812345678",
    "4111111111111112",
]


# sanity check that the fixtures themselves agree with the textbook algorithm
@pytest.mark.parametrize("number", VALID_LUHN)
def test_fixtures_valid_reference(number):
    assert luhn(number) % 10 == 0


@pytest.mark.parametrize("number", INVALID_LUHN)
def test_fixtures_invalid_reference(number):
    assert luhn(number) % 10 != 0


def test_issue_example_validates():
    assert validate("79927398713") == "79927398713"


@pytest.mark.parametrize("number", VALID_LUHN)
def test_valid_luhn_checksum_is_zero(number):
    assert checksum(number) == 0


@pytest.mark.parametrize("number", VALID_LUHN)
def test_validate_accepts_valid_numbers(number):
    assert validate(number) == number


@pytest.mark.parametrize("number", INVALID_LUHN)
def test_validate_rejects_bad_checksum(number):
    assert checksum(number) != 0
    with pytest.raises(InvalidChecksum):
        validate(number)


@pytest.mark.parametrize("number", ["", None, 0])
def test_validate_rejects_empty(number):
    with pytest.raises(InvalidFormat):
        validate(number)
