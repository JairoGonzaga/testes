"""Plano de casos (condição B): leitura, validação e geração de testes por template.

Formato de um caso (o mesmo usado nos casos do gabarito):

    {"id": "C1", "regra": "R2", "tipo": "fronteira", "descricao": "...",
     "entrada": {"args": [1024], "kwargs": {"binary": true}},
     "esperado": {"retorno": "1.0 KiB"}}            # ou {"excecao": "ValueError"}

Valores que JSON não representa podem vir como {"$expr": "float('inf')"}.
"""

import ast
import builtins
import inspect
import json
import math
import re

TIPOS = {"normal", "fronteira", "invalida"}
FUNCOES_PERMITIDAS = ("float", "int", "str", "bytes", "list", "tuple", "set", "dict",
                      "frozenset", "bool", "complex")
EXCECOES_EMBUTIDAS = {nome for nome, obj in vars(builtins).items()
                      if isinstance(obj, type) and issubclass(obj, BaseException)}

_NOS_PERMITIDOS = (ast.Expression, ast.Constant, ast.UnaryOp, ast.BinOp, ast.List, ast.Tuple,
                   ast.Set, ast.Dict, ast.Load, ast.Call, ast.Name, ast.keyword,
                   ast.UAdd, ast.USub, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
                   ast.Mod, ast.Pow)


class PlanoInvalido(ValueError):
    pass


# ---------------------------------------------------------------------------------
# Valores
# ---------------------------------------------------------------------------------
def validar_expr(expr: str) -> None:
    """Aceita só literais, operações aritméticas e chamadas a float/int/str/... ."""
    try:
        arvore = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise PlanoInvalido(f"$expr com erro de sintaxe: {expr!r}") from e
    for no in ast.walk(arvore):
        if not isinstance(no, _NOS_PERMITIDOS):
            raise PlanoInvalido(f"$expr com construção não permitida ({type(no).__name__}): {expr!r}")
        if isinstance(no, ast.Name) and no.id not in FUNCOES_PERMITIDAS:
            raise PlanoInvalido(f"$expr usa nome não permitido ({no.id}): {expr!r}")
        if isinstance(no, ast.Call) and not (isinstance(no.func, ast.Name) and no.func.id in FUNCOES_PERMITIDAS):
            raise PlanoInvalido(f"$expr chama função não permitida: {expr!r}")
        if isinstance(no, ast.BinOp) and isinstance(no.op, ast.Pow):
            exp = no.right
            if not (isinstance(exp, ast.Constant) and isinstance(exp.value, int) and abs(exp.value) <= 400):
                raise PlanoInvalido(f"$expr com expoente muito grande ou não constante: {expr!r}")


def para_codigo(valor) -> str:
    """Converte um valor do plano (JSON) em código-fonte Python."""
    if isinstance(valor, dict) and set(valor) == {"$expr"}:
        expr = str(valor["$expr"])
        validar_expr(expr)
        return expr
    if isinstance(valor, dict):
        return "{" + ", ".join(f"{para_codigo(k)}: {para_codigo(v)}" for k, v in valor.items()) + "}"
    if isinstance(valor, list):
        return "[" + ", ".join(para_codigo(v) for v in valor) + "]"
    if isinstance(valor, float) and not math.isfinite(valor):
        return f"float({str(valor)!r})"
    if valor is None or isinstance(valor, (bool, int, float, str)):
        return repr(valor)
    raise PlanoInvalido(f"valor não suportado: {valor!r}")


def para_python(valor):
    codigo = para_codigo(valor)
    ambiente = {"__builtins__": {n: getattr(builtins, n) for n in FUNCOES_PERMITIDAS}}
    return eval(codigo, ambiente)


def assinatura_inspect(assinatura: str) -> inspect.Signature:
    nome = re.match(r"\s*def\s+(\w+)", assinatura).group(1)
    fonte = "from __future__ import annotations\n" + assinatura.rstrip().rstrip(":") + ":\n    pass\n"
    ns = {}
    exec(fonte, ns)
    return inspect.signature(ns[nome])


# ---------------------------------------------------------------------------------
# Leitura e validação do plano
# ---------------------------------------------------------------------------------
def extrair_json(texto: str):
    texto = texto.strip()
    candidatos = [texto]
    bloco = re.search(r"```(?:json)?\s*\n(.*?)```", texto, flags=re.S)
    if bloco:
        candidatos.append(bloco.group(1))
    if "{" in texto and "}" in texto:
        candidatos.append(texto[texto.index("{"): texto.rindex("}") + 1])
    for c in candidatos:
        try:
            return json.loads(c)
        except json.JSONDecodeError:
            continue
    raise PlanoInvalido("a resposta não contém um JSON válido")


