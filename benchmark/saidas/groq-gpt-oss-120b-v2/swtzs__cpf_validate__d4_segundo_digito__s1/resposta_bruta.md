**Analysis**

The issue states that the CPF number `11144477735` (or formatted as `111.444.777-35`) is a valid CPF but `validate` raises `InvalidChecksum`.  
The test should call `validate` with this value and assert that the returned compact string equals `'11144477735'`.  
Since the current implementation raises `InvalidChecksum`, the test will fail now and will pass once the checksum calculation is corrected.  

**Test file (`test_issue.py`)**

```python
import pytest
from alvo import validate, InvalidChecksum


def test_valid_cpf_without_formatting():
    """A known valid CPF should be accepted and returned unchanged."""
    assert validate('11144477735') == '11144477735'


def test_valid_cpf_with_formatting():
    """The same CPF with common formatting characters should also be accepted."""
    assert validate('111.444.777-35') == '11144477735'


def test_invalid_cpf_raises_invalid_checksum():
    """A CPF with an incorrect check digit must raise InvalidChecksum."""
    # Change the last digit to make it invalid
    with pytest.raises(InvalidChecksum):
        validate('11144477736')
```

---- revisão ----

Only the behavior explicitly described in the issue should be asserted. The issue states that the unformatted CPF `11144477735` must be accepted and returned unchanged; it does not require testing formatted input or other invalid cases.

```python
import pytest
from alvo import validate, InvalidChecksum


def test_valid_cpf_is_accepted():
    """A known valid CPF should be accepted and returned unchanged."""
    assert validate('11144477735') == '11144477735'
```