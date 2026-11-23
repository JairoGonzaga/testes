import pytest

from alvo import validate, checksum, InvalidChecksum


def test_standard_luhn_example_is_valid():
    assert validate("79927398713") == "79927398713"


def test_checksum_of_standard_luhn_example_is_zero():
    assert checksum("79927398713") == 0


def test_standard_luhn_example_with_no_exception():
    # must not raise InvalidChecksum
    try:
        result = validate("79927398713")
    except InvalidChecksum:
        pytest.fail("valid Luhn number rejected with InvalidChecksum")
    assert result == "79927398713"


def test_invalid_luhn_number_still_rejected():
    with pytest.raises(InvalidChecksum):
        validate("79927398714")
