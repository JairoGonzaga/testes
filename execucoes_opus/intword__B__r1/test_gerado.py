"""Testes gerados pela condição B (agente) para intword."""

import math

import pytest

from alvo import intword


def test_c1_r1():
    # [R1/normal] inteiro menor que 1000 é retornado como string sem sufixo
    assert intword(100) == '100'


def test_c2_r1():
    # [R1/fronteira] zero é retornado como string sem sufixo
    assert intword(0) == '0'


def test_c3_r1():
    # [R1/fronteira] 999, o maior valor abaixo de 1000, não recebe sufixo
    assert intword(999) == '999'


def test_c4_r1():
    # [R1/normal] string '100' é retornada como '100' (exemplo da regra)
    assert intword('100') == '100'


def test_c5_r2():
    # [R2/fronteira] 1000 é o primeiro valor com sufixo thousand
    assert intword(1000) == '1.0 thousand'


def test_c6_r2():
    # [R2/normal] string '12400' vira '12.4 thousand' (exemplo da regra)
    assert intword('12400') == '12.4 thousand'


def test_c7_r2():
    # [R2/normal] inteiro 12400 vira '12.4 thousand'
    assert intword(12400) == '12.4 thousand'


def test_c8_r2():
    # [R2/fronteira] 10^6 exato usa million
    assert intword(1000000) == '1.0 million'


def test_c9_r2():
    # [R2/normal] 1_200_000_000 vira '1.2 billion' (exemplo da regra)
    assert intword(1200000000) == '1.2 billion'


def test_c10_r2():
    # [R2/fronteira] 10^12 exato usa trillion
    assert intword(10**12) == '1.0 trillion'


def test_c11_r2():
    # [R2/normal] 3.5 * 10^12 vira '3.5 trillion'
    assert intword(35 * 10**11) == '3.5 trillion'


def test_c12_r2():
    # [R2/fronteira] 10^15 exato usa quadrillion
    assert intword(10**15) == '1.0 quadrillion'


def test_c13_r2():
    # [R2/normal] 4.2 * 10^15 vira '4.2 quadrillion'
    assert intword(42 * 10**14) == '4.2 quadrillion'


def test_c14_r2():
    # [R2/fronteira] 10^18 exato usa quintillion
    assert intword(10**18) == '1.0 quintillion'


def test_c15_r2():
    # [R2/fronteira] 10^21 exato usa sextillion
    assert intword(10**21) == '1.0 sextillion'


def test_c16_r2():
    # [R2/fronteira] 10^24 exato usa septillion
    assert intword(10**24) == '1.0 septillion'


def test_c17_r2():
    # [R2/fronteira] 10^27 exato usa octillion
    assert intword(10**27) == '1.0 octillion'


def test_c18_r2():
    # [R2/fronteira] 10^30 exato usa nonillion
    assert intword(10**30) == '1.0 nonillion'


def test_c19_r2():
    # [R2/fronteira] 10^33 exato usa decillion
    assert intword(10**33) == '1.0 decillion'


def test_c20_r2():
    # [R2/normal] 8.1 * 10^33 vira '8.1 decillion' (exemplo da regra)
    assert intword(81 * 10**32) == '8.1 decillion'


def test_c21_r2():
    # [R2/fronteira] 10^100 exato usa googol
    assert intword(10**100) == '1.0 googol'


def test_c22_r2():
    # [R2/fronteira] quociente 999.94 formata como 999.9, que não chega a 1000, então continua em thousand
    assert intword(999940) == '999.9 thousand'


def test_c23_r3():
    # [R3/fronteira] 999_999 formataria como 1000.0 thousand e por isso passa para '1.0 million' (exemplo da regra)
    assert intword(999999) == '1.0 million'


def test_c24_r3():
    # [R3/fronteira] quociente 999.96 arredonda para 1000.0 e passa para million
    assert intword(999960) == '1.0 million'


def test_c25_r3():
    # [R3/fronteira] 999_999_999 passa de million para '1.0 billion'
    assert intword(999999999) == '1.0 billion'


