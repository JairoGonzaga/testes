"""
Testes unitários para alvo.validate (CPF).

Todos os casos se baseiam apenas nas regras de negócio R1 a R7.
Cada teste traz no nome a regra que verifica.
"""

import random

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


# ---------------------------------------------------------------------------
# Auxiliares
# ---------------------------------------------------------------------------

def _calcular_dv(base9):
    """Oráculo: implementa literalmente a fórmula da R4 para os 9 primeiros dígitos."""
    n = [int(c) for c in base9]
    d1 = (11 - sum((10 - i) * n[i] for i in range(9))) % 11 % 10
    d2 = (11 - (sum((11 - i) * n[i] for i in range(9)) + 2 * d1)) % 11 % 10
    return f"{d1}{d2}"


def _formatar(cpf11):
    return f"{cpf11[:3]}.{cpf11[3:6]}.{cpf11[6:9]}-{cpf11[9:]}"


def _assert_invalid_format_e_nao_invalid_length(valor):
    """R2/R5: o erro precisa ser InvalidFormat e não a subclasse InvalidLength (R3)."""
    with pytest.raises(InvalidFormat) as excinfo:
        validate(valor)
    assert not isinstance(excinfo.value, InvalidLength)
    assert not isinstance(excinfo.value, InvalidChecksum)


def _bases_aleatorias(qtd=40, semente=20240501):
    rng = random.Random(semente)
    bases = []
    while len(bases) < qtd:
        base = "".join(rng.choice("0123456789") for _ in range(9))
        if base != "000000000":  # evita o número zero (R2)
            bases.append(base)
    return bases


# CPFs válidos (forma compacta), com os dígitos verificadores calculados à mão pela R4.
CPFS_VALIDOS = [
    "39053344705",  # exemplo das regras; d1: (11 - S1) mod 11 = 10 -> 0
    "11111111111",  # exemplo da R7
    "12345678909",
    "52998224725",
    "23100299981",  # forma correta do exemplo inválido 231.002.999-00
    "00000000191",  # zeros à esquerda
    "00000102008",  # zeros à esquerda; d1: (11 - S1) mod 11 = 0
    "52998224806",  # d1: (11 - S1) mod 11 = 0
    "52998224130",  # d2: (11 - S2) mod 11 = 10 -> 0
    "52998224210",  # d2: (11 - S2) mod 11 = 0
    "52998224300",  # d1 e d2: ambos 10 -> 0
    "52998224059",
]


def _variacoes_com_dv_errado():
    """Para cada CPF válido, troca só o 10º ou só o 11º dígito por qualquer outro valor."""
    casos = []
    for cpf in CPFS_VALIDOS:
        for d in "0123456789":
            if d != cpf[10]:
                casos.append(cpf[:10] + d)            # 11º dígito (d2) errado
            if d != cpf[9]:
                casos.append(cpf[:9] + d + cpf[10])   # 10º dígito (d1) errado
    return casos


# ---------------------------------------------------------------------------
# R1 — compactação (remove espaços, hífens e pontos; espaços em branco nas pontas)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "entrada",
    [
        "390.533.447-05",             # exemplo das regras
        "39053344705",                # já compacto
        " 39053344705 ",              # espaços nas pontas
        "390 533 447 05",             # espaços internos
        "390-533-447-05",             # só hífens
        "390.533.447.05",             # só pontos
        "3-9.0 5..3--3 4 4 7 0 5",    # separadores em qualquer posição e repetidos
        "-39053344705.",              # separadores nas pontas
        "\t390.533.447-05\n",         # tabulação/quebra de linha nas pontas
        "  390.533.447-05\r\n",       # espaços em branco variados nas pontas
    ],
)
def test_r1_compacta_separadores_e_espacos(entrada):
    assert validate(entrada) == "39053344705"


def test_r1_comprimento_considerado_apos_compactacao():
    # "390.533.447-05" tem 14 caracteres, mas 11 dígitos depois de compactado
    assert len("390.533.447-05") == 14
    assert validate("390.533.447-05") == "39053344705"


@pytest.mark.parametrize(
    "entrada",
    [
        "390,533,447-05",   # vírgula não é removida
        "390.533.447/05",   # barra não é removida
        "390_533_447_05",   # sublinhado não é removido
    ],
)
def test_r1_r2_outros_separadores_nao_sao_removidos(entrada):
    _assert_invalid_format_e_nao_invalid_length(entrada)


# ---------------------------------------------------------------------------
# R2 — formato: só dígitos 0-9, não vazio, diferente de zero; não strings
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "entrada",
    [
        "390.533.447=0",    # exemplo das regras
        "3905334470a",
        "A9053344705",
        "390533447O5",      # letra O no lugar de zero
        "+39053344705",
        "390.533.447-0#",
        "39053344705x",
        "3905334470 5x",
    ],
)
def test_r2_caractere_nao_digito_levanta_invalid_format(entrada):
    _assert_invalid_format_e_nao_invalid_length(entrada)


