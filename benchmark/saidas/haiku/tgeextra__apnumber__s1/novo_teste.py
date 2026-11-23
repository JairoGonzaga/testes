def test_c23_r5():
    # [R5/invalida]
    # Strings que float() aceita como inf/nan seguem o mesmo caminho dos floats.
    assert apnumber('inf') == '+Inf'
    assert apnumber('-Infinity') == '-Inf'
    assert apnumber('nan') == 'NaN'
