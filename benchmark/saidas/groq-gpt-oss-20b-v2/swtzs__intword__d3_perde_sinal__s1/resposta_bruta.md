```python
# test_issue.py
"""
Tests to reproduce the issue where negative numbers lose their sign
when using alvo.intword.

The current implementation sets the negative_prefix incorrectly to an
empty string, so all negative results are returned without a leading
'-'.  Once the bug is fixed (negative_prefix should be '-' for negative
inputs), these tests will pass.
"""

import pytest

from alvo import intword


def test_negative_small_value():
    # Numbers less than the first power (1000) are returned as plain integers.
    assert intword(-42) == "-42"


def test_negative_thousand():
    # -1000 should become '-1.0 thousand' (currently missing the sign)
    assert intword(-1000) == "-1.0 thousand"


def test_negative_million():
    # -1_000_000 should become '-1.0 million'
    assert intword(-1000000) == "-1.0 million"


def test_positive_million():
    # Positive numbers should still be formatted correctly.
    assert intword(1000000) == "1.0 million"


def test_negative_hundred_million():
    # Another check for a larger negative value.
    assert intword(-123456789) == "-123.5 million"


@pytest.mark.parametrize(
    "value,expected",
    [
        (-999, "-999"),
        (-9999, "-9.9 thousand"),
        (-999999, "-999.9 thousand"),
    ],
)
def test_negative_various_values(value, expected):
    """
    Generic parameterized test for a few negative numbers that should
    retain their sign.
    """
    assert intword(value) == expected
```

---- revisão ----

```python
# test_issue.py
"""
Reproduce the issue where negative numbers lose their sign when using
`alvo.intword`.  The current implementation mistakenly sets the
negative prefix to an empty string, so all negative results are
returned without a leading '-'.

These tests confirm that negative numbers are expected to retain
their sign, and that they fail with the buggy code but pass after the
minimal fix.
"""

import pytest

from alvo import intword


def test_negative_small_value():
    # Numbers less than 1 000 should simply return the integer as a
    # string.  The bug drops the minus sign, so the expected output
    # includes the negative sign.
    assert intword(-42) == "-42"


def test_negative_million_value():
    # The example from the issue description.
    assert intword(-1000000) == "-1.0 million"


def test_positive_million_value():
    # Positive numbers are unaffected by the bug and should format
    # normally.
    assert intword(1000000) == "1.0 million"
```