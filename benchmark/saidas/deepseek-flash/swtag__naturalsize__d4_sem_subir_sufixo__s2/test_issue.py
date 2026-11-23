"""Reproduction tests for the issue: naturalsize() returns e.g. '1000.0 kB'.

When the formatted value rounds up to the size of the next unit (1000.0 /
1024.0), the unit must be promoted instead of showing "1000.0 kB".

See ISSUE.md:

    >>> naturalsize(999999)
    '1000.0 kB'   # expected: '1.0 MB'
"""

import pytest

from alvo import naturalsize


@pytest.mark.parametrize(
    "value, kwargs, expected",
    [
        # --- decimal (base 1000) ---
        (999999, {}, "1.0 MB"),
        (999999.0, {}, "1.0 MB"),
        (999999999, {}, "1.0 GB"),
        (999999999999, {}, "1.0 TB"),
        # --- binary (base 1024) ---
        (1048575, {"binary": True}, "1.0 MiB"),          # 1023.999... KiB
        (1073741823, {"binary": True}, "1.0 GiB"),       # 1023.999... MiB
        # --- gnu (base 1024, no space, short suffix) ---
        (1048575, {"gnu": True}, "1.0M"),                # 1023.999... K
        (1073741823, {"gnu": True}, "1.0G"),             # 1023.999... M
    ],
)
def test_rounding_up_promotes_to_next_unit(value, kwargs, expected):
    """Values that round up to the next unit get the next unit's suffix."""
    assert naturalsize(value, **kwargs) == expected


def test_issue_example():
    """The exact example from ISSUE.md."""
    assert naturalsize(999999) == "1.0 MB"


@pytest.mark.parametrize(
    "value, kwargs, expected",
    [
        # values that do NOT round up to the next unit must keep their unit
        (0, {}, "0 Bytes"),
        (1, {}, "1 Byte"),
        (-1, {}, "-1 Byte"),
        (999, {}, "999 Bytes"),
        (1000, {}, "1.0 kB"),
        (1500, {}, "1.5 kB"),
        (999949, {}, "999.9 kB"),
        (500000, {}, "500.0 kB"),
        (1000000, {}, "1.0 MB"),
        (1024, {"binary": True}, "1.0 KiB"),
        (1536, {"binary": True}, "1.5 KiB"),
        (1048576, {"binary": True}, "1.0 MiB"),
        (999, {"gnu": True}, "999B"),
        (1024, {"gnu": True}, "1.0K"),
        (1536, {"gnu": True}, "1.5K"),
    ],
)
def test_existing_behaviour_is_preserved(value, kwargs, expected):
    """Guards against an over-eager promotion of the unit."""
    assert naturalsize(value, **kwargs) == expected
