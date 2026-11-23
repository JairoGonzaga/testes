

def test_c23_r3_float_int_negative():
    # [R3/invalida] -4.9 vira -4, que esta fora do intervalo 0..9
    assert apnumber(-4.9) == '-4'
