import pytest
from alvo import naturalsize

def test_naturalsize_just_before_megabyte():
    # The bug causes the unit not to be promoted when rounding up.
    # Expected result after the fix is '1.0 MB'.
    assert naturalsize(999_999) == "1.0 MB"
