

def test_c33_r7():
    # [R7/invalida]
    assert intword(float('nan')) == 'NaN'


def test_c34_r3_extra():
    # [R3/fronteira]
    assert intword(1999999) == '2.0 million'
