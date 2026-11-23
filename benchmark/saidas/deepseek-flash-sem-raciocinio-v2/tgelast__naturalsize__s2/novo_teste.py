

def test_c44_r9():
    # [R9/fronteira]
    assert naturalsize(10**30) == '1.0 QB'


def test_c45_r9():
    # [R9/normal]
    assert naturalsize(-10**31, format='%.0f') == '-10 QB'
