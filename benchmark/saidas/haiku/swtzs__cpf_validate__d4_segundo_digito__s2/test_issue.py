import pytest

from alvo import InvalidChecksum, validate


def test_valid_cpf_111_444_777_35_is_accepted():
    assert validate('11144477735') == '11144477735'


def test_valid_formatted_cpf_is_accepted_and_compacted():
    assert validate('111.444.777-35') == '11144477735'


@pytest.mark.parametrize('cpf', ['52998224725', '529.982.247-25'])
def test_other_valid_cpf_is_accepted(cpf):
    assert validate(cpf) == '52998224725'


def test_invalid_second_check_digit_is_still_rejected():
    with pytest.raises(InvalidChecksum):
        validate('11144477736')
