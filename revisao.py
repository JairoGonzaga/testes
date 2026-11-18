"""Passo 5 (revisão cega): planilhas para dois revisores e conciliação.

Uso:
    python revisao.py exportar               # cria revisao/planilha_revisor1.xlsx e _revisor2.xlsx
    python revisao.py exportar --amostra 8   # no máximo 8 testes por execução (sorteados)
    python revisao.py conciliar              # junta as duas planilhas → revisao/revisao_final.xlsx

Cada linha é um teste (ou um caso de teste parametrizado). A planilha NÃO mostra qual
condição gerou o teste nem a execução; a ligação fica em revisao/chave.csv, que os
revisores não devem abrir até terminar.

Cada revisor preenche, sem conversar com o outro:
    regra          regra que o caso realmente verifica (R1, R2…). Já vem uma sugestão.
    classificacao  correto | incorreto | inconclusivo  (contra regras.md e gabarito.json)
    observacao     opcional

Depois, `conciliar` aponta as divergências; a dupla discute e preenche a versão final.
"""

import argparse
import ast
import random
import re
import sys
from pathlib import Path

import pandas as pd

from nucleo import config, funcoes as fn
from nucleo.plano import assinatura_inspect

CLASSES = ["correto", "incorreto", "inconclusivo"]
RESULTADO = {"passed": "passou", "failed": "falhou", "error": "erro"}

INSTRUCOES = [
    ("Como revisar", ""),
    ("1.", "Abra funcoes/<funcao>/regras.md e gabarito.json da função indicada na linha."),
    ("2.", "Para cada linha, leia o código do teste e as chamadas observadas (argumentos reais)."),
    ("3.", "Coluna 'regra': confirme ou corrija a regra que o caso verifica (R1, R2…)."),
    ("4.", "Coluna 'classificacao': correto = a expectativa decorre das regras; incorreto = "
           "contradiz as regras; inconclusivo = testa algo fora do escopo/não definido pelas "
           "regras ou não dá para decidir."),
    ("5.", "Num teste parametrizado, avalie só o caso daquela linha (veja o id entre colchetes)."),
    ("6.", "Não converse com o outro revisor e não abra revisao/chave.csv até terminar."),
    ("Obs.", "'resultado_referencia' ajuda, mas não decide: um teste pode passar e verificar algo "
             "irrelevante, ou falhar porque a expectativa está certa e a referência diverge das regras."),
]


def pastas_de(entrada: Path):
    sufixo = entrada.name.replace("execucoes", "")
    return config.RAIZ / f"revisao{sufixo}"


