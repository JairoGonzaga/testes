"""Passo 4 (execução): roda os testes gerados na referência, nos defeitos e nos mutantes.

Uso:
    python executar.py                # execucoes/
    python executar.py --piloto       # execucoes_piloto/
    python executar.py --fake         # execucoes_fake/ (testes da tubulação)
    python executar.py --refazer      # recalcula mesmo o que já tem resultado

Os testes NÃO são regerados: o mesmo test_gerado.py roda contra cada versão.
Para cada execução grava:
    resultado.json                  todas as métricas automáticas
    pytest/junit_referencia.xml     relatório JUnit da execução na referência
"""

import argparse
import json

from nucleo import config, funcoes as fn
from nucleo.avaliacao import avaliar, salvar


def fmt(x):
    return "  -  " if x is None else f"{x:5.0%}"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--piloto", action="store_true")
    p.add_argument("--fake", action="store_true")
    p.add_argument("--entrada", default=None, help="pasta das execuções (sobrepõe --piloto/--fake)")
    p.add_argument("--refazer", action="store_true")
    p.add_argument("--sem-mutantes", action="store_true", help="mais rápido; não calcula mutation score")
    a = p.parse_args()

    base = config.RAIZ / a.entrada if a.entrada else config.pasta_execucoes(a.piloto, a.fake)
    pastas = sorted(d for d in base.iterdir() if (d / "meta.json").exists()) if base.exists() else []
    if not pastas:
        raise SystemExit(f"Nenhuma execução em {base}. Rode antes: python gerar.py")

    print(f"{'execução':32} util  testes  falso_al  defeitos  mutation  fronteiras  ramos")
    for pasta in pastas:
        destino = pasta / "resultado.json"
        if destino.exists() and not a.refazer:
            r = json.loads(destino.read_text(encoding="utf-8"))
        else:
            meta = json.loads((pasta / "meta.json").read_text(encoding="utf-8"))
            funcao = fn.carregar(meta["funcao"])
            r = avaliar(funcao, pasta / "test_gerado.py", pasta_saida=pasta / "pytest",
                        com_mutantes=not a.sem_mutantes)
            salvar(r, destino)
        if r["utilizavel"]:
            print(f"{pasta.name:32} sim  {r['n_testes']:6}  {fmt(r['falsos_alarmes'])}     "
                  f"{fmt(r['deteccao_defeitos'])}     {fmt(r.get('mutation_score'))}     "
                  f"{fmt(r['cobertura_fronteiras'])}      {fmt(r['cobertura_ramos'])}")
        else:
            print(f"{pasta.name:32} NÃO  ({r['motivo']})")
    print("\nPróximo passo: python revisao.py exportar" + (f" --entrada {base.name}" if base != config.PASTA_EXECUCOES else ""))


if __name__ == "__main__":
    main()
