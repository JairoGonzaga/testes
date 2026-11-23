import pytest

from alvo import validate, InvalidLength


def test_too_many_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')


def test_many_extra_digits_raise_invalid_length():
    with pytest.raises(InvalidLength):
        validate('1114447773500')


def test_formatted_too_long_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111.444.777-350')


def test_too_few_digits_still_invalid_length():
    with pytest.raises(InvalidLength):
        validate('1114447773')


def test_valid_cpf_still_passes():
    assert validate('111.444.777-35') == '11144477735'
