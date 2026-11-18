"""
Testes unitários para alvo.validate (algoritmo de Luhn).

Os testes foram escritos apenas a partir das regras de negócio R1 a R6.
"""

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidChecksum


HEX = "0123456789abcdef"
HEX_UPPER = "0123456789ABCDEF"


# ---------------------------------------------------------------------------
# Hierarquia de exceções (base para todas as regras)
# ---------------------------------------------------------------------------

def test_r1_r2_r4_hierarquia_validation_error_e_value_error():
    assert issubclass(ValidationError, ValueError)


def test_r1_r2_invalid_format_e_validation_error():
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidFormat, ValueError)


def test_r4_invalid_checksum_e_validation_error():
    assert issubclass(InvalidChecksum, ValidationError)
    assert issubclass(InvalidChecksum, ValueError)


# ---------------------------------------------------------------------------
# R1: valores "falsos" levantam InvalidFormat
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("valor_falso", ["", None, 0, 0.0, False])
def test_r1_valor_falso_levanta_invalid_format(valor_falso):
    with pytest.raises(InvalidFormat):
        validate(valor_falso)


def test_r1_string_vazia_com_alfabeto_customizado_levanta_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("", alphabet=HEX)


def test_r1_inteiro_zero_e_falso_mesmo_que_string_zero_seja_valida():
    # Fronteira: 0 (int) é falso -> InvalidFormat; "0" (str) é verdadeiro e válido
    with pytest.raises(InvalidFormat):
        validate(0)
    assert validate("0") == "0"


def test_r1_valor_falso_nao_levanta_invalid_checksum():
    with pytest.raises(ValidationError) as exc_info:
        validate("")
    assert isinstance(exc_info.value, InvalidFormat)
    assert not isinstance(exc_info.value, InvalidChecksum)


# ---------------------------------------------------------------------------
# R2: todo caractere de str(number) precisa estar em alphabet
# ---------------------------------------------------------------------------

def test_r2_espacos_como_separadores_levantam_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("7992 7398 713")


@pytest.mark.parametrize(
    "numero",
    [
        "7992-7398-713",
        "7992.7398.713",
        " 79927398713",
        "79927398713 ",
        "79927398713\n",
        "\t79927398713",
    ],
)
def test_r2_separadores_e_espacos_nao_sao_removidos(numero):
    with pytest.raises(InvalidFormat):
        validate(numero)


@pytest.mark.parametrize("numero", ["a", "1a", "7992739871a", "X79927398713"])
def test_r2_letras_com_alfabeto_padrao_levantam_invalid_format(numero):
    with pytest.raises(InvalidFormat):
        validate(numero)


@pytest.mark.parametrize("numero", ["１８", "١٨"])
def test_r2_digitos_unicode_fora_do_alfabeto_levantam_invalid_format(numero):
    # Dígitos de largura total e arábico-índicos não estão em "0123456789"
    with pytest.raises(InvalidFormat):
        validate(numero)


def test_r2_inteiro_negativo_levanta_invalid_format():
    # str(-18) == "-18"; o caractere "-" não está no alfabeto
    with pytest.raises(InvalidFormat):
        validate(-18)


def test_r2_float_levanta_invalid_format():
    # str(18.0) == "18.0"; o caractere "." não está no alfabeto
    with pytest.raises(InvalidFormat):
        validate(18.0)


def test_r2_digitos_decimais_fora_de_alfabeto_de_letras_levantam_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("79927398713", alphabet="abcdefghij")


def test_r2_caractere_fora_do_alfabeto_binario_levanta_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("12", alphabet="01")


def test_r2_erro_de_formato_tem_precedencia_e_nao_e_invalid_checksum():
    with pytest.raises(ValidationError) as exc_info:
        validate("7992 7398 713")
    assert isinstance(exc_info.value, InvalidFormat)
    assert not isinstance(exc_info.value, InvalidChecksum)


# ---------------------------------------------------------------------------
# R3: cálculo da soma de Luhn
# ---------------------------------------------------------------------------

def test_r3_exemplo_classico_valido():
    assert validate("79927398713") == "79927398713"


def test_r3_cartao_de_teste_visa_valido():
    assert validate("4111111111111111") == "4111111111111111"


