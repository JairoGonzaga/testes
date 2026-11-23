"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_c1_r1():
    # [R1/fronteira]
    with pytest.raises(InvalidFormat):
        validate('')


def test_validate_valid_and_invalid_checksum():
    assert validate("18") == "18"

    with pytest.raises(InvalidChecksum):
        validate("19")
