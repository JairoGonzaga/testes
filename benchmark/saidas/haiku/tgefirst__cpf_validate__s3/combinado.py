"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal]
    assert validate('390.533.447-05') == '39053344705'


def test_c1_r2():
    # [R2/erro]
    with pytest.raises(InvalidChecksum) as excinfo:
        validate('390.533.447-06')
    assert isinstance(excinfo.value, ValidationError)
