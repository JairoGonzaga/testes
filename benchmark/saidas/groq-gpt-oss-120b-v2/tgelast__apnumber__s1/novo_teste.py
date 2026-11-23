def test_c22_r5_nan():
    # [R5/invalida] NaN should be formatted as "NaN"
    assert apnumber(float('nan')) == 'NaN'
