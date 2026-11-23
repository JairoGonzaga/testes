import pytest

from alvo import naturalsize


def test_negative_one_byte_uses_singular_form():
    # Issue: naturalsize(-1) returns '-1 Bytes' instead of '-1 Byte'.
    assert naturalsize(-1) == "-1 Byte"


@pytest.mark.parametrize("binary", [False, True])
def test_negative_one_byte_singular_for_both_unit_systems(binary):
    # Same bug on the shared "less than one base unit" branch for binary units.
    assert naturalsize(-1, binary=binary) == "-1 Byte"