def fontes_dos_testes(codigo: str) -> dict:
    """nome (ou Classe::nome) → código-fonte com decoradores."""
    try:
        arvore = ast.parse(codigo)
    except SyntaxError:
        return {}
    linhas = codigo.splitlines()
    fontes = {}

    def trecho(no):
        inicio = min([d.lineno for d in no.decorator_list] + [no.lineno]) - 1
        return "\n".join(linhas[inicio:no.end_lineno])

    for no in arvore.body:
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fontes[no.name] = trecho(no)
        elif isinstance(no, ast.ClassDef):
            for filho in no.body:
                if isinstance(filho, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    fontes[f"{no.name}::{filho.name}"] = trecho(filho)
    return fontes


def formatar_chamada(nome_funcao, args: dict, padroes: dict) -> str:
    if "_repr" in args:
        return f"{nome_funcao}({args['_repr']})"
    partes = [f"{k}={v!r}" for k, v in args.items() if not (k in padroes and padroes[k] == v)]
    return f"{nome_funcao}({', '.join(partes)})"


def regra_sugerida(texto: str) -> str:
    achadas = re.findall(r"(?<![A-Za-z0-9])[Rr](\d{1,2})(?![0-9])", texto)
    return ", ".join(dict.fromkeys(f"R{n}" for n in achadas))


def exportar(entrada: Path, amostra: int, semente: int):
    import json
    pasta_rev = pastas_de(entrada)
    pasta_rev.mkdir(parents=True, exist_ok=True)
    linhas, chave = [], []
    rng = random.Random(semente)
    for pasta in sorted(d for d in entrada.iterdir() if (d / "resultado.json").exists()):
        meta = json.loads((pasta / "meta.json").read_text(encoding="utf-8"))
        res = json.loads((pasta / "resultado.json").read_text(encoding="utf-8"))
        if not res.get("utilizavel"):
            continue
        funcao = fn.carregar(meta["funcao"])
        sig = assinatura_inspect(funcao.assinatura)
        padroes = {k: p.default for k, p in sig.parameters.items() if p.default is not p.empty}
        fontes = fontes_dos_testes((pasta / "test_gerado.py").read_text(encoding="utf-8"))
        itens = list(res["testes_referencia"].items())
        if amostra and len(itens) > amostra:
            itens = rng.sample(itens, amostra)
        for nodeid, resultado in itens:
            partes = nodeid.split("::")[1:]
            item = "::".join(partes)
            nome_base = re.sub(r"\[.*\]$", "", item)
            codigo = fontes.get(nome_base, "(código não encontrado)")
            chamadas = [formatar_chamada(funcao.nome_funcao, a, padroes)
                        for a in res.get("chamadas_por_teste", {}).get(nodeid, [])]
            texto_msg = res.get("mensagens_referencia", {}).get(nodeid, "")
            msg = [l[1:].strip() for l in texto_msg.splitlines() if l.startswith("E ")] \
                or texto_msg.strip().splitlines()
            linhas.append({
                "funcao": funcao.nome, "item": item, "codigo": codigo,
                "chamadas_observadas": "\n".join(chamadas) or "(nenhuma chamada registrada)",
                "resultado_referencia": RESULTADO.get(resultado, resultado),
                "mensagem": " | ".join(msg[:3])[:300] if msg and resultado != "passed" else "",
                "regra_sugerida": regra_sugerida(item + "\n" + codigo),
            })
            chave.append({"run_id": meta["run_id"], "funcao": funcao.nome, "condicao": meta["condicao"],
                          "repeticao": meta["repeticao"], "nodeid": nodeid})
    if not linhas:
        raise SystemExit("Nenhum teste para revisar. Rode antes: python executar.py")

    ordem = list(range(len(linhas)))
    rng.shuffle(ordem)
    df = pd.DataFrame([linhas[i] for i in ordem])
    ch = pd.DataFrame([chave[i] for i in ordem])
    ids = [f"T{k:04d}" for k in range(1, len(df) + 1)]
    df.insert(0, "id_cego", ids)
    ch.insert(0, "id_cego", ids)
    df["regra"] = df["regra_sugerida"].str.split(",").str[0].fillna("").str.strip()
    df["classificacao"] = ""
    df["observacao"] = ""
    ch.to_csv(pasta_rev / "chave.csv", index=False, encoding="utf-8-sig")
    for n in (1, 2):
        salvar_planilha(df, pasta_rev / f"planilha_revisor{n}.xlsx")
    print(f"{len(df)} testes para revisar → {pasta_rev}/planilha_revisor1.xlsx e planilha_revisor2.xlsx")
    print("A chave (qual condição gerou cada teste) está em chave.csv — não abra antes de terminar.")


def salvar_planilha(df: pd.DataFrame, caminho: Path, destacar=None):
    from openpyxl.styles import Alignment, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
    with pd.ExcelWriter(caminho, engine="openpyxl") as w:
        df.to_excel(w, sheet_name="revisao", index=False)
        pd.DataFrame(INSTRUCOES, columns=["passo", "instrução"]).to_excel(w, sheet_name="instrucoes", index=False)
        ws = w.sheets["revisao"]
        larguras = {"id_cego": 9, "funcao": 14, "item": 30, "codigo": 70, "chamadas_observadas": 42,
                    "resultado_referencia": 12, "mensagem": 30, "regra_sugerida": 10, "regra": 8,
                    "classificacao": 14, "observacao": 30}
        for i, col in enumerate(df.columns, start=1):
            letra = ws.cell(row=1, column=i).column_letter
            ws.column_dimensions[letra].width = larguras.get(col, 14)
        for linha in ws.iter_rows(min_row=2):
            for cel in linha:
                cel.alignment = Alignment(wrap_text=True, vertical="top")
        for col in df.columns:
            if col.startswith("classificacao"):
                letra = ws.cell(row=1, column=list(df.columns).index(col) + 1).column_letter
                dv = DataValidation(type="list", formula1='"' + ",".join(CLASSES) + '"', allow_blank=True)
                ws.add_data_validation(dv)
                dv.add(f"{letra}2:{letra}{len(df) + 1}")
        if destacar is not None:
            amarelo = PatternFill("solid", fgColor="FFF2CC")
            for idx, flag in enumerate(destacar, start=2):
                if flag:
                    for cel in ws[idx]:
                        cel.fill = amarelo
        ws.freeze_panes = "B2"
        w.sheets["instrucoes"].column_dimensions["B"].width = 110


def _normalizar(df):
    df = df.copy()
    df["classificacao"] = df["classificacao"].fillna("").astype(str).str.strip().str.lower()
    df["regra"] = df["regra"].fillna("").astype(str).str.strip().str.upper()
    return df


def kappa(a, b):
    """Kappa de Cohen para duas listas de rótulos."""
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    rotulos = set(a) | set(b)
    pe = sum((list(a).count(r) / n) * (list(b).count(r) / n) for r in rotulos)
    return None if pe == 1 else (po - pe) / (1 - pe)


def conciliar(entrada: Path):
    pasta_rev = pastas_de(entrada)
    r1 = _normalizar(pd.read_excel(pasta_rev / "planilha_revisor1.xlsx", sheet_name="revisao"))
    r2 = _normalizar(pd.read_excel(pasta_rev / "planilha_revisor2.xlsx", sheet_name="revisao"))
    for nome, df in (("revisor 1", r1), ("revisor 2", r2)):
        vazias = (~df["classificacao"].isin(CLASSES)).sum()
        if vazias:
            print(f"Atenção: {nome} tem {vazias} linha(s) sem classificação válida.")
    base = r1[["id_cego", "funcao", "item", "codigo", "chamadas_observadas", "resultado_referencia"]]
    m = base.merge(r1[["id_cego", "regra", "classificacao", "observacao"]].rename(
        columns={"regra": "regra_r1", "classificacao": "classificacao_r1", "observacao": "obs_r1"}), on="id_cego")
    m = m.merge(r2[["id_cego", "regra", "classificacao", "observacao"]].rename(
        columns={"regra": "regra_r2", "classificacao": "classificacao_r2", "observacao": "obs_r2"}), on="id_cego")
    concordam = (m["regra_r1"] == m["regra_r2"]) & (m["classificacao_r1"] == m["classificacao_r2"]) \
        & m["classificacao_r1"].isin(CLASSES)
    m["divergente"] = ["não" if c else "sim" for c in concordam]
    m["regra"] = m["regra_r1"].where(concordam, "")
    m["classificacao"] = m["classificacao_r1"].where(concordam, "")
    m["decisao_discussao"] = ""
    salvar_planilha(m, pasta_rev / "revisao_final.xlsx", destacar=list(~concordam))
    k = kappa(list(m["classificacao_r1"]), list(m["classificacao_r2"]))
    concord = (m["classificacao_r1"] == m["classificacao_r2"]).mean()
    print(f"{len(m)} linhas | concordância na classificação: {concord:.0%} | kappa de Cohen: "
          f"{'-' if k is None else f'{k:.2f}'} | divergências (regra ou classificação): {(~concordam).sum()}")
    print(f"Discutam as linhas amarelas e preencham 'regra' e 'classificacao' em {pasta_rev}/revisao_final.xlsx")
    (pasta_rev / "concordancia.txt").write_text(
        f"linhas={len(m)}\nconcordancia_classificacao={concord:.4f}\nkappa={k}\n"
        f"divergencias={(~concordam).sum()}\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("acao", choices=["exportar", "conciliar"])
    p.add_argument("--entrada", default="execucoes")
    p.add_argument("--amostra", type=int, default=0, help="máximo de testes por execução (0 = todos)")
    p.add_argument("--semente", type=int, default=2026)
    a = p.parse_args()
    entrada = config.RAIZ / a.entrada
    if not entrada.exists():
        sys.exit(f"Pasta {entrada} não existe.")
    if a.acao == "exportar":
        exportar(entrada, a.amostra, a.semente)
    else:
        conciliar(entrada)


if __name__ == "__main__":
    main()
