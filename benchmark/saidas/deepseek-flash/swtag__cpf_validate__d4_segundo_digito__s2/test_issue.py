"""Reprodução do issue: CPFs válidos rejeitados com InvalidChecksum.

O segundo dígito verificador deve considerar o primeiro dígito verificador
com peso 11 (isto é, ``2 * d1``) no somatório:

    d1 = sum((10 - i) * digito[i] for i in 0..8);  d1 = (11 - d1) % 11 % 10
    d2 = sum((11 - i) * digito[i] for i in 0..8) + 2 * d1
    d2 = (11 - d2) % 11 % 10

A implementação atual soma apenas ``d1`` (sem o fator 2), o que faz com que
CPFs válidos como ``111.444.777-35`` sejam rejeitados e números inválidos
sejam aceitos.
"""

import random

import pytest

from alvo import validate, InvalidChecksum


WEIGHTS_DV1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
WEIGHTS_DV2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]


def _reference_check_digits(base9):
    """Cálculo de referência (correto) dos dois dígitos verificadores do CPF."""
    assert len(base9) == 9 and base9.isdigit()

    d1 = sum(int(ch) * w for ch, w in zip(base9, WEIGHTS_DV1))
    d1 = (11 - d1) % 11
    if d1 >= 10:
        d1 = 0

    d2 = sum(int(ch) * w for ch, w in zip(base9 + str(d1), WEIGHTS_DV2))
    d2 = (11 - d2) % 11
    if d2 >= 10:
        d2 = 0

    return "%d%d" % (d1, d2)


def _make_cpf(base9):
    return base9 + _reference_check_digits(base9)


def _format(cpf):
    return "%s.%s.%s-%s" % (cpf[:3], cpf[3:6], cpf[6:9], cpf[9:])


# Bases cujo primeiro dígito verificador é diferente de zero: são exatamente
# os casos que a implementação atual (com o bug) rejeita.
BASE9_CASES = [
    "111444777",  # 111.444.777-35  (CPF clássico citado no issue)
    "529982247",  # 529.982.247-25
    "000000001",  # 000.000.001-91
    "100000000",  # 100.000.000-19
    "210820178",  # 210.820.178-50
    "909225256",  # 909.225.256-50
    "942765876",  # 942.765.876-20
    "773546111",  # 773.546.111-90
    "482370865",  # 482.370.865-20
    "000000009",  # 000.000.009-49
]

VALID_CPFS = [_make_cpf(b) for b in BASE9_CASES]

# Números que a fórmula com bug (usando ``+ d1`` no lugar de ``+ 2 * d1``)
# aceitaria como válidos, embora o dígito verificador esteja errado.
BUGGY_ACCEPTED_INVALID = [
    "11140007791",  # correto seria 11140007793
    "11140017750",  # correto seria 11140017756
    "11140027710",  # correto seria 11140027719
]


def test_reference_helper_sanity():
    """Sanidade da implementação de referência usada nos testes."""
    assert _reference_check_digits("111444777") == "35"
    assert _reference_check_digits("529982247") == "25"
    assert _make_cpf("111444777") == "11144477735"
    for cpf in VALID_CPFS:
        assert cpf == _make_cpf(cpf[:9])


def test_issue_example_11144477735_is_accepted():
    """O exemplo exato do issue: '111.444.777-35' é um CPF válido."""
    assert validate("11144477735") == "11144477735"


def test_issue_example_formatted_is_accepted():
    assert validate("111.444.777-35") == "11144477735"


@pytest.mark.parametrize("cpf", VALID_CPFS)
def test_valid_cpf_is_accepted(cpf):
    assert validate(cpf) == cpf


@pytest.mark.parametrize("cpf", VALID_CPFS)
def test_valid_formatted_cpf_is_accepted(cpf):
    assert validate(_format(cpf)) == cpf


@pytest.mark.parametrize("cpf", BUGGY_ACCEPTED_INVALID)
def test_invalid_check_digits_still_rejected(cpf):
    """CPF com dígito verificador errado continua sendo rejeitado."""
    assert cpf[-2:] != _reference_check_digits(cpf[:9])
    with pytest.raises(InvalidChecksum):
        validate(cpf)


def test_random_valid_cpfs_are_accepted():
    rng = random.Random(20240607)
    bases = set()
    while len(bases) < 200:
        base = "".join(rng.choice("0123456789") for _ in range(9))
        if int(base) == 0:
            continue
        if _reference_check_digits(base)[0] == "0":
            # foca nos casos afetados pelo bug (d1 != 0)
            continue
        bases.add(base)

    for base in sorted(bases):
        cpf = _make_cpf(base)
        assert validate(cpf) == cpf, "CPF válido rejeitado: %s" % _format(cpf)
        assert validate(_format(cpf)) == cpf


def test_random_invalid_check_digits_are_rejected():
    rng = random.Random(424242)
    checked = 0
    while checked < 200:
        base = "".join(rng.choice("0123456789") for _ in range(9))
        if int(base) == 0:
            continue
        correct = _reference_check_digits(base)
        wrong = "%d%d" % ((int(correct[0]) + 1) % 10, int(correct[1]))
        if wrong == correct:
            continue
        cpf = base + wrong
        checked += 1
        with pytest.raises(InvalidChecksum):
            validate(cpf)
