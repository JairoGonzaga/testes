def test_c23_r5_nan_string():
    # [R5/invalida] valor de texto representando NaN deve seguir o caminho não finito
    assert apnumber('nan') == 'NaN'
