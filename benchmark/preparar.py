"""Monta os dados do benchmark (SWT-Bench e TestGenEval adaptados) a partir de funcoes/.

Uso:
    python benchmark/preparar.py --amostras 3 --sandbox <pasta fora do repositório>

Gera em benchmark/dados/:
    swt/<instância>/      buggy.py, fixed.py, patch.diff, linhas_alteradas.json, issue.md
    tge/<função>/         alvo.py, teste_ouro.py, ctx_first.py, ctx_last.py, ctx_extra.py
    prompts/<job>.md      prompt entregue ao modelo (um por tarefa; amostras reusam o prompt)
    jobs.json             lista de tarefas (id, tipo, prompt, saída)
E, para o modo agente do SWT-Bench, uma sandbox por amostra (só alvo.py com defeito + ISSUE.md).

Nada aqui chama modelo: é só preparação determinística.
"""

import argparse
import ast
import difflib
import json
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from nucleo import funcoes as fn  # noqa: E402
from nucleo import plano  # noqa: E402

BENCH = RAIZ / "benchmark"
DADOS = BENCH / "dados"


def rel(p: Path) -> str:
    """Caminho relativo à pasta benchmark/ (jobs.json não leva caminhos da máquina local)."""
    return Path(p).resolve().relative_to(BENCH).as_posix()


def sem_home(p: Path) -> str:
    """Caminho fora do repositório, com a pasta do usuário trocada por ~."""
    p, home = Path(p).resolve(), Path.home().resolve()
    try:
        return "~/" + p.relative_to(home).as_posix()
    except ValueError:
        return p.as_posix()


# ---------------------------------------------------------------------------------
# Normalização de fontes
# ---------------------------------------------------------------------------------
def ler(p: Path) -> str:
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def sem_cabecalho_defeito(txt: str) -> str:
    linhas = txt.split("\n")
    while linhas and re.match(r"#\s*(DEFEITO INJETADO|Trecho original)", linhas[0]):
        linhas.pop(0)
    return "\n".join(linhas)


def sem_docstring_modulo(txt: str) -> str:
    """Remove a docstring do módulo (fala de 'versão de referência' e das adaptações)."""
    arvore = ast.parse(txt)
    if arvore.body and isinstance(arvore.body[0], ast.Expr) and isinstance(
            getattr(arvore.body[0], "value", None), ast.Constant) and isinstance(arvore.body[0].value.value, str):
        no = arvore.body[0]
        linhas = txt.split("\n")
        resto = linhas[no.end_lineno:]
        while resto and not resto[0].strip():
            resto.pop(0)
        return "\n".join(linhas[:no.lineno - 1] + resto)
    return txt


def linhas_alteradas(buggy: str, fixed: str) -> dict:
    """Linhas (1-based) tocadas pelo patch: removidas/alteradas na buggy e inseridas/alteradas na fixed."""
    a, b = buggy.split("\n"), fixed.split("\n")
    rb, rf = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        rb += [i + 1 for i in range(i1, i2) if a[i].strip()]
        rf += [j + 1 for j in range(j1, j2) if b[j].strip()]
    return {"buggy": rb, "fixed": rf}


# ---------------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------------
def bloco(codigo: str, lang="python") -> str:
    return f"```{lang}\n{codigo.rstrip()}\n```"


PROMPT_SWT_ZS = """\
You are given an issue report for a small Python project and the full source of the module it
concerns, `alvo.py`.

Write a pytest test file that REPRODUCES the issue:
- the tests must FAIL on the current code (because of the bug described in the issue), and
- the tests must PASS once the issue is fixed.

Rules:
- Import from the module with `from alvo import ...`. The test file will be saved as
  `test_issue.py` in the same folder as `alvo.py`.
- Do not modify, copy or re-implement the module. Do not fix the bug.
- The answer is a single complete, runnable pytest file.

## Issue: {title}

{body}

## Source: alvo.py

{fonte}
"""

PROMPT_SWT_AGENTE = """\
You are working in a sandbox folder that contains a small Python module, `alvo.py`, and an issue
report about it, `ISSUE.md`.

Your task: write a pytest test file `test_issue.py` (in the same folder) that REPRODUCES the issue:
- the tests must FAIL on the current code (because of the bug described in the issue), and
- the tests must PASS once the issue is fixed.

Rules:
- Import from the module with `from alvo import ...`.
- You may run Python and `python -m pytest` inside the sandbox to check your work.
- Do not fix the bug in `alvo.py` (any change to it is discarded; only `test_issue.py` is evaluated).
"""

