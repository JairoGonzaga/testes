# Agente de testes orientado a regras de negócio

Implementação da metodologia da 2ª entrega (Fundamentos de Testes de Software, 2026.2).
O projeto compara duas formas de pedir a um modelo de IA testes pytest a partir de regras
de negócio escritas em texto:

| Condição | Como funciona |
|---|---|
| **A — geração direta** | Uma chamada. O modelo recebe regras + assinatura e devolve o arquivo pytest. |
| **B — agente** | O modelo devolve um **plano de casos em JSON**. O programa valida o plano, gera os testes por template, confere se o pytest consegue carregá-los e, se houver problema técnico, pede reparo ao modelo (no máximo 3 chamadas). |

```
regras.md ──► gerar.py ──► test_gerado.py ──► executar.py ──► resultado.json
(+ assinatura)   (A ou B)                       │  referência, defeitos, mutantes
                                                ▼
                         revisao.py (2 revisores, cego) ──► analisar.py ──► resultados/
```

---

## 1. Instalação (uma vez)

Precisa de Python 3.10 ou mais novo.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

Copie `.env.exemplo` para `.env` e preencha `PROVEDOR`, `MODELO` e a chave de API (ou use
o provedor `arquivo`, explicado abaixo, se não tiver chave).
Use um modelo pequeno e barato (confira o nome exato no painel do provedor). A coleta
inteira são ~36 execuções com 1 a 3 chamadas cada, com prompts de 1 a 3 mil tokens.

## 2. Teste a tubulação sem gastar crédito (10 minutos)

O provedor `fake` monta respostas a partir do gabarito, com erros propositais. Serve só
para ver tudo funcionando; a saída vai para pastas `*_fake/`, que nunca entram no relatório.

```bash
python gerar.py --provedor fake
python executar.py --fake
python revisao.py exportar --entrada execucoes_fake
python analisar.py --entrada execucoes_fake      # funciona mesmo sem a revisão preenchida
```

### Sem chave de API? Use o provedor `arquivo` (copiar e colar)

Com `PROVEDOR=arquivo`, o `gerar.py` não chama API nenhuma. Ele grava cada prompt em
`respostas_manuais/<execução>/prompt_1.txt` e marca a execução como "pendente". Vocês colam
o prompt no chat da IA, salvam a resposta, sem editar, em `resposta_1.txt` na mesma pasta e
rodam o `gerar.py` de novo. Se o agente pedir reparo, aparece um `prompt_2.txt`, e assim por
diante. As respostas salvas são reaproveitadas, então o resultado é reproduzível. Usem uma
conversa nova para cada prompt.

### Exemplo pronto: rodada com Claude Opus

As pastas `execucoes_opus/`, `respostas_opus/` e `resultados_opus/` têm uma rodada rápida
(1 repetição) feita com subagentes Claude Opus pelo provedor `arquivo`. Leiam
`resultados_opus/LEIAME.md`. Ela serve de exemplo e de prévia, mas não substitui a coleta oficial.

## 3. Passo a passo da metodologia

### Passo 2 — Preparação (JÁ FEITA, mas precisa ser conferida pela equipe)

Para cada função em `funcoes/` já existem:

| Arquivo | O que é | Vai para o modelo? |
|---|---|---|
| `regras.md` | regras R1, R2… escritas a partir da documentação | **sim** |
| `meta.json` | assinatura e exceções importáveis | **sim** (assinatura) |
| `gabarito.json` | resultado esperado por regra + valores-limite (fronteiras) | não |
| `referencia.py` | versão correta (adaptada do projeto original) | não |
| `defeitos/*.py` | 3–4 versões com defeito injetado (fronteira, lógica, cálculo) | não |
| `mutantes/*.py` | mutantes gerados automaticamente (conjunto fixo) | não |
| `mutantes/equivalentes.txt` | mutantes equivalentes, verificados à mão | não |

**O que vocês precisam fazer:** dois integrantes leem `regras.md` e `gabarito.json` de cada
função, conferem com a documentação original e conciliam as diferenças. Depois de
qualquer mudança, rodem:

```bash
python verificar_gabarito.py
```

Ele confere que todos os casos do gabarito passam na referência, que o gabarito detecta
todos os defeitos, que os critérios de fronteira funcionam e que ele mata todos os mutantes
não equivalentes. Hoje, todas as 6 funções passam em tudo.

Funções escolhidas (todas determinísticas, sem rede/banco, tipos simples):

