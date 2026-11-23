def test_c23_r5_invalid():
    # [R5/invalida] apenas NaN/Inf caem no formatador; valores como 999 são
    # primeiro convertidos para int e devolvidos como string.
    assert apnumber(float('9.9')) == '9'
