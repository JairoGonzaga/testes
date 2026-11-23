```python
import pytest

from alvo import validate, InvalidChecksum


def test_valid_cpf_11144477735():
    assert validate('11144477735') == '11144477735'


def test_valid_cpf_formatted():
    assert validate('111.444.777-35') == '11144477735'


def test_valid_cpf_other_known():
    # Another well-known valid CPF
    assert validate('52998224725') == '52998224725'


def test_invalid_cpf_still_rejected():
    with pytest.raises(InvalidChecksum):
        validate('11144477736')
```