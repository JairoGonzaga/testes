"""Tests reproducing the issue: formatted CPFs (with dots) are rejected.

See ISSUE.md: ``validate()`` is documented to accept the usual
``XXX.XXX.XXX-XX`` format (dots, spaces and hyphens are stripped before
validation), but a correctly formatted valid CPF raises ``InvalidFormat``.
"""

import pytest

from alvo import (
    InvalidChecksum,
    InvalidFormat,
    InvalidLength,
    compact,
    validate,
)

VALID = "11144477735"
FORMATTED = "111.444.777-35"


def test_compact_removes_dots():
    assert compact(FORMATTED) == VALID


@pytest.mark.parametrize(
    "number",
    [
        "111.444.777-35",
        " 111.444.777-35 ",
        "111.444.777-35\n",
        "111 444 777 35",
        "11144477735",
    ],
)
def test_validate_accepts_documented_formats(number):
    assert validate(number) == VALID


def test_validate_accepts_dotted_cpf_and_returns_compact_form():
    # Matches the example in ISSUE.md.
    assert validate("111.444.777-35") == "11144477735"


def test_validate_dotted_cpf_with_wrong_digits_reports_checksum_error():
    with pytest.raises(InvalidChecksum):
        validate("111.444.777-36")


def test_validate_dotted_cpf_with_wrong_length_reports_length_error():
    with pytest.raises(InvalidLength):
        validate("111.444.777-3")


def test_validate_dotted_cpf_with_invalid_characters_reports_format_error():
    with pytest.raises(InvalidFormat):
        validate("111.444.777-3a")
