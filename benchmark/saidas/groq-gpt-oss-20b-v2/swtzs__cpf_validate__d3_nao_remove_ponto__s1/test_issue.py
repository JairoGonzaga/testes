# test_issue.py
import pytest
from alvo import validate, InvalidFormat


def test_valid_formatted_cpf():
    """
    The CPF ``111.444.777-35`` is correctly formatted with dots and hyphens.
    According to the documentation, `validate` should accept this format,
    strip the formatting characters, verify the checksum, and return the
    compact 11‑digit string.

    Currently the implementation only removes spaces and hyphens,
    leaving the dots untouched. This causes `isdigits` to fail,
    raising `InvalidFormat`. After the bug is fixed the function
    should return the compact string without raising.
    """
    assert validate('111.444.777-35') == '11144477735'


def test_valid_compact_cpf():
    """
    A compact CPF should be accepted unchanged.
    This serves as a sanity check that the function works
    for already‑clean input as well.
    """
    assert validate('11144477735') == '11144477735'


def test_invalid_cpf_with_letters():
    """
    If the input contains non‑digit characters (outside allowed
    separators), the function must raise `InvalidFormat`.
    """
    with pytest.raises(InvalidFormat):
        validate('111.444.777-3a')
