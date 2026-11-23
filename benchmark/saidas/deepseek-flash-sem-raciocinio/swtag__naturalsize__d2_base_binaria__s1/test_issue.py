import pytest

from alvo import naturalsize


def test_binary_uses_powers_of_1024():
    # 3000000 / 1024**2 == 2.86... -> '2.9 MiB' (not '3.0 MiB' from 1000-based)
    assert naturalsize(3000000, binary=True) == '2.9 MiB'


def test_binary_mib_exact():
    assert naturalsize(1024 ** 2, binary=True) == '1.0 MiB'


def test_binary_gib():
    assert naturalsize(1024 ** 3, binary=True) == '1.0 GiB'


def test_binary_boundary_1024():
    assert naturalsize(1024, binary=True) == '1.0 KiB'


def test_binary_rollover_to_next_unit():
    # 1023.96 KiB would round to 1024.0 KiB, must roll over to 1.0 MiB
    assert naturalsize(1024 * 1023.96, binary=True) == '1.0 MiB'


def test_decimal_still_correct():
    assert naturalsize(3000000) == '3.0 MB'
    assert naturalsize(1000) == '1.0 kB'
    assert naturalsize(999) == '999 Bytes'
    assert naturalsize(1) == '1 Byte'


@pytest.mark.parametrize(
    "value,expected",
    [
        (2 * 1024, '2.0 KiB'),
        (1024 ** 4, '1.0 TiB'),
        (1536, '1.5 KiB'),
        (-3000000, '-2.9 MiB'),
    ],
)
def test_binary_values(value, expected):
    assert naturalsize(value, binary=True) == expected