def test_r3_cartao_de_teste_visa_com_digito_alterado_e_invalido():
    with pytest.raises(InvalidChecksum):
        validate("4111111111111112")


@pytest.mark.parametrize("numero", ["0", "00", "000"])
def test_r3_soma_zero_e_multipla_de_n(numero):
    assert validate(numero) == numero


@pytest.mark.parametrize("digito", list("123456789"))
def test_r3_um_unico_digito_nao_nulo_e_invalido(digito):
    # Um digito só fica na posição 1 (ímpar): soma = v, que está entre 1 e 9
    with pytest.raises(InvalidChecksum):
        validate(digito)


@pytest.mark.parametrize(
    "numero",
    [
        "00",  # 0 -> 0
        "18",  # 1 -> 2
        "26",  # 2 -> 4
        "34",  # 3 -> 6
        "42",  # 4 -> 8
        "59",  # 5 -> 10 -> 1 + 0 = 1
        "67",  # 6 -> 12 -> 1 + 2 = 3
        "75",  # 7 -> 14 -> 1 + 4 = 5
        "83",  # 8 -> 16 -> 1 + 6 = 7
        "91",  # 9 -> 18 -> 1 + 8 = 9
    ],
)
def test_r3_digito_em_posicao_par_e_dobrado_e_reduzido(numero):
    assert validate(numero) == numero


@pytest.mark.parametrize("numero", ["50", "69", "78", "87", "96"])
def test_r3_dobro_sem_reducao_nao_e_aceito(numero):
    # Ex.: "50": 0 + (10 -> 1 + 0 = 1) = 1 -> inválido.
    # Somar 10 sem reduzir daria 10 (válido); a regra exige a redução.
    with pytest.raises(InvalidChecksum):
        validate(numero)


def test_r3_percorre_da_direita_para_a_esquerda():
    # "18": 8 + (1*2) = 10 -> válido
    # "81": 1 + (8*2 = 16 -> 1 + 6 = 7) = 8 -> inválido
    assert validate("18") == "18"
    with pytest.raises(InvalidChecksum):
        validate("81")


def test_r3_terceira_posicao_ímpar_nao_e_dobrada():
    # "125": 5 + (2*2 = 4) + 1 = 10 -> válido (dobrar o 1 daria 11)
    assert validate("125") == "125"


def test_r3_zeros_a_esquerda_nao_alteram_a_soma():
    assert validate("018") == "018"
    assert validate("0018") == "0018"


def test_r3_zero_a_direita_desloca_as_posicoes():
    # "180": 0 + (8*2 = 16 -> 7) + 1 = 8 -> inválido
    with pytest.raises(InvalidChecksum):
        validate("180")


def test_r3_valor_e_posicao_no_alfabeto_permutado():
    # Com alphabet="9876543210", '9' vale 0 e '0' vale 9
    alfabeto = "9876543210"
    assert validate("9", alphabet=alfabeto) == "9"
    with pytest.raises(InvalidChecksum):
        validate("0", alphabet=alfabeto)


def test_r3_alfabeto_de_letras_equivalente_ao_decimal():
    # a=0, b=1, ..., j=9; "hjjchdjihbd" corresponde a "79927398713"
    assert validate("hjjchdjihbd", alphabet="abcdefghij") == "hjjchdjihbd"


def test_r3_alfabeto_de_letras_equivalente_a_checksum_invalido():
    # "hjjchdjihba" corresponde a "79927398710"
    with pytest.raises(InvalidChecksum):
        validate("hjjchdjihba", alphabet="abcdefghij")


def test_r3_base_2_valida_com_numero_par_de_uns():
    # n = 2: '1' em posição ímpar soma 1; em posição par: 2 -> 2//2 + 2%2 = 1
    assert validate("11", alphabet="01") == "11"
    assert validate("0110", alphabet="01") == "0110"
    assert validate("101", alphabet="01") == "101"


@pytest.mark.parametrize("numero", ["1", "10", "0111", "111"])
def test_r3_base_2_invalida_com_numero_impar_de_uns(numero):
    with pytest.raises(InvalidChecksum):
        validate(numero, alphabet="01")


def test_r3_mesma_string_depende_de_n():
    # "18" em base 10: soma 10 -> válido; em base 16: soma 10 -> não é múltipla de 16
    assert validate("18") == "18"
    with pytest.raises(InvalidChecksum):
        validate("18", alphabet=HEX)


