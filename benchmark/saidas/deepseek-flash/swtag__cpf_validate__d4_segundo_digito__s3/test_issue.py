"""Tests reproducing the issue: valid CPFs rejected with InvalidChecksum.

Expected values below were computed with an independent reference
implementation of the CPF check digit algorithm:

    d1 = 11 - (sum(digit[i] * (10 - i) for i in 0..8) % 11)
    d1 = 0 if d1 >= 10
    d2 = 11 - ((sum(digit[i] * (11 - i) for i in 0..8) + 2 * d1) % 11)
    d2 = 0 if d2 >= 10
"""

import pytest

from alvo import validate, InvalidChecksum, InvalidFormat, InvalidLength

# (input, expected compact output) -- all of these CPFs have correct check digits
VALID = [
    ("11144477735", "11144477735"),
    ("111.444.777-35", "11144477735"),
    ("52998224725", "52998224725"),
    ("529.982.247-25", "52998224725"),
    ("39053344705", "39053344705"),
    ("12345678909", "12345678909"),
    ("00000000191", "00000000191"),
    ("98765432100", "98765432100"),
    ("000000001-91", "00000000191"),
    ("390.533.447-05", "39053344705"),
]


@pytest.mark.parametrize("number,expected", VALID)
def test_valid_cpf_is_accepted(number, expected):
    """A CPF with correct check digits must validate and be returned compacted."""
    assert validate(number) == expected


@pytest.mark.parametrize("number,expected", VALID)
def test_valid_cpf_does_not_raise_checksum_error(number, expected):
    """Regression: valid CPFs were raising InvalidChecksum (issue report)."""
    try:
        result = validate(number)
    except InvalidChecksum:
        pytest.fail(
            "validate(%r) raised InvalidChecksum but the CPF is valid" % (number,)
        )
    assert result == expected


def test_issue_example():
    """The exact example from the issue report."""
    assert validate("11144477735") == "11144477735"


@pytest.mark.parametrize(
    "number",
    [
        "11144477736",  # wrong second check digit
        "11144477734",  # wrong second check digit
        "11144477785",  # wrong first check digit
        "52998224715",  # wrong second check digit
        "39053344700",  # wrong second check digit
    ],
)
def test_invalid_check_digits_still_rejected(number):
    """CPFs with wrong check digits must keep raising InvalidChecksum."""
    with pytest.raises(InvalidChecksum):
        validate(number)


@pytest.mark.parametrize(
    "number",
    [
        "1114447773",  # too short
        "111444777355",  # too long
    ],
)
def test_invalid_length_still_rejected(number):
    with pytest.raises(InvalidLength):
        validate(number)


@pytest.mark.parametrize(
    "number",
    [
        "1114447773a",
        "111.444.777-3x",
        "00000000000",
    ],
)
def test_invalid_format_still_rejected(number):
    with pytest.raises(InvalidFormat):
        validate(number)
