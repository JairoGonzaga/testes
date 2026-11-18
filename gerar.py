"""Passo 3 (geração): roda as condições A e B para cada função e repetição.

Uso:
    python gerar.py --piloto                 # piloto (funções marcadas como piloto)
    python gerar.py                          # coleta principal: 5 funções × 2 condições × 3 rep.
    python gerar.py --funcoes ordinal --condicoes B --repeticoes 1
    python gerar.py --refazer                # gera de novo mesmo o que já existe

Cada execução fica em execucoes/<funcao>__<A|B>__r<n>/ com:
    meta.json            provedor, modelo, chamadas, tokens, tempo, status
    conversa.json        tudo o que foi enviado e recebido (inclusive em falhas)
    test_gerado.py       o arquivo de testes gerado
    plano.json           (só B) os casos do plano usados nos testes
    validacao_plano.json (só B) problemas encontrados em cada tentativa

Execuções já concluídas são puladas, então dá para interromper e continuar depois.
Status possíveis: "ok"; "falha" (o método não produziu testes, ex.: nenhum plano válido em 3
chamadas — é um RESULTADO e não é refeito); "erro" (problema de API/rede) e "pendente"
(provedor arquivo esperando resposta) são refeitos na próxima vez que você rodar o gerar.py.
Com PROVEDOR=fake a saída vai para execucoes_fake/ (nunca misture com as reais).
"""

import argparse
import hashlib
import json
import traceback
from datetime import datetime

from nucleo import config, funcoes as fn
from nucleo.condicoes import Registro, condicao_a, condicao_b
from nucleo.llm import ClienteLLM, RespostaPendente


def versao_arquivos() -> str:
    """Hash dos arquivos que precisam ficar congelados (prompts, plano/template, condições)."""
    h = hashlib.sha1()
    for nome in ("prompts.py", "plano.py", "condicoes.py", "config.py"):
        h.update((config.RAIZ / "nucleo" / nome).read_bytes())
    return h.hexdigest()[:10]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--piloto", action="store_true")
    p.add_argument("--funcoes", default="", help="lista separada por vírgula (padrão: todas)")
    p.add_argument("--condicoes", default="A,B")
    p.add_argument("--repeticoes", type=int, default=config.REPETICOES)
    p.add_argument("--refazer", action="store_true")
    p.add_argument("--provedor", default=None, help="sobrepõe PROVEDOR do .env")
    p.add_argument("--saida", default=None, help="pasta de saída (padrão: execucoes/)")
    a = p.parse_args()

    cliente = ClienteLLM(provedor=a.provedor)
    lista = fn.listar(piloto=a.piloto, nomes=[x for x in a.funcoes.split(",") if x] or None)
    condicoes = [c.strip().upper() for c in a.condicoes.split(",") if c.strip()]
    saida = (config.RAIZ / a.saida) if a.saida else config.pasta_execucoes(a.piloto, cliente.provedor == "fake")
    saida.mkdir(parents=True, exist_ok=True)
    versao = versao_arquivos()
    print(f"Provedor: {cliente.provedor} | modelo: {cliente.modelo} | versão dos prompts: {versao}")
    print(f"Saída: {saida}\n")

    total = falhas = erros = pendentes = 0
    for rep in range(1, a.repeticoes + 1):          # intercala para diluir efeitos de horário
        for funcao in lista:
            for cond in condicoes:
                run_id = f"{funcao.nome}__{cond}__r{rep}"
                pasta = saida / run_id
                meta_arq = pasta / "meta.json"
                if meta_arq.exists() and not a.refazer:
                    status_antigo = json.loads(meta_arq.read_text(encoding="utf-8")).get("status")
                    if status_antigo in ("ok", "falha"):  # "falha" é resultado do método: não refazer
                        print(f"  {run_id}: já existe ({status_antigo}), pulando")
                        continue
                pasta.mkdir(parents=True, exist_ok=True)
                for velho in ("test_gerado.py", "plano.json", "validacao_plano.json", "resultado.json"):
                    (pasta / velho).unlink(missing_ok=True)

                reg = Registro()
                contexto = {"funcao": funcao, "condicao": cond, "repeticao": rep}
                try:
                    info = (condicao_a if cond == "A" else condicao_b)(funcao, cliente, pasta, contexto, reg)
                except RespostaPendente as e:
                    info = {"status": "pendente", "erro": f"aguardando resposta para {e}"}
                except Exception as e:  # noqa: BLE001 — erro de API/rede: registra e segue
                    info = {"status": "erro", "erro": f"{type(e).__name__}: {e}",
                            "traceback": traceback.format_exc()[-3000:]}
                meta = {"run_id": run_id, "funcao": funcao.nome, "condicao": cond, "repeticao": rep,
                        "piloto": funcao.piloto, "provedor": cliente.provedor, "modelo": cliente.modelo,
                        "temperatura": cliente.temperatura, "max_chamadas": config.MAX_CHAMADAS,
                        "versao_prompts": versao, "data": datetime.now().isoformat(timespec="seconds"),
                        **info, **reg.resumo()}
                if cliente.provedor == "arquivo":  # replay: o tempo real é o registrado com a resposta
                    meta["tempo_total_s"] = round(meta["tempo_total_s"] + meta["tempo_modelo_s"], 2)
                    meta["tokens_aproximados"] = True
                meta_arq.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
                (pasta / "conversa.json").write_text(json.dumps(reg.conversa, ensure_ascii=False, indent=1),
                                                     encoding="utf-8")
                total += 1
                falhas += meta["status"] == "falha"
                erros += meta["status"] == "erro"
                pendentes += meta["status"] == "pendente"
                extra = f" (reparos: {info.get('reparos', 0)})" if cond == "B" else ""
                print(f"  {run_id}: {meta['status']} | {reg.chamadas} chamada(s), "
                      f"{reg.tokens_entrada}+{reg.tokens_saida} tokens, {reg.tempo_total_s:.1f}s{extra}"
                      + (f" — {info.get('erro')}" if meta["status"] != "ok" else ""))
    if pendentes:
        print(f"\n{pendentes} execução(ões) aguardando resposta (provedor arquivo): salve cada resposta em "
              "resposta_<n>.txt, ao lado do prompt_<n>.txt, e rode o mesmo comando de novo.")
    if erros:
        print(f"\n{erros} execução(ões) com ERRO de API/rede: rode o mesmo comando de novo para refazê-las.")
    print(f"\n{total} execução(ões) feitas, {falhas} com falha do método. Próximo passo: python executar.py"
          + (" --piloto" if a.piloto else "") + (" --fake" if cliente.provedor == "fake" else ""))


if __name__ == "__main__":
    main()
