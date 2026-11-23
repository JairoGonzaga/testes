"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal]
    assert validate('390.533.447-05') == '39053344705'


def test_invalid_cases():
    # Invalid checksum (correct format and length but wrong check digits)
    with pytest.raises(InvalidChecksum):
        validate('390.533.447-04')
    # Invalid length (too short)
    with pytest.raises(InvalidLength):
        validate('1234567890')
    # Invalid format (non‑digit character after cleaning)
    with pytest.raises(InvalidFormat):
        validate('12A-34-5678-90')
    # Invalid format (numeric value is zero)
    with pytest.raises(InvalidFormat):
        validate('000.000.000-00')
