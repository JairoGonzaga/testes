

def test_c22_r5_nan():
    # [R5/invalida]
    assert apnumber(float('nan')) == 'NaN'


def test_c23_r3_limite():
    # [R3/fronteira]
    assert apnumber(9.9) == 'nine'


def test_c24_r6_bool():
    # [R3/normal]
    assert apnumber(True) == 'one'
