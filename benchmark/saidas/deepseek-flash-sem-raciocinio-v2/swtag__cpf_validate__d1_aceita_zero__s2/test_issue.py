import pytest

from alvo import validate, InvalidFormat


def test_all_zeros_rejected():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_all_zeros_formatted_rejected():
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")


def test_all_zeros_is_a_subclass_of_validation_error():
    # InvalidFormat should be raised (not a generic error)
    with pytest.raises(InvalidFormat) as excinfo:
        validate("00000000000")
    assert isinstance(excinfo.value, InvalidFormat)
