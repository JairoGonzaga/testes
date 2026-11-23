import pytest
from alvo import apnumber

def test_apnumber_single_digit_nine():
    assert apnumber(9) == "nine"