@pytest.mark.parametrize(
    "entrada",
    [
        "",
        " ",
        "   ",
        ".",
        "-",
        "...---   ",
        "\t\n",
    ],
)
def test_r2_vazio_apos_compactacao_levanta_invalid_format(entrada):
    _assert_invalid_format_e_nao_invalid_length(entrada)


@pytest.mark.parametrize(
    "entrada",
    [
        "00000000000",       # 11 zeros (os dígitos verificadores até conferiam, mas é zero)
        "000.000.000-00",
        " 00000000000 ",
        "0",
        "00",
        "0-0.0",
        "0000000000",        # 10 zeros
        "000000000000",      # 12 zeros
    ],
)
def test_r2_numero_igual_a_zero_levanta_invalid_format(entrada):
    _assert_invalid_format_e_nao_invalid_length(entrada)


@pytest.mark.parametrize(
    "entrada",
    [
        None,
        39053344705,
        39053344705.0,
        b"39053344705",
    ],
)
def test_r2_valor_que_nao_e_string_levanta_invalid_format(entrada):
    _assert_invalid_format_e_nao_invalid_length(entrada)


def test_r2_invalid_format_e_validation_error_e_value_error():
    with pytest.raises(ValueError) as excinfo:
        validate("390.533.447=0")
    assert isinstance(excinfo.value, InvalidFormat)
    assert isinstance(excinfo.value, ValidationError)


# ---------------------------------------------------------------------------
# R3 — comprimento: exatamente 11 dígitos
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "entrada",
    [
        "3905334470",         # 10 dígitos (fronteira inferior)
        "390533447050",       # 12 dígitos (fronteira superior; os 11 primeiros são válidos)
        "390.533.447-0",      # 10 dígitos formatado
        "390.533.447-051",    # 12 dígitos formatado
        "  3905334470  ",     # 10 dígitos com espaços nas pontas
        "390533447",          # 9 dígitos
        "1",                  # 1 dígito
        "0000000191",         # 10 dígitos com zeros à esquerda (sem preenchimento)
        "039053344705",       # 12 dígitos com zero à esquerda
        "123456789091234",    # 15 dígitos
    ],
)
def test_r3_comprimento_diferente_de_11_levanta_invalid_length(entrada):
    with pytest.raises(InvalidLength):
        validate(entrada)


def test_r3_invalid_length_e_invalid_format_validation_error_e_value_error():
    with pytest.raises(InvalidLength) as excinfo:
        validate("3905334470")
    assert isinstance(excinfo.value, InvalidFormat)
    assert isinstance(excinfo.value, ValidationError)
    assert isinstance(excinfo.value, ValueError)


# ---------------------------------------------------------------------------
# R4 — dígitos verificadores
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("cpf", CPFS_VALIDOS)
def test_r4_cpf_com_digitos_verificadores_corretos_e_aceito(cpf):
    assert validate(cpf) == cpf


@pytest.mark.parametrize("cpf", CPFS_VALIDOS)
def test_r4_cpf_valido_formatado_e_aceito(cpf):
    assert validate(_formatar(cpf)) == cpf


def test_r4_exemplo_das_regras_levanta_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate("231.002.999-00")


@pytest.mark.parametrize("cpf", _variacoes_com_dv_errado())
def test_r4_digito_verificador_errado_levanta_invalid_checksum(cpf):
    with pytest.raises(InvalidChecksum):
        validate(cpf)


@pytest.mark.parametrize(
    "entrada",
    [
        "390.533.447-04",   # d2 errado, formatado
        "390.533.447-15",   # d1 errado, formatado
        "39053344750",      # verificadores trocados de posição
        "12345678990",      # verificadores trocados de posição
        "39053344605",      # dígito do corpo alterado
        "93053344705",      # dígitos do corpo transpostos
    ],
)
def test_r4_alteracoes_no_numero_levantam_invalid_checksum(entrada):
    with pytest.raises(InvalidChecksum):
        validate(entrada)


def test_r4_resto_10_vira_digito_0():
    # d1 = (11 - 221) mod 11 = 10 -> mod 10 = 0
    assert validate("39053344705") == "39053344705"
    # d1 e d2 caem os dois no caso 10 -> 0
    assert validate("52998224300") == "52998224300"
    # d2 com resto 10 -> 0
    assert validate("52998224130") == "52998224130"


def test_r4_resto_10_nao_aceita_digito_1():
    # se 10 virasse 1 em vez de 0, esses números passariam
    with pytest.raises(InvalidChecksum):
        validate("39053344715")
    with pytest.raises(InvalidChecksum):
        validate("52998224311")
    with pytest.raises(InvalidChecksum):
        validate("52998224131")


