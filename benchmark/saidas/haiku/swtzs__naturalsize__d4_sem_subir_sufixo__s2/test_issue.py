import pytest

from alvo import naturalsize


@pytest.mark.parametrize(
    "value, kwargs, expected",
    [
        (999999, {}, "1.0 MB"),
        (999999999, {}, "1.0 GB"),
        (1048575, {"binary": True}, "1.0 MiB"),
    ],
)
def test_unit_is_promoted_when_rounding_reaches_next_unit(value, kwargs, expected):
    assert naturalsize(value, **kwargs) == expected