PROMPT_TGE_FULL = """\
Below is the source code of a Python module, `alvo.py`.

Write a complete pytest unit-test suite for this module.
- Import with `from alvo import ...`. The test file will be saved as `test_alvo.py` next to `alvo.py`.
- The tests must pass on this code.
- Exercise all of its behaviour (aim for full line and branch coverage), including edge cases and
  error handling, and make the assertions strong enough to catch bugs: the suite will be evaluated
  by coverage and by mutation testing.
- The answer is a single complete, runnable pytest file.

## Source: alvo.py

{fonte}
"""

PROMPT_TGE_COMPL = {
    "first": """\
Below is the source code of a Python module, `alvo.py`, and the beginning of its test file,
`test_alvo.py` (imports and the first test function).

Write the NEXT test function of this test file.
- It must pass on this code and test behaviour of the module.
- The answer is only the code of the new test function (plus any extra import it needs at the top).
  It will be appended to the end of the test file shown below.
""",
    "last": """\
Below is the source code of a Python module, `alvo.py`, and its test file, `test_alvo.py`, with the
LAST test function removed.

Write the missing last test function of this test file.
- It must pass on this code and test behaviour of the module.
- The answer is only the code of the new test function (plus any extra import it needs at the top).
  It will be appended to the end of the test file shown below.
""",
    "extra": """\
Below is the source code of a Python module, `alvo.py`, and its complete test file, `test_alvo.py`.

Write ONE additional test function that improves this test suite: it should test behaviour that the
existing tests do not check yet (increasing coverage or the ability to catch bugs).
- It must pass on this code.
- The answer is only the code of the new test function (plus any extra import it needs at the top).
  It will be appended to the end of the test file shown below.
""",
}

SUFIXO_COMPL = """
## Source: alvo.py

{fonte}

## Test file: test_alvo.py (current content)

{teste}
"""


