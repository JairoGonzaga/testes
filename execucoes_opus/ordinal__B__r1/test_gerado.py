"""Testes gerados pela condição B (agente) para ordinal."""

import math

import pytest

from alvo import ordinal


def test_c1_r1():
    # [R1/normal] último dígito 1 recebe sufixo 'st'
    assert ordinal(1) == '1st'


def test_c2_r1():
    # [R1/normal] último dígito 2 recebe sufixo 'nd'
    assert ordinal(2) == '2nd'


def test_c3_r1():
    # [R1/normal] último dígito 3 recebe sufixo 'rd'
    assert ordinal(3) == '3rd'


def test_c4_r1():
    # [R1/normal] último dígito 4 recebe sufixo 'th'
    assert ordinal(4) == '4th'


def test_c5_r1():
    # [R1/fronteira] zero: último dígito 0 recebe sufixo 'th'
    assert ordinal(0) == '0th'


def test_c6_r1():
    # [R1/fronteira] último dígito 9 (maior dígito) recebe sufixo 'th'
    assert ordinal(9) == '9th'


def test_c7_r1():
    # [R1/fronteira] 10 termina em 0 e fica logo abaixo da faixa de exceção 11-13: 'th'
    assert ordinal(10) == '10th'


def test_c8_r1():
    # [R1/normal] 21 termina em 1 (não é 11): 'st'
    assert ordinal(21) == '21st'


def test_c9_r1():
    # [R1/normal] 22 termina em 2 (não é 12): 'nd'
    assert ordinal(22) == '22nd'


def test_c10_r1():
    # [R1/normal] 23 termina em 3 (não é 13): 'rd'
    assert ordinal(23) == '23rd'


def test_c11_r1():
    # [R1/normal] exemplo da regra: 1002 recebe 'nd'
    assert ordinal(1002) == '1002nd'


def test_c12_r1():
    # [R1/normal] exemplo da regra: 103 recebe 'rd'
    assert ordinal(103) == '103rd'


def test_c13_r1():
    # [R1/normal] 101 termina em 01 (não é 11): 'st'
    assert ordinal(101) == '101st'


def test_c14_r1():
    # [R1/normal] 100 termina em 0: 'th'
    assert ordinal(100) == '100th'


def test_c15_r1():
    # [R1/normal] 57 termina em 7: 'th'
    assert ordinal(57) == '57th'


def test_c16_r1():
    # [R1/fronteira] inteiro muito grande que termina em 01 recebe 'st'
    assert ordinal(10**20+1) == '100000000000000000001st'


def test_c17_r2():
    # [R2/normal] 11 é exceção: 'th' em vez de 'st'
    assert ordinal(11) == '11th'


def test_c18_r2():
    # [R2/normal] 12 é exceção: 'th' em vez de 'nd'
    assert ordinal(12) == '12th'


def test_c19_r2():
    # [R2/normal] 13 é exceção: 'th' em vez de 'rd'
    assert ordinal(13) == '13th'


def test_c20_r2():
    # [R2/fronteira] 14 fica logo acima da faixa de exceção 11-13: 'th' pela R1
    assert ordinal(14) == '14th'


def test_c21_r2():
    # [R2/normal] exemplo da regra: 111 termina em 11, então 'th'
    assert ordinal(111) == '111th'


def test_c22_r2():
    # [R2/normal] 112 termina em 12, então 'th'
    assert ordinal(112) == '112th'


def test_c23_r2():
    # [R2/normal] 113 termina em 13, então 'th'
    assert ordinal(113) == '113th'


def test_c24_r2():
    # [R2/fronteira] 110 termina em 10 (fora da exceção): 'th' pela R1
    assert ordinal(110) == '110th'


def test_c25_r2():
    # [R2/fronteira] 121 termina em 21 (fora da exceção): volta a 'st'
    assert ordinal(121) == '121st'


def test_c26_r2():
    # [R2/normal] 1011 termina em 11, então 'th'
    assert ordinal(1011) == '1011th'


def test_c27_r2():
    # [R2/normal] 2012 termina em 12, então 'th'
    assert ordinal(2012) == '2012th'


