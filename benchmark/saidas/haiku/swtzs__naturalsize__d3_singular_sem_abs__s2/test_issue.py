import pytest

from alvo import naturalsize


def test_negative_one_byte_uses_singular_form():
    assert naturalsize(-1) == "-1 Byte"


def test_positive_one_byte_uses_singular_form():
    assert naturalsize(1) == "1 Byte"


def test_negative_one_byte_binary_uses_singular_form():
    assert naturalsize(-1, binary=True) == "-1 Byte"


@pytest.mark.parametrize(
    "value, expected",
    [
        (-2, "-2 Bytes"),
        (0, "0 Bytes"),
        (2, "2 Bytes"),
    ],
)
def test_plural_bytes_kept_for_other_small_values(value, expected):
    assert naturalsize(value) == expected
