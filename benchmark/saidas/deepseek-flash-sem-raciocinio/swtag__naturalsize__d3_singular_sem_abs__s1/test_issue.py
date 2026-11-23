import pytest

from alvo import naturalsize


def test_negative_one_is_singular_byte():
    assert naturalsize(-1) == "-1 Byte"


def test_negative_one_not_plural():
    assert naturalsize(-1) != "-1 Bytes"


@pytest.mark.parametrize("value", [1, -1])
def test_singular_byte_both_signs(value):
    assert naturalsize(value) == f"{value} Byte"