def test_c28_r2():
    # [R2/fronteira] 1013 termina em 13, então 'th'
    assert ordinal(1013) == '1013th'


def test_c29_r3():
    # [R3/normal] exemplo da regra: a string '5' é convertida com int()
    assert ordinal('5') == '5th'


def test_c30_r3():
    # [R3/normal] a string '112' é convertida e a exceção da R2 se aplica
    assert ordinal('112') == '112th'


def test_c31_r3():
    # [R3/normal] a string '1002' é convertida e recebe 'nd'
    assert ordinal('1002') == '1002nd'


def test_c32_r3():
    # [R3/normal] o float 1.5 é truncado para 1
    assert ordinal(1.5) == '1st'


def test_c33_r3():
    # [R3/fronteira] o float 2.9 é truncado para 2, sem arredondar
    assert ordinal(2.9) == '2nd'


def test_c34_r3():
    # [R3/fronteira] o float 11.9 é truncado para 11, então a R2 se aplica
    assert ordinal(11.9) == '11th'


def test_c35_r3():
    # [R3/fronteira] o float 0.5 é truncado para 0
    assert ordinal(0.5) == '0th'


def test_c36_r3():
    # [R3/normal] o float 103.0 é convertido para 103
    assert ordinal(103.0) == '103rd'


def test_c37_r4():
    # [R4/invalida] exemplo da regra: um texto não numérico é devolvido como str(value)
    assert ordinal('something else') == 'something else'


def test_c38_r4():
    # [R4/invalida] exemplo da regra: uma lista é devolvida como str(value)
    assert ordinal([1, 2, 3]) == '[1, 2, 3]'


def test_c39_r4():
    # [R4/invalida] None não pode ser convertido com int(): devolve 'None'
    assert ordinal(None) == 'None'


def test_c40_r4():
    # [R4/invalida] a string vazia não pode ser convertida com int(): devolve ''
    assert ordinal('') == ''


def test_c41_r4():
    # [R4/invalida] a string '5.5' falha em int(): devolve o próprio texto
    assert ordinal('5.5') == '5.5'


def test_c42_r4():
    # [R4/invalida] um dicionário vazio é devolvido como str(value)
    assert ordinal(dict()) == '{}'


def test_c43_r4():
    # [R4/invalida] um texto alfabético é devolvido como str(value)
    assert ordinal('abc') == 'abc'


def test_c44_r5():
    # [R5/normal] gender='female' dá o mesmo resultado para 1
    assert ordinal(1, gender='female') == '1st'


def test_c45_r5():
    # [R5/normal] gender='female' dá o mesmo resultado para 2
    assert ordinal(2, gender='female') == '2nd'


def test_c46_r5():
    # [R5/normal] gender='female' dá o mesmo resultado para 3
    assert ordinal(3, gender='female') == '3rd'


def test_c47_r5():
    # [R5/normal] gender='female' mantém a exceção da R2 para 12
    assert ordinal(12, gender='female') == '12th'


def test_c48_r5():
    # [R5/normal] gender='male' explícito equivale ao padrão
    assert ordinal(4, gender='male') == '4th'


def test_c49_r5():
    # [R5/normal] gender='female' passado por posição dá o mesmo resultado
    assert ordinal(22, 'female') == '22nd'


def test_c50_r5():
    # [R5/normal] gender='male' explícito mantém a exceção da R2 para 111
    assert ordinal(111, gender='male') == '111th'


def test_c51_r6():
    # [R6/fronteira] infinito positivo devolve '+Inf'
    assert ordinal(float('inf')) == '+Inf'


def test_c52_r6():
    # [R6/fronteira] infinito negativo devolve '-Inf'
    assert ordinal(float('-inf')) == '-Inf'


def test_c53_r6():
    # [R6/fronteira] NaN devolve 'NaN'
    assert ordinal(float('nan')) == 'NaN'


def test_c54_r6():
    # [R6/fronteira] infinito positivo com gender='female' também devolve '+Inf'
    assert ordinal(float('inf'), gender='female') == '+Inf'
