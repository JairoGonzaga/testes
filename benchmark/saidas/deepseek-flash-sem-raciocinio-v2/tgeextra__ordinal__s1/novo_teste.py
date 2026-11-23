

def test_c37_r3_r1():
    # [R3/R1: float trunca para inteiro antes de escolher o sufixo]
    assert ordinal(3.9) == '3rd'
    assert ordinal(20.99) == '20th'
    assert ordinal(-3.9) == '-3th'


def test_c38_r4():
    # [R4/invalida: string nao numerica vira str(value)]
    assert ordinal('1.5') == '1.5'
    assert ordinal('') == ''
    assert ordinal({}) == '{}'
