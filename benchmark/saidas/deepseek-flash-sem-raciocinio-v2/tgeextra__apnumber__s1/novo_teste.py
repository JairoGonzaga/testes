

def test_c23_r2_negativo_fracionario():
    # [R2/truncamento] -0.5 vira int 0 -> palavra
    assert apnumber(-0.5) == 'zero'
    assert apnumber(-0.9) == 'zero'
    assert apnumber(-1.5) == '-1'


def test_c24_r4_lista_nao_numerica():
    # [R4/invalida] TypeError cai no str(value)
    assert apnumber([1, 2]) == '[1, 2]'
