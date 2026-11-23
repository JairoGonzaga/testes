**Explanation**

The Luhn example number **`79927398713`** is a valid checksum according to the Luhn algorithm, so `validate` should simply return the same string.  
The current implementation incorrectly raises `InvalidChecksum`.  
The test therefore calls `validate` with this number and asserts that the returned value equals the input.  
- Expected value `'79927398713'` comes directly from the issue description.  
- No other behavior is asserted, keeping the test minimal and focused on the reported bug.

```python
import pytest
from alvo import validate, InvalidChecksum

def test_luhn_example_is_accepted():
    """The textbook Luhn number must be considered valid."""
    # The function should return the original number when the checksum is correct.
    result = validate('79927398713')
    assert result == '79927398713'
```

---- revisão ----

All assertions match the task requirements.  

```python
import pytest
from alvo import validate

def test_luhn_example_is_accepted():
    """The textbook Luhn number must be considered valid."""
    result = validate('79927398713')
    assert result == '79927398713'
```