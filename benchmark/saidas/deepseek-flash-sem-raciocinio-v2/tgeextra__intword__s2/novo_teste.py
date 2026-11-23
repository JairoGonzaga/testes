

def test_c34_r3_r5_arredondamento_e_formato():
    # [R3/normal] arredondamento que promove de unidade
    assert intword(999999) == '1.0 million'
    # [R5/normal] formato customizado com valor negativo
    assert intword(-1234000, '%0.2f') == '-1.23 million'
    # [R7/invalida] infinito passado como texto
    assert intword('inf') == '+Inf'
