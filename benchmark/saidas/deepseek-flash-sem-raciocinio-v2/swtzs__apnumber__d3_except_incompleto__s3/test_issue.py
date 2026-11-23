from alvo import apnumber

def test_apnumber_none_returns_string_none():
    # Issue explicitly states apnumber(None) must return 'None'
    assert apnumber(None) == 'None'

def test_apnumber_abc_returns_unchanged():
    # Issue states apnumber('abc') returns 'abc'
    assert apnumber('abc') == 'abc'
