import pytest

from alvo import InvalidChecksum, InvalidFormat, InvalidLength, validate


VALID_CPFS = [
    "11144477735",
    "111.444.777-35",
    "52998224725",
    "529.982.247-25",
    "01234567890",
    "12345678909",
]


@pytest.mark.parametrize("number", VALID_CPFS)
def test_valid_cpf_accepted(number):
    assert validate(number) == "".join(c for c in number if c.isdigit())


def test_well_known_valid_cpf():
    # 111.444.777-35 is a classic valid CPF mentioned in the issue
    assert validate("11144477735") == "11144477735"


INVALID_CHECKSUM_CPFS = [
    "11144477736",
    "11144477734",
    "52998224726",
    "52998224724",
    "12345678900",
]


@pytest.mark.parametrize("number", INVALID_CHECKSUM_CPFS)
def test_invalid_checksum_rejected(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_invalid_length():
    with pytest.raises(InvalidLength):
        validate("1114447773")


def test_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("1114447773a")


def test_invalid_all_zeros():
    with pytest.raises(InvalidFormat):
        validate("00000000000")
