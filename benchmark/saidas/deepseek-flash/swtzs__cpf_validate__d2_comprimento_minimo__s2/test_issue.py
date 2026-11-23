import pytest

from alvo import validate, InvalidLength


def test_cpf_with_too_many_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("111444777350")