# ---------------------------------------------------------------------------
# R4: soma não múltipla de n levanta InvalidChecksum
# ---------------------------------------------------------------------------

def test_r4_exemplo_da_especificacao_levanta_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate("79927398710")


@pytest.mark.parametrize("digito_verificador", list("0124567890".replace("3", "")))
def test_r4_digito_verificador_errado_levanta_invalid_checksum(digito_verificador):
    with pytest.raises(InvalidChecksum):
        validate("7992739871" + digito_verificador)


def test_r4_invalid_checksum_e_capturavel_como_validation_error_e_value_error():
    with pytest.raises(ValidationError):
        validate("79927398710")
    with pytest.raises(ValueError):
        validate("79927398710")


def test_r4_checksum_invalido_nao_e_invalid_format():
    with pytest.raises(ValidationError) as exc_info:
        validate("79927398710")
    assert isinstance(exc_info.value, InvalidChecksum)
    assert not isinstance(exc_info.value, InvalidFormat)


def test_r4_inteiro_com_checksum_invalido():
    with pytest.raises(InvalidChecksum):
        validate(79927398710)


# ---------------------------------------------------------------------------
# R5: número válido é retornado sem alteração e com o mesmo tipo
# ---------------------------------------------------------------------------

def test_r5_string_valida_retorna_a_propria_string():
    resultado = validate("79927398713")
    assert resultado == "79927398713"
    assert type(resultado) is str


def test_r5_inteiro_valido_retorna_inteiro():
    resultado = validate(79927398713)
    assert resultado == 79927398713
    assert type(resultado) is int


def test_r5_inteiro_pequeno_valido_retorna_inteiro():
    resultado = validate(18)
    assert resultado == 18
    assert type(resultado) is int


def test_r5_zeros_a_esquerda_sao_preservados_no_retorno():
    assert validate("0018") == "0018"


def test_r5_alfabeto_padrao_explicito_equivale_ao_padrao():
    assert validate("79927398713", alphabet="0123456789") == "79927398713"


def test_r5_retorno_sem_alteracao_em_outra_base():
    resultado = validate("1a2b1", alphabet=HEX)
    assert resultado == "1a2b1"
    assert type(resultado) is str


# ---------------------------------------------------------------------------
# R6: outras bases via alphabet; diferencia maiúsculas de minúsculas
# ---------------------------------------------------------------------------

def test_r6_exemplo_hexadecimal_da_especificacao_e_valido():
    # n = 16: 1 + (b=11 -> 22 -> 1 + 6 = 7) + 2 + (a=10 -> 20 -> 1 + 4 = 5) + 1 = 16
    assert validate("1a2b1", alphabet=HEX) == "1a2b1"


def test_r6_hexadecimal_com_checksum_invalido():
    # Soma = 17 -> não é múltipla de 16
    with pytest.raises(InvalidChecksum):
        validate("1a2b2", alphabet=HEX)


def test_r6_hexadecimal_reducao_com_n_16():
    # "8f": f=15 + (8 -> 16 -> 1 + 0 = 1) = 16 -> válido
    # "f1": 1 + (f=15 -> 30 -> 1 + 14 = 15) = 16 -> válido
    assert validate("8f", alphabet=HEX) == "8f"
    assert validate("f1", alphabet=HEX) == "f1"


def test_r6_hexadecimal_digito_unico_f_e_invalido():
    with pytest.raises(InvalidChecksum):
        validate("f", alphabet=HEX)


def test_r6_maiusculas_nao_estao_no_alfabeto_minusculo():
    with pytest.raises(InvalidFormat):
        validate("1A2B1", alphabet=HEX)


def test_r6_minusculas_nao_estao_no_alfabeto_maiusculo():
    with pytest.raises(InvalidFormat):
        validate("1a2b1", alphabet=HEX_UPPER)


def test_r6_alfabeto_maiusculo_aceita_maiusculas():
    assert validate("1A2B1", alphabet=HEX_UPPER) == "1A2B1"


def test_r6_mistura_de_maiusculas_e_minusculas_levanta_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("1a2B1", alphabet=HEX)


def test_r6_letras_hexadecimais_invalidas_no_alfabeto_padrao():
    with pytest.raises(InvalidFormat):
        validate("1a2b1")
