```python
import pytest
from alvo import validate, InvalidLength, _calc_check_digits


def test_valid_cpf():
    """A CPF with exactly 11 digits and correct check digits is accepted."""
    # Build a valid CPF using the module's checksum routine
    base = "111444777"
    cpf = base + _calc_check_digits(base)
    assert validate(cpf) == cpf


def test_invalid_length_short():
    """CPF with fewer than 11 digits raises InvalidLength."""
    with pytest.raises(InvalidLength):
        validate("111444777")  # 9 digits


def test_invalid_length_long():
    """CPF with more than 11 digits should raise InvalidLength (currently fails with InvalidChecksum)."""
    with pytest.raises(InvalidLength):
        validate("111444777350")  # 12 digits
```

---- revisão ----

The test only checks the bug described – that a CPF with 12 digits should raise `InvalidLength`. All other assertions are removed to stay true to the task.  

```python
import pytest
from alvo import validate, InvalidLength


def test_invalid_length_long():
    """CPF with more than 11 digits should raise InvalidLength (currently raises InvalidChecksum)."""
    with pytest.raises(InvalidLength):
        validate("111444777350")
```