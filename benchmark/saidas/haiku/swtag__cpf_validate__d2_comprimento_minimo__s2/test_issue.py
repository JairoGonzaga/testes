import pytest

from alvo import InvalidLength, validate


def test_twelve_digits_raises_invalid_length():
    # Reproduction from the issue: 12 digits must be reported as a length error,
    # not as a checksum error.
    with pytest.raises(InvalidLength):
        validate("111444777350")


@pytest.mark.parametrize(
    "number",
    [
        "111444777350",    # 12 digits (issue example)
        "1114447773500",   # 13 digits
        "11144477735000",  # 14 digits
        "111.444.777-350",  # 12 digits once the formatting characters are removed
    ],
)
def test_too_many_digits_raises_invalid_length(number):
    with pytest.raises(InvalidLength):
        validate(number)
