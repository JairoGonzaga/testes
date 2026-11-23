import math

import pytest

from alvo import apnumber


def test_c22_r5():
    # [R5/invalida]
    assert apnumber(float('nan')) == 'NaN'
    assert apnumber('nan') == 'NaN'
