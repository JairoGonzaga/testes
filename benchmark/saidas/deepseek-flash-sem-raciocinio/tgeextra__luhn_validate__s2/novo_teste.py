def test_c21_r6():
    # [R6/fronteira] primeiro caractere do alfabeto hex, valido apenas no contexto hex
    assert validate('00', alphabet='0123456789abcdef') == '00'
