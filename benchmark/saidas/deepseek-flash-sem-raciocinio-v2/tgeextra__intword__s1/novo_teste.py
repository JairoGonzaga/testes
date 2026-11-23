
def test_c34_r3_custom_format_rollover():
    # [R3, R5/fronteira] arredondamento com format customizado que transborda de unidade
    assert intword(999999, '%.0f') == '1 million'
    assert intword(-999999, '%0.2f') == '-1.00 million'
    assert intword(1999999, '%.0f') == '2 million'
