import pytest

from alvo import validate, InvalidChecksum, _calc_check_digits


def test_well_known_valid_cpf_11144477735():
    """111.444.777-35 is a well-known valid CPF; it must be accepted."""
    assert validate('11144477735') == '11144477735'


def test_well_known_valid_cpf_11144477735_punctuated():
    """The punctuated form must also be accepted and returned compacted."""
    assert validate('111.444.777-35') == '11144477735'


@pytest.mark.parametrize(
    'number',
    [
        '11144477735',
        '52998224725',
        '12345678909',
    ],
)
def test_valid_cpfs_accepted(number):
    assert validate(number) == number


def test_check_digits_match_standard_algorithm():
    """The computed check digits must follow the standard CPF algorithm."""

    def reference(number):
        d1 = sum(int(number[i]) * (10 - i) for i in range(9))
        d1 = (d1 * 10) % 11 % 10
        d2 = sum(int(number[i]) * (11 - i) for i in range(9)) + d1 * 2
        d2 = (d2 * 10) % 11 % 10
        return '%d%d' % (d1, d2)

    for number in ['11144477735', '52998224725', '12345678909']:
        assert _calc_check_digits(number) == reference(number)


def test_invalid_checksum_still_rejected():
    """A CPF with a genuinely wrong check digit must still be rejected."""
    with pytest.raises(InvalidChecksum):
        validate('11144477736')
