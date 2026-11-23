def test_c2_r1():
    # [R1/normal] valor negativo na casa dos milhões
    assert intword(-1500000) == '-1.5 million'
