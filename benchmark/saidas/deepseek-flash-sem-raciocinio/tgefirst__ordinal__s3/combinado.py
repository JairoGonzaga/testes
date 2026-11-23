"""Testes de ordinal."""

import math

import pytest

from alvo import ordinal


def test_c1_r1():
    # [R1/normal]
    assert ordinal(1) == '1st'


def test_ordinal_teens_and_special_cases():
    # [R1/normal] teens use 'th'
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
    assert ordinal(13) == '13th'
    # [R1/normal] 21, 22, 23
    assert ordinal(21) == '21st'
    assert ordinal(22) == '22nd'
    assert ordinal(23) == '23rd'
    # [R1/normal] 0 -> '0th'
    assert ordinal(0) == '0th'
    # [R1/normal] negative numbers
    assert ordinal(-1) == '-1st'
    assert ordinal(-2) == '-2nd'
    # [R2/not-finite] NaN and infinities
    assert ordinal(float('nan')) == 'NaN'
    assert ordinal(float('inf')) == '+Inf'
    assert ordinal(float('-inf')) == '-Inf'
    # [R3/invalid] strings that can't be converted return as-is
    assert ordinal('abc') == 'abc'
    # [R1/normal] string numbers are converted
    assert ordinal('3') == '3rd'
    # [R3/invalid] None returns 'None'
    assert ordinal(None) == 'None'
