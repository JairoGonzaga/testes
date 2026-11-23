import pytest

from alvo import InvalidLength, validate


def test_cpf_with_12_digits_raises_invalid_length():
    # Issue example: 12 digits must raise InvalidLength, not InvalidChecksum.
    with pytest.raises(InvalidLength):
        validate("111444777350")


@pytest.mark.parametrize(
    "cpf",
    [
        "111444777350",      # 12 digits (issue example)
        "1114447773500",     # 13 digits
        "11144477735000",    # 14 digits
        "111.444.777-350",   # 12 digits after compaction
        "111.444.777-3500",  # 13 digits after compaction
    ],
)
def test_cpf_with_too_many_digits_raises_invalid_length(cpf):
    with pytest.raises(InvalidLength):
        validate(cpf)


@pytest.mark.parametrize("cpf", ["1114447773", "111.444.777-3"])
def test_cpf_with_too_few_digits_raises_invalid_length(cpf):
    with pytest.raises(InvalidLength):
        validate(cpf)


@pytest.mark.parametrize("cpf", ["11144477735", "111.444.777-35"])
def test_valid_cpf_with_11_digits_is_accepted(cpf):
    assert validate(cpf) == "11144477735"
