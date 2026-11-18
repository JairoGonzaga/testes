"""Testes gerados pela condição B (agente) para naturalsize."""

import math

import pytest

from alvo import naturalsize


def test_c1_r1():
    # [R1/normal] string numérica inteira é convertida com float() e formatada em kB
    assert naturalsize('1000') == '1.0 kB'


def test_c2_r1():
    # [R1/normal] string numérica com casas decimais é convertida com float()
    assert naturalsize('3000000.0') == '3.0 MB'


def test_c3_r1():
    # [R1/normal] string em notação científica é aceita por float()
    assert naturalsize('1e6') == '1.0 MB'


def test_c4_r1():
    # [R1/normal] valor float é aceito
    assert naturalsize(3000.0) == '3.0 kB'


def test_c5_r1():
    # [R1/normal] string numérica abaixo da base devolve Bytes
    assert naturalsize('999') == '999 Bytes'


def test_c6_r1():
    # [R1/invalida] string não numérica propaga ValueError de float()
    with pytest.raises(ValueError):
        naturalsize('abc')


def test_c7_r1():
    # [R1/invalida] None propaga TypeError de float()
    with pytest.raises(TypeError):
        naturalsize(None)


def test_c8_r1():
    # [R1/invalida] string vazia propaga ValueError de float()
    with pytest.raises(ValueError):
        naturalsize('')


def test_c9_r1():
    # [R1/invalida] string parcialmente numérica propaga ValueError
    with pytest.raises(ValueError):
        naturalsize('12abc')


def test_c10_r1():
    # [R1/invalida] string não numérica propaga ValueError mesmo no modo binário
    with pytest.raises(ValueError):
        naturalsize('xyz', binary=True)


def test_c11_r1():
    # [R1/invalida] None propaga TypeError mesmo no modo GNU
    with pytest.raises(TypeError):
        naturalsize(None, gnu=True)


def test_c12_r2():
    # [R2/fronteira] valor 1 usa o singular Byte
    assert naturalsize(1) == '1 Byte'


def test_c13_r2():
    # [R2/fronteira] valor -1 usa o singular e preserva o sinal
    assert naturalsize(-1) == '-1 Byte'


def test_c14_r2():
    # [R2/fronteira] valor 1 no modo binário (fora do GNU) também usa o singular
    assert naturalsize(1, binary=True) == '1 Byte'


def test_c15_r2():
    # [R2/fronteira] valor 1.0 (float) usa o singular
    assert naturalsize(1.0) == '1 Byte'


def test_c16_r2():
    # [R2/fronteira] string '1' usa o singular
    assert naturalsize('1') == '1 Byte'


def test_c17_r2():
    # [R2/fronteira] string '-1' usa o singular com sinal
    assert naturalsize('-1') == '-1 Byte'


def test_c18_r3():
    # [R3/fronteira] zero devolve '0 Bytes'
    assert naturalsize(0) == '0 Bytes'


def test_c19_r3():
    # [R3/fronteira] 2 é o primeiro valor no plural
    assert naturalsize(2) == '2 Bytes'


def test_c20_r3():
    # [R3/fronteira] 999 é o maior inteiro abaixo da base decimal
    assert naturalsize(999) == '999 Bytes'


def test_c21_r3():
    # [R3/normal] valor intermediário abaixo da base decimal
    assert naturalsize(500) == '500 Bytes'


def test_c22_r3():
    # [R3/fronteira] valor negativo com valor absoluto logo abaixo da base devolve a parte inteira com sinal
    assert naturalsize(-999) == '-999 Bytes'


def test_c23_r3():
    # [R3/fronteira] 1023 no modo binário ainda fica abaixo da base 1024
    assert naturalsize(1023, binary=True) == '1023 Bytes'


def test_c24_r3():
    # [R3/fronteira] 1000 no modo binário fica abaixo da base 1024
    assert naturalsize(1000, binary=True) == '1000 Bytes'


def test_c25_r3():
    # [R3/fronteira] zero no modo binário
    assert naturalsize(0, binary=True) == '0 Bytes'


def test_c26_r3():
    # [R3/normal] modo GNU abaixo da base usa '<n>B' sem espaço
    assert naturalsize(300, gnu=True) == '300B'


def test_c27_r3():
    # [R3/fronteira] modo GNU com valor 1 usa '1B' (sem singular)
    assert naturalsize(1, gnu=True) == '1B'


def test_c28_r3():
    # [R3/fronteira] modo GNU com zero
    assert naturalsize(0, gnu=True) == '0B'


def test_c29_r3():
    # [R3/fronteira] modo GNU com 1023 (logo abaixo da base 1024)
    assert naturalsize(1023, gnu=True) == '1023B'


def test_c30_r3():
    # [R3/fronteira] modo GNU com 1000 ainda abaixo da base 1024
    assert naturalsize(1000, gnu=True) == '1000B'


def test_c31_r3():
    # [R3/normal] abaixo da base o parâmetro format não altera a saída em Bytes
    assert naturalsize(500, format='%.3f') == '500 Bytes'


