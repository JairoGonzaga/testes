"""Passo 6 (análise): consolida tudo em CSV e faz a comparação pareada B − A por função.

Uso:
    python analisar.py                       # execucoes/ + revisao/revisao_final.xlsx
    python analisar.py --entrada execucoes_fake
    python analisar.py --revisao revisao/planilha_revisor1.xlsx   # usar uma planilha específica

Saídas (pasta resultados/):
    execucoes.csv      uma linha por execução (função × condição × repetição)
    por_funcao.csv     mediana das repetições por função e condição, e a diferença B − A
    resumo.md          tabelas prontas para o relatório
    comparacao.png     gráfico pareado A × B por função, uma área por métrica

Decisão registrada: uma execução NÃO utilizável (erro de sintaxe/importação) entra com 0 nas
métricas de detecção e cobertura (o arquivo entregue não serve para nada) e fica de fora das
métricas de oráculo (falsos alarmes, expectativas corretas), que não existem sem testes.
Use --ignorar-inutilizaveis para tirá-las de todas as métricas.
"""

import argparse
import json
import math
from pathlib import Path

import pandas as pd

from nucleo import config, funcoes as fn
from revisao import CLASSES, fontes_dos_testes, regra_sugerida

# (coluna, rótulo, questão, principal?, maior_e_melhor)
METRICAS = [
    ("expectativas_corretas", "Expectativas corretas", "QP1", True, True),
    ("falsos_alarmes", "Falsos alarmes", "QP1", False, False),
    ("deteccao_defeitos", "Detecção de defeitos", "QP2", True, True),
    ("mutation_score", "Mutation score", "QP2", False, True),
    ("cobertura_regras", "Cobertura de regras (revisão)", "QP3", True, True),
    ("cobertura_regras_auto", "Cobertura de regras (automática)", "QP3", False, True),
    ("cobertura_fronteiras", "Cobertura de fronteiras", "QP3", False, True),
    ("cobertura_ramos", "Cobertura de ramos (auxiliar)", "QP3", False, True),
    ("utilizavel", "Execuções utilizáveis", "QP4", True, True),
]
CUSTO = [("n_testes", "Testes gerados (casos)"), ("n_validos", "Testes válidos"), ("chamadas", "Chamadas"), ("tokens_entrada", "Tokens de entrada"), ("tokens_saida", "Tokens de saída"),
         ("tempo_total_s", "Tempo (s)"), ("testes_incorretos", "Testes a corrigir à mão")]
ZERAR_SE_INUTILIZAVEL = ["deteccao_defeitos", "mutation_score", "cobertura_regras", "cobertura_regras_auto",
                         "cobertura_fronteiras", "cobertura_ramos"]
COR_A, COR_B, TINTA, TINTA_2, GRADE = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df"


def carregar_execucoes(entrada: Path) -> pd.DataFrame:
    linhas = []
    for pasta in sorted(d for d in entrada.iterdir() if (d / "meta.json").exists()):
        meta = json.loads((pasta / "meta.json").read_text(encoding="utf-8"))
        res_arq = pasta / "resultado.json"
        res = json.loads(res_arq.read_text(encoding="utf-8")) if res_arq.exists() else None
        funcao = fn.carregar(meta["funcao"])
        linha = {k: meta.get(k) for k in ("run_id", "funcao", "condicao", "repeticao", "provedor", "modelo",
                                          "status", "chamadas", "tokens_entrada", "tokens_saida",
                                          "tempo_total_s", "reparos", "versao_prompts")}
        linha["avaliada"] = res is not None
        linha["utilizavel"] = float(bool(res and res.get("utilizavel")))
        if res and res.get("utilizavel"):
            for k in ("n_testes", "n_validos", "falsos_alarmes", "deteccao_defeitos", "mutation_score",
                      "cobertura_fronteiras", "cobertura_ramos"):
                linha[k] = res.get(k)
            # cobertura de regras automática: regras testáveis com ≥ 1 teste válido marcado com a regra
            fontes = fontes_dos_testes((pasta / "test_gerado.py").read_text(encoding="utf-8"))
            cobertas = set()
            for nodeid, resultado in res["testes_referencia"].items():
                if resultado != "passed":
                    continue
                item = "::".join(nodeid.split("::")[1:])
                nome = item.split("[")[0]
                for r in regra_sugerida(item + "\n" + fontes.get(nome, "")).split(", "):
                    cobertas.add(r)
            testaveis = set(funcao.regras_testaveis)
            linha["cobertura_regras_auto"] = len(cobertas & testaveis) / len(testaveis) if testaveis else None
            linha["_testaveis"] = sorted(testaveis)
        else:
            linha["_testaveis"] = sorted(funcao.regras_testaveis)
        linhas.append(linha)
    return pd.DataFrame(linhas)


