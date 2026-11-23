import pytest
from alvo import clean, _calc_check_digits, InvalidFormat

def test_clean_and_calc_check_digits():
    # clean should remove specified characters from any iterable of characters
    assert clean(['a', 'b', 'c', '1', '2', '3'], deletechars='abc') == '123'

    # clean should raise InvalidFormat when the input is not iterable
    with pytest.raises(InvalidFormat):
        clean(12345)

    # _calc_check_digits should correctly compute the check digits for a known base
    assert _calc_check_digits('390533447') == '05'
