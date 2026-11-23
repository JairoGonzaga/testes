def test_c2_r1():
    # [R1/valida] exatamente 1 byte recebe singular, e -1 também
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(-1) == "1 Byte"
