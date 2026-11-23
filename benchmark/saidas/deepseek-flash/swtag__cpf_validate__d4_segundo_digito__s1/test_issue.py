"""Reproducao do issue: CPFs validos rejeitados com InvalidChecksum.

O digito verificador calculado pelo modulo esta errado: ao calcular o segundo
digito, o primeiro digito verificador nao entra com o peso correto (deveria
pesar 2, mas o modulo o soma com peso 1).  Assim, qualquer CPF cujo primeiro
digito verificador seja diferente de zero e rejeitado indevidamente.
"""

import random

import pytest

from alvo import InvalidChecksum, validate


def reference_check_digits(base9):
    """Implementacao de referencia (algoritmo oficial) dos digitos do CPF."""
    digits = [int(c) for c in base9]
    total = sum((10 - i) * digits[i] for i in range(9))
    r = total % 11
    d1 = 0 if r < 2 else 11 - r
    total = sum((11 - i) * digits[i] for i in range(9)) + 2 * d1
    r = total % 11
    d2 = 0 if r < 2 else 11 - r
    return "%d%d" % (d1, d2)


KNOWN_VALID = [
    "11144477735",
    "52998224725",
    "111.444.777-35",
    "529.982.247-25",
    "39053344705",
    "12345678909",
]


@pytest.mark.parametrize("number", KNOWN_VALID)
def test_known_valid_cpfs_are_accepted(number):
    expected = "".join(c for c in number if c.isdigit())
    assert validate(number) == expected
    assert reference_check_digits(expected[:9]) == expected[-2:]


def test_issue_example_11144477735():
    assert validate("11144477735") == "11144477735"


def test_valid_cpfs_with_nonzero_first_check_digit():
    """CPFs gerados pelo algoritmo oficial cujo d1 != 0 devem ser aceitos."""
    bases = []
    for n in range(100000000, 100000900):
        base = "%09d" % n
        if reference_check_digits(base)[0] != "0":
            bases.append(base)
        if len(bases) >= 50:
            break
    assert len(bases) == 50
    for base in bases:
        number = base + reference_check_digits(base)
        assert validate(number) == number


def test_valid_cpfs_generated_randomly():
    rng = random.Random(20240101)
    checked = 0
    while checked < 200:
        base = "%09d" % rng.randrange(1, 10**9)
        dv = reference_check_digits(base)
        if dv[0] == "0":
            continue  # nao exercita o bug; ja funcionava
        number = base + dv
        assert validate(number) == number
        checked += 1
    assert checked == 200


def test_invalid_check_digits_still_rejected():
    base = "111444777"
    good = base + reference_check_digits(base)
    assert validate(good) == good
    for digit in "0123456789":
        bad = base + digit + good[-1]
        if bad[-2:] == good[-2:]:
            continue
        with pytest.raises(InvalidChecksum):
            validate(bad)
