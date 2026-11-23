import pytest

from alvo import naturalsize


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (3000000, "2.9 MiB"),
        (2 * 1024**2, "2.0 MiB"),
        (1024**3, "1.0 GiB"),
        (1536 * 1024, "1.5 MiB"),
        (1000, "1000 Bytes"),
    ],
)
def test_naturalsize_binary_uses_powers_of_1024(value, expected):
    assert naturalsize(value, binary=True) == expected
