def test_c23_r5_nan_string():
    # [R5/invalida] NaN textual tambem e formatado
    assert apnumber('nan') == 'NaN'
