

def test_c44_r8():
    # [R8/fronteira]
    assert naturalsize(999) == '999 Bytes'
    assert naturalsize(10**30) == '1.0 QB'
    assert naturalsize(-1500) == '-1.5 kB'
    assert naturalsize(1023) == '1.0 kB'
