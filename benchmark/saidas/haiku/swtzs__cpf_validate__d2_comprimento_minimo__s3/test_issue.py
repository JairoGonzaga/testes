import pytest

from alvo import InvalidLength, validate


@pytest.mark.parametrize(
    "number",
    [
        "111444777350",     # 12 digits, from the issue
        "1114447773500",    # 13 digits
        "11144477735000",   # 14 digits
        "111.444.777-350",  # 12 digits once formatting characters are removed
    ],
)
def test_cpf_with_too_many_digits_raises_invalid_length(number):
    with pytest.raises(InvalidLength):
        validate(number)


@pytest.mark.parametrize("number", ["1114447773", "111444777", "1"])
def test_cpf_with_too_few_digits_raises_invalid_length(number):
    with pytest.raises(InvalidLength):
        validate(number)
