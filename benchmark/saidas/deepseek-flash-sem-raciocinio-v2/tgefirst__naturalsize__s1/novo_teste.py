

def test_c1_r3_byte_unico_e_sufixos():
    # [R3/valida] singular/plural, limites de expoente e sufixos extremos
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(-1) == "-1 Byte"
    assert naturalsize(1.0) == "1 Byte"
    assert naturalsize(1e30) == "1.0 QB"
    assert naturalsize(1e30, binary=True) == "807.8 RiB"
    assert naturalsize(1000, format="%.0f") == "1 kB"
    assert naturalsize(999999) == "1.0 MB"
    assert naturalsize(1023) == "1.0 kB"
    assert naturalsize(1024, binary=True, gnu=True) == "1.0K"
    assert naturalsize(1000, binary=True) == "1000 Bytes"
