"""Testes de apnumber."""

import math

import pytest

from alvo import apnumber


def test_c1_r1():
    # [R1/fronteira]
    assert apnumber(0) == 'zero'


def test_c1_r2():
    # [R1/intervalo]
    expected = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    ]
    for value, word in enumerate(expected):
        assert apnumber(value) == word
