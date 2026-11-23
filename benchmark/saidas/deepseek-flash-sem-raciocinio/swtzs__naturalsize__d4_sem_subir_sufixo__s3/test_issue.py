import pytest
from alvo import naturalsize


def test_boundary_decimal_rounds_up_to_next_unit():
    assert naturalsize(999999) == "1.0 MB"


def test_boundary_binary_rounds_up_to_next_unit():
    assert naturalsize(1024 * 1024 - 1, binary=True) == "1.0 MiB"


def test_boundary_gnu_rounds_up_to_next_unit():
    assert naturalsize(1024 * 1024 - 1, gnu=True) == "1.0M"


def test_boundary_decimal_kilobytes_rounds_up():
    assert naturalsize(999949) == "1000.0 kB" or naturalsize(999950) == "1.0 MB"


def test_regular_value_still_works():
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(1500) == "1.5 kB"