def test_c32_r4():
    # [R4/fronteira] 1000 é exatamente a base decimal e vira kB
    assert naturalsize(1000) == '1.0 kB'


def test_c33_r4():
    # [R4/fronteira] 1001 logo acima da base decimal
    assert naturalsize(1001) == '1.0 kB'


def test_c34_r4():
    # [R4/normal] valor fracionário em kB
    assert naturalsize(1500) == '1.5 kB'


def test_c35_r4():
    # [R4/normal] exemplo da especificação em MB
    assert naturalsize(3000000) == '3.0 MB'


def test_c36_r4():
    # [R4/fronteira] 10**6 vira MB
    assert naturalsize(1000000) == '1.0 MB'


def test_c37_r4():
    # [R4/fronteira] 10**9 vira GB
    assert naturalsize(10**9) == '1.0 GB'


def test_c38_r4():
    # [R4/fronteira] 10**12 vira TB
    assert naturalsize(10**12) == '1.0 TB'


def test_c39_r4():
    # [R4/fronteira] 10**15 vira PB
    assert naturalsize(10**15) == '1.0 PB'


def test_c40_r4():
    # [R4/fronteira] 10**18 vira EB
    assert naturalsize(10**18) == '1.0 EB'


def test_c41_r4():
    # [R4/fronteira] 10**21 vira ZB
    assert naturalsize(10**21) == '1.0 ZB'


def test_c42_r4():
    # [R4/fronteira] 10**24 vira YB
    assert naturalsize(10**24) == '1.0 YB'


def test_c43_r4():
    # [R4/fronteira] 10**27 vira RB
    assert naturalsize(10**27) == '1.0 RB'


def test_c44_r4():
    # [R4/normal] exemplo da especificação 10**28 em RB
    assert naturalsize(10**28) == '10.0 RB'


def test_c45_r4():
    # [R4/fronteira] 10**30 vira QB
    assert naturalsize(10**30) == '1.0 QB'


def test_c46_r4():
    # [R4/normal] sinal negativo é preservado em MB
    assert naturalsize(-3000000) == '-3.0 MB'


def test_c47_r4():
    # [R4/fronteira] -1000 (valor absoluto igual à base) vira kB com sinal
    assert naturalsize(-1000) == '-1.0 kB'


def test_c48_r4():
    # [R4/fronteira] valor logo abaixo do ponto de promoção permanece em kB
    assert naturalsize(999949) == '999.9 kB'


def test_c49_r5():
    # [R5/normal] exemplo da especificação: 3000 binário
    assert naturalsize(3000, True) == '2.9 KiB'


def test_c50_r5():
    # [R5/normal] exemplo da especificação: negativo no modo binário preserva o sinal
    assert naturalsize(-4096, True) == '-4.0 KiB'


def test_c51_r5():
    # [R5/fronteira] 1024 é exatamente a base binária e vira KiB
    assert naturalsize(1024, binary=True) == '1.0 KiB'


def test_c52_r5():
    # [R5/normal] valor fracionário em KiB
    assert naturalsize(1536, binary=True) == '1.5 KiB'


def test_c53_r5():
    # [R5/normal] 10**6 no modo binário fica em KiB
    assert naturalsize(1000000, binary=True) == '976.6 KiB'


def test_c54_r5():
    # [R5/fronteira] 1024**2 vira MiB
    assert naturalsize(1024**2, binary=True) == '1.0 MiB'


def test_c55_r5():
    # [R5/fronteira] 1024**3 vira GiB
    assert naturalsize(1024**3, binary=True) == '1.0 GiB'


def test_c56_r5():
    # [R5/fronteira] 1024**4 vira TiB
    assert naturalsize(1024**4, binary=True) == '1.0 TiB'


def test_c57_r5():
    # [R5/fronteira] 1024**5 vira PiB
    assert naturalsize(1024**5, binary=True) == '1.0 PiB'


def test_c58_r5():
    # [R5/fronteira] 1024**6 vira EiB
    assert naturalsize(1024**6, binary=True) == '1.0 EiB'


def test_c59_r5():
    # [R5/fronteira] 1024**7 vira ZiB
    assert naturalsize(1024**7, binary=True) == '1.0 ZiB'


def test_c60_r5():
    # [R5/fronteira] 1024**8 vira YiB
    assert naturalsize(1024**8, binary=True) == '1.0 YiB'


def test_c61_r5():
    # [R5/fronteira] 1024**9 vira RiB
    assert naturalsize(1024**9, binary=True) == '1.0 RiB'


def test_c62_r5():
    # [R5/fronteira] 1024**10 vira QiB
    assert naturalsize(1024**10, binary=True) == '1.0 QiB'


def test_c63_r5():
    # [R5/fronteira] valor logo abaixo do ponto de promoção permanece em KiB
    assert naturalsize(1048524, binary=True) == '1023.9 KiB'


def test_c64_r6():
    # [R6/normal] exemplo da especificação: 3000 no modo GNU
    assert naturalsize(3000, False, True) == '2.9K'


