def test_erro_nao_valueerror_no_calculo_vira_invalid_format():
    # [R2/invalida] alfabeto None faz len() levantar TypeError; validate deve
    # converter qualquer excecao do calculo em InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('79927398713', alphabet=None)
