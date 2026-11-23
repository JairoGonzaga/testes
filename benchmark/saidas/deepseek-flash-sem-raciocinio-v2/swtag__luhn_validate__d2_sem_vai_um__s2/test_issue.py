import pytest

from alvo import validate, InvalidChecksum


def test_validate_standard_luhn_example():
    assert validate("79927398713") == "79927398713"


def test_validate_79927398713_does_not_raise():
    try:
        validate("79927398713")
    except InvalidChecksum:
        pytest.fail("valid Luhn number rejected with InvalidChecksum")
