import pytest

from alvo import naturalsize


def test_exactly_one_kilobyte_is_converted_to_next_unit():
    # 1000 bytes is exactly one kilobyte, so it must not stay in bytes.
    assert naturalsize(1000) == "1.0 kB"


def test_exactly_one_kibibyte_is_converted_to_next_unit_in_binary_mode():
    # Same boundary bug in binary mode: 1024 bytes is exactly one KiB.
    assert naturalsize(1024, binary=True) == "1.0 KiB"


@pytest.mark.parametrize(
    "value, expected",
    [
        (999, "999 Bytes"),
        (1000, "1.0 kB"),
        (1500, "1.5 kB"),
        (1000000, "1.0 MB"),
    ],
)
def test_decimal_unit_boundaries(value, expected):
    assert naturalsize(value) == expected
