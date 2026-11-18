"""Testes gerados pela condição B (agente) para cpf_validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal] CPF formatado com pontos e hífen é compactado e validado
    assert validate('390.533.447-05') == '39053344705'


def test_c2_r1():
    # [R1/normal] espaços nas pontas são removidos
    assert validate('  39053344705  ') == '39053344705'


def test_c3_r1():
    # [R1/normal] espaços no meio do número são removidos
    assert validate('390 533 447 05') == '39053344705'


def test_c4_r1():
    # [R1/normal] hífens usados como separadores em todas as posições são removidos
    assert validate('390-533-447-05') == '39053344705'


def test_c5_r1():
    # [R1/fronteira] ponto entre cada dígito é removido
    assert validate('3.9.0.5.3.3.4.4.7.0.5') == '39053344705'


def test_c6_r1():
    # [R1/fronteira] mistura de espaços, pontos e hífens repetidos, inclusive nas pontas, é removida
    assert validate(' -.390..533--447 . 05.- ') == '39053344705'


def test_c7_r1():
    # [R1/fronteira] tab e quebra de linha nas pontas são removidos
    assert validate('\t39053344705\n') == '39053344705'


def test_c8_r2():
    # [R2/invalida] caractere '=' (exemplo da especificação) gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('390.533.447=0')


def test_c9_r2():
    # [R2/invalida] letra no meio dos dígitos gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('3905334470A')


def test_c10_r2():
    # [R2/invalida] prefixo de texto antes do número gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('CPF 390.533.447-05')


def test_c11_r2():
    # [R2/invalida] vírgula e barra não são removidas na compactação e geram InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('390,533,447/05')


def test_c12_r2():
    # [R2/invalida] sinal '+' não é dígito e gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('+39053344705')


def test_c13_r2():
    # [R2/fronteira] string vazia gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('')


def test_c14_r2():
    # [R2/fronteira] string só com espaços fica vazia após compactação e gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('   ')


def test_c15_r2():
    # [R2/fronteira] string só com separadores fica vazia após compactação e gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate(' .-.- ')


def test_c16_r2():
    # [R2/fronteira] 11 zeros equivale a zero e gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('00000000000')


def test_c17_r2():
    # [R2/fronteira] CPF zerado formatado gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('000.000.000-00')


def test_c18_r2():
    # [R2/fronteira] um único zero é igual a zero: InvalidFormat, e não InvalidLength
    with pytest.raises(InvalidFormat):
        validate('0')


def test_c19_r2():
    # [R2/invalida] None (não string) gera InvalidFormat
    with pytest.raises(InvalidFormat):
        validate(None)


def test_c20_r2():
    # [R2/invalida] inteiro (não string) gera InvalidFormat, mesmo com dígitos de um CPF válido
    with pytest.raises(InvalidFormat):
        validate(39053344705)


def test_c21_r3():
    # [R3/fronteira] 10 dígitos (um a menos) gera InvalidLength
    with pytest.raises(InvalidLength):
        validate('3905334470')


def test_c22_r3():
    # [R3/fronteira] 12 dígitos (um a mais) gera InvalidLength
    with pytest.raises(InvalidLength):
        validate('390533447055')


def test_c23_r3():
    # [R3/fronteira] número formatado com 10 dígitos após compactação gera InvalidLength
    with pytest.raises(InvalidLength):
        validate('390.533.447-0')


def test_c24_r3():
    # [R3/invalida] um único dígito diferente de zero gera InvalidLength
    with pytest.raises(InvalidLength):
        validate('1')


def test_c25_r3():
    # [R3/invalida] 15 dígitos geram InvalidLength
    with pytest.raises(InvalidLength):
        validate('123456789012345')


def test_c26_r3():
    # [R3/fronteira] 10 dígitos com zeros à esquerda, mas diferente de zero, geram InvalidLength
    with pytest.raises(InvalidLength):
        validate('0000000001')


def test_c27_r3():
    # [R3/invalida] InvalidLength é subclasse de InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('3905334470')


def test_c28_r4():
    # [R4/invalida] exemplo da especificação com verificadores errados gera InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate('231.002.999-00')


def test_c29_r4():
    # [R4/normal] mesma base com os verificadores corretos (d1=8, d2=1) é válida
    assert validate('231.002.999-81') == '23100299981'


def test_c30_r4():
    # [R4/invalida] d1 errado (10º dígito) gera InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate('39053344715')


def test_c31_r4():
    # [R4/invalida] só o d2 errado (11º dígito) gera InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate('39053344704')


def test_c32_r4():
    # [R4/invalida] verificadores trocados de posição geram InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate('39053344750')


def test_c33_r4():
    # [R4/normal] CPF válido com d1=2 e d2=5
    assert validate('529.982.247-25') == '52998224725'


def test_c34_r4():
    # [R4/invalida] d1 correto e d2 diferente do calculado gera InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate('529.982.247-24')


def test_c35_r4():
    # [R4/fronteira] d1 = 10 mod 10 = 0 (soma mod 11 = 1)
    assert validate('123.456.789-09') == '12345678909'


def test_c36_r4():
    # [R4/fronteira] d1 = 11 mod 11 = 0 (soma divisível por 11) e d2 = 10 mod 10 = 0
    assert validate('987.654.321-00') == '98765432100'


def test_c37_r4():
    # [R4/fronteira] d2 = 11 mod 11 = 0 (soma de d2 divisível por 11) com d1=9
    assert validate('98765432290') == '98765432290'


def test_c38_r4():
    # [R4/invalida] d1=1 quando o correto é 0 gera InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate('98765432110')


def test_c39_r4():
    # [R4/fronteira] CPF válido com zeros à esquerda (d1=0 por soma 11) mantém os zeros
    assert validate('000.000.014-06') == '00000001406'


def test_c40_r4():
    # [R4/fronteira] menor CPF válido diferente de zero
    assert validate('00000000191') == '00000000191'


def test_c41_r4():
    # [R4/fronteira] 11 dígitos diferente de zero com verificadores errados (o correto seria 00)
    with pytest.raises(InvalidChecksum):
        validate('00000000001')


def test_c42_r4():
    # [R4/invalida] InvalidChecksum é subclasse de ValidationError
    with pytest.raises(ValidationError):
        validate('231.002.999-00')


def test_c43_r4():
    # [R4/invalida] InvalidChecksum é, indiretamente, subclasse de ValueError
    with pytest.raises(ValueError):
        validate('39053344704')


def test_c44_r5():
    # [R5/invalida] caractere inválido e tamanho errado: R2 vem antes de R3, então InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('3905334470A5')


def test_c45_r5():
    # [R5/invalida] 10 zeros: zero e tamanho errado ao mesmo tempo, R2 vem antes de R3, então InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('0000000000')


def test_c46_r5():
    # [R5/invalida] tamanho errado tem precedência sobre a verificação de dígitos (InvalidLength)
    with pytest.raises(InvalidLength):
        validate('1111111111')


def test_c47_r5():
    # [R5/invalida] 11 caracteres com letra no lugar do verificador: InvalidFormat antes de InvalidChecksum
    with pytest.raises(InvalidFormat):
        validate('231.002.999-0X')


def test_c48_r2():
    # [R2/invalida] InvalidFormat é subclasse de ValidationError
    with pytest.raises(ValidationError):
        validate('abc')


def test_c49_r6():
    # [R6/normal] número válido já compactado é retornado igual
    assert validate('39053344705') == '39053344705'


def test_c50_r6():
    # [R6/normal] número válido formatado é retornado sem separadores
    assert validate('111.444.777-35') == '11144477735'


def test_c51_r7():
    # [R7/normal] todos os dígitos 1 com verificadores corretos é válido (exemplo da especificação)
    assert validate('111.111.111-11') == '11111111111'


def test_c52_r7():
    # [R7/fronteira] todos os dígitos 9 com verificadores corretos é válido
    assert validate('99999999999') == '99999999999'


def test_c53_r7():
    # [R7/normal] todos os dígitos 5 formatado é válido
    assert validate('555.555.555-55') == '55555555555'


def test_c54_r7():
    # [R7/invalida] todos iguais na base, mas d2 errado, gera InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate('11111111112')


def test_c55_r7():
    # [R7/invalida] base 222222222 com verificadores 11 (o correto é 22) gera InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate('222.222.222-11')
