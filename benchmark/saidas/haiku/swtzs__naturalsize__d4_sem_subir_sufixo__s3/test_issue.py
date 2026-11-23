import pytest

from alvo import naturalsize


def test_issue_example_promotes_unit_when_rounding_reaches_next_unit():
    assert naturalsize(999999) == "1.0 MB"


@pytest.mark.parametrize(
    "value, kwargs, expected",
    [
        (999999, {}, "1.0 MB"),
        (999999999, {}, "1.0 GB"),
        (1048575, {"binary": True}, "1.0 MiB"),
        (1048575, {"gnu": True}, "1.0M"),
    ],
)
def test_unit_is_promoted_when_rounded_value_reaches_next_unit(value, kwargs, expected):
    assert naturalsize(value, **kwargs) == expected


def test_value_below_rounding_threshold_keeps_current_unit():
    assert naturalsize(999499) == "999.5 kB"
