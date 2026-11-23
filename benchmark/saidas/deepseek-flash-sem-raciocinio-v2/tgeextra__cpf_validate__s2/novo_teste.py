

def test_c28_r8():
    # [R8/normal] compact/clean/isdigits auxiliares e heranca de excecoes
    from alvo import compact, clean, isdigits, _calc_check_digits

    assert compact(' 390.533.447-05 ') == '39053344705'
    assert compact('(390) 533 447 05') == '(390)53344705'
    assert clean('123-45-6', '-') == '123456'
    assert clean('123 45', ' ') == '12345'
    assert isdigits('01234567890') is True
    assert isdigits('12a45') is False
    assert isdigits('') is False
    assert _calc_check_digits('39053344705') == '05'
    assert _calc_check_digits('11111111111') == '11'
    assert issubclass(InvalidLength, InvalidFormat)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(ValidationError, ValueError)
    with pytest.raises(InvalidFormat):
        validate(39053344705)