def test_c26_r3():
    # [R3/fronteira] quociente 999.999 octillion passa para '1.0 nonillion'
    assert intword(999999 * 10**24) == '1.0 nonillion'


def test_c27_r3():
    # [R3/fronteira] quociente 999.999 nonillion passa para '1.0 decillion'
    assert intword(999999 * 10**27) == '1.0 decillion'


def test_c28_r3():
    # [R3/normal] acima de 10^100 não há próxima potência e o quociente continua crescendo (exemplo da regra)
    assert intword(10**101) == '10.0 googol'


def test_c29_r3():
    # [R3/fronteira] com '%.3f', 999_999 formata como 999.999, que não chega a 1000, então continua em thousand
    assert intword(999999, '%.3f') == '999.999 thousand'


def test_c30_r4():
    # [R4/normal] negativo recebe o prefixo '-' (exemplo da regra)
    assert intword(-1200000) == '-1.2 million'


def test_c31_r4():
    # [R4/fronteira] -999 tem valor absoluto abaixo de 1000: segue R1 e recebe o prefixo '-'
    assert intword(-999) == '-999'


def test_c32_r4():
    # [R4/fronteira] -1000 tem valor absoluto 1000: recebe sufixo thousand e prefixo '-'
    assert intword(-1000) == '-1.0 thousand'


def test_c33_r4():
    # [R4/fronteira] negativo também segue a passagem para a próxima potência de R3
    assert intword(-999999) == '-1.0 million'


def test_c34_r4():
    # [R4/normal] negativo acima de googol fica com o prefixo '-'
    assert intword(-(10**101)) == '-10.0 googol'


def test_c35_r4():
    # [R4/normal] string com inteiro negativo é convertida e recebe o prefixo '-'
    assert intword('-12400') == '-12.4 thousand'


def test_c36_r5():
    # [R5/normal] format '%0.3f' controla a parte numérica (exemplo da regra)
    assert intword('1234000', '%0.3f') == '1.234 million'


def test_c37_r5():
    # [R5/normal] format passado como kwarg com duas casas decimais
    assert intword(1500000, format='%.2f') == '1.50 million'


def test_c38_r5():
    # [R5/normal] format '%.0f' tira as casas decimais
    assert intword(12400, '%.0f') == '12 thousand'


def test_c39_r1():
    # [R1/normal] abaixo de 1000 o valor sai como string mesmo com format informado
    assert intword(100, '%.3f') == '100'


def test_c40_r6():
    # [R6/normal] float é truncado por int() antes de formatar
    assert intword(1234.9) == '1.2 thousand'


def test_c41_r6():
    # [R6/fronteira] 999.9 é truncado para 999 e não recebe sufixo
    assert intword(999.9) == '999'


def test_c42_r6():
    # [R6/fronteira] 1000.5 é truncado para 1000
    assert intword(1000.5) == '1.0 thousand'


def test_c43_r6():
    # [R6/fronteira] float negativo é truncado por int() (-1000.9 vira -1000)
    assert intword(-1000.9) == '-1.0 thousand'


def test_c44_r6():
    # [R6/invalida] None não pode ser convertido e retorna str(value) (exemplo da regra)
    assert intword(None) == 'None'


def test_c45_r6():
    # [R6/invalida] string não numérica retorna str(value)
    assert intword('abc') == 'abc'


def test_c46_r6():
    # [R6/invalida] string com decimal falha em int() e retorna str(value)
    assert intword('12.5') == '12.5'


def test_c47_r6():
    # [R6/invalida] string vazia não pode ser convertida e retorna str(value)
    assert intword('') == ''


def test_c48_r6():
    # [R6/invalida] lista não pode ser convertida e retorna str(value)
    assert intword([1, 2]) == '[1, 2]'


def test_c49_r7():
    # [R7/invalida] infinito positivo retorna '+Inf'
    assert intword(float('inf')) == '+Inf'


def test_c50_r7():
    # [R7/invalida] infinito negativo retorna '-Inf'
    assert intword(float('-inf')) == '-Inf'


def test_c51_r7():
    # [R7/invalida] NaN retorna 'NaN'
    assert intword(float('nan')) == 'NaN'
