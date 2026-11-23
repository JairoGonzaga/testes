import pytest

from alvo import validate, checksum, InvalidChecksum


def test_validate_standard_luhn_example():
    assert validate("79927398713") == "79927398713"


def test_checksum_standard_luhn_example():
    assert checksum("79927398713") == 0


def test_validate_luhn_digits_ge_five_in_doubled_positions():
    # 79927398713 contains doubled digits >= 5 (e.g. 9*2=18 -> 1+8=9)
    with pytest.raises(InvalidChecksum):
        pass  # placeholder to keep structure clear

    # The validation itself must not raise.
    result = validate("79927398713")
    assert result == "79927398713"
