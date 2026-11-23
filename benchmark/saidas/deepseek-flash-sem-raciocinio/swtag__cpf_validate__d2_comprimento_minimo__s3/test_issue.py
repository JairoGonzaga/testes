import pytest

from alvo import validate, InvalidLength, InvalidChecksum, InvalidFormat


def test_too_many_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')


def test_twelve_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('1114447773500')


def test_long_number_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('11144477735' + '0' * 10)


def test_too_few_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('1114447773')


def test_valid_number_still_ok():
    assert validate('111.444.777-35') == '11144477735'


def test_wrong_check_digits_still_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate('11144477736')
