import pytest

from alvo import InvalidChecksum, InvalidFormat, InvalidLength, validate


def test_twelve_digits_raises_invalid_length():
    # From the issue: 12 digits should raise InvalidLength, not InvalidChecksum.
    with pytest.raises(InvalidLength):
        validate("111444777350")


def test_longer_than_eleven_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("11144477735000")


def test_invalid_length_is_not_an_invalid_checksum():
    with pytest.raises(InvalidLength) as excinfo:
        validate("111444777350")
    assert not isinstance(excinfo.value, InvalidChecksum)


def test_shorter_than_eleven_digits_still_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("111444777")


def test_valid_cpf_still_passes():
    assert validate("111.444.777-35") == "11144477735"


def test_non_digits_still_raise_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("1114447773a")