| Função | Projeto | Uso | Regras | Fronteiras | Defeitos | Mutantes |
|---|---|---|---|---|---|---|
| `apnumber` | humanize 4.17 (MIT) | **piloto** | 5 | 4 | 3 | 26 |
| `ordinal` | humanize 4.17 | avaliação | 6 | 6 | 4 | 31 |
| `intword` | humanize 4.17 | avaliação | 7 | 6 | 4 | 60 |
| `naturalsize` | humanize 4.17 | avaliação | 9 | 8 | 4 | 59 |
| `cpf_validate` | python-stdnum 2.2 (LGPL) | avaliação | 7 | 5 | 4 | 39 |
| `luhn_validate` | python-stdnum 2.2 | avaliação | 6 | 4 | 4 | 13 |

### Passo 2b — Piloto (calibra e congela)

```bash
python gerar.py --piloto
python executar.py --piloto
```

Abram `execucoes_piloto/*/conversa.json` e `test_gerado.py`. Se algo quebrar por motivo
técnico (o modelo não entende o formato, por exemplo), ajustem `nucleo/prompts.py`.
Quando estiver bom, **não mexam mais** em `nucleo/prompts.py`, `nucleo/plano.py`,
`nucleo/condicoes.py` e `nucleo/config.py`. O `gerar.py` grava em cada execução um
`versao_prompts` (hash desses arquivos): ele precisa ser o mesmo em todas as execuções da
coleta principal, e o `analisar.py` mostra esse valor no resumo.

### Passo 3 — Geração (coleta principal: 5 funções × 2 condições × 3 repetições = 30)

```bash
python gerar.py
```

Pode interromper e rodar de novo: o que já terminou é pulado. Execuções com **erro** de
API/rede são refeitas automaticamente na próxima rodada; execuções com **falha** do
método (por exemplo, o agente não conseguiu um plano válido em 3 chamadas) são um
resultado e **não** são refeitas.

### Passo 4 — Execução

```bash
python executar.py
```

Roda cada `test_gerado.py`, sem regenerar, na referência (com coverage), nas versões
defeituosas e nos mutantes. Leva alguns minutos. Cada execução ganha um `resultado.json` e
`pytest/junit_referencia.xml`.

### Passo 5 — Revisão cega (dois revisores)

```bash
python revisao.py exportar               # ou: --amostra 8 (máximo de 8 testes por execução)
```

Cria `revisao/planilha_revisor1.xlsx` e `planilha_revisor2.xlsx` (iguais, em ordem
aleatória, sem dizer qual condição gerou cada teste). Cada revisor preenche **sozinho**:

- `regra` — já vem uma sugestão; confirme ou corrija;
- `classificacao` — `correto`, `incorreto` ou `inconclusivo` (há uma aba de instruções);
- `observacao` — opcional, mas anotem exemplos interessantes para a análise qualitativa.

Depois:

```bash
python revisao.py conciliar
```

Gera `revisao/revisao_final.xlsx` com as divergências em amarelo e a concordância (com o
kappa de Cohen). A dupla discute as linhas amarelas e preenche `regra` e `classificacao`.

> Se faltar tempo: use `--amostra`. A métrica de cobertura de regras pela revisão fica
> subestimada com amostra; nesse caso usem a **cobertura de regras automática** (regras
> com pelo menos um teste válido marcado com a regra) e registrem isso como limitação.

### Passo 6 — Análise

```bash
python analisar.py
```

Saídas em `resultados/`:

- `execucoes.csv` — uma linha por execução, com todas as métricas;
- `por_funcao.csv` — mediana das repetições por função e condição, e B − A;
- `resumo.md` — tabelas prontas para colar no relatório;
- `comparacao.png` — gráfico A × B por função para cada métrica.

---

## 4. Como cada métrica é calculada

| QP | Métrica | Onde sai | Como |
|---|---|---|---|
| QP1 | **Expectativas corretas** | revisão | corretos ÷ revisados |
| QP1 | Falsos alarmes | executar | testes que falham na referência ÷ executados |
| QP2 | **Detecção de defeitos** | executar | defeitos com ≥ 1 teste válido falhando ÷ defeitos |
| QP2 | Mutation score | executar | mutantes mortos ÷ (mutantes − equivalentes) |
| QP3 | **Cobertura de regras** | revisão | regras com ≥ 1 caso correto ÷ regras testáveis |
| QP3 | Cobertura de regras (automática) | analisar | regras com ≥ 1 teste válido marcado com a regra ÷ regras testáveis |
| QP3 | Cobertura de fronteiras | executar | fronteiras do gabarito exercitadas por testes válidos ÷ fronteiras |
| QP3 | Cobertura de ramos (auxiliar) | executar | coverage.py rodando só os testes válidos |
| QP4 | **Execuções utilizáveis** | executar | execuções sem erro de sintaxe/importação ÷ execuções |
| QP4 | Custo e esforço | gerar + revisão | chamadas, tokens, tempo e testes incorretos (a corrigir à mão) |

