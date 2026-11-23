import pytest

from alvo import naturalsize


def test_issue_example():
    # 3000000 / 1024**2 = 2.861... -> '2.9 MiB'  (bug: gives '3.0 MiB')
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


@pytest.mark.parametrize(
    "value, expected",
    [
        (1024, "1.0 KiB"),
        (1536, "1.5 KiB"),
        (1024 ** 2, "1.0 MiB"),
        (100000000, "95.4 MiB"),          # 95.367... MiB
        (1024 ** 3, "1.0 GiB"),
        (1024 ** 3 * 2, "2.0 GiB"),
        (1024 ** 5 * 2, "2.0 PiB"),
        (2251799813685248, "2.0 PiB"),    # 2 * 1024**5 exactly (bug: 2.3 PiB)
    ],
)
def test_binary_uses_powers_of_1024(value, expected):
    assert naturalsize(value, binary=True) == expected


def test_binary_just_over_one_kib():
    assert naturalsize(1025, binary=True) == "1.0 KiB"


def test_decimal_and_gnu_unchanged():
    assert naturalsize(3000000) == "3.0 MB"
    assert naturalsize(3000000, gnu=True) == "2.9M"
