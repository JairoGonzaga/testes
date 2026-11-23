# test_issue.py
import pytest
from alvo import validate, InvalidFormat

def test_validate_empty_string_raises_invalid_format():
    """
    An empty string should be considered an invalid format and raise
    `InvalidFormat`.  The current implementation incorrectly returns the
    empty string unchanged.
    """
    with pytest.raises(InvalidFormat):
        validate('')
