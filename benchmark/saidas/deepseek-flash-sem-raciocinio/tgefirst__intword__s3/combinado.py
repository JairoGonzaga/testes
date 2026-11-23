"""Testes de intword."""

import math

import pytest

from alvo import intword


def test_c1_r1():
    # [R1/normal]
    assert intword(0) == '0'


def test_round_up_promotes_unit():
    # when rounding reaches the next power of a thousand, promote to the larger unit
    assert intword(999_950) == "1.0 million"
    assert intword(1_999_950_000) == "2.0 billion"
