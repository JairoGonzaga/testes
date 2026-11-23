"""Avalia os testes gerados no benchmark SWT-Bench / TestGenEval adaptado.

Uso:
    python benchmark/avaliar.py --modelo haiku [--journal <journal.jsonl do workflow>] [--transcricoes <pasta>]

1. (opcional) Extrai as respostas do journal do workflow para benchmark/saidas/<modelo>/<job>/.
2. SWT-Bench: roda cada test_issue.py na versão com defeito e na corrigida, com cobertura de linhas.
     aplicável (W)   — coleta sem erro e executa ≥ 1 teste nas duas versões;
     sucesso (S)     — ≥ 1 teste falha→passa (F→P) e nenhum teste falha na versão corrigida;
     F→P, F→F, P→P, P→F por teste;  cobertura do patch (ΔC) — linhas do patch executadas.
3. TestGenEval, geração completa: nucleo.avaliacao.avaliar (validade, cobertura, mutação, defeitos)
     + all-pass (todos os testes passam na referência) e any-pass.
4. TestGenEval, completar testes (first/last/extra): contexto + teste novo; pass@1 = o(s) teste(s) novo(s)
     coleta(m) e passa(m) na referência; Δ de cobertura e de mutation score sobre o contexto.
Saídas em benchmark/resultados/<modelo>/: swt.csv, tge_full.csv, tge_compl.csv, resumo.json, resumo.md.
"""

import argparse
import ast
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from math import comb
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from nucleo import avaliacao  # noqa: E402
from nucleo import config  # noqa: E402
from nucleo import funcoes as fn  # noqa: E402
from nucleo.pytest_exec import PLUGIN, rodar_pytest  # noqa: E402

BENCH = RAIZ / "benchmark"
DADOS = BENCH / "dados"
ARQ_SAIDA = {"swt_zs": "test_issue.py", "swt_agente": "test_issue.py", "tge_full": "test_alvo.py",
             "tge_first": "novo_teste.py", "tge_last": "novo_teste.py", "tge_extra": "novo_teste.py"}


# ---------------------------------------------------------------------------------
# 1. Extração das respostas
# ---------------------------------------------------------------------------------
def sem_cercas(code: str) -> str:
    linhas = code.strip("\n").split("\n")
    if linhas and linhas[0].strip().startswith("```"):
        linhas = linhas[1:]
        if linhas and linhas[-1].strip().startswith("```"):
            linhas = linhas[:-1]
    return "\n".join(linhas).rstrip() + "\n"


def ferramentas_usadas(transcricao: Path) -> dict:
    cont = defaultdict(int)
    if not transcricao.exists():
        return {}
    for linha in transcricao.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            d = json.loads(linha)
        except json.JSONDecodeError:
            continue
        c = (d.get("message") or {}).get("content")
        if isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    cont[b.get("name")] += 1
    return dict(cont)


