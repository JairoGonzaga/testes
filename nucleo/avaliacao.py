"""Cálculo das métricas automáticas de um arquivo de testes (passo 4 da metodologia).

- utilizável: o pytest coleta pelo menos um teste, sem erro de sintaxe ou importação;
- teste válido: passa na versão de referência;
- falsos alarmes: testes que falham na referência ÷ testes executados;
- detecção de defeitos: versões defeituosas com ≥ 1 teste válido falhando ÷ versões;
- mutation score: mutantes mortos ÷ (mutantes − equivalentes);
- cobertura de fronteiras: fronteiras do gabarito exercitadas por testes válidos ÷ total;
- cobertura de ramos (auxiliar): coverage.py rodando só os testes válidos.
"""

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import config
from .criterios import satisfaz
from .pytest_exec import rodar_pytest

EXECUTADO = ("passed", "failed", "error")


def _detectou(resultado: dict, validos: list) -> bool:
    if resultado.get("timeout"):
        return True  # laço infinito ou travamento conta como detectado
    if resultado.get("erros_coleta"):
        return True  # a versão nem pôde ser importada
    return any(resultado["resultados"].get(n) in ("failed", "error") for n in validos)


def cobertura_fronteiras(funcao, chamadas: list, validos: set) -> dict:
    fronteiras = funcao.gabarito.get("fronteiras", [])
    argumentos = [c["args"] for c in chamadas if c.get("teste") in validos]
    cobertas = [f["id"] for f in fronteiras if any(satisfaz(f["criterio"], a) for a in argumentos)]
    total = len(fronteiras)
    return {"total": total, "cobertas": cobertas,
            "nao_cobertas": [f["id"] for f in fronteiras if f["id"] not in cobertas],
            "taxa": (len(cobertas) / total) if total else None}


def avaliar(funcao, arquivo_teste: Path, pasta_saida: Path = None, com_mutantes=True,
            workers=None) -> dict:
    workers = workers or config.WORKERS
    r = {"utilizavel": False, "motivo": None}
    if not Path(arquivo_teste).exists():
        r["motivo"] = "nenhum arquivo de teste foi gerado"
        return r

    ref = rodar_pytest(arquivo_teste, funcao.referencia, funcao.nome_funcao, registrar_chamadas=True,
                       junit=(pasta_saida / "junit_referencia.xml") if pasta_saida else None)
    if ref["timeout"]:
        r["motivo"] = "tempo esgotado na versão de referência"
        return r
    if ref["erros_coleta"]:
        r["motivo"] = "erro de coleta (sintaxe/importação)"
        r["erro_coleta"] = ref["erros_coleta"][0]["erro"][-1500:]
        return r
    executados = {n: o for n, o in ref["resultados"].items() if o in EXECUTADO}
    if not executados:
        r["motivo"] = "nenhum teste coletado"
        return r

    validos = [n for n, o in executados.items() if o == "passed"]
    r.update({
        "utilizavel": True,
        "n_testes": len(executados),
        "n_validos": len(validos),
        "falsos_alarmes": (len(executados) - len(validos)) / len(executados),
        "testes_referencia": executados,
        "mensagens_referencia": ref.get("mensagens", {}),
    })

    # argumentos observados por teste (ajuda a revisão manual)
    por_teste = {}
    for c in ref["chamadas"]:
        if c.get("teste"):
            por_teste.setdefault(c["teste"], [])
            if len(por_teste[c["teste"]]) < 5:
                por_teste[c["teste"]].append(c["args"])
    r["chamadas_por_teste"] = por_teste
    r["fronteiras"] = cobertura_fronteiras(funcao, ref["chamadas"], set(validos))
    r["cobertura_fronteiras"] = r["fronteiras"]["taxa"]

    # cobertura de ramos só com os testes válidos
    r["cobertura_ramos"] = r["cobertura_linhas"] = None
    if validos:
        cov = rodar_pytest(arquivo_teste, funcao.referencia, funcao.nome_funcao, so_validos=validos,
                           cobertura=True)
        resumo = cov.get("cobertura")
        if resumo:
            if resumo.get("num_branches"):
                r["cobertura_ramos"] = resumo["covered_branches"] / resumo["num_branches"]
            if resumo.get("num_statements"):
                r["cobertura_linhas"] = resumo["covered_lines"] / resumo["num_statements"]
        else:
            r["aviso_cobertura"] = "pytest-cov não disponível ou falhou"

    # versões defeituosas e mutantes
    versoes = [("defeito", p) for p in funcao.defeitos]
    if com_mutantes:
        versoes += [("mutante", p) for p in funcao.mutantes]

    def rodar(item):
        tipo, caminho = item
        if not validos:
            return tipo, caminho.stem, False
        res = rodar_pytest(arquivo_teste, caminho, funcao.nome_funcao)
        return tipo, caminho.stem, _detectou(res, validos)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        resultados = list(pool.map(rodar, versoes))

    defeitos = {nome: det for tipo, nome, det in resultados if tipo == "defeito"}
    r["defeitos"] = defeitos
    r["deteccao_defeitos"] = (sum(defeitos.values()) / len(defeitos)) if defeitos else None

    if com_mutantes:
        equivalentes = funcao.equivalentes
        mutantes = {nome: det for tipo, nome, det in resultados if tipo == "mutante"}
        considerados = {n: d for n, d in mutantes.items() if n not in equivalentes}
        mortos = sum(considerados.values())
        r["mutantes"] = {"total": len(mutantes), "equivalentes": len(mutantes) - len(considerados),
                         "mortos": mortos,
                         "sobreviventes": sorted(n for n, d in considerados.items() if not d)}
        r["mutation_score"] = (mortos / len(considerados)) if considerados else None
    return r


def salvar(resultado: dict, caminho: Path):
    caminho.write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=repr), encoding="utf-8")