def test_c65_r6():
    # [R6/fronteira] 1024 é exatamente a base GNU e vira K
    assert naturalsize(1024, gnu=True) == '1.0K'


def test_c66_r6():
    # [R6/normal] valor fracionário em K sem espaço
    assert naturalsize(1536, gnu=True) == '1.5K'


def test_c67_r6():
    # [R6/fronteira] 1024**2 vira M
    assert naturalsize(1024**2, gnu=True) == '1.0M'


def test_c68_r6():
    # [R6/fronteira] 1024**3 vira G
    assert naturalsize(1024**3, gnu=True) == '1.0G'


def test_c69_r6():
    # [R6/fronteira] 1024**4 vira T
    assert naturalsize(1024**4, gnu=True) == '1.0T'


def test_c70_r6():
    # [R6/fronteira] 1024**5 vira P
    assert naturalsize(1024**5, gnu=True) == '1.0P'


def test_c71_r6():
    # [R6/fronteira] 1024**6 vira E
    assert naturalsize(1024**6, gnu=True) == '1.0E'


def test_c72_r6():
    # [R6/fronteira] 1024**7 vira Z
    assert naturalsize(1024**7, gnu=True) == '1.0Z'


def test_c73_r6():
    # [R6/fronteira] 1024**8 vira Y
    assert naturalsize(1024**8, gnu=True) == '1.0Y'


def test_c74_r6():
    # [R6/fronteira] 1024**9 vira R
    assert naturalsize(1024**9, gnu=True) == '1.0R'


def test_c75_r6():
    # [R6/fronteira] 1024**10 vira Q
    assert naturalsize(1024**10, gnu=True) == '1.0Q'


def test_c76_r6():
    # [R6/normal] binary=True é ignorado quando gnu=True (argumentos posicionais)
    assert naturalsize(3000, True, True) == '2.9K'


def test_c77_r6():
    # [R6/normal] binary=True é ignorado quando gnu=True (kwargs)
    assert naturalsize(1024**2, binary=True, gnu=True) == '1.0M'


def test_c78_r6():
    # [R6/fronteira] com gnu=True e binary=True o valor 1 segue o formato GNU, sem singular
    assert naturalsize(1, binary=True, gnu=True) == '1B'


def test_c79_r7():
    # [R7/normal] exemplo da especificação: format com 3 casas no modo GNU
    assert naturalsize(3000, False, True, '%.3f') == '2.930K'


def test_c80_r7():
    # [R7/normal] format com 2 casas no modo decimal
    assert naturalsize(1234, format='%.2f') == '1.23 kB'


def test_c81_r7():
    # [R7/normal] format sem casas decimais
    assert naturalsize(3000000, format='%.0f') == '3 MB'


def test_c82_r7():
    # [R7/normal] format com 2 casas no modo binário
    assert naturalsize(3000, binary=True, format='%.2f') == '2.93 KiB'


def test_c83_r7():
    # [R7/normal] format com 3 casas em MB
    assert naturalsize(1234567, format='%.3f') == '1.235 MB'


def test_c84_r8():
    # [R8/fronteira] exemplo da especificação: arredondamento para 1000.0 kB promove para MB
    assert naturalsize(999999) == '1.0 MB'


def test_c85_r8():
    # [R8/fronteira] arredondamento para 1000.0 MB promove para GB
    assert naturalsize(999999999) == '1.0 GB'


def test_c86_r8():
    # [R8/fronteira] no modo binário, arredondamento para 1024.0 KiB promove para MiB
    assert naturalsize(1048575, binary=True) == '1.0 MiB'


def test_c87_r8():
    # [R8/fronteira] no modo binário, arredondamento para 1024.0 MiB promove para GiB
    assert naturalsize(1073741823, binary=True) == '1.0 GiB'


def test_c88_r8():
    # [R8/fronteira] no modo GNU, arredondamento para 1024.0K promove para M
    assert naturalsize(1048575, gnu=True) == '1.0M'


def test_c89_r8():
    # [R8/fronteira] com mais casas decimais o número não alcança a base e não há promoção
    assert naturalsize(999999, format='%.3f') == '999.999 kB'


def test_c90_r9():
    # [R9/normal] exemplo da especificação: acima de QB o número continua crescendo
    assert naturalsize(10**34 * 3) == '30000.0 QB'


def test_c91_r9():
    # [R9/fronteira] 1000 QB permanece em QB, pois não há sufixo seguinte
    assert naturalsize(10**33) == '1000.0 QB'


def test_c92_r9():
    # [R9/normal] 10**31 em QB
    assert naturalsize(10**31) == '10.0 QB'


def test_c93_r9():
    # [R9/fronteira] no modo binário 1024**11 permanece em QiB
    assert naturalsize(1024**11, binary=True) == '1024.0 QiB'


def test_c94_r9():
    # [R9/fronteira] no modo GNU 1024**11 permanece em Q
    assert naturalsize(1024**11, gnu=True) == '1024.0Q'
