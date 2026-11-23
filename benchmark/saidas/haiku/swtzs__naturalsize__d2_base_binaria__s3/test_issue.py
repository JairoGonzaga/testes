import pytest

from alvo import naturalsize


@pytest.mark.parametrize(
    "value, expected",
    [
        (3000000, "2.9 MiB"),
        (5 * 1024**3, "5.0 GiB"),
        (1.5 * 1024**2, "1.5 MiB"),
        (1023, "1023 Bytes"),
    ],
)
def test_binary_uses_powers_of_1024(value, expected):
    assert naturalsize(value, binary=True) == expected
