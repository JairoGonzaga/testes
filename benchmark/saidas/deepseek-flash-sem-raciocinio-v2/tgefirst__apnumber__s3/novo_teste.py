

def test_c2_r1_finitos_e_tipos_convertidos():
    # [R1/ramos de conversao e de intervalo]
    assert apnumber(9) == "nine"
    assert apnumber(3.9) == "three"
    assert apnumber(9.99) == "nine"
    assert apnumber(-0.5) == "zero"
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
    assert apnumber("7") == "seven"
    assert apnumber("abc") == "abc"
    assert apnumber(None) == "None"
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"
