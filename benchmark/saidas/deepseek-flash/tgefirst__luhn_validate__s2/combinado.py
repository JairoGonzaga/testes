"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_c1_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate('')


def test_validate_invalid_character_raises_invalid_format():
    # [R2/formato]
    with pytest.raises(InvalidFormat):
        validate("7992739871x")
