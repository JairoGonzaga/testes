import pytest

from alvo import validate


def test_issue_example_is_accepted():
    # Exemplo da issue: 79927398713 é um número Luhn válido.
    assert validate('79927398713') == '79927398713'


@pytest.mark.parametrize('number', ['59', '91'])
def test_valid_number_with_doubled_digit_5_or_more_is_accepted(number):
    # Dígito >= 5 em posição dobrada: o dobro deve ser reduzido pela soma dos dígitos
    # (5 -> 10 -> 1, 9 -> 18 -> 9), e não pelo módulo 10 (5 -> 0, 9 -> 8).
    assert validate(number) == number