**Teste válido** = passa na versão de referência. Só testes válidos contam para detecção,
mutantes e fronteiras. **Fronteira exercitada** = algum teste válido chamou a função com
argumentos que satisfazem o critério da fronteira no gabarito (um "espião" registra os
argumentos reais de cada chamada).

## 5. Desvios em relação à metodologia (registrem no relatório)

1. **Amostra menor:** 5 funções na avaliação (30 execuções) e 1 no piloto, em vez de 10 e 3,
   por causa do prazo.
2. **Seleção por conveniência:** funções escolhidas por terem regras documentadas e claras
   (humanize e python-stdnum), em vez de sorteio de uma lista completa.
3. **Referências adaptadas:** camada de tradução (i18n) removida; exceções do stdnum copiadas
   para o arquivo; normalização de traços Unicode do CPF retirada (ficou fora do escopo).
4. **Defeitos injetados à mão** (fronteira, lógica, cálculo), sem defeitos do histórico de commits.
5. **Mutantes:** gerador próprio baseado na AST, com operadores usuais do mutmut, gerado uma
   vez e mantido fixo. O mutmut 3 roda a suíte do projeto por mutante, e aqui são 30 arquivos
   de teste diferentes contra o mesmo conjunto de mutantes. Os equivalentes foram marcados à
   mão, com justificativa, em `mutantes/equivalentes.txt`.
6. **Tempo esgotado conta como detecção** (mutante ou defeito que trava a execução).
7. **Execuções não utilizáveis entram com 0** em detecção e cobertura, e ficam de fora das
   métricas de oráculo. Com `analisar.py --ignorar-inutilizaveis`, são excluídas de tudo.
8. **O agente nunca roda os testes na referência:** a checagem técnica usa um *stub* com a
   mesma assinatura, que só levanta `NotImplementedError`. Assim o plano continua sendo feito
   só a partir das regras.
9. **Mesmo contexto para A e B:** os dois prompts pedem para cobrir todas as regras, incluir
   fronteiras e entradas inválidas e indicar a regra de cada caso. Muda só o formato da resposta.
10. **Cegueira parcial:** o estilo do código (template × livre) pode revelar a condição ao revisor.

## 6. Estrutura

```
gerar.py               passo 3 — gera os testes (A e B)
executar.py            passo 4 — roda nas versões e calcula métricas automáticas
revisao.py             passo 5 — planilhas cegas e conciliação
analisar.py            passo 6 — CSV, comparação pareada, resumo e gráfico
verificar_gabarito.py  passo 2 — confere gabarito, referência, defeitos e mutantes
nucleo/                código compartilhado (prompts, plano/template, agente, pytest, métricas)
funcoes/<nome>/        dados de cada função (regras, gabarito, referência, defeitos, mutantes)
execucoes/             uma pasta por execução (criada pelo gerar.py)
revisao/, resultados/  criadas pelos passos 5 e 6
```

### Adicionar uma função

Crie `funcoes/<nome>/` com `meta.json`, `regras.md`, `gabarito.json`, `referencia.py` e
`defeitos/`, copiando o formato de uma existente. Depois rode
`python verificar_gabarito.py <nome>`, que também gera os mutantes. Inspecione
`mutantes/sobreviventes_gabarito.txt` e copie para `equivalentes.txt` só os que forem
realmente equivalentes.

## 7. Problemas comuns

- **"Defina MODELO"** → falta `MODELO=` no `.env`.
- **Erro 401/403** → chave de API errada ou sem crédito.
- **Erro sobre `temperature`** → apague `TEMPERATURA` do `.env` (modelos novos não aceitam).
- **Erro de limite de requisições (429)** → rode de novo o `gerar.py`; ele continua de onde parou.
- **A planilha abre com acentos estranhos** → abram o `.xlsx` (não o `.csv`) ou importem como UTF-8.
