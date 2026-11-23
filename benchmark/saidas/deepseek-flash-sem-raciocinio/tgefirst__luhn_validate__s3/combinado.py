"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_c1_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate('')


def test_c2_r1():
    # [R1/fronteira] strings não numéricas no alfabeto padrão são formato inválido
    import pytest
    from alvo import validate, InvalidFormat

    for value in ('1', '12a', '  1', '0-1', 'abc', -1, 1.5):
        with pytest.raises(InvalidFormat):
            validate(value)
