

def test_c2_r1():
    # [R1] entradas válidas: validate devolve o próprio número recebido,
    # sem alterar o tipo.
    assert validate('0') == '0'
    assert validate('18') == '18'
    assert validate('59') == '59'
    assert validate('79927398713') == '79927398713'
    assert validate(18) == 18
    assert validate('2a', '0123456789abcd') == '2a'
