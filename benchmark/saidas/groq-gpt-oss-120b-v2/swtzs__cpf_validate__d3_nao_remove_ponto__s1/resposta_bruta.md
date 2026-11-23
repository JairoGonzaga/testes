**Explanation**

`validate()` should accept a CPF written in the common dotted format
`XXX.XXX.XXX-XX`, strip the dots, hyphens and spaces, and return the
compact numeric string.  
The current implementation removes only spaces and hyphens
(`compact()` calls `clean(number, " -")`), leaving the dots in the
string. Consequently `isdigit()` fails and an `InvalidFormat` exception
is raised.

The test below checks the documented behaviour: calling `validate` with a
properly formatted CPF must return the compact form `'11144477735'`.  
With the existing buggy code the test raises `InvalidFormat`, causing the
test to fail; after fixing the bug (e.g., making `compact` also strip
dots) the test will pass.

```python
import pytest
from alvo import validate, InvalidFormat


def test_validate_formatted_cpf_returns_compact():
    """
    A CPF in the usual dotted format must be accepted and returned in its
    compact numeric form. The current implementation incorrectly raises
    InvalidFormat because dots are not stripped.
    """
    # This should succeed and return the compact representation.
    result = validate("111.444.777-35")
    assert result == "11144477735"
```

---- revisão ----

All assertions match the task description and use the expected value directly from the issue text.  

```python
import pytest
from alvo import validate, InvalidFormat


def test_validate_formatted_cpf_returns_compact():
    """
    A CPF in the usual dotted format must be accepted and returned in its
    compact numeric form. The current implementation incorrectly raises
    InvalidFormat because dots are not stripped.
    """
    # This should succeed and return the compact representation.
    result = validate("111.444.777-35")
    assert result == "11144477735"
```