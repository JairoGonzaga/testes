"""Configuração do experimento.

Tudo o que precisa ficar CONGELADO depois do piloto está aqui. Os valores podem vir de
variáveis de ambiente ou do arquivo `.env` na raiz do projeto (veja `.env.exemplo`).
"""

import os
import sys
from pathlib import Path

for _fluxo in (sys.stdout, sys.stderr):  # evita erro de acentuação no terminal do Windows
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

RAIZ = Path(__file__).resolve().parent.parent


def _carregar_env():
    """Lê o arquivo .env (formato CHAVE=valor) sem precisar de biblioteca extra."""
    arquivo = RAIZ / ".env"
    if not arquivo.exists():
        return
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        valor = valor.split(" #", 1)[0].strip().strip('"').strip("'")
        if valor:
            os.environ.setdefault(chave.strip(), valor)


_carregar_env()

# --- Modelo -----------------------------------------------------------------------
# PROVEDOR: "openai", "anthropic" ou "fake" (o fake não chama IA nenhuma: serve só
# para testar a tubulação sem gastar crédito).
PROVEDOR = os.getenv("PROVEDOR", "fake").lower()
MODELO = os.getenv("MODELO", "")
# None = usa o padrão do provedor. Alguns modelos (de raciocínio) não aceitam temperatura.
TEMPERATURA = float(os.environ["TEMPERATURA"]) if os.getenv("TEMPERATURA") else None
MAX_TOKENS_RESPOSTA = int(os.getenv("MAX_TOKENS_RESPOSTA", "8000"))
TIMEOUT_CHAMADA_S = int(os.getenv("TIMEOUT_CHAMADA_S", "180"))

# --- Limites iguais para as duas condições (metodologia) ---------------------------
MAX_CHAMADAS = 3              # chamadas ao modelo por execução
TEMPO_MAX_EXECUCAO_S = 600    # tempo máximo de geração por execução
REPETICOES = 3                # repetições por função × condição

# --- Execução dos testes -------------------------------------------------------------
TIMEOUT_PYTEST_S = int(os.getenv("TIMEOUT_PYTEST_S", "60"))
WORKERS = int(os.getenv("WORKERS", str(max(1, (os.cpu_count() or 2)))))

# --- Pastas --------------------------------------------------------------------------
PASTA_FUNCOES = RAIZ / "funcoes"
PASTA_EXECUCOES = RAIZ / "execucoes"
PASTA_EXECUCOES_PILOTO = RAIZ / "execucoes_piloto"
PASTA_REVISAO = RAIZ / "revisao"
PASTA_RESULTADOS = RAIZ / "resultados"


def pasta_execucoes(piloto: bool = False, fake: bool = False) -> Path:
    base = PASTA_EXECUCOES_PILOTO if piloto else PASTA_EXECUCOES
    return base.with_name(base.name + "_fake") if fake else base
