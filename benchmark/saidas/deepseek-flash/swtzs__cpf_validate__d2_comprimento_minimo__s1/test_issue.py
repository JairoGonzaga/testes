import pytest

from alvo import InvalidLength, validate


def test_cpf_with_twelve_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("111444777350")


@pytest.mark.parametrize(
    "number",
    [
        "111444777350",
        "1114447773500",
        "111.444.777-350",
        "111444777350000",
    ],
)
def test_cpf_with_more_than_eleven_digits_raises_invalid_length(number):
    with pytest.raises(InvalidLength):
        validate(number)