def juntar_revisao(df: pd.DataFrame, arquivo: Path, chave: Path) -> pd.DataFrame:
    rev = pd.read_excel(arquivo, sheet_name="revisao")
    rev["classificacao"] = rev["classificacao"].fillna("").astype(str).str.strip().str.lower()
    rev["regra"] = rev["regra"].fillna("").astype(str).str.strip().str.upper()
    pendentes = (~rev["classificacao"].isin(CLASSES)).sum()
    if pendentes:
        print(f"Atenção: {pendentes} linha(s) da revisão sem classificação final — ficam de fora.")
    rev = rev[rev["classificacao"].isin(CLASSES)]
    ch = pd.read_csv(chave, encoding="utf-8-sig")
    rev = rev.merge(ch[["id_cego", "run_id"]], on="id_cego", how="inner")
    agreg = []
    for run_id, g in rev.groupby("run_id"):
        corretos = g[g["classificacao"] == "correto"]
        agreg.append({"run_id": run_id, "n_revisados": len(g), "n_corretos": len(corretos),
                      "testes_incorretos": int((g["classificacao"] == "incorreto").sum()),
                      "n_inconclusivos": int((g["classificacao"] == "inconclusivo").sum()),
                      "_regras_corretas": set(corretos["regra"])})
    agreg = pd.DataFrame(agreg)
    df = df.merge(agreg, on="run_id", how="left")
    df["expectativas_corretas"] = df["n_corretos"] / df["n_revisados"]
    amostral = (df["n_revisados"] < df["n_testes"]).sum()
    if amostral:
        print(f"Atenção: em {amostral} execução(ões) só parte dos testes foi revisada (amostra). A cobertura "
              "de regras pela revisão fica subestimada; use a cobertura de regras automática no relatório.")
    df["cobertura_regras"] = [
        (len(rc & set(t)) / len(t)) if isinstance(rc, set) and t else math.nan
        for rc, t in zip(df["_regras_corretas"], df["_testaveis"])]
    return df


def pct(x):
    return "–" if pd.isna(x) else f"{x:.0%}"


def num(x):
    if pd.isna(x):
        return "–"
    if abs(x) >= 100 or float(x).is_integer():
        return f"{x:,.0f}".replace(",", ".")
    return f"{x:.1f}".replace(".", ",")


def dif(x, eh_pct=True):
    if pd.isna(x):
        return "–"
    if eh_pct:
        return f"{x * 100:+.0f} p.p."
    return f"{x:+,.0f}".replace(",", ".") if abs(x) >= 10 else f"{x:+.1f}".replace(".", ",")


def tabela_md(cab, linhas):
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cab) + "|"]
    out += ["| " + " | ".join(str(c) for c in l) + " |" for l in linhas]
    return "\n".join(out)


def comparar(df: pd.DataFrame, coluna: str):
    """Mediana das repetições por função × condição; devolve tabela com A, B e B − A.

    Para "utilizavel" (sim/não) usa a proporção das repetições, não a mediana."""
    if coluna not in df or df[coluna].notna().sum() == 0:
        return None
    grupos = df.groupby(["funcao", "condicao"])[coluna]
    p = (grupos.mean() if coluna == "utilizavel" else grupos.median()).unstack("condicao")
    if not {"A", "B"} <= set(p.columns):
        return None
    p = p[["A", "B"]]
    p["B_menos_A"] = p["B"] - p["A"]
    return p


