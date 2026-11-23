import pytest

from alvo import InvalidChecksum, validate


def test_issue_example_compact_cpf_is_accepted():
    # Issue: validate('11144477735') raises InvalidChecksum; expected to return it.
    assert validate('11144477735') == '11144477735'


def test_issue_example_formatted_cpf_is_accepted():
    # 111.444.777-35 is a valid CPF; the formatted form must normalize and pass.
    assert validate('111.444.777-35') == '11144477735'


@pytest.mark.parametrize('cpf', [
    '52998224725',  # 529.982.247-25 (second check digit is wrongly rejected today)
    '00000000191',  # 000.000.001-91
    '11144477735',  # 111.444.777-35
])
def test_valid_cpfs_are_accepted(cpf):
    assert validate(cpf) == cpf


def test_wrong_second_check_digit_is_still_rejected():
    # 111.444.777-36 has an incorrect second check digit and must stay invalid.
    with pytest.raises(InvalidChecksum):
        validate('11144477736')
