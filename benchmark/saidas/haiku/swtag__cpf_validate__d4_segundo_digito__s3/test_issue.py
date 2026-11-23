"""Reprodução do issue: CPF válido rejeitado com InvalidChecksum.

Regra oficial do CPF:
- 1º dígito verificador: soma dos 9 primeiros dígitos com pesos 10..2.
- 2º dígito verificador: soma dos 10 primeiros dígitos (incluindo o 1º dígito
  verificador) com pesos 11..2, ou seja, o 1º dígito verificador entra com
  peso 2.

O código atual soma o 1º dígito verificador com peso 1, por isso CPFs válidos
com 1º dígito verificador diferente de zero são rejeitados.
"""

import random

import pytest

from alvo import InvalidChecksum, validate


def _dv_oficial(base9):
    """Calcula os dois dígitos verificadores segundo a regra oficial."""
    soma1 = sum(int(d) * peso for d, peso in zip(base9, range(10, 1, -1)))
    dv1 = (soma1 * 10) % 11 % 10
    base10 = base9 + str(dv1)
    soma2 = sum(int(d) * peso for d, peso in zip(base10, range(11, 1, -1)))
    dv2 = (soma2 * 10) % 11 % 10
    return f"{dv1}{dv2}"


def test_reference_matches_known_valid_cpfs():
    """Garante que a referência usada nos testes está correta."""
    assert _dv_oficial("111444777") == "35"
    assert _dv_oficial("529982247") == "25"
    assert _dv_oficial("123456789") == "09"


def test_issue_example_is_accepted():
    """Exemplo do issue: 11144477735 é um CPF válido e deve ser aceito."""
    assert validate("11144477735") == "11144477735"


def test_formatted_issue_example_is_accepted():
    """111.444.777-35 é um CPF válido com máscara e deve retornar sem máscara."""
    assert validate("111.444.777-35") == "11144477735"


@pytest.mark.parametrize(
    "cpf, esperado",
    [
        ("52998224725", "52998224725"),
        ("529.982.247-25", "52998224725"),
        ("12345678909", "12345678909"),
        ("123.456.789-09", "12345678909"),
    ],
)
def test_known_valid_cpfs_are_accepted(cpf, esperado):
    assert validate(cpf) == esperado


@pytest.mark.parametrize("cpf", ["11144477736", "52998224726", "11144477745"])
def test_cpf_with_wrong_check_digits_is_still_rejected(cpf):
    with pytest.raises(InvalidChecksum):
        validate(cpf)


def test_generated_valid_cpfs_are_accepted():
    """CPFs gerados com a regra oficial devem ser aceitos pela validação."""
    rng = random.Random(20241122)
    testados = 0
    while testados < 300:
        base9 = "".join(str(rng.randrange(10)) for _ in range(9))
        if base9 == "0" * 9:
            continue
        cpf = base9 + _dv_oficial(base9)
        assert validate(cpf) == cpf, f"CPF válido {cpf} foi rejeitado"
        testados += 1
