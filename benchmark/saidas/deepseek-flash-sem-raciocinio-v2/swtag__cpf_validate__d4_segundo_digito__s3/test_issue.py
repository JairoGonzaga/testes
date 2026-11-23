import pytest

from alvo import validate, InvalidChecksum


def test_known_valid_cpf_is_accepted():
    # CPF 111.444.777-35 has correct check digits 3 and 5
    assert validate('11144477735') == '11144477735'


def test_known_valid_cpf_with_formatting_is_accepted():
    assert validate('111.444.777-35') == '11144477735'


def test_invalid_check_digit_still_raises():
    # same CPF with a wrong last check digit must still be rejected
    with pytest.raises(InvalidChecksum):
        validate('11144477736')
