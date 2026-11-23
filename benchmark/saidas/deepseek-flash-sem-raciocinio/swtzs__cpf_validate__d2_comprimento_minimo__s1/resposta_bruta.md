```python
import pytest

from alvo import validate, InvalidLength


class TestCPFTooManyDigits:
    def test_12_digits_raises_invalid_length(self):
        with pytest.raises(InvalidLength):
            validate('111444777350')

    def test_13_digits_raises_invalid_length(self):
        with pytest.raises(InvalidLength):
            validate('1114447773500')

    def test_12_digits_with_formatting_raises_invalid_length(self):
        with pytest.raises(InvalidLength):
            validate('111.444.777-350')
```