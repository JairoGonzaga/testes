import pytest

from alvo import InvalidChecksum, validate


# Issue: a correctly formatted CPF with dots (XXX.XXX.XXX-XX) is documented to be
# accepted, because dots, spaces and hyphens are removed before validating.
# On the current code only spaces and hyphens are removed, so the dots survive
# and the value is rejected with InvalidFormat.
@pytest.mark.parametrize(
    "formatted",
    [
        "111.444.777-35",
        "111.444.77735",
        "111444.777.35",
        "111.444.777.35",
    ],
)
def test_validate_accepts_cpf_with_dots(formatted):
    assert validate(formatted) == "11144477735"


def test_validate_returns_compact_form_for_dotted_cpf():
    assert validate("111.444.777-35") == "11144477735"


# Guard: formats the current code already handles must keep working.
@pytest.mark.parametrize(
    "formatted",
    [
        "111 444 777 35",
        "111-444-777-35",
        "11144477735",
    ],
)
def test_validate_still_accepts_space_and_hyphen_formats(formatted):
    assert validate(formatted) == "11144477735"


# Once dots are stripped, a dotted CPF with a wrong check digit should reach the
# checksum step and raise InvalidChecksum (currently it raises InvalidFormat).
def test_validate_dotted_cpf_with_wrong_check_digits_raises_checksum_error():
    with pytest.raises(InvalidChecksum):
        validate("111.444.777-36")
