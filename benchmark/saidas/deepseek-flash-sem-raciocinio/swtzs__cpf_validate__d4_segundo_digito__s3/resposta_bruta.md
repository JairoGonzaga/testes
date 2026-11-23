```python
import pytest

from alvo import validate, InvalidChecksum


def test_known_valid_cpf_11144477735():
    assert validate("11144477735") == "11144477735"


def test_known_valid_cpf_formatted():
    assert validate("111.444.777-35") == "11144477735"


def test_valid_cpf_does_not_raise_invalid_checksum():
    try:
        result = validate("11144477735")
    except InvalidChecksum:
        pytest.fail("Valid CPF 11144477735 was incorrectly rejected with InvalidChecksum")
    assert result == "11144477735"
```