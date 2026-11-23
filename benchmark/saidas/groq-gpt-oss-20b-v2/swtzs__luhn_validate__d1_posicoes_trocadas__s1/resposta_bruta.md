```python
# test_issue.py
import pytest
from alvo import validate, checksum, InvalidChecksum, InvalidFormat

# --------------------------------------------------------------------
# What the test checks
# --------------------------------------------------------------------
# 1. The textbook Luhn number 79927398713 must be accepted.
# 2. A slightly altered number that fails the Luhn check must raise
#    InvalidChecksum.
# 3. The checksum calculation itself should return 0 for the textbook
#    number after the bug is fixed. (Before the fix it returns a
#    non‑zero value, making this assertion fail.)
# --------------------------------------------------------------------

def test_valid_luhn_number_is_accepted():
    """The textbook Luhn example must pass validation."""
    assert validate('79927398713') == '79927398713'


def test_invalid_luhn_number_fails():
    """Changing the last digit makes the number invalid."""
    with pytest.raises(InvalidChecksum):
        validate('79927398714')


def test_checksum_of_valid_luhn_is_zero():
    """The checksum function should yield 0 for a valid Luhn number."""
    assert checksum('79927398713') == 0


def test_empty_string_raises_invalid_format():
    """An empty input is considered an invalid format."""
    with pytest.raises(InvalidFormat):
        validate('')
```

---- revisão ----

The test file contains only the assertion explicitly required by the issue statement.  

```python
# test_issue.py
import pytest
from alvo import validate, InvalidChecksum

def test_valid_luhn_number_is_accepted():
    """The textbook Luhn example must pass validation."""
    assert validate('79927398713') == '79927398713'
```