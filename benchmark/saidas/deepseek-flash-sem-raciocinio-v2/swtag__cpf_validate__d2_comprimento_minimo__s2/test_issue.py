import pytest

from alvo import InvalidChecksum, InvalidLength, ValidationError, validate


def test_twelve_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')


def test_thirteen_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('1114447773500')


def test_too_long_is_length_error_not_checksum():
    with pytest.raises(InvalidLength) as excinfo:
        validate('111444777350')
    assert not isinstance(excinfo.value, InvalidChecksum)
    assert isinstance(excinfo.value, ValidationError)


def test_valid_cpf_still_ok():
    assert validate('11144477735') == '11144477735'
    assert validate('111.444.777-35') == '11144477735'


def test_short_cpf_still_invalid_length():
    with pytest.raises(InvalidLength):
        validate('1114447773')
