"""Gerador simples de mutantes (no estilo do mutmut), baseado na AST do Python.

Cada mutante é uma cópia da versão de referência com UMA alteração:
  - comparações: <  <=  >  >=  ==  !=  in  not in  is  is not (troca pelo vizinho);
  - aritmética: + ↔ -, * → /, / → *, // → /, % → //, ** → *;
  - lógica: and ↔ or, remoção de `not`, True ↔ False;
  - constantes: inteiro n → n + 1, string "s" → "XXsXX".
Docstrings e definições de classes de exceção não são mutadas.

Por que não usar o mutmut direto? O mutmut 3 exige uma estrutura de projeto própria e
roda a suíte inteira por mutante; aqui precisamos rodar 30+ arquivos de teste diferentes
contra o MESMO conjunto fixo de mutantes. Os operadores são os mesmos de uso comum.
"""

import ast
import json
from pathlib import Path

_TROCA_CMP = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
              ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.In: ast.NotIn, ast.NotIn: ast.In,
              ast.Is: ast.IsNot, ast.IsNot: ast.Is}
_TROCA_BIN = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Div, ast.Div: ast.Mult,
              ast.FloorDiv: ast.Div, ast.Mod: ast.FloorDiv, ast.Pow: ast.Mult}
_SIMBOLO = {ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=", ast.Eq: "==", ast.NotEq: "!=",
            ast.In: "in", ast.NotIn: "not in", ast.Is: "is", ast.IsNot: "is not", ast.Add: "+",
            ast.Sub: "-", ast.Mult: "*", ast.Div: "/", ast.FloorDiv: "//", ast.Mod: "%",
            ast.Pow: "**", ast.And: "and", ast.Or: "or"}


def _docstrings(arvore):
    ids = set()
    for no in ast.walk(arvore):
        if isinstance(no, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            corpo = no.body
            if corpo and isinstance(corpo[0], ast.Expr) and isinstance(corpo[0].value, ast.Constant) \
                    and isinstance(corpo[0].value.value, str):
                ids.add(id(corpo[0].value))
    return ids


class _Mutador(ast.NodeTransformer):
    def __init__(self, alvo=None, ignorar=()):
        self.alvo = alvo
        self.ignorar = set(ignorar)
        self.pontos = []

    def _ponto(self, no, descricao):
        indice = len(self.pontos)
        self.pontos.append({"linha": getattr(no, "lineno", None), "descricao": descricao})
        return indice == self.alvo

    def visit_ClassDef(self, no):
        return no  # não muta classes (exceções)

    def visit_JoinedStr(self, no):
        return no  # não muta f-strings

    def visit_Compare(self, no):
        self.generic_visit(no)
        for i, op in enumerate(no.ops):
            novo = _TROCA_CMP.get(type(op))
            if novo and self._ponto(no, f"{_SIMBOLO[type(op)]} → {_SIMBOLO[novo]}"):
                no.ops[i] = novo()
                return no
        return no

    def _binop(self, no):
        self.generic_visit(no)
        novo = _TROCA_BIN.get(type(no.op))
        if novo and self._ponto(no, f"{_SIMBOLO[type(no.op)]} → {_SIMBOLO[novo]}"):
            no.op = novo()
        return no

    visit_BinOp = _binop
    visit_AugAssign = _binop

    def visit_BoolOp(self, no):
        self.generic_visit(no)
        novo = ast.Or if isinstance(no.op, ast.And) else ast.And
        if self._ponto(no, f"{_SIMBOLO[type(no.op)]} → {_SIMBOLO[novo]}"):
            no.op = novo()
        return no

    def visit_UnaryOp(self, no):
        self.generic_visit(no)
        if isinstance(no.op, ast.Not) and self._ponto(no, "remove not"):
            return no.operand
        return no

    def visit_Constant(self, no):
        if id(no) in self.ignorar:
            return no
        v = no.value
        if isinstance(v, bool):
            if self._ponto(no, f"{v} → {not v}"):
                return ast.copy_location(ast.Constant(not v), no)
        elif isinstance(v, int):
            if self._ponto(no, f"{v} → {v + 1}"):
                return ast.copy_location(ast.Constant(v + 1), no)
        elif isinstance(v, str):
            if self._ponto(no, f"{v!r} → {'XX' + v + 'XX'!r}"):
                return ast.copy_location(ast.Constant("XX" + v + "XX"), no)
        return no


def listar_pontos(fonte: str) -> list:
    arvore = ast.parse(fonte)
    m = _Mutador(ignorar=_docstrings(arvore))
    m.visit(arvore)
    return m.pontos


def gerar_mutante(fonte: str, indice: int) -> str:
    arvore = ast.parse(fonte)
    m = _Mutador(alvo=indice, ignorar=_docstrings(arvore))
    arvore = m.visit(arvore)
    ast.fix_missing_locations(arvore)
    return ast.unparse(arvore) + "\n"


def gerar_todos(arquivo_referencia: Path, pasta_saida: Path) -> list:
    fonte = arquivo_referencia.read_text(encoding="utf-8")
    pontos = listar_pontos(fonte)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    for antigo in pasta_saida.glob("m*.py"):
        antigo.unlink()
    original_normalizado = ast.unparse(ast.parse(fonte))
    indice, vistos = {}, set()
    for i, ponto in enumerate(pontos):
        codigo = gerar_mutante(fonte, i)
        if codigo.strip() == original_normalizado.strip() or codigo in vistos:
            continue  # mutação sem efeito sintático ou duplicada
        try:
            compile(codigo, "mutante", "exec")
        except SyntaxError:
            continue
        vistos.add(codigo)
        nome = f"m{len(indice) + 1:03d}"
        cab = f"# MUTANTE {nome} — linha {ponto['linha']} da referência: {ponto['descricao']}\n"
        (pasta_saida / f"{nome}.py").write_text(cab + codigo, encoding="utf-8")
        indice[nome] = ponto
    (pasta_saida / "indice.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1),
                                             encoding="utf-8")
    return list(indice)
