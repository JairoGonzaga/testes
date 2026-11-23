"""Reproduces: valid CPF rejected with InvalidChecksum.

The second check digit must weight the first check digit by 2 (weights 11..2
over the 10 leading digits, the 10th being the first check digit), but
validate() adds the first check digit with weight 1.
"""
import pytest

from alvo import validate


def test_issue_example_11144477735_is_accepted():
    # Example from ISSUE.md: a valid CPF must be returned in compact form.
    assert validate('11144477735') == '11144477735'


def test_issue_example_formatted_111_444_777_35_is_accepted():
    assert validate('111.444.777-35') == '11144477735'


def test_known_valid_cpf_529_982_247_25_is_accepted():
    assert validate('529.982.247-25') == '52998224725'


@pytest.mark.parametrize(
    'cpf',
    [
        '54734217769',
        '88671483037',
        '11091905738',
        '98065589952',
        '98605873965',
        '96205189771',
    ],
)
def test_valid_cpf_with_nonzero_first_check_digit_is_accepted(cpf):
    assert validate(cpf) == cpf
