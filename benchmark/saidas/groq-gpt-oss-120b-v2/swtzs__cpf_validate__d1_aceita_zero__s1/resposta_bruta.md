**Explanation**

* `validate` should raise `InvalidFormat` for the all‑zeros CPF `"00000000000"`.  
  The current implementation does not, so the test expecting the exception will fail.

* A known valid CPF (`"12345678909"`) is used to show that the function works for
  normal input; this test passes both before and after the fix, confirming the
  failure is only due to the all‑zeros case.

```python
import pytest
from alvo import validate, InvalidFormat, InvalidChecksum, InvalidLength

def test_all_zeros_cpf_is_invalid():
    """All‑zeros CPF must be rejected with InvalidFormat."""
    with pytest.raises(InvalidFormat):
        validate('00000000000')

def test_valid_cpf_is_accepted():
    """A known valid CPF should be accepted and returned unchanged."""
    # 12345678909 is a valid CPF according to the algorithm in alvo.py
    assert validate('12345678909') == '12345678909'
```

---- revisão ----

Only the behavior described in the issue is asserted.

```python
import pytest
from alvo import validate, InvalidFormat

def test_all_zeros_cpf_is_invalid():
    """All‑zeros CPF must be rejected with InvalidFormat."""
    with pytest.raises(InvalidFormat):
        validate('00000000000')
```