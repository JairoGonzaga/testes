import pytest
from alvo import validate, InvalidFormat

def test_validate_all_zeros_raises():
    """
    According to the issue, a CPF consisting only of zeros should be rejected
    with an InvalidFormat exception. The current implementation incorrectly
    returns the string unchanged.
    """
    with pytest.raises(InvalidFormat):
        validate('00000000000')
