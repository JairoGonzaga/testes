"""Gera as respostas do benchmark (SWT-Bench + TestGenEval adaptados) com modelos do OpenRouter.

Usa as mesmas 210 tarefas de `dados/jobs.json` (criadas por preparar.py) e grava as respostas no
mesmo formato que avaliar.py espera: `saidas/<rotulo>/<tarefa>/{test_issue.py|test_alvo.py|novo_teste.py, meta.json}`.

- Tarefas sem ferramentas (SWT zeroshot e TGE): uma chamada; o prompt é o arquivo `dados/prompts/...`.
  O código é o maior bloco ```python da resposta.
- SWT modo agente: laço de ferramentas (read_file, write_file, run_python, run_pytest) numa sandbox
  nova por modelo e tarefa (só alvo.py com defeito + ISSUE.md). A resposta é o test_issue.py final.

Provedores (--provedor):
- openrouter (padrão): chave OPENROUTER_API_KEY; ids como `baidu/ernie-5.5-flash-preview:free`.
- deepseek: API direta da DeepSeek, chave DEEPSEEK_API_KEY; ids `deepseek-flash` ou `deepseek-v4-pro`.
  A API não devolve custo: ele é calculado pelos tokens (cache hit/miss, saída) e pela tabela de preços,
  com o preço de pico (seg-sex 01-04h e 06-10h UTC) ou fora de pico conforme a hora de cada chamada.
- groq: API da Groq (plano gratuito, custo 0), chave GROQ_API_KEY; ids da lista em
  api.groq.com/openai/v1/models (ex.: `openai/gpt-oss-120b`). O rótulo ganha o prefixo `groq-`.
  O plano gratuito limita requisições e tokens por minuto e por dia: o runner respeita o Retry-After
  dos 429 (até --espera-max segundos) e para com "cota esgotada" se a espera for maior; rode de novo
  depois, que as tarefas prontas são puladas. HTTP 413 = a conversa passou do limite de tokens por
  minuto do modelo (o max_tokens não conta): a tarefa vira erro e as outras seguem.

A chave vem da variável de ambiente, do arquivo .env na raiz do projeto ou da variável de usuário do
Windows. Retoma de onde parou: tarefas que já têm meta.json são puladas.

Uso:
    python benchmark/gerar_openrouter.py --modelos baidu/ernie-5.5-flash-preview:free --amostras 1
    python benchmark/gerar_openrouter.py --provedor deepseek --modelos deepseek-flash --limite 1  # fumaça
    python benchmark/gerar_openrouter.py --provedor deepseek --modelos deepseek-flash
    python benchmark/gerar_openrouter.py --provedor deepseek --cota            # saldo da conta DeepSeek
    python benchmark/gerar_openrouter.py --provedor groq --modelos openai/gpt-oss-120b --workers 2 --harness v2
    python benchmark/avaliar.py --modelo deepseek-flash
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH.parent))
from nucleo import config  # noqa: E402  (carrega o .env)

DADOS = BENCH / "dados"


def sem_home(p: Path) -> str:
    """Caminho com a pasta do usuário trocada por ~ (o meta.json vai para o repositório)."""
    p, home = Path(p).resolve(), Path.home().resolve()
    try:
        return "~/" + p.relative_to(home).as_posix()
    except ValueError:
        return p.as_posix()
PROVEDORES = {
    "openrouter": {"url": "https://openrouter.ai/api/v1/chat/completions",
                   "modelos": "https://openrouter.ai/api/v1/models", "chave": "OPENROUTER_API_KEY"},
    "deepseek": {"url": "https://api.deepseek.com/chat/completions",
                 "modelos": "https://api.deepseek.com/models", "chave": "DEEPSEEK_API_KEY"},
    "groq": {"url": "https://api.groq.com/openai/v1/chat/completions",
             "modelos": "https://api.groq.com/openai/v1/models", "chave": "GROQ_API_KEY"},
}
RPM_PADRAO = {"groq": 28}  # plano gratuito da Groq: 30 req/min na maioria dos modelos
# US$ por milhão de tokens: (cache hit, cache miss, saída), fora de pico e no pico.
# Fonte: api-docs.deepseek.com/quick_start/pricing (consultada em 2026-11-22).
PRECOS_DEEPSEEK = {
    "deepseek-flash": {"fora": (0.003, 0.15, 0.6), "pico": (0.006, 0.3, 1.2)},
    "deepseek-v4-pro": {"fora": (0.022, 0.66, 1.98), "pico": (0.044, 1.32, 3.96)},
}
PRECOS_DEEPSEEK["deepseek-v4-flash"] = PRECOS_DEEPSEEK["deepseek-flash"]  # nome antigo, ainda aceito
ARQ_SAIDA = {"swt_zs": "test_issue.py", "swt_agente": "test_issue.py", "tge_full": "test_alvo.py",
             "tge_first": "novo_teste.py", "tge_last": "novo_teste.py", "tge_extra": "novo_teste.py"}
MAX_TOKENS = 16384
MAX_TURNOS_AGENTE = 15
TIMEOUT_FERRAMENTA_S = 60
LIMITE_SAIDA_FERRAMENTA = 6000

SISTEMA_DIRETO = ("You are an expert Python developer writing pytest tests. Answer with the requested Python "
                  "code in a single ```python code block. Do not add explanations outside the code block.")

SISTEMA_AGENTE = ("You are an expert Python developer working autonomously in a sandbox folder through the "
                  "tools provided. Paths are relative to the sandbox folder. Work step by step with the tools; "
                  "when you are done, write the final `test_issue.py` with write_file and then reply with one "
                  "short sentence and no tool call.")

# ---------------------------------------------------------------------------------
# Harness v2 (--harness v2): mesmas tarefas e prompts de dados/, com instruções de método no
# sistema, autorrevisão no zeroshot (2 chamadas, sem executar nada) e modo agente também no TGE.
# Nada do gabarito vai para o modelo: nem o código corrigido, nem mutantes, nem a suíte-ouro.
# ---------------------------------------------------------------------------------
MAX_TURNOS_AGENTE_V2 = 20

_REGRAS_ORACULO = (
    "Rules for expected values (most wrong tests come from breaking these):\n"
    "- Assert only behaviour that is stated by the task (the issue, or the code itself). Do not assert stricter "
    "rules, 'real-world' conventions or edge cases that the text does not state.\n"
    "- Never use memorized or mentally computed constants (check digits, checksums, unit scales, big-number "
    "arithmetic, rounding). Take each expected value from the task text, or obtain it by tracing the code "
    "line by line.\n"
    "- Python semantics matter: `%` with negatives, `int('3.9')` raises, `str.isdigit`, regex `$` also matches "
    "before a trailing newline, float formatting. When unsure, avoid the case instead of guessing.")

SISTEMA_DIRETO_V2 = (
    "You are an expert Python developer writing pytest tests.\n" + _REGRAS_ORACULO + "\n"
    "For an issue-reproduction task: the test must fail now only because of the reported bug and pass after the "
    "minimal fix the issue asks for; keep it small (the inputs/outputs from the issue, plus at most a couple of "
    "closely related cases whose expected values the issue states).\n"
    "First write a short analysis in plain text (at most 10 lines): what exact behaviour is promised and where each "
    "expected value comes from. Then give the complete file in a single ```python code block.")

REVISAO_V2 = (
    "Review your test file assertion by assertion, against the task above:\n"
    "1. Is this behaviour stated by the task text (not by your own assumptions or real-world conventions)?\n"
    "2. Is the expected value copied from the task or obtained by tracing the code, not computed from memory?\n"
    "3. For an issue: does it fail on the current code only because of the reported bug, and would it pass after "
    "the minimal fix? For a module test: does it pass on the code exactly as given?\n"
    "Delete or correct every assertion that fails any check (when in doubt, delete it). Answer with one line of "
    "notes and then the complete corrected file in a single ```python code block.")

SISTEMA_AGENTE_V2_SWT = (
    "You are an expert Python developer working autonomously in a sandbox folder through the tools provided. "
    "Paths are relative to the sandbox folder.\n" + _REGRAS_ORACULO + "\n"
    "Method:\n"
    "1. Read `alvo.py` and `ISSUE.md`. Identify the exact behaviour the issue promises.\n"
    "2. Compute every expected value you need with run_python on inputs taken from the issue (or by tracing "
    "the code), never from memory.\n"
    "3. Write `test_issue.py`, small and focused on the reported behaviour, and run it with run_pytest: it must "
    "FAIL, and the failure must be the reported bug (not an import error or a wrong expectation).\n"
    "4. Check the other side: create `fixcheck/alvo.py` = a copy of alvo.py with the smallest fix the issue "
    "implies, copy your test to `fixcheck/test_issue.py`, and run `run_pytest fixcheck/test_issue.py`. Every test "
    "must PASS there. Any assertion that fails on the fixed copy is wrong: correct it or delete it, then repeat "
    "steps 3 and 4.\n"
    "5. Leave the final `test_issue.py` in the sandbox root and reply with one short sentence and no tool call.")

SISTEMA_AGENTE_V2_TGE = (
    "You are an expert Python developer working autonomously in a sandbox folder through the tools provided. "
    "Paths are relative to the sandbox folder. `alvo.py` is the module under test and is CORRECT by definition: "
    "when a test fails, the test is wrong, never the code.\n" + _REGRAS_ORACULO + "\n"
    "Method: write the tests, run them with run_pytest, and for every failure check the real behaviour with "
    "run_python and fix the expectation (or delete the test). Repeat until everything passes. Keep assertions "
    "exact (full return values, exception types), since the tests are also graded by mutation testing. When "
    "done, reply with one short sentence and no tool call.")

SUFIXO_V2_TGE_FULL = (
    "\n\nYou are in a sandbox with `alvo.py` and tools to read/write files and run Python and pytest. Write the "
    "suite to `test_alvo.py` with write_file. Every test must pass: run `run_pytest test_alvo.py` until it does. "
    "You can check coverage with `run_pytest --cov=alvo --cov-branch --cov-report=term-missing test_alvo.py`.")

SUFIXO_V2_TGE_COMPL = (
    "\n\nYou are in a sandbox with `alvo.py` and `contexto_test_alvo.py` (the current test file shown above, "
    "read-only) and tools to read/write files and run Python and pytest. Write ONLY your new test function (plus "
    "any extra import it needs) to `novo_teste.py`, with a name not used in the current file. Before each "
    "run_pytest the harness rebuilds `test_alvo.py` = contexto_test_alvo.py + novo_teste.py, so run "
    "`run_pytest test_alvo.py`: your new test must pass.")

FERRAMENTAS = [
    {"type": "function", "function": {
        "name": "read_file", "description": "Read a text file from the sandbox folder.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "write_file", "description": "Create or overwrite a text file in the sandbox folder.",
        "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                       "required": ["path", "content"]}}},
    {"type": "function", "function": {
        "name": "run_pytest",
        "description": "Run `python -m pytest -q <args>` in the sandbox folder and return its output.",
        "parameters": {"type": "object", "properties": {"args": {"type": "string",
                       "description": "e.g. 'test_issue.py' or 'test_issue.py -x'"}}, "required": ["args"]}}},
    {"type": "function", "function": {
        "name": "run_python", "description": "Run a Python script (given as source code) in the sandbox folder "
                                             "and return stdout/stderr.",
        "parameters": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}}},
]


# ---------------------------------------------------------------------------------
# Chave e cliente HTTP
# ---------------------------------------------------------------------------------
def chave_api(provedor: str = "openrouter") -> str:
    var = PROVEDORES[provedor]["chave"]
    chave = os.environ.get(var, "").strip()
    if not chave and sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                chave = str(winreg.QueryValueEx(k, var)[0]).strip()
        except OSError:
            pass
    if not chave:
        raise SystemExit(f"{var} não encontrada (variável de ambiente, .env na raiz do projeto "
                         "ou variável de usuário do Windows).")
    return chave


def rotulo_de(modelo_id: str, sem_raciocinio: bool = False, harness: str = "v1",
              provedor: str = "openrouter") -> str:
    r = re.sub(r"[^A-Za-z0-9._-]+", "_", modelo_id.split("/", 1)[-1])
    r = f"groq-{r}" if provedor == "groq" else r
    r = r + "-sem-raciocinio" if sem_raciocinio else r
    return r if harness == "v1" else f"{r}-{harness}"


def info_modelos(ids, provedor="openrouter"):
    p = PROVEDORES[provedor]
    if provedor == "deepseek":
        r = requests.get(p["modelos"], headers={"Authorization": f"Bearer {chave_api(provedor)}"}, timeout=60)
        if r.status_code == 401:
            raise SystemExit("DEEPSEEK_API_KEY recusada pela DeepSeek (HTTP 401).")
        r.raise_for_status()
        disponiveis = {m["id"] for m in r.json().get("data", [])} | {"deepseek-v4-flash"}
        faltando = [i for i in ids if i not in disponiveis]
        if faltando:
            raise SystemExit(f"Modelos não encontrados na DeepSeek: {faltando} (há: {sorted(disponiveis)})")
        sem_preco = [i for i in ids if i not in PRECOS_DEEPSEEK]
        if sem_preco:
            print(f"aviso: sem tabela de preço para {sem_preco}; o custo sairá 0")
        return {i: {"supported_parameters": ["tools"], "top_provider": {"max_completion_tokens": MAX_TOKENS}}
                for i in ids}
    if provedor == "groq":
        r = requests.get(p["modelos"], headers={"Authorization": f"Bearer {chave_api(provedor)}"}, timeout=60)
        if r.status_code == 401:
            raise SystemExit("GROQ_API_KEY recusada pela Groq (HTTP 401).")
        r.raise_for_status()
        por_id = {m["id"]: m for m in r.json().get("data", []) if m.get("active", True)}
        faltando = [i for i in ids if i not in por_id]
        if faltando:
            raise SystemExit(f"Modelos não encontrados na Groq: {faltando} (há: {sorted(por_id)})")
        return {i: {"supported_parameters": ["tools"],
                    "top_provider": {"max_completion_tokens": por_id[i].get("max_completion_tokens") or MAX_TOKENS}}
                for i in ids}
    dados = requests.get(p["modelos"], timeout=60).json()["data"]
    por_id = {m["id"]: m for m in dados}
    faltando = [i for i in ids if i not in por_id]
    if faltando:
        raise SystemExit(f"Modelos não encontrados no OpenRouter: {faltando}")
    return {i: por_id[i] for i in ids}


def horario_de_pico(t=None) -> bool:
    """DeepSeek: pico = seg-sex, 01:00-04:00 e 06:00-10:00 UTC (preço em dobro)."""
    g = time.gmtime(t)
    return g.tm_wday < 5 and (1 <= g.tm_hour < 4 or 6 <= g.tm_hour < 10)


def custo_deepseek(modelo: str, usage: dict, t=None) -> float:
    tabela = PRECOS_DEEPSEEK.get(modelo)
    if not tabela:
        return 0.0
    hit, miss, saida = tabela["pico" if horario_de_pico(t) else "fora"]
    n_hit = usage.get("prompt_cache_hit_tokens") or 0
    n_miss = usage.get("prompt_cache_miss_tokens")
    if n_miss is None:
        n_miss = max(0, (usage.get("prompt_tokens") or 0) - n_hit)
    return (n_hit * hit + n_miss * miss + (usage.get("completion_tokens") or 0) * saida) / 1e6


class CotaEsgotada(PermissionError):
    """A cota diária de requisições a modelos gratuitos acabou (renova às 00:00 UTC)."""


def cota_gratuita(provedor="openrouter") -> dict:
    """OpenRouter: quanto resta da cota diária de modelos :free. DeepSeek: saldo da conta. Não consome cota."""
    if provedor == "groq":
        return {"aviso": "a Groq não tem endpoint de cota; veja os limites em console.groq.com/settings/limits"}
    if provedor == "deepseek":
        r = requests.get("https://api.deepseek.com/user/balance",
                         headers={"Authorization": f"Bearer {chave_api(provedor)}"}, timeout=60)
        r.raise_for_status()
        return r.json()
    r = requests.get("https://openrouter.ai/api/v1/key", headers={"Authorization": f"Bearer {chave_api()}"},
                     timeout=60)
    r.raise_for_status()
    d = r.json().get("data") or {}
    return {"is_free_tier": d.get("is_free_tier"), "free_model_daily_requests": d.get("free_model_daily_requests"),
            "limite_credito": d.get("limit"), "uso_usd": d.get("usage")}


class Ritmo:
    """Limita as requisições por minuto, somando todas as threads (modelos :free aceitam 20/min)."""

    def __init__(self, rpm):
        self.intervalo = 60.0 / rpm if rpm else 0.0
        self.proxima = 0.0
        self.trava = threading.Lock()

    def esperar(self):
        if not self.intervalo:
            return
        with self.trava:
            agora = time.monotonic()
            espera = self.proxima - agora
            self.proxima = max(agora, self.proxima) + self.intervalo
        if espera > 0:
            time.sleep(espera)


class Cliente:
    def __init__(self, modelo_id, info, temperatura=None, ritmo=None, provedor="openrouter", sem_raciocinio=False,
                 max_tokens=None, espera_max=900):
        self.modelo = modelo_id
        self.provedor = provedor
        self.url = PROVEDORES[provedor]["url"]
        self.sem_raciocinio = sem_raciocinio
        self.sessao = requests.Session()
        cab = {"Authorization": f"Bearer {chave_api(provedor)}", "Content-Type": "application/json"}
        if provedor == "openrouter":
            cab["X-Title"] = "testgen-benchmark"
        self.sessao.headers.update(cab)
        teto = ((info.get("top_provider") or {}).get("max_completion_tokens")) or MAX_TOKENS
        self.max_tokens = min(max_tokens or MAX_TOKENS, int(teto))
        self.espera_max = espera_max
        self.temperatura = temperatura
        self.ferramentas_ok = "tools" in (info.get("supported_parameters") or [])
        self.ritmo = ritmo or Ritmo(None)

    @staticmethod
    def _checar_cota(r):
        """429 com X-RateLimit-Remaining=0 e reset distante = cota diária esgotada (não adianta tentar de novo)."""
        resta, reset = r.headers.get("X-RateLimit-Remaining"), r.headers.get("X-RateLimit-Reset")
        if resta == "0" and reset and reset.isdigit():
            faltam_s = int(reset) / 1000 - time.time()
            if faltam_s > 120:
                quando = time.strftime("%H:%M", time.localtime(int(reset) / 1000))
                raise CotaEsgotada(f"cota diária de modelos gratuitos esgotada; renova às {quando} (horário local)")

    def chamar(self, mensagens, ferramentas=None):
        corpo = {"model": self.modelo, "messages": mensagens, "max_tokens": self.max_tokens}
        if self.provedor == "openrouter":
            corpo["usage"] = {"include": True}
        elif self.provedor == "deepseek" and self.sem_raciocinio:
            corpo["thinking"] = {"type": "disabled"}
        if self.temperatura is not None:
            corpo["temperature"] = self.temperatura
        if ferramentas:
            corpo["tools"] = ferramentas
        ultimo = None
        tentativa = esperas = 0
        while tentativa < 6:
            tentativa += 1
            try:
                self.ritmo.esperar()
                t_req = time.time()
                r = self.sessao.post(self.url, json=corpo, timeout=config.TIMEOUT_CHAMADA_S * 2)
                if r.status_code in (401, 402, 403):
                    raise PermissionError(f"HTTP {r.status_code}: {r.text[:300]}")
                if r.status_code == 400 and ("tool_use_failed" in r.text or "output_parse_failed" in r.text):
                    # o modelo gerou uma chamada de ferramenta com JSON quebrado (Groq): varia a cada tentativa
                    ultimo = f"HTTP 400 (geração inválida): {r.text[:200]}"
                    time.sleep(2)
                    continue
                if r.status_code in (400, 413, 422):  # malformado ou grande demais: repetir não ajuda
                    raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
                if r.status_code == 404 and "data policy" in r.text.lower():
                    raise PermissionError(
                        "HTTP 404: nenhum provedor aceita a política de dados da conta. Modelos :free costumam "
                        "exigir que a conta permita provedores gratuitos em openrouter.ai/settings/privacy. "
                        + r.text[:200])
                if r.status_code == 429:
                    self._checar_cota(r)
                    espera = _retry_after(r)
                    if espera is not None:  # limite por minuto/dia com prazo informado: esperar não gasta tentativa
                        if espera > self.espera_max:
                            raise CotaEsgotada(f"limite de requisições/tokens do plano; liberaria em {espera:.0f}s "
                                               f"(> --espera-max {self.espera_max:.0f}s): {r.text[:200]}")
                        esperas += 1
                        if esperas <= 200:
                            tentativa -= 1
                            time.sleep(espera + 0.5)
                            continue
                if r.status_code in (408, 429, 500, 502, 503, 504):
                    ultimo = f"HTTP {r.status_code}: {r.text[:300]}"
                    time.sleep(min(60, 2 * 2 ** tentativa))
                    continue
                d = r.json()
                if not d.get("choices"):
                    ultimo = f"resposta sem choices: {json.dumps(d.get('error', d))[:300]}"
                    codigo = (d.get("error") or {}).get("code")
                    if codigo in (400, 401, 402, 403):
                        raise PermissionError(ultimo)
                    time.sleep(min(60, 2 * 2 ** tentativa))
                    continue
                if self.provedor == "deepseek" and isinstance(d.get("usage"), dict):
                    d["usage"]["cost"] = custo_deepseek(self.modelo, d["usage"], t_req)
                return d
            except (requests.RequestException, ValueError) as e:
                ultimo = f"{type(e).__name__}: {e}"
                time.sleep(min(60, 2 * 2 ** tentativa))
        raise RuntimeError(f"falhou após 6 tentativas: {ultimo}")


def _retry_after(r):
    """Segundos do cabeçalho Retry-After (Groq e APIs compatíveis com a OpenAI); None se ausente ou inválido."""
    v = r.headers.get("retry-after") or r.headers.get("Retry-After")
    try:
        return max(0.0, float(v)) if v is not None else None
    except ValueError:
        return None


# ---------------------------------------------------------------------------------
# Extração do código
# ---------------------------------------------------------------------------------
_PENSAMENTO = re.compile(r"<think>.*?</think>", re.S)
_BLOCO = re.compile(r"```[ \t]*(?:python|py|python3)?[ \t]*\n(.*?)```", re.S | re.I)


def extrair_codigo(texto: str) -> str:
    texto = _PENSAMENTO.sub("", texto or "")
    blocos = _BLOCO.findall(texto)
    if blocos:
        codigo = max(blocos, key=len)
    else:  # sem cercas: a resposta inteira, tirando uma cerca aberta sem fechar
        codigo = re.sub(r"^```[^\n]*\n", "", texto.strip())
    return codigo.strip("\n") + "\n"


class Uso:
    def __init__(self):
        self.entrada = self.saida = self.raciocinio = self.chamadas = 0
        self.custo = 0.0
        self.provedores = set()

    def somar(self, d):
        u = d.get("usage") or {}
        self.entrada += u.get("prompt_tokens") or 0
        self.saida += u.get("completion_tokens") or 0
        self.raciocinio += ((u.get("completion_tokens_details") or {}).get("reasoning_tokens")) or 0
        self.custo += float(u.get("cost") or 0)
        self.chamadas += 1
        if d.get("provider"):
            self.provedores.add(d["provider"])

    def dict(self):
        return {"tokens_entrada": self.entrada, "tokens_saida": self.saida, "tokens_raciocinio": self.raciocinio,
                "custo_usd": round(self.custo, 6), "chamadas_api": self.chamadas,
                "provedores": sorted(self.provedores)}


# ---------------------------------------------------------------------------------
# Tarefas sem ferramentas
# ---------------------------------------------------------------------------------
def tarefa_direta(cli: Cliente, job: dict, uso: Uso, harness: str = "v1"):
    prompt = (BENCH / job["prompt"]).read_text(encoding="utf-8")
    sistema = SISTEMA_DIRETO if harness == "v1" else SISTEMA_DIRETO_V2
    msgs = [{"role": "system", "content": sistema}, {"role": "user", "content": prompt}]
    d = cli.chamar(msgs)
    uso.somar(d)
    esc = d["choices"][0]
    texto = (esc.get("message") or {}).get("content") or ""
    extra = {"finish_reason": esc.get("finish_reason"), "resposta_bruta": texto}
    if harness != "v1" and texto.strip() and esc.get("finish_reason") != "length":
        # autorrevisão: uma segunda chamada, sem executar nada (continua sendo zeroshot quanto à execução)
        msgs += [{"role": "assistant", "content": texto}, {"role": "user", "content": REVISAO_V2}]
        d2 = cli.chamar(msgs)
        uso.somar(d2)
        esc2 = d2["choices"][0]
        texto2 = (esc2.get("message") or {}).get("content") or ""
        if _BLOCO.search(_PENSAMENTO.sub("", texto2)):
            extra.update(finish_reason=esc2.get("finish_reason"), revisado=True,
                         resposta_bruta=texto + "\n\n---- revisão ----\n\n" + texto2)
            texto = texto2
    return extrair_codigo(texto) if texto.strip() else "", extra


# ---------------------------------------------------------------------------------
# SWT modo agente
# ---------------------------------------------------------------------------------
def _caminho_seguro(sb: Path, rel: str) -> Path:
    p = (sb / (rel or ".")).resolve()
    if p != sb and sb not in p.parents:
        raise ValueError(f"path outside the sandbox: {rel}")
    return p


def _rodar(cmd, sb: Path) -> str:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("PYTHON", "OPENROUTER", "ANTHROPIC", "OPENAI", "DEEPSEEK", "GROQ"))}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        p = subprocess.run(cmd, cwd=sb, env=env, capture_output=True, text=True, timeout=TIMEOUT_FERRAMENTA_S,
                           encoding="utf-8", errors="replace")
        saida = f"exit code {p.returncode}\n{p.stdout}{p.stderr}"
    except subprocess.TimeoutExpired:
        saida = f"timeout after {TIMEOUT_FERRAMENTA_S}s"
    if len(saida) > LIMITE_SAIDA_FERRAMENTA:
        meio = LIMITE_SAIDA_FERRAMENTA // 2
        saida = saida[:meio] + "\n...[truncated]...\n" + saida[-meio:]
    return saida


def executar_ferramenta(nome: str, args: dict, sb: Path, cont: dict) -> str:
    cont[nome] = cont.get(nome, 0) + 1
    try:
        if nome == "read_file":
            p = _caminho_seguro(sb, args.get("path", ""))
            if p.is_dir():
                return "\n".join(sorted(x.name for x in p.iterdir()))
            return p.read_text(encoding="utf-8", errors="replace")[:LIMITE_SAIDA_FERRAMENTA * 3]
        if nome == "write_file":
            p = _caminho_seguro(sb, args.get("path", ""))
            if p == sb / "alvo.py":  # cópias em subpastas (ex.: fixcheck/alvo.py) são permitidas
                return "error: alvo.py is read-only in this task (do not change the module)"
            if p == sb / "contexto_test_alvo.py":
                return "error: contexto_test_alvo.py is read-only; write your new test to novo_teste.py"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(args.get("content", ""), encoding="utf-8")
            return f"wrote {p.relative_to(sb)} ({len(args.get('content', ''))} chars)"
        if nome == "run_pytest":
            ctx = sb / "contexto_test_alvo.py"
            if ctx.exists():  # TGE completar: test_alvo.py = contexto + teste novo, como na avaliação
                novo = sb / "novo_teste.py"
                corpo = novo.read_text(encoding="utf-8") if novo.exists() else ""
                (sb / "test_alvo.py").write_text(ctx.read_text(encoding="utf-8").rstrip() + "\n\n\n" + corpo,
                                                 encoding="utf-8")
            extra = (args.get("args") or "").split()
            return _rodar([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *extra], sb)
        if nome == "run_python":
            script = sb / "_script_agente.py"
            script.write_text(args.get("code", ""), encoding="utf-8")
            try:
                return _rodar([sys.executable, script.name], sb)
            finally:
                script.unlink(missing_ok=True)
        return f"error: unknown tool {nome}"
    except Exception as e:  # o erro volta para o modelo, como numa ferramenta real
        return f"error: {type(e).__name__}: {e}"


def tarefa_agente(cli: Cliente, job: dict, uso: Uso, raiz_sb: Path, harness: str = "v1"):
    sb = (raiz_sb / job["id"]).resolve()
    if sb.exists():
        shutil.rmtree(sb)
    sb.mkdir(parents=True)
    prompt = (BENCH / job["prompt"]).read_text(encoding="utf-8")
    alvo_saida = ARQ_SAIDA[job["tipo"]]
    if job["tipo"] == "swt_agente":
        inst = DADOS / "swt" / job["instancia"]
        shutil.copy(inst / "buggy.py", sb / "alvo.py")
        shutil.copy(inst / "issue.md", sb / "ISSUE.md")
        prompt += ("\n\nYou have tools to read and write files in the sandbox and to run Python and pytest there. "
                   "Start by reading `alvo.py` and `ISSUE.md`.")
        sistema = SISTEMA_AGENTE if harness == "v1" else SISTEMA_AGENTE_V2_SWT
    else:  # TGE em modo agente (só no harness v2): alvo.py é a referência, considerada correta
        pasta_tge = DADOS / "tge" / job["funcao"]
        shutil.copy(pasta_tge / "alvo.py", sb / "alvo.py")
        if job["tipo"] == "tge_full":
            prompt += SUFIXO_V2_TGE_FULL
        else:
            shutil.copy(pasta_tge / f"ctx_{job['tipo'].split('_')[1]}.py", sb / "contexto_test_alvo.py")
            prompt += SUFIXO_V2_TGE_COMPL
        sistema = SISTEMA_AGENTE_V2_TGE
    max_turnos = MAX_TURNOS_AGENTE if harness == "v1" else MAX_TURNOS_AGENTE_V2
    msgs = [{"role": "system", "content": sistema}, {"role": "user", "content": prompt}]
    cont, final, motivo, turno = {}, "", None, 0
    pytests = []  # (turno, args, exit code) de cada run_pytest, para medir o processo do agente
    for turno in range(1, max_turnos + 1):
        d = cli.chamar(msgs, FERRAMENTAS)
        uso.somar(d)
        esc = d["choices"][0]
        msg = esc.get("message") or {}
        chamadas = msg.get("tool_calls") or []
        registro = {"role": "assistant", "content": msg.get("content") or ""}
        if msg.get("reasoning_content"):  # DeepSeek com ferramentas exige devolver o raciocínio
            registro["reasoning_content"] = msg["reasoning_content"]
        if chamadas:
            registro["tool_calls"] = chamadas
        msgs.append(registro)
        if not chamadas:
            final, motivo = msg.get("content") or "", esc.get("finish_reason")
            break
        for c in chamadas:
            fn = c.get("function") or {}
            try:
                args = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError as e:
                saida = f"error: invalid JSON arguments: {e}"
                cont["argumentos_invalidos"] = cont.get("argumentos_invalidos", 0) + 1
            else:
                saida = executar_ferramenta(fn.get("name", ""), args if isinstance(args, dict) else {}, sb, cont)
                if fn.get("name") == "run_pytest":
                    m = re.match(r"exit code (-?\d+)", saida)
                    pytests.append({"turno": turno, "args": str(args.get("args", ""))[:200],
                                    "exit": int(m.group(1)) if m else None})
            msgs.append({"role": "tool", "tool_call_id": c.get("id"), "content": saida})
    else:
        motivo = "limite_de_turnos"
    arq = sb / alvo_saida
    if arq.exists() and arq.read_text(encoding="utf-8").strip():
        codigo, origem = arq.read_text(encoding="utf-8"), "arquivo"
    elif _BLOCO.search(_PENSAMENTO.sub("", final or "")):
        codigo, origem = extrair_codigo(final), "mensagem_final"
    else:
        codigo, origem = "", "nenhuma"
    ferr = {"Bash": cont.get("run_pytest", 0) + cont.get("run_python", 0), "Write": cont.get("write_file", 0),
            "Read": cont.get("read_file", 0)}
    if cont.get("argumentos_invalidos"):
        ferr["argumentos_invalidos"] = cont["argumentos_invalidos"]
    extra = {"finish_reason": motivo, "turnos": turno, "origem_codigo": origem, "ferramentas": ferr,
             "pytests": pytests, "sandbox": sem_home(sb), "nota": (final or "")[:500]}
    (sb.parent / f"{job['id']}_conversa.json").write_text(json.dumps(msgs, ensure_ascii=False, indent=1),
                                                         encoding="utf-8")
    return codigo, extra


# ---------------------------------------------------------------------------------
# Orquestração
# ---------------------------------------------------------------------------------
ORDEM_TIPOS = ["swt_zs", "tge_full", "tge_first", "tge_last", "tge_extra", "swt_agente"]  # agente por último:
# gasta ~5 requisições por tarefa; com cota diária curta, os tipos baratos fecham primeiro


def rodar_modelo(modelo_id, info, jobs, args):
    """Devolve None se terminou (ou bateu o teto de custo) ou o motivo da parada (cota, chave, crédito)."""
    harness = getattr(args, "harness", "v1")
    provedor = getattr(args, "provedor", "openrouter")
    rotulo = rotulo_de(modelo_id, args.sem_raciocinio, harness, provedor)
    saidas = BENCH / "saidas" / rotulo
    raiz_sb = Path(args.sandbox).resolve() / rotulo
    rpm = args.rpm if args.rpm is not None else (18 if modelo_id.endswith(":free") else RPM_PADRAO.get(provedor))
    cli = Cliente(modelo_id, info, args.temperatura, Ritmo(rpm), provedor, args.sem_raciocinio,
                  getattr(args, "max_tokens", None), getattr(args, "espera_max", 900))
    if args.provedor == "deepseek" and horario_de_pico():
        print(f"[{rotulo}] aviso: horário de pico da DeepSeek (preço em dobro); fora de pico: "
              "seg-sex fora de 01-04h e 06-10h UTC, e fim de semana inteiro")
    pendentes = [j for j in jobs if not (saidas / j["id"] / "meta.json").exists()]
    pendentes.sort(key=lambda j: (ORDEM_TIPOS.index(j["tipo"]), j["amostra"], j["id"]))
    motivo_parada = []
    if not cli.ferramentas_ok:
        print(f"[{rotulo}] aviso: o modelo não anuncia suporte a ferramentas; o modo agente pode falhar")
    print(f"[{rotulo}] {len(pendentes)} tarefas pendentes de {len(jobs)} (max_tokens={cli.max_tokens})", flush=True)
    trava = threading.Lock()
    total = {"custo": 0.0, "ok": 0, "falhas": 0}
    parar = threading.Event()

    def um(job):
        if parar.is_set():
            return
        uso, t0 = Uso(), time.perf_counter()
        pasta = saidas / job["id"]
        try:
            if job["tipo"] == "swt_agente" or (harness != "v1" and job["tipo"].startswith("tge_")):
                codigo, extra = tarefa_agente(cli, job, uso, raiz_sb, harness)
            else:
                codigo, extra = tarefa_direta(cli, job, uso, harness)
            erro = None
        except PermissionError as e:  # cota esgotada / chave inválida / sem crédito: não adianta continuar
            codigo, extra, erro = "", {}, f"{type(e).__name__}: {e}"
            with trava:
                if not motivo_parada:
                    motivo_parada.append(str(e))
            parar.set()
        except Exception as e:
            codigo, extra, erro = "", {}, f"{type(e).__name__}: {e}"
        pasta.mkdir(parents=True, exist_ok=True)
        bruta = extra.pop("resposta_bruta", None)
        if bruta is not None:
            (pasta / "resposta_bruta.md").write_text(bruta, encoding="utf-8")
        if codigo.strip():
            (pasta / ARQ_SAIDA[job["tipo"]]).write_text(codigo, encoding="utf-8")
        if erro:  # a mensagem do provedor pode trazer o id da organização da conta
            erro = re.sub(r"org_[0-9A-Za-z]{10,}", "org_***", erro)
        meta = {"modelo_id": modelo_id, "erro": erro, "tempo_s": round(time.perf_counter() - t0, 1),
                **uso.dict(), **extra}
        # com erro de API não grava meta.json: a tarefa é refeita na próxima execução
        nome_meta = "meta.json" if erro is None else "erro.json"
        (pasta / nome_meta).write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        with trava:
            total["custo"] += uso.custo
            total["ok" if (erro is None and codigo.strip()) else "falhas"] += 1
            feitos = total["ok"] + total["falhas"]
            if erro or feitos % 10 == 0 or feitos == len(pendentes):
                print(f"[{rotulo}] {feitos}/{len(pendentes)} ok={total['ok']} sem_codigo_ou_erro={total['falhas']} "
                      f"custo=${total['custo']:.4f}" + (f"  ERRO {job['id']}: {erro[:200]}" if erro else ""),
                      flush=True)
            if args.teto_usd and total["custo"] >= args.teto_usd and not parar.is_set():
                print(f"[{rotulo}] teto de ${args.teto_usd} atingido; parando novas tarefas", flush=True)
                parar.set()

    with ThreadPoolExecutor(args.workers) as ex:
        for f in as_completed([ex.submit(um, j) for j in pendentes]):
            f.result()

    # consolida o uso do modelo inteiro (inclusive execuções anteriores)
    agg = {"modelo_id": modelo_id, "tarefas": 0, "com_codigo": 0, "custo_usd": 0.0, "tokens_entrada": 0,
           "tokens_saida": 0, "tokens_raciocinio": 0, "tempo_s": 0.0, "truncadas": 0}
    for j in jobs:
        m = saidas / j["id"] / "meta.json"
        if not m.exists():
            continue
        d = json.loads(m.read_text(encoding="utf-8"))
        agg["tarefas"] += 1
        agg["com_codigo"] += (saidas / j["id"] / ARQ_SAIDA[j["tipo"]]).exists()
        for k in ("custo_usd", "tokens_entrada", "tokens_saida", "tokens_raciocinio", "tempo_s"):
            agg[k] += d.get(k) or 0
        agg["truncadas"] += d.get("finish_reason") == "length"
    agg["custo_usd"] = round(agg["custo_usd"], 4)
    agg["tempo_s"] = round(agg["tempo_s"], 1)
    if saidas.exists():
        (saidas / "_uso.json").write_text(json.dumps(agg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[{rotulo}] fim: {json.dumps(agg, ensure_ascii=False)}", flush=True)
    return motivo_parada[0] if motivo_parada else None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--provedor", choices=sorted(PROVEDORES), default="openrouter")
    p.add_argument("--modelos", nargs="+", help="ids do provedor (ex.: baidu/ernie-5.5-flash-preview:free, "
                                                "deepseek-flash)")
    p.add_argument("--cota", action="store_true",
                   help="só mostra a cota diária de modelos :free (OpenRouter) ou o saldo (DeepSeek) e sai")
    p.add_argument("--sem-raciocinio", action="store_true",
                   help="DeepSeek: desliga o modo thinking (mais barato; rótulo ganha '-sem-raciocinio')")
    p.add_argument("--harness", choices=["v1", "v2"], default="v1",
                   help="v2: instruções de método, autorrevisão no zeroshot e TGE em modo agente "
                        "(rótulo ganha '-v2'; não sobrescreve o v1)")
    p.add_argument("--tipos", nargs="*", help="filtra tipos de tarefa (swt_zs swt_agente tge_full tge_first ...)")
    p.add_argument("--amostras", type=int, nargs="*", help="só estas amostras (ex.: --amostras 1)")
    p.add_argument("--limite", type=int, help="só as N primeiras tarefas de cada tipo (teste de fumaça)")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--rpm", type=float, default=None,
                   help="máx. requisições por minuto (padrão: 18 para modelos :free, 28 na Groq, "
                        "sem limite para os pagos)")
    p.add_argument("--max-tokens", type=int, default=None,
                   help=f"teto de tokens de saída por chamada (padrão {MAX_TOKENS}; na Groq, reduza se vier HTTP 413)")
    p.add_argument("--espera-max", type=float, default=900,
                   help="maior espera (s) aceita num 429 com Retry-After; acima disso para como cota esgotada")
    p.add_argument("--temperatura", type=float, default=None, help="padrão: a do provedor")
    p.add_argument("--teto-usd", type=float, default=5.0, help="para de lançar tarefas acima deste custo por modelo")
    p.add_argument("--sandbox", default=str(Path(tempfile.gettempdir()) / "bench_sandbox_openrouter"),
                   help="pasta (fora do repositório) para as sandboxes do modo agente")
    a = p.parse_args()
    if a.cota:
        print(json.dumps(cota_gratuita(a.provedor), ensure_ascii=False, indent=1))
        return
    if not a.modelos:
        p.error("--modelos é obrigatório (ou use --cota)")
    if a.sem_raciocinio and a.provedor != "deepseek":
        p.error("--sem-raciocinio só vale para --provedor deepseek")

    jobs = json.loads((DADOS / "jobs.json").read_text(encoding="utf-8"))
    if a.tipos:
        jobs = [j for j in jobs if j["tipo"] in a.tipos]
    if a.amostras:
        jobs = [j for j in jobs if j["amostra"] in a.amostras]
    if a.limite:
        por_tipo = {}
        for j in jobs:
            por_tipo.setdefault(j["tipo"], []).append(j)
        jobs = [j for ls in por_tipo.values() for j in ls[:a.limite]]
    chave_api(a.provedor)
    infos = info_modelos(a.modelos, a.provedor)
    parados = []
    for m in a.modelos:
        motivo = rodar_modelo(m, infos[m], jobs, a)
        if motivo:
            if a.provedor != "groq":  # OpenRouter/DeepSeek: cota/saldo é da conta, os outros modelos parariam igual
                raise SystemExit(f"Parado: {motivo}\nRode o mesmo comando de novo depois: as tarefas prontas são puladas.")
            parados.append(f"{m}: {motivo}")  # Groq: cada modelo tem seu limite diário, segue para o próximo
    if parados:
        raise SystemExit("Parados (limite do plano):\n  " + "\n  ".join(parados)
                         + "\nRode o mesmo comando de novo depois: as tarefas prontas são puladas.")


if __name__ == "__main__":
    main()
