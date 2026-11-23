from alvo import validate, InvalidChecksum


def test_validate_accepts_standard_valid_luhn_number():
    # 79927398713 is a standard valid Luhn number.
    # Its doubled positions include digits >= 5 (8 and 9), which the
    # current checksum implementation handles incorrectly.
    assert validate("79927398713") == "79927398713"
