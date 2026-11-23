import pytest
from alvo import naturalsize


def test_naturalsize_rounds_up_to_next_unit_decimal():
    assert naturalsize(999999) == "1.0 MB"


def test_naturalsize_rounds_up_to_next_unit_binary():
    assert naturalsize(1048575, binary=True) == "1.0 MiB"


def test_naturalsize_rounds_up_to_next_unit_gnu():
    assert naturalsize(1048575, gnu=True) == "1.0M"
