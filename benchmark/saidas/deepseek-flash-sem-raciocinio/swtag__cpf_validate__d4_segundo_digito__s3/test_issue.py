import pytest

from alvo import validate, InvalidChecksum


def test_known_valid_cpf_is_accepted():
    # 111.444.777-35 is a well-known valid CPF
    assert validate('11144477735') == '11144477735'


def test_known_valid_cpf_with_punctuation_is_accepted():
    assert validate('111.444.777-35') == '11144477735'


@pytest.mark.parametrize('number', ['52998224725', '529.982.247-25', '12345678909'])
def test_other_valid_cpfs_are_accepted(number):
    result = validate(number)
    assert result.isdigit()
    assert len(result) == 11


@pytest.mark.parametrize('number', ['11144477734', '11144477736', '52998224724'])
def test_wrong_check_digit_still_rejected(number):
    with pytest.raises(InvalidChecksum):
        validate(number)