# ---------------------------------------------------------------------------------
# Teste "humano" (ouro) para a tarefa de completar testes
# ---------------------------------------------------------------------------------
def teste_ouro(funcao) -> tuple:
    casos = [dict(c, id=f"C{i + 1}") for i, c in enumerate(funcao.gabarito["casos"])]
    txt = plano.renderizar_testes(casos, funcao, cabecalho=f"Testes de {funcao.nome_funcao}.")
    partes = re.split(r"(?m)^(?=def test_)", txt)
    return partes[0], partes[1:]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--amostras", type=int, default=3)
    p.add_argument("--sandbox", required=True, help="pasta (fora do repo) para as sandboxes do modo agente")
    p.add_argument("--modelo", default="haiku", help="rótulo do modelo (pasta de saídas)")
    a = p.parse_args()

    issues = json.loads(ler(BENCH / "issues.json"))
    if DADOS.exists():
        shutil.rmtree(DADOS)
    (DADOS / "prompts").mkdir(parents=True)
    sandbox_raiz = Path(a.sandbox).resolve()
    saidas = BENCH / "saidas" / a.modelo
    jobs, problemas = [], []

    nomes = sorted(d.name for d in (RAIZ / "funcoes").iterdir() if (d / "meta.json").exists())
    for nome in nomes:
        funcao = fn.carregar(nome)
        fixed = sem_docstring_modulo(ler(funcao.referencia))
        ref_ns = {}
        exec(compile(fixed, "fixed", "exec"), ref_ns)

        # ---------------- SWT-Bench: uma instância por defeito -------------------------
        for d in funcao.defeitos:
            inst = f"{nome}__{d.stem}"
            buggy = sem_docstring_modulo(sem_cabecalho_defeito(ler(d)))
            pasta = DADOS / "swt" / inst
            pasta.mkdir(parents=True)
            (pasta / "buggy.py").write_text(buggy, encoding="utf-8")
            (pasta / "fixed.py").write_text(fixed, encoding="utf-8")
            patch = "".join(difflib.unified_diff(buggy.splitlines(True), fixed.splitlines(True),
                                                 "a/alvo.py", "b/alvo.py"))
            (pasta / "patch.diff").write_text(patch, encoding="utf-8")
            alt = linhas_alteradas(buggy, fixed)
            (pasta / "linhas_alteradas.json").write_text(json.dumps(alt), encoding="utf-8")
            if not (alt["buggy"] or alt["fixed"]):
                problemas.append(f"{inst}: patch vazio")

            iss = issues[inst]
            bug_ns = {}
            exec(compile(buggy, "buggy", "exec"), bug_ns)

            def roda(ns):
                try:
                    return ("ok", repr(eval(iss["repro"], ns)))
                except Exception as e:  # noqa: BLE001
                    return ("exc", type(e).__name__)
            if roda(bug_ns) == roda(ref_ns):
                problemas.append(f"{inst}: repro do relato não diverge")
            issue_md = f"# {iss['title']}\n\n{iss['body']}\n"
            (pasta / "issue.md").write_text(issue_md, encoding="utf-8")

            prompt_zs = DADOS / "prompts" / f"swtzs__{inst}.md"
            prompt_zs.write_text(PROMPT_SWT_ZS.format(title=iss["title"], body=iss["body"], fonte=bloco(buggy)),
                                 encoding="utf-8")
            prompt_ag = DADOS / "prompts" / "swtag.md"
            prompt_ag.write_text(PROMPT_SWT_AGENTE, encoding="utf-8")
            for s in range(1, a.amostras + 1):
                jid = f"swtzs__{inst}__s{s}"
                jobs.append({"id": jid, "tipo": "swt_zs", "instancia": inst, "funcao": nome, "amostra": s,
                             "prompt": rel(prompt_zs), "saida": rel(saidas / jid / "test_issue.py")})
                jid = f"swtag__{inst}__s{s}"
                sb = sandbox_raiz / jid
                if sb.exists():
                    shutil.rmtree(sb)
                sb.mkdir(parents=True)
                (sb / "alvo.py").write_text(buggy, encoding="utf-8")
                (sb / "ISSUE.md").write_text(issue_md, encoding="utf-8")
                jobs.append({"id": jid, "tipo": "swt_agente", "instancia": inst, "funcao": nome, "amostra": s,
                             "prompt": rel(prompt_ag), "sandbox": sem_home(sb),
                             "saida": rel(saidas / jid / "test_issue.py")})

        # ---------------- TestGenEval: geração completa e completar testes -------------
        pasta = DADOS / "tge" / nome
        pasta.mkdir(parents=True)
        (pasta / "alvo.py").write_text(fixed, encoding="utf-8")
        cab, testes = teste_ouro(funcao)
        cab = cab.rstrip() + "\n\n\n"
        ouro = cab + "".join(testes)
        (pasta / "teste_ouro.py").write_text(ouro.rstrip() + "\n", encoding="utf-8")
        ctx = {"first": cab + testes[0], "last": cab + "".join(testes[:-1]), "extra": ouro}
        for k, v in ctx.items():
            (pasta / f"ctx_{k}.py").write_text(v.rstrip() + "\n", encoding="utf-8")

        prompt_full = DADOS / "prompts" / f"tgefull__{nome}.md"
        prompt_full.write_text(PROMPT_TGE_FULL.format(fonte=bloco(fixed)), encoding="utf-8")
        for s in range(1, a.amostras + 1):
            jid = f"tgefull__{nome}__s{s}"
            jobs.append({"id": jid, "tipo": "tge_full", "funcao": nome, "amostra": s,
                         "prompt": rel(prompt_full), "saida": rel(saidas / jid / "test_alvo.py")})
        for k in ("first", "last", "extra"):
            pr = DADOS / "prompts" / f"tge{k}__{nome}.md"
            pr.write_text(PROMPT_TGE_COMPL[k] + SUFIXO_COMPL.format(
                fonte=bloco(fixed), teste=bloco((pasta / f"ctx_{k}.py").read_text(encoding="utf-8"))),
                encoding="utf-8")
            for s in range(1, a.amostras + 1):
                jid = f"tge{k}__{nome}__s{s}"
                jobs.append({"id": jid, "tipo": f"tge_{k}", "funcao": nome, "amostra": s,
                             "prompt": rel(pr), "saida": rel(saidas / jid / "novo_teste.py")})

    (DADOS / "jobs.json").write_text(json.dumps(jobs, indent=1, ensure_ascii=False), encoding="utf-8")
    por_tipo = {}
    for j in jobs:
        por_tipo[j["tipo"]] = por_tipo.get(j["tipo"], 0) + 1
    print(f"{len(jobs)} tarefas: {por_tipo}")
    if problemas:
        print("PROBLEMAS:\n  " + "\n  ".join(problemas))
        raise SystemExit(1)
    print("Todos os relatos reproduzem o defeito e todos os patches são não vazios.")


if __name__ == "__main__":
    main()