@pytest.mark.parametrize("base", _bases_aleatorias())
def test_r4_formula_dos_verificadores_para_bases_diversas(base):
    dv = _calcular_dv(base)
    cpf = base + dv
    assert validate(cpf) == cpf
    assert validate(_formatar(cpf)) == cpf

    d1_errado = str((int(dv[0]) + 1) % 10)
    d2_errado = str((int(dv[1]) + 1) % 10)
    with pytest.raises(InvalidChecksum):
        validate(base + d1_errado + dv[1])
    with pytest.raises(InvalidChecksum):
        validate(base + dv[0] + d2_errado)


def test_r4_invalid_checksum_e_validation_error_e_value_error():
    with pytest.raises(ValueError) as excinfo:
        validate("231.002.999-00")
    assert isinstance(excinfo.value, InvalidChecksum)
    assert isinstance(excinfo.value, ValidationError)


def test_r2_r3_r4_hierarquia_das_excecoes():
    assert issubclass(ValidationError, ValueError)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidLength, InvalidFormat)
    assert issubclass(InvalidChecksum, ValidationError)


# ---------------------------------------------------------------------------
# R5 — ordem das verificações: R2 -> R3 -> R4
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "entrada",
    [
        "12a",              # não dígito e comprimento errado -> R2 vence
        "3905334470X5",     # 12 caracteres com letra -> R2 vence
        "abc",
        "0000000000",       # zero com 10 dígitos -> R2 vence
        "000000000000",     # zero com 12 dígitos -> R2 vence
        "0",
        "",                 # vazio (comprimento 0) -> R2 vence
    ],
)
def test_r5_formato_verificado_antes_do_comprimento(entrada):
    _assert_invalid_format_e_nao_invalid_length(entrada)


@pytest.mark.parametrize(
    "entrada",
    [
        "231.002.999-0X",   # verificadores errados e caractere inválido -> R2 vence
        "231.002.999=00",
        "2310029990O",
    ],
)
def test_r5_formato_verificado_antes_do_checksum(entrada):
    with pytest.raises(InvalidFormat) as excinfo:
        validate(entrada)
    assert not isinstance(excinfo.value, InvalidChecksum)


@pytest.mark.parametrize(
    "entrada",
    [
        "2310029990",       # 10 dígitos
        "231002999000",     # 12 dígitos
        "231.002.999-0",
    ],
)
def test_r5_comprimento_verificado_antes_do_checksum(entrada):
    with pytest.raises(InvalidLength) as excinfo:
        validate(entrada)
    assert not isinstance(excinfo.value, InvalidChecksum)


# ---------------------------------------------------------------------------
# R6 — retorno: número compactado (11 dígitos, sem separadores)
# ---------------------------------------------------------------------------

def test_r6_exemplo_das_regras_retorna_compactado():
    assert validate("390.533.447-05") == "39053344705"


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        ("390.533.447-05", "39053344705"),
        (" 123.456.789-09 ", "12345678909"),
        ("529 982 247 25", "52998224725"),
        ("231-002-999-81", "23100299981"),
        ("000.000.001-91", "00000000191"),   # zeros à esquerda preservados
        ("000.001.020-08", "00000102008"),
    ],
)
def test_r6_retorna_string_compacta_de_11_digitos(entrada, esperado):
    resultado = validate(entrada)
    assert isinstance(resultado, str)
    assert resultado == esperado
    assert len(resultado) == 11
    assert all(c in "0123456789" for c in resultado)


@pytest.mark.parametrize("cpf", CPFS_VALIDOS)
def test_r6_resultado_validado_novamente_e_o_mesmo(cpf):
    resultado = validate(_formatar(cpf))
    assert validate(resultado) == resultado


# ---------------------------------------------------------------------------
# R7 — todos os dígitos iguais não recebem tratamento especial
# ---------------------------------------------------------------------------

def test_r7_exemplo_das_regras():
    assert validate("111.111.111-11") == "11111111111"


@pytest.mark.parametrize("digito", "123456789")
def test_r7_digitos_repetidos_com_verificadores_corretos_sao_validos(digito):
    # pela R4, n repetido 9 vezes gera d1 = d2 = n
    cpf = digito * 11
    assert validate(cpf) == cpf
    assert validate(_formatar(cpf)) == cpf


@pytest.mark.parametrize(
    "entrada",
    [
        "11111111112",
        "111.111.111-12",
        "22222222221",
        "55555555556",
        "99999999990",
    ],
)
def test_r7_digitos_repetidos_com_verificadores_errados_levantam_invalid_checksum(entrada):
    with pytest.raises(InvalidChecksum):
        validate(entrada)
