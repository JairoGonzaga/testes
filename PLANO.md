# Plano até a entrega (segunda, 23/11)

| Dia | O que fazer | Quem | Tempo |
|---|---|---|---|
| **Ter 17 – Qua 18** | Instalar, rodar a simulação (`--provedor fake`), criar a chave de API e preencher o `.env` | Infra | 1 h |
| **Ter 17 – Qua 18** | Conferir `regras.md` e `gabarito.json` das 6 funções contra a documentação original e conciliar entre os dois. Depois de mudar algo, rodar `python verificar_gabarito.py` | Revisores 1 e 2 | 2–3 h |
| **Qua 18** | Piloto (`gerar.py --piloto` + `executar.py --piloto`). Ler as respostas, ajustar `nucleo/prompts.py` só se algo quebrar e **congelar**. Anotar o `versao_prompts` | Infra | 1 h |
| **Qui 19** | Coleta principal: `gerar.py` e `executar.py`. Guardar uma cópia da pasta `execucoes/` | Infra | 30–60 min |
| **Qui 19 – Sáb 21** | `revisao.py exportar` (com `--amostra 8` se houver mais de 400 linhas). Cada revisor preenche a sua planilha **sem conversar** | Revisores 1 e 2 | 2–4 h cada |
| **Sáb 21** | `revisao.py conciliar`, discussão das linhas amarelas e preenchimento da versão final | Revisores 1 e 2 | 1 h |
| **Qui 19 – Sáb 21** | Escrever no relatório o método e os desvios (seção 5 do README), mais a descrição das funções e dos defeitos | Relatório | 2 h |
| **Dom 22** | `analisar.py`, tabelas e gráfico no relatório, análise qualitativa (exemplos de expectativas erradas), limitações | Todos | 3 h |
| **Seg 23** | Revisão final e entrega (código + `resultados/` + relatório) | Todos | — |

Com 2 pessoas, as duas são revisoras e uma delas cuida da infra. Com 3, a terceira cuida
da infra e do relatório. Com 4, separem infra e relatório.

## O que entregar

1. O repositório (código + `funcoes/` + `execucoes/` + `revisao/` + `resultados/`), sem o `.env`.
2. `resultados/resumo.md` e `resultados/comparacao.png` no relatório.
3. Os desvios da metodologia (README, seção 5) e as limitações.

## Dicas para a análise qualitativa

- `cpf_validate` R7: modelos costumam "saber" que CPF com dígitos repetidos é inválido, mas
  a regra diz o contrário. É um bom exemplo de expectativa sem fundamento nas regras (QP1).
- `ordinal` com negativos e `intword` com valores na metade do arredondamento estão fora
  do escopo: testes sobre isso devem ser classificados como `inconclusivo`.
- Comparem quais defeitos cada condição deixou passar (`resultado.json` → `defeitos`),
  por exemplo `cpf_validate/d4_segundo_digito`, que só aparece com CPFs em que d1 ≠ 0.