def validar_plano(dados, funcao):
    """Devolve (casos_validos, erros). `erros` lista problemas para o pedido de reparo."""
    erros = []
    if isinstance(dados, list):
        dados = {"casos": dados}
    if not isinstance(dados, dict) or not isinstance(dados.get("casos"), list):
        return [], ['o JSON precisa ter a forma {"casos": [ ... ]}']
    if not dados["casos"]:
        return [], ["a lista de casos está vazia"]

    ids_regras = set(funcao.ids_regras)
    excecoes_ok = EXCECOES_EMBUTIDAS | set(funcao.excecoes)
    sig = assinatura_inspect(funcao.assinatura)
    validos, ids_usados = [], set()

    for i, caso in enumerate(dados["casos"], start=1):
        if not isinstance(caso, dict):
            erros.append(f"item {i}: cada caso precisa ser um objeto JSON")
            continue
        problemas = []
        cid = str(caso.get("id") or f"C{i}")
        if cid in ids_usados:
            cid = f"{cid}_{i}"
        ids_usados.add(cid)

        regra = caso.get("regra")
        if regra not in ids_regras:
            problemas.append(f"regra {regra!r} não existe (use uma de {', '.join(sorted(ids_regras))})")
        tipo = caso.get("tipo", "normal")
        if tipo not in TIPOS:
            tipo = "normal"

        entrada = caso.get("entrada", {})
        if not isinstance(entrada, dict):
            problemas.append("'entrada' precisa ser um objeto com 'args' e 'kwargs'")
            entrada = {}
        args = entrada.get("args", [])
        kwargs = entrada.get("kwargs", {}) or {}
        if not isinstance(args, list):
            problemas.append("'entrada.args' precisa ser uma lista")
            args = []
        if not isinstance(kwargs, dict):
            problemas.append("'entrada.kwargs' precisa ser um objeto")
            kwargs = {}
        try:
            args_py = [para_python(a) for a in args]
            kwargs_py = {k: para_python(v) for k, v in kwargs.items()}
            sig.bind(*args_py, **kwargs_py)
        except PlanoInvalido as e:
            problemas.append(str(e))
        except TypeError as e:
            problemas.append(f"argumentos incompatíveis com a assinatura ({e})")
        except Exception as e:  # noqa: BLE001
            problemas.append(f"valor de entrada inválido ({type(e).__name__}: {e})")

        esperado = caso.get("esperado")
        if not isinstance(esperado, dict) or len({"retorno", "excecao"} & set(esperado)) != 1:
            problemas.append("'esperado' precisa ter exatamente uma chave: 'retorno' ou 'excecao'")
        elif "excecao" in esperado:
            if esperado["excecao"] not in excecoes_ok:
                problemas.append(f"exceção {esperado['excecao']!r} não disponível")
        else:
            try:
                para_codigo(esperado["retorno"])
            except PlanoInvalido as e:
                problemas.append(str(e))

        if problemas:
            erros.append(f"caso {cid}: " + "; ".join(problemas))
        else:
            validos.append({"id": cid, "regra": regra, "tipo": tipo,
                            "descricao": str(caso.get("descricao", "")),
                            "entrada": {"args": args, "kwargs": kwargs}, "esperado": esperado})
    return validos, erros


# ---------------------------------------------------------------------------------
# Template
# ---------------------------------------------------------------------------------
def _nome_teste(caso, usados):
    base = re.sub(r"\W+", "_", f"test_{caso['id']}_{caso['regra']}".lower()).strip("_")
    nome, k = base, 2
    while nome in usados:
        nome, k = f"{base}_{k}", k + 1
    usados.add(nome)
    return nome


def renderizar_testes(casos, funcao, cabecalho="Testes gerados a partir de um plano de casos.") -> str:
    linhas = [f'"""{cabecalho}"""', "", "import math", "", "import pytest", "",
              funcao.linha_importacao, "", ""]
    usados = set()
    for caso in casos:
        args = [para_codigo(a) for a in caso["entrada"].get("args", [])]
        kwargs = [f"{k}={para_codigo(v)}" for k, v in (caso["entrada"].get("kwargs") or {}).items()]
        chamada = f"{funcao.nome_funcao}({', '.join(args + kwargs)})"
        descricao = " ".join(str(caso.get("descricao", "")).split())[:200]
        linhas.append(f"def {_nome_teste(caso, usados)}():")
        linhas.append(f"    # [{caso['regra']}/{caso.get('tipo', 'normal')}] {descricao}".rstrip())
        esperado = caso["esperado"]
        if "excecao" in esperado:
            linhas.append(f"    with pytest.raises({esperado['excecao']}):")
            linhas.append(f"        {chamada}")
        else:
            valor = esperado["retorno"]
            if isinstance(valor, float) and math.isnan(valor):
                linhas.append(f"    assert math.isnan({chamada})")
            elif isinstance(valor, float):
                linhas.append(f"    assert {chamada} == pytest.approx({para_codigo(valor)})")
            else:
                linhas.append(f"    assert {chamada} == {para_codigo(valor)}")
        linhas += ["", ""]
    return "\n".join(linhas).rstrip() + "\n"
