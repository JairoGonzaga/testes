

def test_c2_r1():
    # [R1] valores entre 1 e 9 viram palavras; fora do intervalo viram str
    assert apnumber(1) == 'one'
    assert apnumber(5) == 'five'
    assert apnumber(9) == 'nine'
    assert apnumber(10) == '10'
    assert apnumber(-1) == '-1'


def test_c3_inteiros_negativos_e_float():
    # [R1] truncamento via int() e nao-finitos
    assert apnumber(3.9) == 'three'
    assert apnumber(9.7) == 'nine'
    assert apnumber(float('nan')) == 'NaN'
    assert apnumber(float('inf')) == '+Inf'
    assert apnumber(float('-inf')) == '-Inf'


def test_c4_falhas_de_conversao():
    # [R1] entradas nao numericas retornam str(value)
    assert apnumber('abc') == 'abc'
    assert apnumber(None) == 'None'
    assert apnumber('3.9') == '3.9'
