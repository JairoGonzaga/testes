import pytest

from alvo import InvalidLength, validate


@pytest.mark.parametrize(
    "number",
    [
        "111444777350",  # 12 digits, example from the issue
        "1114447773500",  # 13 digits
        "11144477735000",  # 14 digits
        "111444777350111444777350",  # 24 digits
        "111.444.777-350",  # 12 digits once the punctuation is removed
    ],
)
def test_cpf_with_too_many_digits_raises_invalid_length(number):
    with pytest.raises(InvalidLength):
        validate(number)
