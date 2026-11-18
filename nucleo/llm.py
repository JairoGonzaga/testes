"""Cliente único para OpenAI, Anthropic, "arquivo" (copiar e colar) ou "fake" (sem IA).

Provedor "arquivo": em vez de chamar uma API, grava cada prompt em
respostas_manuais/<execução>/prompt_<n>.txt e espera a resposta em resposta_<n>.txt.
Serve para quem não tem chave de API (cola o prompt no chat da IA e salva a resposta) ou
para usar outro agente como modelo. Rode o gerar.py de novo depois de salvar as respostas:
as respostas já salvas são reaproveitadas, então a execução é reproduzida igual.

Cada chamada devolve o texto e registra tokens de entrada/saída e tempo, que vão para o
log da execução (QP4 — custo).
"""

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

from . import config


class RespostaPendente(Exception):
    """Provedor "arquivo": o prompt foi gravado e a resposta ainda não foi colada."""


@dataclass
class Resposta:
    texto: str
    tokens_entrada: int
    tokens_saida: int
    tempo_s: float


class ClienteLLM:
    def __init__(self, provedor=None, modelo=None, temperatura=None):
        self.provedor = (provedor or config.PROVEDOR).lower()
        self.modelo = modelo or config.MODELO
        self.temperatura = config.TEMPERATURA if temperatura is None else temperatura
        if self.provedor == "openai":
            from openai import OpenAI  # precisa de OPENAI_API_KEY
            self._cliente = OpenAI(timeout=config.TIMEOUT_CHAMADA_S, max_retries=3)
        elif self.provedor == "anthropic":
            import anthropic  # precisa de ANTHROPIC_API_KEY
            self._cliente = anthropic.Anthropic(timeout=config.TIMEOUT_CHAMADA_S, max_retries=3)
        elif self.provedor == "arquivo":
            self._pasta = Path(os.getenv("PASTA_RESPOSTAS", str(config.RAIZ / "respostas_manuais")))
            self.modelo = self.modelo or "manual"
        elif self.provedor == "fake":
            from .fake import ProvedorFake
            self._cliente = ProvedorFake()
            self.modelo = self.modelo or "fake"
        else:
            raise SystemExit(f"PROVEDOR desconhecido: {self.provedor!r} (use openai, anthropic, arquivo ou fake)")
        if not self.modelo:
            raise SystemExit("Defina MODELO no arquivo .env (ex.: MODELO=gpt-5-mini ou MODELO=claude-haiku-4-5).")

    def conversar(self, sistema: str, mensagens: list, contexto: dict = None) -> Resposta:
        """mensagens: lista de {"role": "user"|"assistant", "content": str}."""
        inicio = time.perf_counter()
        if self.provedor == "openai":
            kwargs = {"model": self.modelo,
                      "messages": [{"role": "system", "content": sistema}] + mensagens}
            if self.temperatura is not None:
                kwargs["temperature"] = self.temperatura
            r = self._cliente.chat.completions.create(**kwargs)
            texto = r.choices[0].message.content or ""
            entrada, saida = r.usage.prompt_tokens, r.usage.completion_tokens
        elif self.provedor == "anthropic":
            kwargs = {"model": self.modelo, "max_tokens": config.MAX_TOKENS_RESPOSTA,
                      "system": sistema, "messages": mensagens}
            if self.temperatura is not None:
                # versões recentes do SDK não têm mais o parâmetro; modelos novos podem recusá-lo
                kwargs["extra_body"] = {"temperature": self.temperatura}
            r = self._cliente.messages.create(**kwargs)
            texto = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
            entrada, saida = r.usage.input_tokens, r.usage.output_tokens
        elif self.provedor == "arquivo":
            return self._arquivo(sistema, mensagens, contexto or {})
        else:
            texto = self._cliente.responder(sistema, mensagens, contexto or {})
            entrada = (len(sistema) + sum(len(m["content"]) for m in mensagens)) // 4
            saida = len(texto) // 4
        return Resposta(texto, entrada, saida, time.perf_counter() - inicio)

    def _arquivo(self, sistema, mensagens, ctx) -> Resposta:
        run_id = f"{ctx['funcao'].nome}__{ctx['condicao']}__r{ctx['repeticao']}"
        n = sum(1 for m in mensagens if m["role"] == "user")
        pasta = self._pasta / run_id
        resposta = pasta / f"resposta_{n}.txt"
        if not resposta.exists():
            pasta.mkdir(parents=True, exist_ok=True)
            partes = [f"=== SISTEMA ===\n{sistema}"]
            for i, m in enumerate(mensagens):
                papel = "USUÁRIO" if m["role"] == "user" else "ASSISTENTE"
                partes.append(f"=== {papel} ===\n{m['content']}")
            (pasta / f"prompt_{n}.txt").write_text("\n\n".join(partes) + "\n", encoding="utf-8")
            raise RespostaPendente(str(pasta / f"prompt_{n}.txt"))
        texto = resposta.read_text(encoding="utf-8")
        info_arq = pasta / f"resposta_{n}.json"   # opcional: tokens e tempo medidos fora
        info = json.loads(info_arq.read_text(encoding="utf-8")) if info_arq.exists() else {}
        entrada = info.get("tokens_entrada", (len(sistema) + sum(len(m["content"]) for m in mensagens)) // 4)
        return Resposta(texto, entrada, info.get("tokens_saida", len(texto) // 4), info.get("tempo_s", 0.0))
