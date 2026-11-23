import pytest

from alvo import InvalidLength, validate


def test_cpf_with_12_digits_raises_invalid_length():
    # Issue: validate('111444777350') raised InvalidChecksum instead of InvalidLength.
    with pytest.raises(InvalidLength):
        validate("111444777350")


@pytest.mark.parametrize(
    "number",
    [
        "111444777350",
        "1114447773500",
        "11144477735000",
        "111.444.777-3500",
    ],
)
def test_cpf_with_too_many_digits_raises_invalid_length(number):
    with pytest.raises(InvalidLength):
        validate(number)


def test_cpf_with_too_few_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("1114447773")


def test_valid_cpf_still_validates():
    assert validate("111.444.777-35") == "11144477735"