def grafico(df, metricas, destino: Path, titulo: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    paineis = [(c, r) for c, r, *_ in metricas if comparar(df, c) is not None]
    if not paineis:
        return
    ncols = 3
    nrows = math.ceil(len(paineis) / ncols)
    fig, eixos = plt.subplots(nrows, ncols, figsize=(4.2 * ncols, (0.42 * df["funcao"].nunique() + 1.1) * nrows + 0.6),
                              squeeze=False)
    plt.rcParams["font.size"] = 9
    for ax in eixos.flat[len(paineis):]:
        ax.axis("off")
    for ax, (col, rotulo) in zip(eixos.flat, paineis):
        p = comparar(df, col).sort_index(ascending=False)
        ys = range(len(p))
        d = 0.14  # A um pouco acima e B um pouco abaixo, para nunca se esconderem
        for y, (_, row) in zip(ys, p.iterrows()):
            if pd.notna(row["A"]) and pd.notna(row["B"]):
                ax.plot([row["A"], row["B"]], [y + d, y - d], color=GRADE, linewidth=2, zorder=1,
                        solid_capstyle="round")
        ax.scatter(p["A"], [y + d for y in ys], s=46, color=COR_A, zorder=3, edgecolors="white",
                   linewidths=1.5, label="A — direta")
        ax.scatter(p["B"], [y - d for y in ys], s=46, color=COR_B, zorder=3, edgecolors="white",
                   linewidths=1.5, label="B — agente")
        ax.set_ylim(-0.6, len(p) - 0.4)
        ax.set_yticks(list(ys), p.index, color=TINTA_2)
        ax.set_xlim(-0.05, 1.05)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"], color=TINTA_2)
        ax.set_title(rotulo, loc="left", color=TINTA, fontsize=10)
        ax.grid(axis="x", color=GRADE, linewidth=0.6)
        ax.set_axisbelow(True)
        for lado in ("top", "right", "left"):
            ax.spines[lado].set_visible(False)
        ax.spines["bottom"].set_color(GRADE)
        ax.tick_params(length=0)
    alcas, nomes = eixos.flat[0].get_legend_handles_labels()
    fig.legend(alcas, nomes, loc="upper right", ncol=2, frameon=False, labelcolor=TINTA_2)
    fig.suptitle(titulo, x=0.01, ha="left", color=TINTA, fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(destino, dpi=200, facecolor="#fcfcfb")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--entrada", default="execucoes")
    p.add_argument("--revisao", default=None, help="planilha de revisão (padrão: revisao*/revisao_final.xlsx)")
    p.add_argument("--ignorar-inutilizaveis", action="store_true")
    a = p.parse_args()

    entrada = config.RAIZ / a.entrada
    sufixo = entrada.name.replace("execucoes", "")
    pasta_rev = config.RAIZ / f"revisao{sufixo}"
    saida = config.RAIZ / f"resultados{sufixo}"
    saida.mkdir(parents=True, exist_ok=True)

    df = carregar_execucoes(entrada)
    if df.empty:
        raise SystemExit(f"Nenhuma execução em {entrada}.")
    com_erro = df["status"].isin(["erro", "pendente"])
    if com_erro.any():
        print(f"Atenção: {com_erro.sum()} execução(ões) com erro ou pendentes ficam de fora "
              f"(refaça com gerar.py): {', '.join(df.loc[com_erro, 'run_id'])}")
        df = df[~com_erro]
    if (~df["avaliada"]).any():
        print(f"Atenção: {(~df['avaliada']).sum()} execução(ões) sem resultado.json — rode executar.py.")
    falso = (df["provedor"] == "fake").any()

    arq_rev = Path(a.revisao) if a.revisao else pasta_rev / "revisao_final.xlsx"
    tem_revisao = arq_rev.exists() and (pasta_rev / "chave.csv").exists()
    if tem_revisao:
        df = juntar_revisao(df, arq_rev, pasta_rev / "chave.csv")
        print(f"Revisão manual: {arq_rev.relative_to(config.RAIZ) if arq_rev.is_relative_to(config.RAIZ) else arq_rev}")
    else:
        print("Sem revisão manual ainda: QP1 (expectativas corretas) e QP3 (cobertura de regras pela revisão) "
              "ficam em branco.")
        for c in ("expectativas_corretas", "cobertura_regras", "testes_incorretos"):
            df[c] = math.nan

    inutil = df["utilizavel"] == 0
    if a.ignorar_inutilizaveis:
        df = df[~inutil]
    else:
        for c in ZERAR_SE_INUTILIZAVEL:
            if c in df:
                df.loc[inutil & df["avaliada"], c] = 0.0

    colunas_csv = [c for c in df.columns if not c.startswith("_")]
    df[colunas_csv].to_csv(saida / "execucoes.csv", index=False, encoding="utf-8-sig")

    # ---------------- comparação pareada ----------------
    linhas_resumo, por_funcao = [], []
    for col, rotulo, qp, principal, maior_melhor in METRICAS:
        c = comparar(df, col)
        if c is None:
            continue
        validos = c.dropna(subset=["B_menos_A"])
        d = validos["B_menos_A"]
        tol = 1e-9
        if col == "utilizavel":  # proporção sobre todas as execuções
            va, vb = (df.loc[df["condicao"] == k, col].mean() for k in ("A", "B"))
        else:
            va, vb = c["A"].median(), c["B"].median()
        linhas_resumo.append([qp, ("**" + rotulo + "**") if principal else rotulo,
                              pct(va), pct(vb), dif(d.median()),
                              f"{(d > tol).sum()} / {(d.abs() <= tol).sum()} / {(d < -tol).sum()}",
                              "maior" if maior_melhor else "menor"])
        t = c.reset_index()
        t.insert(1, "metrica", col)
        por_funcao.append(t)
    custo_linhas = []
    for col, rotulo in CUSTO:
        c = comparar(df, col)
        if c is None:
            continue
        custo_linhas.append([rotulo, num(c["A"].median()), num(c["B"].median()),
                             dif(c["B_menos_A"].median(), eh_pct=False)])
        t = c.reset_index()
        t.insert(1, "metrica", col)
        por_funcao.append(t)
    if por_funcao:
        pd.concat(por_funcao).to_csv(saida / "por_funcao.csv", index=False, encoding="utf-8-sig")

    n_func = df["funcao"].nunique()
    md = ["# Resultados", ""]
    if falso:
        md += ["> **ATENÇÃO: dados do provedor FAKE (simulação). Não use no relatório.**", ""]
    modelos = ", ".join(sorted(set(f"{p}/{m}" for p, m in zip(df["provedor"], df["modelo"]))))
    md += [f"Modelo: {modelos}. Funções: {n_func}. Execuções: {len(df)} "
           f"({(df['condicao'] == 'A').sum()} A, {(df['condicao'] == 'B').sum()} B). "
           f"Versão dos prompts: {', '.join(sorted(df['versao_prompts'].dropna().unique()))}.", "",
           "Cada função conta uma vez: primeiro tira-se a mediana das repetições de cada condição; "
           "depois, a diferença B − A por função. As colunas A e B mostram a mediana entre funções "
           "(para execuções utilizáveis, a proporção de todas as execuções). A coluna *B>A / = / B<A* "
           "conta funções.", "",
           "## Comparação pareada (mediana entre funções)", "",
           tabela_md(["QP", "Métrica", "A (direta)", "B (agente)", "Mediana de B − A", "B>A / = / B<A",
                      "Melhor quando"], linhas_resumo), "",
           "Em negrito, a métrica principal de cada questão.", ""]
    if custo_linhas:
        md += ["## Tamanho, custo e esforço (QP4) — mediana por execução", "",
               tabela_md(["Medida", "A (direta)", "B (agente)", "Mediana de B − A"], custo_linhas), ""]
    md += ["## Por função (mediana das repetições)", ""]
    for col, rotulo, qp, principal, _ in METRICAS:
        if not principal and col not in ("mutation_score", "cobertura_fronteiras", "falsos_alarmes"):
            continue
        c = comparar(df, col)
        if c is None:
            continue
        md += [f"### {qp} — {rotulo}", "",
               tabela_md(["Função", "A", "B", "B − A"],
                         [[f, pct(r["A"]), pct(r["B"]), dif(r["B_menos_A"])] for f, r in c.iterrows()]), ""]
    if tem_revisao and (pasta_rev / "concordancia.txt").exists():
        md += ["## Concordância entre revisores", "", "```",
               (pasta_rev / "concordancia.txt").read_text(encoding="utf-8").strip(), "```", ""]
    falhas = df[df["status"] != "ok"]
    if not falhas.empty:
        md += ["## Execuções com falha na geração", "", ", ".join(falhas["run_id"]), ""]
    md += ["## Limitações", "",
           f"- Com {n_func} funções a leitura é exploratória: não generaliza para outros modelos ou sistemas.",
           "- A revisão não é totalmente cega: o estilo do código (template × livre) pode revelar a condição.",
           "- Execuções não utilizáveis entram com 0 em detecção e cobertura (ver decisão no topo de analisar.py).", ""]
    (saida / "resumo.md").write_text("\n".join(md), encoding="utf-8")

    titulo = "A (geração direta) × B (agente), mediana das repetições por função"
    if falso:
        titulo += " — SIMULAÇÃO (fake)"
    grafico(df, [m for m in METRICAS if m[3] or m[0] in ("mutation_score", "cobertura_fronteiras", "falsos_alarmes")],
            saida / "comparacao.png", titulo)
    print("\n".join(md[:md.index("## Por função (mediana das repetições)")]))
    print(f"\nArquivos em {saida}: execucoes.csv, por_funcao.csv, resumo.md, comparacao.png")


if __name__ == "__main__":
    main()
