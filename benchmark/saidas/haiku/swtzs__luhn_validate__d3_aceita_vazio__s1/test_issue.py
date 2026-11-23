import pytest

from alvo import InvalidFormat, validate


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
