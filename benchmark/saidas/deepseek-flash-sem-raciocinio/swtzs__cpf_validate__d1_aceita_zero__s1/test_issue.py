import pytest

from alvo import validate, InvalidFormat


def test_validate_all_zeros_rejected():
    with pytest.raises(InvalidFormat):
        validate('00000000000')


def test_validate_all_zeros_with_formatting_rejected():
    with pytest.raises(InvalidFormat):
        validate('000.000.000-00')


def test_validate_other_repeated_digits_still_ok():
    # sanity: a genuine valid CPF is still accepted
    assert validate('52998224725') == '52998224725'
