"""Junta os resumos de vários modelos numa tabela comparativa.

Lê `resultados/<modelo>/resumo.json` (de avaliar.py) e, quando existe, `saidas/<modelo>/_uso.json`
(custo e tokens, de gerar_openrouter.py). Grava `resultados/comparativo.md` e `resultados/comparativo.csv`.

Uso:
    python benchmark/comparar.py                       # todos os modelos avaliados
    python benchmark/comparar.py --modelos haiku qwen3.7-flash
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BENCH = Path(__file__).resolve().parent
RES = BENCH / "resultados"

# (coluna, caminho no resumo.json, é percentual?)
COLUNAS = [
    ("SWT zs S", ("swt", "zeroshot", "S"), True),
    ("SWT zs pass@3", ("swt", "zeroshot", "pass@3"), True),
    ("SWT zs ΔC", ("swt", "zeroshot", "cobertura_patch"), True),
    ("SWT ag S", ("swt", "agente", "S"), True),
    ("SWT ag pass@3", ("swt", "agente", "pass@3"), True),
    ("SWT ag W", ("swt", "agente", "W"), True),
    ("SWT ag execuções", ("swt", "agente", "chamadas_bash_media"), False),
    ("ag turnos", ("swt", "agente", "processo", "turnos_media"), False),
    ("ag rodou pytest", ("swt", "agente", "processo", "rodou_pytest"), True),
    ("ag viu falhar", ("swt", "agente", "processo", "viu_falhar"), True),
    ("TGE all-pass", ("tge_full", "all_pass_pass@1"), True),
    ("TGE any-pass", ("tge_full", "any_pass_pass@1"), True),
    ("TGE linhas", ("tge_full", "cobertura_linhas"), True),
    ("TGE ramos", ("tge_full", "cobertura_ramos"), True),
    ("TGE mutação", ("tge_full", "mutation_score"), True),
    ("TGE defeitos", ("tge_full", "deteccao_defeitos"), True),
    ("TGE falsos alarmes", ("tge_full", "falsos_alarmes"), True),
    ("first pass@1", ("tge_compl", "first", "pass@1"), True),
    ("first Δmut", ("tge_compl", "first", "delta_mutation_score"), True),
    ("last pass@1", ("tge_compl", "last", "pass@1"), True),
    ("extra pass@1", ("tge_compl", "extra", "pass@1"), True),
]


def pegar(d, caminho):
    for k in caminho:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def fmt(v, pct):
    if v is None:
        return "–"
    return f"{100 * v:.1f}%" if pct else f"{v:.1f}"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--modelos", nargs="*", help="rótulos (pastas de resultados/); padrão: todos")
    a = p.parse_args()
    nomes = a.modelos or sorted(x.name for x in RES.iterdir() if (x / "resumo.json").exists())
    linhas = []
    for n in nomes:
        r = json.loads((RES / n / "resumo.json").read_text(encoding="utf-8"))
        uso_arq = BENCH / "saidas" / n / "_uso.json"
        uso = json.loads(uso_arq.read_text(encoding="utf-8")) if uso_arq.exists() else {}
        linha = {"modelo": n, "id": uso.get("modelo_id", n), "custo_usd": uso.get("custo_usd"),
                 "tokens_saida": uso.get("tokens_saida"), "truncadas": uso.get("truncadas")}
        for col, cam, _ in COLUNAS:
            linha[col] = pegar(r, cam)
        linhas.append(linha)

    with open(RES / "comparativo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)

    md = ["# Comparativo entre modelos", "",
          "S = sucesso SWT (falha no código com defeito, passa no corrigido); ΔC = cobertura das linhas do patch; "
          "ag = modo agente (turnos, % que rodou pytest, % que viu o próprio teste falhar no código com defeito); "
          "TGE = suíte completa (pass@1 da amostra); first/last/extra = completar testes.", ""]
    cab = ["Modelo", "Custo (US$)"] + [c for c, _, _ in COLUNAS]
    md += ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for l in linhas:
        custo = "–" if l["custo_usd"] is None else f"{l['custo_usd']:.3f}"
        md.append("| " + " | ".join([l["modelo"], custo] + [fmt(l[c], pct) for c, _, pct in COLUNAS]) + " |")
    (RES / "comparativo.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
