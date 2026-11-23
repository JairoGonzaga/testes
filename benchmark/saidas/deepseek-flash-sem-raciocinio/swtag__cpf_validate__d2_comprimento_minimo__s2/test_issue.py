import pytest

from alvo import InvalidChecksum, InvalidLength, validate


@pytest.mark.parametrize(
    "number",
    [
        "111444777350",  # 12 digits
        "1114447773500",  # 13 digits
        "111.444.777-350",  # 12 digits with punctuation
        "11144477735",  # 11 digits -> valid, sanity check
    ],
)
def test_too_many_digits_raises_invalid_length(number):
    if number == "11144477735":
        assert validate(number) == number
        return
    with pytest.raises(InvalidLength):
        validate(number)


def test_exactly_eleven_digits_wrong_checksum_raises_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate("11144477734")


def test_too_few_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("1114447773")
