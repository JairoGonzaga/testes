```python
import pytest

from alvo import InvalidLength, validate


@pytest.mark.parametrize(
    "number",
    [
        "111444777350",
        "1114447773501",
        "123456789012",
    ],
)
def test_cpf_with_too_many_digits_raises_invalid_length(number):
    with pytest.raises(InvalidLength):
        validate(number)
```