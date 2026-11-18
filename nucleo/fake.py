"""Provedor "fake": imita respostas de um modelo SEM chamar IA nenhuma.

Serve só para testar a tubulação (gerar → executar → revisar → analisar) sem gastar
crédito. Ele monta respostas a partir do gabarito, com falhas propositais:
  - descarta parte dos casos (cobertura incompleta);
  - na condição A, às vezes troca uma expectativa (oráculo errado) ou gera erro de sintaxe;
  - na condição B, às vezes manda um plano com regra inexistente (exercita o reparo).

NUNCA use resultados do provedor fake no relatório.
"""

import json
import random
from collections import defaultdict

from .plano import para_codigo


class ProvedorFake:
    def responder(self, sistema, mensagens, ctx):
        funcao = ctx["funcao"]
        rng = random.Random(f"{funcao.nome}-{ctx.get('condicao')}-{ctx.get('repeticao')}-{len(mensagens)}")
        casos = [dict(c, id=f"C{i}", descricao="caso do fake")
                 for i, c in enumerate(funcao.gabarito.get("casos", []), start=1)]
        casos = [c for c in casos if rng.random() < 0.75] or casos[:1]
        if ctx.get("condicao") == "B":
            if len(mensagens) == 1 and rng.random() < 0.3:
                casos[0] = dict(casos[0], regra="R99")  # força um pedido de reparo
            return json.dumps({"casos": casos}, ensure_ascii=False)
        return "```python\n" + self._arquivo_estilo_a(funcao, casos, rng) + "```"

    @staticmethod
    def _arquivo_estilo_a(funcao, casos, rng):
        if rng.random() < 0.1:
            return "import pytest\nfrom alvo import x\n\ndef test_quebrado(:\n    pass\n"
        retornos = [c for c in casos if "retorno" in c["esperado"]]
        if retornos and rng.random() < 0.7:
            alvo = rng.choice(retornos)
            alvo["esperado"] = {"retorno": str(alvo["esperado"]["retorno"]) + "?"}  # oráculo errado
        por_regra = defaultdict(lambda: {"ret": [], "exc": []})
        for c in casos:
            chave = "exc" if "excecao" in c["esperado"] else "ret"
            por_regra[c["regra"]][chave].append(c)
        linhas = ["import math", "import pytest", "", funcao.linha_importacao, "", ""]
        for regra, grupos in por_regra.items():
            r = regra.lower()
            if grupos["ret"]:
                params = ",\n    ".join(
                    f"({para_codigo(c['entrada'].get('args', []))}, {para_codigo(c['entrada'].get('kwargs', {}))}, "
                    f"{para_codigo(c['esperado']['retorno'])})" for c in grupos["ret"])
                linhas += [f'@pytest.mark.parametrize("args, kwargs, esperado", [\n    {params},\n])',
                           f"def test_{r}_retorno(args, kwargs, esperado):",
                           f"    assert {funcao.nome_funcao}(*args, **kwargs) == esperado", "", ""]
            if grupos["exc"]:
                params = ",\n    ".join(
                    f"({para_codigo(c['entrada'].get('args', []))}, {para_codigo(c['entrada'].get('kwargs', {}))}, "
                    f"{c['esperado']['excecao']})" for c in grupos["exc"])
                linhas += [f'@pytest.mark.parametrize("args, kwargs, excecao", [\n    {params},\n])',
                           f"def test_{r}_excecao(args, kwargs, excecao):",
                           "    with pytest.raises(excecao):",
                           f"        {funcao.nome_funcao}(*args, **kwargs)", "", ""]
        return "\n".join(linhas)