def extrair(journal: Path, saidas: Path, jobs: dict, transcricoes: Path = None):
    rotulo, n = {}, 0
    for linha in journal.read_text(encoding="utf-8").splitlines():
        d = json.loads(linha)
        if d.get("type") == "started":
            rotulo[d["key"]] = (d.get("label"), d.get("agentId"))
        elif d.get("type") == "result" and d["key"] in rotulo:
            jid, agente = rotulo[d["key"]]
            res = d.get("result") or {}
            if jid not in jobs or not isinstance(res, dict) or not (res.get("code") or "").strip():
                continue
            pasta = saidas / jid
            pasta.mkdir(parents=True, exist_ok=True)
            (pasta / ARQ_SAIDA[jobs[jid]["tipo"]]).write_text(sem_cercas(res["code"]), encoding="utf-8")
            meta = {"agente": agente, "nota": res.get("note")}
            if transcricoes:
                meta["ferramentas"] = ferramentas_usadas(transcricoes / f"agent-{agente}.jsonl")
            (pasta / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
            n += 1
    print(f"{n} respostas extraídas para {saidas}")


# ---------------------------------------------------------------------------------
# Execução com linhas executadas (para a cobertura do patch)
# ---------------------------------------------------------------------------------
def rodar_com_linhas(arquivo_teste: Path, arquivo_alvo: Path, nome_funcao: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="bench_swt_") as tmp:
        tmp = Path(tmp)
        shutil.copy(arquivo_teste, tmp / "test_gerado.py")
        shutil.copy(arquivo_alvo, tmp / "alvo.py")
        shutil.copy(PLUGIN, tmp / "conftest.py")
        (tmp / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
        env = dict(os.environ)
        env.update({"AT_RESULTADOS": str(tmp / "resultados.json"), "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTHONHASHSEED": "0", "AT_FUNCAO": nome_funcao})
        env.pop("AT_LOG_CHAMADAS", None)
        env.pop("AT_SO_VALIDOS", None)
        cmd = [sys.executable, "-m", "pytest", "test_gerado.py", "-q", "-p", "no:cacheprovider",
               "--rootdir", str(tmp), "-c", str(tmp / "pytest.ini"), "--no-header", "-rN",
               "--cov=alvo", f"--cov-report=json:{tmp / 'cov.json'}"]
        saida = {"timeout": False, "resultados": {}, "erros_coleta": [], "linhas": []}
        try:
            proc = subprocess.run(cmd, cwd=tmp, env=env, capture_output=True, text=True,
                                  timeout=config.TIMEOUT_PYTEST_S, encoding="utf-8", errors="replace")
        except subprocess.TimeoutExpired:
            saida["timeout"] = True
            return saida
        arq = tmp / "resultados.json"
        if arq.exists():
            dados = json.loads(arq.read_text(encoding="utf-8"))
            saida["resultados"] = dados.get("resultados", {})
            saida["erros_coleta"] = dados.get("erros_coleta", [])
        elif proc.returncode != 0:
            saida["erros_coleta"].append({"nodeid": "", "erro": (proc.stdout + proc.stderr)[-2000:]})
        if (tmp / "cov.json").exists():
            cov = json.loads((tmp / "cov.json").read_text(encoding="utf-8"))
            info = next((v for k, v in cov.get("files", {}).items() if Path(k).name == "alvo.py"), None)
            if info:
                saida["linhas"] = info.get("executed_lines", [])
        return saida


# ---------------------------------------------------------------------------------
# 2. SWT-Bench
# ---------------------------------------------------------------------------------
FALHA = ("failed", "error")


def avaliar_swt(job: dict, saidas: Path) -> dict:
    inst = job["instancia"]
    pasta = DADOS / "swt" / inst
    arq = saidas / job["id"] / "test_issue.py"
    linha = {"job": job["id"], "modo": "zeroshot" if job["tipo"] == "swt_zs" else "agente", "instancia": inst,
             "funcao": job["funcao"], "amostra": job["amostra"], "gerado": arq.exists()}
    if not arq.exists():
        linha.update(aplicavel=False, sucesso=False, motivo="sem resposta")
        return linha
    nome = fn.carregar(job["funcao"]).nome_funcao
    b = rodar_com_linhas(arq, pasta / "buggy.py", nome)
    f = rodar_com_linhas(arq, pasta / "fixed.py", nome)
    rb = {k: v for k, v in b["resultados"].items() if v in ("passed",) + FALHA}
    rf = {k: v for k, v in f["resultados"].items() if v in ("passed",) + FALHA}
    aplicavel = not (b["timeout"] or f["timeout"] or b["erros_coleta"] or f["erros_coleta"]) and bool(rf)
    cat = defaultdict(int)
    for nodeid in set(rb) | set(rf):
        ob = "F" if rb.get(nodeid, "error") in FALHA else "P"
        of = "F" if rf.get(nodeid, "error") in FALHA else "P"
        cat[f"{ob}2{of}"] += 1
    sucesso = aplicavel and cat["F2P"] > 0 and cat["P2F"] == 0 and cat["F2F"] == 0
    alt = json.loads((pasta / "linhas_alteradas.json").read_text(encoding="utf-8"))
    tot = len(alt["buggy"]) + len(alt["fixed"])
    exec_b, exec_f = set(b["linhas"]), set(f["linhas"])
    cobertas = sum(1 for x in alt["buggy"] if x in exec_b) + sum(1 for x in alt["fixed"] if x in exec_f)
    linha.update(aplicavel=aplicavel, sucesso=sucesso, n_testes=len(rf) or len(rb),
                 F2P=cat["F2P"], F2F=cat["F2F"], P2P=cat["P2P"], P2F=cat["P2F"],
                 cobertura_patch=(cobertas / tot) if (tot and aplicavel) else None,
                 motivo=None if aplicavel else ("timeout" if (b["timeout"] or f["timeout"]) else "erro de coleta"))
    meta = saidas / job["id"] / "meta.json"
    dados_meta = json.loads(meta.read_text(encoding="utf-8")) if meta.exists() else {}
    if meta.exists():
        ferr = dados_meta.get("ferramentas") or {}
        linha["chamadas_bash"] = ferr.get("Bash", 0) + ferr.get("PowerShell", 0)
        linha["chamadas_ferramentas"] = sum(v for k, v in ferr.items()
                                            if k not in ("StructuredOutput", "argumentos_invalidos"))
        if job["tipo"] == "swt_agente":  # processo do agente (gerar_openrouter.py grava estes campos)
            pyt = dados_meta.get("pytests")
            linha.update(turnos=dados_meta.get("turnos"), origem_codigo=dados_meta.get("origem_codigo"),
                         finish_reason=dados_meta.get("finish_reason"),
                         argumentos_invalidos=ferr.get("argumentos_invalidos", 0),
                         custo_usd=dados_meta.get("custo_usd"),
                         rodou_pytest=None if pyt is None else bool(pyt),
                         # o teste certo FALHA no código com defeito: viu o próprio teste falhar antes de entregar?
                         viu_falhar=None if pyt is None else any(x.get("exit") not in (0, None) for x in pyt),
                         ultimo_pytest_falhou=None if not pyt else pyt[-1].get("exit") not in (0, None))
    # gerar_openrouter.py grava a sandbox de cada modelo no meta.json; o run do Haiku usa a de jobs.json
    sandbox = dados_meta.get("sandbox") or job.get("sandbox")
    if job["tipo"] == "swt_agente" and sandbox:
        sb_alvo = Path(sandbox).expanduser() / "alvo.py"
        if sb_alvo.exists():
            linha["alterou_alvo"] = sb_alvo.read_text(encoding="utf-8") != (pasta / "buggy.py").read_text(encoding="utf-8")
    return linha


# ---------------------------------------------------------------------------------
# 3 e 4. TestGenEval
# ---------------------------------------------------------------------------------
def metricas_avaliar(r: dict) -> dict:
    return {k: r.get(k) for k in ("utilizavel", "n_testes", "n_validos", "falsos_alarmes", "cobertura_linhas",
                                  "cobertura_ramos", "mutation_score", "deteccao_defeitos", "motivo")}


def avaliar_tge_full(job: dict, saidas: Path) -> dict:
    arq = saidas / job["id"] / "test_alvo.py"
    linha = {"job": job["id"], "funcao": job["funcao"], "amostra": job["amostra"], "gerado": arq.exists()}
    r = avaliacao.avaliar(fn.carregar(job["funcao"]), arq, com_mutantes=True)
    linha.update(metricas_avaliar(r))
    ok = bool(r.get("utilizavel"))
    linha["all_pass"] = ok and r["n_validos"] == r["n_testes"]
    linha["any_pass"] = ok and r["n_validos"] > 0
    return linha


def nomes_testes(codigo: str) -> list:
    try:
        arvore = ast.parse(codigo)
    except SyntaxError:
        return []
    return [n.name for n in arvore.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            and n.name.startswith("test")]


_cache_ctx = {}


def avaliar_ctx(nome: str, k: str) -> dict:
    chave = (nome, k)
    if chave not in _cache_ctx:
        _cache_ctx[chave] = avaliacao.avaliar(fn.carregar(nome), DADOS / "tge" / nome / f"ctx_{k}.py", com_mutantes=True)
    return _cache_ctx[chave]


def avaliar_tge_compl(job: dict, saidas: Path) -> dict:
    k = job["tipo"].split("_")[1]
    nome = job["funcao"]
    arq = saidas / job["id"] / "novo_teste.py"
    linha = {"job": job["id"], "modo": k, "funcao": nome, "amostra": job["amostra"], "gerado": arq.exists(),
             "pass": False}
    if not arq.exists():
        linha["motivo"] = "sem resposta"
        return linha
    novo = arq.read_text(encoding="utf-8")
    ctx = (DADOS / "tge" / nome / f"ctx_{k}.py").read_text(encoding="utf-8")
    novos = nomes_testes(novo)
    linha["n_funcoes_novas"] = len(novos)
    combinado = saidas / job["id"] / "combinado.py"
    combinado.write_text(ctx.rstrip() + "\n\n\n" + novo, encoding="utf-8")
    funcao = fn.carregar(nome)
    ref = rodar_pytest(combinado, funcao.referencia, funcao.nome_funcao)
    if ref["timeout"] or ref["erros_coleta"]:
        linha["motivo"] = "timeout" if ref["timeout"] else "erro de coleta"
        return linha
    if not novos:
        linha["motivo"] = "nenhuma função de teste nova"
        return linha
    res_novos = {n: o for n, o in ref["resultados"].items()
                 if n.split("::")[-1].split("[")[0] in novos and o in ("passed", "failed", "error")}
    linha["n_casos_novos"] = len(res_novos)
    linha["pass"] = bool(res_novos) and all(o == "passed" for o in res_novos.values())
    if not res_novos:
        linha["motivo"] = "teste novo não coletado"
    # contribuição do teste novo: Δ cobertura e Δ mutation score sobre o contexto (só testes válidos contam)
    base = avaliar_ctx(nome, k)
    r = avaliacao.avaliar(funcao, combinado, com_mutantes=True)
    for m in ("cobertura_linhas", "cobertura_ramos", "mutation_score", "deteccao_defeitos"):
        if r.get(m) is not None and base.get(m) is not None:
            linha[f"delta_{m}"] = r[m] - base[m]
    return linha


# ---------------------------------------------------------------------------------
# Agregação
# ---------------------------------------------------------------------------------
def pass_at_k(n, c, k):
    if n - c < k:
        return 1.0
    return 1.0 - comb(n - c, k) / comb(n, k)


def media(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def por_grupo(linhas, chave_grupo, chave_ok, ks=(1, 3)):
    grupos = defaultdict(list)
    for l in linhas:
        grupos[l[chave_grupo]].append(bool(l.get(chave_ok)))
    out = {}
    for k in ks:
        vals = [pass_at_k(len(v), sum(v), k) for v in grupos.values() if len(v) >= k]
        out[f"pass@{k}"] = media(vals)
    return out


def salvar_csv(linhas, destino: Path):
    if not linhas:
        return
    campos = []
    for l in linhas:
        for c in l:
            if c not in campos:
                campos.append(c)
    with destino.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)


def pct(x):
    return "—" if x is None else f"{100 * x:.1f}%"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modelo", default="haiku")
    p.add_argument("--journal", help="journal.jsonl do workflow (extrai as respostas antes de avaliar)")
    p.add_argument("--transcricoes", help="pasta com agent-<id>.jsonl (conta ferramentas usadas)")
    p.add_argument("--workers", type=int, default=config.WORKERS)
    p.add_argument("--amostras", type=int, nargs="*", help="só estas amostras (ex.: --amostras 1)")
    p.add_argument("--tipos", nargs="*", help="só estes tipos de tarefa (ex.: swt_zs tge_full)")
    p.add_argument("--rotulo", help="nome da pasta em resultados/ (padrão: o do modelo)")
    p.add_argument("--limite", type=int,
                   help="só as N primeiras tarefas de cada tipo (o mesmo subconjunto do --limite do gerar_openrouter.py)")
    a = p.parse_args()

    jobs = {j["id"]: j for j in json.loads((DADOS / "jobs.json").read_text(encoding="utf-8"))}
    saidas = BENCH / "saidas" / a.modelo
    if a.journal:
        extrair(Path(a.journal), saidas, jobs, Path(a.transcricoes) if a.transcricoes else None)
    if a.amostras:
        jobs = {k: j for k, j in jobs.items() if j["amostra"] in a.amostras}
    if a.tipos:
        jobs = {k: j for k, j in jobs.items() if j["tipo"] in a.tipos}
    if a.limite:
        contagem = {}
        for k, j in list(jobs.items()):
            contagem[j["tipo"]] = contagem.get(j["tipo"], 0) + 1
            if contagem[j["tipo"]] > a.limite:
                del jobs[k]
    destino = BENCH / "resultados" / (a.rotulo or a.modelo)
    destino.mkdir(parents=True, exist_ok=True)

    swt_jobs = [j for j in jobs.values() if j["tipo"].startswith("swt")]
    with ThreadPoolExecutor(a.workers) as ex:
        swt = list(ex.map(lambda j: avaliar_swt(j, saidas), swt_jobs))
    print(f"SWT: {len(swt)} avaliados")
    full = [avaliar_tge_full(j, saidas) for j in jobs.values() if j["tipo"] == "tge_full"]
    print(f"TGE full: {len(full)} avaliados")
    compl = [avaliar_tge_compl(j, saidas) for j in jobs.values() if j["tipo"] in ("tge_first", "tge_last", "tge_extra")]
    print(f"TGE completar: {len(compl)} avaliados")

    salvar_csv(swt, destino / "swt.csv")
    salvar_csv(full, destino / "tge_full.csv")
    salvar_csv(compl, destino / "tge_compl.csv")

    # ---- resumo ----
    resumo = {"modelo": a.modelo, "swt": {}, "tge_full": {}, "tge_compl": {}}
    for modo in ("zeroshot", "agente"):
        ls = [l for l in swt if l["modo"] == modo]
        ap = [l for l in ls if l["aplicavel"]]
        resumo["swt"][modo] = {
            "n": len(ls), "gerados": sum(l["gerado"] for l in ls),
            "W": media([l["aplicavel"] for l in ls]), "S": media([l["sucesso"] for l in ls]),
            "F2P_algum": media([l.get("F2P", 0) > 0 for l in ls]),
            "P2F_algum": media([l.get("P2F", 0) > 0 for l in ap]),
            "cobertura_patch": media([l.get("cobertura_patch") for l in ap]),
            "cobertura_patch_sucesso": media([l.get("cobertura_patch") for l in ls if l["sucesso"]]),
            **por_grupo(ls, "instancia", "sucesso"),
            "por_funcao": {f: media([l["sucesso"] for l in ls if l["funcao"] == f])
                           for f in sorted({l["funcao"] for l in ls})},
            "por_instancia": {i: sum(l["sucesso"] for l in ls if l["instancia"] == i)
                              for i in sorted({l["instancia"] for l in ls})},
        }
        if modo == "agente":
            resumo["swt"][modo]["chamadas_bash_media"] = media([l.get("chamadas_bash") for l in ls])
            resumo["swt"][modo]["alterou_alvo"] = sum(bool(l.get("alterou_alvo")) for l in ls)
            custos = [l.get("custo_usd") for l in ls if l.get("custo_usd") is not None]
            n_suc = sum(l["sucesso"] for l in ls)
            resumo["swt"][modo]["processo"] = {
                "turnos_media": media([l.get("turnos") for l in ls]),
                "rodou_pytest": media([l.get("rodou_pytest") for l in ls]),
                "viu_falhar": media([l.get("viu_falhar") for l in ls]),
                "ultimo_pytest_falhou": media([l.get("ultimo_pytest_falhou") for l in ls]),
                "entregou_arquivo": media([None if l.get("origem_codigo") is None else l["origem_codigo"] == "arquivo"
                                           for l in ls]),
                "limite_turnos": sum(l.get("finish_reason") == "limite_de_turnos" for l in ls),
                "argumentos_invalidos": sum(l.get("argumentos_invalidos") or 0 for l in ls),
                "sucesso_se_rodou_pytest": media([l["sucesso"] for l in ls if l.get("rodou_pytest")]),
                "sucesso_se_nao_rodou": media([l["sucesso"] for l in ls if l.get("rodou_pytest") is False]),
                "custo_total_usd": sum(custos) if custos else None,
                "custo_por_sucesso_usd": (sum(custos) / n_suc) if (custos and n_suc) else None,
            }
    resumo["tge_full"] = {
        "n": len(full),
        "utilizavel": media([l["utilizavel"] for l in full]),
        **{f"all_pass_{k}": v for k, v in por_grupo(full, "funcao", "all_pass").items()},
        **{f"any_pass_{k}": v for k, v in por_grupo(full, "funcao", "any_pass").items()},
        "falsos_alarmes": media([l.get("falsos_alarmes") for l in full]),
        "n_testes": media([l.get("n_testes") for l in full]),
        "cobertura_linhas": media([l.get("cobertura_linhas") for l in full]),
        "cobertura_ramos": media([l.get("cobertura_ramos") for l in full]),
        "mutation_score": media([l.get("mutation_score") for l in full]),
        "deteccao_defeitos": media([l.get("deteccao_defeitos") for l in full]),
        "por_funcao": {f: {m: media([l.get(m) for l in full if l["funcao"] == f])
                           for m in ("all_pass", "cobertura_linhas", "cobertura_ramos", "mutation_score",
                                     "deteccao_defeitos", "falsos_alarmes")}
                       for f in sorted({l["funcao"] for l in full})},
    }
    for k in ("first", "last", "extra"):
        ls = [l for l in compl if l["modo"] == k]
        resumo["tge_compl"][k] = {
            "n": len(ls), **por_grupo(ls, "funcao", "pass"),
            **{f"delta_{m}": media([l.get(f"delta_{m}") for l in ls])
               for m in ("cobertura_linhas", "cobertura_ramos", "mutation_score", "deteccao_defeitos")},
            "motivos_falha": {m: sum(1 for l in ls if l.get("motivo") == m)
                              for m in sorted({l.get("motivo") for l in ls if l.get("motivo")})},
        }
    resumo["base_ctx"] = {f"{n}/{k}": metricas_avaliar(v) for (n, k), v in _cache_ctx.items()}
    (destino / "resumo.json").write_text(json.dumps(resumo, indent=1, ensure_ascii=False), encoding="utf-8")

    s, t, c = resumo["swt"], resumo["tge_full"], resumo["tge_compl"]
    md = [f"# Benchmark SWT-Bench + TestGenEval (adaptado) — modelo: {a.modelo}", "",
          "## SWT-Bench (reprodução de issue, 23 instâncias × 3 amostras)", "",
          "| Modo | W (aplicável) | S (sucesso) | pass@1 | pass@3 | algum F→P | algum P→F | ΔC patch | ΔC (sucessos) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for modo in ("zeroshot", "agente"):
        r = s[modo]
        md.append(f"| {modo} | {pct(r['W'])} | {pct(r['S'])} | {pct(r['pass@1'])} | {pct(r['pass@3'])} | "
                  f"{pct(r['F2P_algum'])} | {pct(r['P2F_algum'])} | {pct(r['cobertura_patch'])} | "
                  f"{pct(r['cobertura_patch_sucesso'])} |")
    pr = s["agente"].get("processo") or {}
    if pr.get("turnos_media") is not None:
        custo = pr.get("custo_por_sucesso_usd")
        md += ["", "## Processo do agente (SWT modo agente)", "",
               f"- turnos por tarefa: {pr['turnos_media']:.1f}; bateu o limite de turnos: {pr['limite_turnos']}; "
               f"argumentos de ferramenta inválidos: {pr['argumentos_invalidos']}",
               f"- rodou pytest antes de entregar: {pct(pr['rodou_pytest'])}; viu o próprio teste falhar no código "
               f"com defeito: {pct(pr['viu_falhar'])}; último pytest falhando (o esperado): "
               f"{pct(pr['ultimo_pytest_falhou'])}",
               f"- S quando rodou pytest: {pct(pr['sucesso_se_rodou_pytest'])}; S quando não rodou: "
               f"{pct(pr['sucesso_se_nao_rodou'])}; entregou via arquivo: {pct(pr['entregou_arquivo'])}",
               f"- custo por sucesso: {'—' if custo is None else f'US$ {custo:.4f}'}"]
    md += ["", "## TestGenEval — geração completa (6 funções × 3 amostras)", "",
           f"- utilizável: {pct(t['utilizavel'])}; all-pass pass@1 {pct(t['all_pass_pass@1'])}, "
           f"pass@3 {pct(t['all_pass_pass@3'])}; any-pass pass@1 {pct(t['any_pass_pass@1'])}",
           f"- testes por arquivo: {t['n_testes'] or 0:.1f}; falsos alarmes: {pct(t['falsos_alarmes'])}",
           f"- cobertura de linhas {pct(t['cobertura_linhas'])}, de ramos {pct(t['cobertura_ramos'])}; "
           f"mutation score {pct(t['mutation_score'])}; detecção de defeitos {pct(t['deteccao_defeitos'])}",
           "", "## TestGenEval — completar testes (6 funções × 3 amostras por cenário)", "",
           "| Cenário | pass@1 | pass@3 | Δ linhas | Δ ramos | Δ mutation | Δ defeitos |", "|---|---|---|---|---|---|---|"]
    for k in ("first", "last", "extra"):
        r = c[k]
        md.append(f"| {k} | {pct(r['pass@1'])} | {pct(r['pass@3'])} | {pct(r['delta_cobertura_linhas'])} | "
                  f"{pct(r['delta_cobertura_ramos'])} | {pct(r['delta_mutation_score'])} | "
                  f"{pct(r['delta_deteccao_defeitos'])} |")
    (destino / "resumo.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
