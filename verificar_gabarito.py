"""Passo 2 (preparação): confere o gabarito, a referência, os defeitos e os mutantes.

Uso:
    python verificar_gabarito.py                 # todas as funções (avaliação + piloto)
    python verificar_gabarito.py ordinal intword # só algumas
    python verificar_gabarito.py --regerar-mutantes

O que ele faz para cada função:
  1. transforma os casos do gabarito em um arquivo de testes (teste_gabarito.py);
  2. roda esse arquivo na referência: TODOS os casos precisam passar (2c da metodologia);
  3. roda nas versões defeituosas: cada defeito precisa ser detectado pelo gabarito;
     se não for, o defeito não é observável pelas regras e deve ser revisto;
  4. confere se os critérios de fronteira são satisfeitos pelos próprios casos do gabarito;
  5. gera os mutantes (se ainda não existirem) e lista os que o gabarito não mata em
     mutantes/sobreviventes_gabarito.txt — candidatos a mutante equivalente, que a
     equipe deve inspecionar e copiar para mutantes/equivalentes.txt se forem mesmo.
"""

import argparse
import sys

from nucleo import funcoes as fn
from nucleo.avaliacao import avaliar
from nucleo.mutantes import gerar_todos
from nucleo.plano import renderizar_testes


def verificar(funcao, regerar_mutantes=False) -> bool:
    print(f"\n=== {funcao.nome} {'(piloto)' if funcao.piloto else ''}")
    casos = [dict(c, id=f"G{i}") for i, c in enumerate(funcao.gabarito.get("casos", []), start=1)]
    if not casos:
        print("  ✗ gabarito.json sem casos")
        return False
    arquivo = funcao.pasta / "teste_gabarito.py"
    arquivo.write_text(renderizar_testes(casos, funcao, "Casos do gabarito (gerado por verificar_gabarito.py)."),
                       encoding="utf-8")

    if regerar_mutantes or not funcao.mutantes:
        nomes = gerar_todos(funcao.referencia, funcao.pasta_mutantes)
        print(f"  mutantes gerados: {len(nomes)}")

    r = avaliar(funcao, arquivo)
    ok = True
    if not r["utilizavel"]:
        print(f"  ✗ o arquivo do gabarito não rodou: {r['motivo']}\n{r.get('erro_coleta', '')}")
        return False

    falhas = [n for n, o in r["testes_referencia"].items() if o != "passed"]
    if falhas:
        ok = False
        print(f"  ✗ {len(falhas)} caso(s) do gabarito FALHAM na referência (gabarito ou referência errados):")
        for n in falhas:
            msg = r["mensagens_referencia"].get(n, "").strip().splitlines()
            print(f"      {n}  →  {msg[-1] if msg else ''}")
    else:
        print(f"  ✓ {r['n_testes']} casos do gabarito passam na referência")

    nao_detectados = [d for d, det in r["defeitos"].items() if not det]
    if nao_detectados:
        ok = False
        print(f"  ✗ defeitos NÃO detectados pelo gabarito: {', '.join(nao_detectados)}")
    else:
        print(f"  ✓ {len(r['defeitos'])} defeitos detectados pelo gabarito")

    fr = r["fronteiras"]
    if fr["nao_cobertas"]:
        ok = False
        print(f"  ✗ fronteiras não exercitadas pelos casos do gabarito: {', '.join(fr['nao_cobertas'])} "
              "(confira o critério)")
    else:
        print(f"  ✓ {fr['total']} fronteiras exercitadas pelo gabarito")

    m = r["mutantes"]
    sobrev = m["sobreviventes"]
    print(f"  mutantes: {m['total']} (equivalentes marcados: {m['equivalentes']}), "
          f"gabarito mata {m['mortos']} → score {r['mutation_score']:.0%}")
    linhas = []
    for nome in sobrev:
        cab = (funcao.pasta_mutantes / f"{nome}.py").read_text(encoding="utf-8").splitlines()[0]
        linhas.append(f"{nome}   {cab.split('—', 1)[-1].strip()}")
    (funcao.pasta_mutantes / "sobreviventes_gabarito.txt").write_text(
        "# Mutantes que o gabarito NÃO mata. Inspecione cada um: se for equivalente\n"
        "# (comportamento idêntico ao original para qualquer entrada dentro das regras),\n"
        "# copie o nome para equivalentes.txt.\n" + "\n".join(linhas) + "\n", encoding="utf-8")
    if sobrev:
        print(f"  → {len(sobrev)} sobrevivente(s) listados em mutantes/sobreviventes_gabarito.txt")
    return ok


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("funcoes", nargs="*")
    p.add_argument("--regerar-mutantes", action="store_true")
    a = p.parse_args()
    lista = fn.listar(nomes=a.funcoes) if a.funcoes else fn.listar(piloto=True) + fn.listar(piloto=False)
    tudo_ok = all([verificar(f, a.regerar_mutantes) for f in lista])
    print("\nTudo certo." if tudo_ok else "\nHá pendências acima — corrija antes de gerar os testes.")
    sys.exit(0 if tudo_ok else 1)


if __name__ == "__main__":
    main()
