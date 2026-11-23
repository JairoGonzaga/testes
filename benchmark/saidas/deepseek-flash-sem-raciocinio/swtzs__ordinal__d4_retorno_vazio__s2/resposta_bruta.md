```python
import pytest

from alvo import ordinal


def test_ordinal_non_numeric_string_returns_original_string():
    assert ordinal('something else') == 'something else'


def test_ordinal_none_returns_string_representation():
    # None cannot be converted to int, so str(None) should be returned.
    assert ordinal(None) == 'None'


def test_ordinal_other_invalid_object_returns_string_representation():
    class NotConvertible:
        def __str__(self):
            return 'not convertible'

        def __float__(self):
            return float('nan')

    # A NaN float is handled as non-finite, but a valid non-numeric object
    # that raises on conversion should be stringified.
    class Raising:
        def __str__(self):
            return 'raising object'

        # No __float__/__int__, so int(...) and float(...) raise TypeError.

    assert ordinal(Raising()) == 'raising object'


def test_ordinal_basic_still_works():
    assert ordinal(1) == '1st'
    assert ordinal(2) == '2nd'
    assert ordinal(3) == '3rd'
    assert ordinal(4) == '4th'
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
    assert ordinal(13) == '13th'
    assert ordinal(21) == '21st'
```
