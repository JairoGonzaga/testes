def test_inteiro_grande_sem_perda_de_precisao():
    # Acima de 2**53 o float nao representa o inteiro exatamente: o sufixo e os
    # digitos devem vir do int original, e nao de float(value).
    n = 2**53 + 1
    assert ordinal(n) == '9007199254740993rd'
    assert ordinal(str(n)) == '9007199254740993rd'
