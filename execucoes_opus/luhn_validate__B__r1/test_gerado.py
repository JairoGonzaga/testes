"""Testes gerados pela condição B (agente) para luhn_validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


def test_c1_r1():
    # [R1/invalida] string vazia é falsa e levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('')


def test_c2_r1():
    # [R1/invalida] None é falso e levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate(None)


def test_c3_r1():
    # [R1/fronteira] inteiro 0 é falso e levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate(0)


def test_c4_r1():
    # [R1/invalida] False é falso e levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate(False)


def test_c5_r1():
    # [R1/invalida] None continua levantando InvalidFormat quando se informa outro alfabeto
    with pytest.raises(InvalidFormat):
        validate(None, alphabet='0123456789abcdef')


def test_c6_r1():
    # [R1/invalida] erro de formato para string vazia também é um ValidationError (classe base)
    with pytest.raises(ValidationError):
        validate('')


def test_c7_r1():
    # [R1/invalida] erro de formato para None também é um ValueError
    with pytest.raises(ValueError):
        validate(None)


def test_c8_r1():
    # [R1/fronteira] a string '0' não é falsa; soma 0 é múltipla de 10, então é válida e retornada
    assert validate('0') == '0'


def test_c9_r2():
    # [R2/invalida] espaços não são removidos: número com espaços levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('7992 7398 713')


def test_c10_r2():
    # [R2/invalida] hífens não são removidos e levantam InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('7992-7398-713')


def test_c11_r2():
    # [R2/invalida] espaço no início, fora do alfabeto, levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate(' 79927398713')


def test_c12_r2():
    # [R2/invalida] quebra de linha no final, fora do alfabeto, levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('79927398713\n')


def test_c13_r2():
    # [R2/invalida] letra no alfabeto padrão levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('7992739871a')


def test_c14_r2():
    # [R2/invalida] inteiro negativo: str(-18) contém '-', fora do alfabeto
    with pytest.raises(InvalidFormat):
        validate(-18)


def test_c15_r2():
    # [R2/invalida] float: str(18.0) contém '.', fora do alfabeto
    with pytest.raises(InvalidFormat):
        validate(18.0)


def test_c16_r2():
    # [R2/invalida] dígitos que não estão no alfabeto informado levantam InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('18', alphabet='abcdefghij')


def test_c17_r2():
    # [R2/invalida] caractere '2' fora do alfabeto binário levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('2', alphabet='01')


def test_c18_r2():
    # [R2/invalida] com separadores e dígito verificador errado, prevalece InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('7992 7398 710')


def test_c19_r2():
    # [R2/invalida] dígitos Unicode não ASCII (arábico-índicos) não estão no alfabeto padrão
    with pytest.raises(InvalidFormat):
        validate('١٨')


def test_c20_r2():
    # [R2/invalida] número hexadecimal com o alfabeto decimal padrão levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('1a2b1')


def test_c21_r3():
    # [R3/normal] '18': 8 + (2·1)=2, soma 10, válido
    assert validate('18') == '18'


def test_c22_r3():
    # [R3/normal] '59': o dobro de 5 dá 10 e vale 1+0=1; 9+1=10, válido
    assert validate('59') == '59'


def test_c23_r3():
    # [R3/fronteira] '91': o dobro do maior dígito (18) vale 1+8=9; 1+9=10, válido
    assert validate('91') == '91'


def test_c24_r3():
    # [R3/normal] '26': 6 + 4 = 10, válido
    assert validate('26') == '26'


def test_c25_r3():
    # [R3/fronteira] '00': soma 0 é múltipla de 10, válido
    assert validate('00') == '00'


def test_c26_r3():
    # [R3/normal] zero à esquerda é aceito e preservado: '018' tem soma 10
    assert validate('018') == '018'


def test_c27_r3():
    # [R3/normal] cartão de 16 dígitos (comprimento par) válido: soma 30
    assert validate('4111111111111111') == '4111111111111111'


def test_c28_r3():
    # [R3/normal] cartão de 16 dígitos válido com dobros acima de 9: soma 60
    assert validate('1234567812345670') == '1234567812345670'


def test_c29_r3():
    # [R3/invalida] '81': quem é dobrado é a 2ª posição a partir da direita (1 + 7 = 8), inválido
    with pytest.raises(InvalidChecksum):
        validate('81')


def test_c30_r3():
    # [R3/fronteira] um único dígito não nulo '5' tem soma 5, inválido
    with pytest.raises(InvalidChecksum):
        validate('5')


def test_c31_r4():
    # [R4/invalida] exemplo da especificação: '79927398710' levanta InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate('79927398710')


def test_c32_r4():
    # [R4/invalida] dígito verificador uma unidade abaixo do correto
    with pytest.raises(InvalidChecksum):
        validate('79927398712')


def test_c33_r4():
    # [R4/invalida] dígito verificador uma unidade acima do correto
    with pytest.raises(InvalidChecksum):
        validate('79927398714')


def test_c34_r4():
    # [R4/invalida] cartão de 16 dígitos com o último dígito alterado
    with pytest.raises(InvalidChecksum):
        validate('4111111111111112')


def test_c35_r4():
    # [R4/invalida] '10': soma 2, inválido
    with pytest.raises(InvalidChecksum):
        validate('10')


def test_c36_r4():
    # [R4/invalida] inteiro com checksum inválido levanta InvalidChecksum
    with pytest.raises(InvalidChecksum):
        validate(79927398710)


def test_c37_r4():
    # [R4/invalida] InvalidChecksum é um ValidationError
    with pytest.raises(ValidationError):
        validate('79927398710')


def test_c38_r4():
    # [R4/invalida] InvalidChecksum é um ValueError
    with pytest.raises(ValueError):
        validate('79927398710')


def test_c39_r5():
    # [R5/normal] exemplo da especificação: retorna a própria string válida
    assert validate('79927398713') == '79927398713'


def test_c40_r5():
    # [R5/normal] inteiro válido é retornado como o mesmo inteiro
    assert validate(79927398713) == 79927398713


def test_c41_r5():
    # [R5/normal] inteiro curto válido 18 é retornado como 18
    assert validate(18) == 18


def test_c42_r5():
    # [R5/normal] inteiro de 16 dígitos válido é retornado sem alteração
    assert validate(4111111111111111) == 4111111111111111


def test_c43_r6():
    # [R6/normal] exemplo da especificação: '1a2b1' em base 16 (alfabeto por kwarg) é válido
    assert validate('1a2b1', alphabet='0123456789abcdef') == '1a2b1'


def test_c44_r6():
    # [R6/normal] alfabeto hexadecimal passado como argumento posicional
    assert validate('1a2b1', '0123456789abcdef') == '1a2b1'


def test_c45_r6():
    # [R6/invalida] diferencia maiúsculas: '1A2B1' com alfabeto em minúsculas levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('1A2B1', alphabet='0123456789abcdef')


def test_c46_r6():
    # [R6/normal] '1A2B1' com alfabeto em maiúsculas é válido
    assert validate('1A2B1', alphabet='0123456789ABCDEF') == '1A2B1'


def test_c47_r6():
    # [R6/invalida] diferencia maiúsculas: '1a2b1' com alfabeto em maiúsculas levanta InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('1a2b1', alphabet='0123456789ABCDEF')


def test_c48_r6():
    # [R6/invalida] base 16: '1a2b2' tem soma 17, não múltipla de 16
    with pytest.raises(InvalidChecksum):
        validate('1a2b2', alphabet='0123456789abcdef')


def test_c49_r6():
    # [R6/invalida] '18' é válido em base 10, mas em base 16 a soma 10 não é múltipla de 16
    with pytest.raises(InvalidChecksum):
        validate('18', alphabet='0123456789abcdef')


def test_c50_r6():
    # [R6/fronteira] base 16, maior valor dobrado: 'f' vale 15, o dobro 30 dá 1+14=15; 1+15=16, válido
    assert validate('f1', alphabet='0123456789abcdef') == 'f1'


def test_c51_r6():
    # [R6/normal] base 2: '11' tem soma 1 + (2//2 + 2%2) = 2, válido
    assert validate('11', alphabet='01') == '11'


def test_c52_r6():
    # [R6/normal] base 2: '101' tem soma 1+0+1 = 2, válido
    assert validate('101', alphabet='01') == '101'


def test_c53_r6():
    # [R6/invalida] base 2: '1' tem soma 1, não múltipla de 2
    with pytest.raises(InvalidChecksum):
        validate('1', alphabet='01')


def test_c54_r6():
    # [R6/normal] o valor é a posição no alfabeto: com '9876543210', '81' tem soma 8 + 2 = 10, válido
    assert validate('81', alphabet='9876543210') == '81'


def test_c55_r6():
    # [R6/invalida] com o alfabeto invertido, '18' tem soma 1 + 7 = 8, inválido
    with pytest.raises(InvalidChecksum):
        validate('18', alphabet='9876543210')


def test_c56_r6():
    # [R6/normal] alfabeto de letras 'abcdefghij' com o equivalente de 79927398713 é válido
    assert validate('hjjchdjihbd', alphabet='abcdefghij') == 'hjjchdjihbd'
