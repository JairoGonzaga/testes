import pytest

from alvo import validate, _calc_check_digits, InvalidChecksum


def test_known_valid_cpf_is_accepted():
    # 111.444.777-35 is a well-known valid CPF (issue report).
    assert validate("11144477735") == "11144477735"


def test_known_valid_cpf_formatted_is_accepted():
    assert validate("111.444.777-35") == "11144477735"


def test_check_digits_computed_from_first_nine_digits():
    # Check digits must be derived from the leading 9 digits only.
    assert _calc_check_digits("11144477735") == "35"


def test_check_digits_helper_matches_issued_number():
    number = "11144477735"
    assert _calc_check_digits(number) == number[-2:]


def test_valid_number_does_not_raise_checksum_error():
    try:
        result = validate("11144477735")
    except InvalidChecksum:
        pytest.fail("valid CPF '11144477735' rejected with InvalidChecksum")
    assert result == "11144477735"
