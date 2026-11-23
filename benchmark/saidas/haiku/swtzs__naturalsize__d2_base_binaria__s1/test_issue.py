import pytest

from alvo import naturalsize


def test_issue_example_binary_uses_powers_of_1024():
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


@pytest.mark.parametrize(
    "value, expected",
    [
        (2 * 1024**2, "2.0 MiB"),
        (1024**3, "1.0 GiB"),
        (1023, "1023 Bytes"),
    ],
)
def test_binary_uses_powers_of_1024(value, expected):
    assert naturalsize(value, binary=True) == expected
