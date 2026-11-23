import pytest

from alvo import InvalidFormat, validate


def test_validate_vazio_deve_levantar_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
