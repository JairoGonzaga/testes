import pytest

from alvo import checksum, validate


@pytest.mark.parametrize(
    "number",
    [
        "79927398713",
        "4539148803436467",
    ],
)
def test_valid_luhn_number_is_accepted(number):
    assert validate(number) == number


def test_checksum_of_valid_luhn_number_is_zero():
    assert checksum("79927398713") == 0
