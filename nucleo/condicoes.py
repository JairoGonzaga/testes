"""As duas condições do experimento.

A — geração direta: uma chamada; o modelo devolve o arquivo pytest.
B — agente: o modelo devolve um plano JSON; o programa valida o plano, gera os testes por
    template e confere se o pytest consegue carregá-los. Problemas TÉCNICOS (JSON inválido,
    regra inexistente, argumentos que não batem com a assinatura, exceção desconhecida,
    erro de coleta) voltam para o modelo como pedido de reparo, até MAX_CHAMADAS.

O agente NUNCA roda os testes na versão de referência: a checagem de coleta usa um "stub"
(função de mesma assinatura que só levanta NotImplementedError). Assim o plano continua
sendo feito só a partir das regras, sem ver o comportamento do código.
"""

import json
import re
import tempfile
import time
from pathlib import Path

from . import config, prompts
from .plano import PlanoInvalido, extrair_json, renderizar_testes, validar_plano
from .pytest_exec import rodar_pytest


class Registro:
    """Log de uma execução: conversa, chamadas, tokens e tempo (QP4)."""

    def __init__(self):
        self.inicio = time.perf_counter()
        self.conversa = []
        self.chamadas = 0
        self.tokens_entrada = 0
        self.tokens_saida = 0
        self.tempo_modelo_s = 0.0
        self.eventos = []

    def chamar(self, cliente, mensagens, contexto):
        resp = cliente.conversar(prompts.SISTEMA, mensagens, contexto)
        self.chamadas += 1
        self.tokens_entrada += resp.tokens_entrada
        self.tokens_saida += resp.tokens_saida
        self.tempo_modelo_s += resp.tempo_s
        self.conversa.append({"chamada": self.chamadas, "enviado": mensagens[-1]["content"],
                              "recebido": resp.texto, "tokens_entrada": resp.tokens_entrada,
                              "tokens_saida": resp.tokens_saida, "tempo_s": round(resp.tempo_s, 2)})
        return resp

    @property
    def tempo_total_s(self):
        return time.perf_counter() - self.inicio

    def resumo(self):
        return {"chamadas": self.chamadas, "tokens_entrada": self.tokens_entrada,
                "tokens_saida": self.tokens_saida, "tempo_modelo_s": round(self.tempo_modelo_s, 2),
                "tempo_total_s": round(self.tempo_total_s, 2)}


def extrair_codigo(texto: str) -> str:
    blocos = re.findall(r"```(?:python|py)?[ \t]*\n(.*?)```", texto, flags=re.S)
    if blocos:
        return max(blocos, key=len).strip() + "\n"
    return texto.strip() + "\n"


# ---------------------------------------------------------------------------------
# Condição A
# ---------------------------------------------------------------------------------
def condicao_a(funcao, cliente, pasta: Path, contexto: dict, reg: Registro) -> dict:
    mensagens = [{"role": "user", "content": prompts.prompt_direta(funcao)}]
    resp = reg.chamar(cliente, mensagens, contexto)
    codigo = extrair_codigo(resp.texto)
    (pasta / "test_gerado.py").write_text(codigo, encoding="utf-8")
    return {"status": "ok"}


# ---------------------------------------------------------------------------------
# Condição B
# ---------------------------------------------------------------------------------
def _stub(funcao) -> str:
    linhas = ["from __future__ import annotations", ""]
    linhas += [f"class {e}(Exception):\n    pass\n" for e in funcao.excecoes]
    linhas += [funcao.assinatura.rstrip().rstrip(":") + ":", "    raise NotImplementedError('stub')", ""]
    return "\n".join(linhas)


def checar_coleta(funcao, codigo: str):
    """Devolve None se o pytest consegue carregar o arquivo; senão, a mensagem de erro."""
    try:
        compile(codigo, "test_gerado.py", "exec")
    except SyntaxError as e:
        return f"SyntaxError: {e}"
    with tempfile.TemporaryDirectory() as tmp:
        teste, stub = Path(tmp) / "t.py", Path(tmp) / "stub.py"
        teste.write_text(codigo, encoding="utf-8")
        stub.write_text(_stub(funcao), encoding="utf-8")
        r = rodar_pytest(teste, stub, funcao.nome_funcao)
    if r["timeout"]:
        return "tempo esgotado ao carregar os testes"
    if r["erros_coleta"]:
        return r["erros_coleta"][0]["erro"]
    return None


def condicao_b(funcao, cliente, pasta: Path, contexto: dict, reg: Registro) -> dict:
    mensagens = [{"role": "user", "content": prompts.prompt_plano(funcao)}]
    tentativas, melhor, melhor_erros, final = [], [], [], None
    while reg.chamadas < config.MAX_CHAMADAS and reg.tempo_total_s < config.TEMPO_MAX_EXECUCAO_S:
        resp = reg.chamar(cliente, mensagens, contexto)
        mensagens.append({"role": "assistant", "content": resp.texto})
        try:
            validos, erros = validar_plano(extrair_json(resp.texto), funcao)
        except PlanoInvalido as e:
            validos, erros = [], [str(e)]
        if len(validos) >= len(melhor):
            melhor, melhor_erros = validos, erros
        reparo = None
        if not erros:
            erro_coleta = checar_coleta(funcao, renderizar_testes(validos, funcao))
            if erro_coleta is None:
                final = validos
                tentativas.append({"chamada": reg.chamadas, "casos_validos": len(validos), "erros": []})
                break
            erros = [f"erro de coleta: {erro_coleta[-300:]}"]
            reparo = prompts.prompt_reparo_coleta(erro_coleta)
        tentativas.append({"chamada": reg.chamadas, "casos_validos": len(validos), "erros": erros})
        if reg.chamadas < config.MAX_CHAMADAS:
            mensagens.append({"role": "user", "content": reparo or prompts.prompt_reparo_plano(erros)})

    descartados = 0
    if final is None and melhor:
        # acabaram as chamadas: fica com os casos válidos do melhor plano
        if checar_coleta(funcao, renderizar_testes(melhor, funcao)) is None:
            final = melhor
            descartados = len(melhor_erros)
    (pasta / "validacao_plano.json").write_text(json.dumps(tentativas, ensure_ascii=False, indent=1),
                                                encoding="utf-8")
    if final is None:
        return {"status": "falha", "erro": "nenhum plano válido dentro do limite de chamadas",
                "reparos": max(0, reg.chamadas - 1)}
    (pasta / "plano.json").write_text(json.dumps({"casos": final}, ensure_ascii=False, indent=1),
                                      encoding="utf-8")
    cabecalho = f"Testes gerados pela condição B (agente) para {funcao.nome}."
    (pasta / "test_gerado.py").write_text(renderizar_testes(final, funcao, cabecalho), encoding="utf-8")
    return {"status": "ok", "reparos": reg.chamadas - 1, "casos_plano": len(final),
            "casos_descartados": descartados}
