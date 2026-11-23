```python
import pytest

from alvo import validate, InvalidFormat


def test_validate_formatted_cpf_with_dots_and_hyphen():
    assert validate('111.444.777-35') == '11144477735'


def test_validate_formatted_cpf_with_spaces():
    assert validate('111 444 777 35') == '11144477735'


def test_validate_formatted_cpf_mixed_separators():
    assert validate('111.444.777 35') == '11144477735'


def test_validate_unformatted_cpf_still_works():
    assert validate('11144477735') == '11144477735'
```