import pytest
from alvo import apnumber

def test_bool_values():
    assert apnumber(True) == "one"
    assert apnumber(False) == "zero"
