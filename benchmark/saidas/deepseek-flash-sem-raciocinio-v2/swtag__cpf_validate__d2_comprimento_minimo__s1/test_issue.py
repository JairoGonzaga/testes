import pytest

from alvo import validate, compact, InvalidLength, InvalidChecksum, InvalidFormat


def test_twelve_digits_raises_invalid_length():
    number = "111444777350"
    assert len(compact(number)) == 12
    with pytest.raises(InvalidLength):
        validate(number)


def test_thirteen_digits_raises_invalid_length():
    number = "1114447773511"
    assert len(compact(number)) == 13
    with pytest.raises(InvalidLength):
        validate(number)


def test_ten_digits_still_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("1114447773")


def test_valid_cpf_still_accepted():
    assert validate("111.444.777-35") == "11144477735"


def test_non_digits_still_raise_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("1114447773a")


def test_invalid_checksum_still_raised_for_11_digits():
    with pytest.raises(InvalidChecksum):
        validate("11144477736")
