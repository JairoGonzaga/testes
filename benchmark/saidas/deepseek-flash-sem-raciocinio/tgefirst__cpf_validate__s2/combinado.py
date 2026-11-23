"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal]
    assert validate('390.533.447-05') == '39053344705'


def test_c2_r1():
    # [R1/normal] número sem pontuação também é aceito
    assert validate('39053344705') == '39053344705'
