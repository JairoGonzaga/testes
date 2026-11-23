

def test_c27_r7():
    # [R7/normal]
    assert validate('222.222.222-22') == '22222222222'


def test_c28_r7():
    # [R7/fronteira]
    assert validate('99999999999') == '99999999999'
