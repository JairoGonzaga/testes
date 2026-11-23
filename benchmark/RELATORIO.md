# Benchmark de geração de testes: SWT-Bench + TestGenEval (adaptados)
## Haiku × DeepSeek Flash (com e sem raciocínio)

Data: 2026-11-22. Projeto avaliado: `JairoGonzaga/testes`.

O benchmark usa 6 funções: `apnumber`, `cpf_validate`, `intword`, `luhn_validate`, `naturalsize` e `ordinal`. Elas têm 23 defeitos injetados, 39 mutantes por função e um gabarito de casos de teste. Cada modelo recebeu 210 tarefas com 3 amostras por tarefa.

## 1. Resumo

| Medida (pass@1, média das 3 amostras) | Haiku | DeepSeek Flash com raciocínio | DeepSeek Flash sem raciocínio |
|---|---|---|---|
| SWT zeroshot: S (sucesso) | **100%** | **100%** | 87,0% |
| SWT agente: S (sucesso) | 98,6% ¹ | 98,6% | 95,7% |
| TGE geração completa: suíte utilizável | **100%** | 33,3% ² | **100%** |
| TGE geração completa: all-pass | **100%** | 33,3% ² | 27,8% |
| TGE geração completa: falsos alarmes | 0% | 0% ³ | 3,5% |
| TGE geração completa: mutation score | 99,6% | 98,6% ³ | 96,8% |
| TGE completar *first*: pass@1 / Δ mutation | 100% / +25,6 | 100% / **+36,1** | 66,7% / +22,2 |
| TGE completar *last* / *extra*: pass@1 | 100% / 100% | 94,4% ² / 100% | 94,4% / 72,2% |
| Custo das 210 tarefas | n/d ⁴ | US$ 0,51 | **US$ 0,09** |

¹ A única falha do Haiku é de formatação da resposta, não do teste (seção 3.2).
² Estouro do limite de 16.384 tokens de saída: o raciocínio consumiu o orçamento antes do código (seção 4.1).
³ Calculado só sobre as 6 suítes que saíram completas.
⁴ O Haiku rodou como subagente do Claude Code, que não reporta custo por chamada. A geração consumiu ~14,35 M tokens.

**Conclusões principais:**

1. **O benchmark separa os modelos.** Com o Haiku, quase tudo dava 100% e não era possível saber se era mérito do modelo ou facilidade do teste. O DeepSeek sem raciocínio caiu para 87% no SWT zeroshot, 27,8% de all-pass e 66,7% no *first*. Isso mostra que as tarefas têm dificuldade real e que as métricas medem o que prometem.
2. **O erro característico de modelos mais fracos é o oráculo errado, não a reprodução.** Todas as falhas aplicáveis do DeepSeek no SWT reproduzem a issue: há ≥1 F→P e nenhum P→F. Elas falham por um teste *extra* cuja asserção também quebra no código corrigido (F→F). Os valores esperados vêm calculados de cabeça (dígito de Luhn, CPF, escala de `intword`) ou supõem uma correção diferente da real. No TGE, todas as 29 falhas na referência são asserções erradas, sem nenhum erro de import ou coleta.
3. **O raciocínio fecha quase toda a diferença para o Haiku** no SWT e no *completar*. Ele empata nos SWT e supera o Haiku no ganho do *first*: +36,1 contra +25,6 p.p. de mutation. Mas custa 5,6× mais e **não cabe no orçamento de saída para escrever uma suíte inteira**: 12 de 18 suítes foram cortadas.
4. **No modo agente, o DeepSeek segue o processo esperado**: rodou o pytest e viu o próprio teste falhar no código com defeito em 100% das tarefas. O que separa as versões é a *verificação do lado corrigido*. Com raciocínio, o agente às vezes simula a correção numa cópia e confere que o teste passa. Sem raciocínio, isso quase nunca acontece, e é justamente aí que ficam as falhas F→F.

> **Atualização — harness v2 (seção 10):** com prompts que exigem conferir os oráculos executando o código, e sem dar ao modelo nenhum dado do gabarito, o DeepSeek Flash **sem raciocínio** chegou a 100% no SWT zeroshot, 100% de all-pass no TGE completo e 100% no *last*/*extra*, por US$ 0,17.

## 2. Metodologia

As duas metodologias foram reimplementadas sobre o projeto. Os datasets originais (Django, SymPy etc.) não foram usados. As métricas seguem as definições dos artigos.

### 2.1 SWT-Bench (reprodução de issue)

- **Instâncias:** 23, uma por defeito. Cada uma tem uma *issue* em inglês no estilo GitHub, escrita à mão em [issues.json](issues.json). A issue descreve só o sintoma, com exemplo de chamada, e não indica a correção. O `preparar.py` confere que cada `repro` dá resultado diferente na versão com defeito e na corrigida.
- **Entrada do modelo:** a issue e o `alvo.py` **com defeito**. O comentário que nomeava o defeito e a docstring do módulo são removidos antes.
- **Tarefa:** escrever `test_issue.py` que falhe no código atual e passe depois da correção.
- **Modos:**
  - *zeroshot:* uma resposta só.
  - *agente:* sandbox com `alvo.py` + `ISSUE.md`, onde o modelo pode ler, escrever e rodar `pytest`/Python, mas não pode alterar o `alvo.py`.
- **Métricas:**
  - **W** (aplicável): coleta sem erro e roda pelo menos um teste nas duas versões.
  - **S** (sucesso): ≥1 teste F→P, nenhum P→F e nenhum F→F.
  - Contagens de F2P, F2F, P2P e P2F.
  - **ΔC:** fração das linhas do patch executadas pelos testes.
  - pass@1 e pass@3 pelo estimador não-enviesado de Chen et al.

### 2.2 TestGenEval

- **Geração completa:** o modelo recebe o `alvo.py` (referência) e escreve uma suíte inteira. Métricas:
  - utilizável: coleta sem erro.
  - all-pass: todos os testes passam na referência.
  - any-pass: pelo menos um teste passa.
  - cobertura de linhas e de ramos.
  - **mutation score:** 39 mutantes, descontados os equivalentes.
  - **detecção de defeitos:** fração dos 23 defeitos que a suíte pega.
  - **falsos alarmes:** fração de testes que falham na referência.

  Cobertura, mutação, detecção e falsos alarmes são calculados só sobre os testes que passam na referência das suítes utilizáveis.
- **Completar testes:** o modelo recebe o `alvo.py` e um arquivo de testes parcial (o *contexto*, tirado da suíte-ouro) e escreve **um** teste novo:
  - *first:* o contexto é só o primeiro teste.
  - *last:* todos menos o último.
  - *extra:* a suíte inteira, e o teste pedido é adicional.

  Métricas: pass@1 (o teste novo passa na referência) e o **Δ** de cobertura, mutation e defeitos sobre o contexto.

### 2.3 Execução

| | Haiku | DeepSeek Flash (com e sem raciocínio) |
|---|---|---|
| Como foi chamado | subagentes do Claude Code num workflow ([gerar_workflow.js](gerar_workflow.js)), com saída estruturada `{code, note}` | API da DeepSeek direta, pelo [gerar_openrouter.py](gerar_openrouter.py) `--provedor deepseek` |
| Ferramentas no modo agente | as do harness (Read/Write/Bash) | `read_file`, `write_file`, `run_pytest` e `run_python` no sandbox, com até 15 turnos |
| Limite de saída | o do harness | 16.384 tokens por resposta, **incluindo o raciocínio** |
| Temperatura | a padrão | a padrão do provedor |
| Tempo de geração | ~19,5 min | 71 min com raciocínio, 15 min sem (10 em paralelo) |

O "sem raciocínio" é o mesmo modelo, `deepseek-flash`, com `thinking` desligado. A avaliação dos três é local e idêntica, feita pelo [avaliar.py](avaliar.py) com pytest + coverage e uma execução por mutante.

## 3. Resultados: SWT-Bench

### 3.1 Números

| Modelo | Modo | W | S | pass@3 | algum P→F | ΔC patch |
|---|---|---|---|---|---|---|
| Haiku | zeroshot | 100% | 100% | 100% | 0% | 100% |
| Haiku | agente | 98,6% | 98,6% | 100% | 0% | 100% |
| DeepSeek com raciocínio | zeroshot | 100% | 100% | 100% | 0% | 100% |
| DeepSeek com raciocínio | agente | 100% | 98,6% | 100% | 0% | 100% |
| DeepSeek sem raciocínio | zeroshot | 100% | 87,0% | 100% | 0% | 100% |
| DeepSeek sem raciocínio | agente | 100% | 95,7% | 100% | 0% | 100% |

Em 3 amostras, todos os modelos acertam todas as 23 instâncias pelo menos uma vez (pass@3 = 100%).

### 3.2 Por que falharam

São 14 tarefas com S = falso: 1 do Haiku, 1 do DeepSeek com raciocínio e 12 do DeepSeek sem raciocínio. Cada uma foi reexecutada contra o código com defeito e o corrigido, e as contagens batem com o CSV.

**Padrão geral:** das 13 falhas aplicáveis, todas têm F→P ≥ 1 e P→F = 0, ou seja, o teste da issue reproduz o bug. A falha sempre vem de um teste a mais que também falha no código corrigido (F→F).

| Causa | Haiku | DS com raciocínio | DS sem raciocínio |
|---|---|---|---|
| (A) Valor esperado calculado errado (Luhn, CPF, escala de `intword`) | – | – | 6 |
| (B) Supôs um comportamento ou uma correção diferente do patch real | – | 1 | 6 ⁵ |
| (C) Artefato de formato (texto de `note` colado no código) | 1 | – | – |

⁵ Inclui um placeholder `with pytest.raises(InvalidChecksum): pass`, que falha nas duas versões.

Exemplos verificados:

- **CPF válido tratado como inválido.** No `cpf_validate/d2`, zeroshot sem raciocínio, o teste espera `InvalidChecksum` para `11144477735`, mas 111.444.777-35 é o CPF válido clássico.
- **Regra do mundo real ≠ regra da issue.** No `cpf_validate/d1`, agente sem raciocínio, s1 e s3, o teste exige rejeitar *todos* os dígitos repetidos (`11111111111`), como faz o CPF real. A issue e o patch só rejeitam zeros.
- **Diagnóstico errado da causa.** No `intword/d4`, o agente com raciocínio (s3) espera `intword(10**100-1) == "1.0 googol"`. O patch real só troca `bisect_left` por `bisect_right`, e esse valor continua em decillion. O agente sem raciocínio (s1) espera `intword(10**99) == "1.0 decillion"`, um erro de escala de 10⁶⁶. É a única instância que derruba os dois DeepSeek.
- **Luhn de cabeça.** Em `luhn_validate/d1` e `d2`, zeroshot sem raciocínio, aparecem números "válidos" com dígito verificador errado, como `79927398719` e `4716462567063397`.
- **Haiku, `luhn_validate/d2` s2 (agente):** o código está certo, mas a última linha do arquivo virou `note>The test file reproduces the bug: ...` e a coleta dá `SyntaxError`. Sem essa linha, a tarefa seria sucesso, com F2P = 12.

**Instâncias mais difíceis:** `intword/d4_bisect_left` (falha nos 2 DeepSeek), `cpf_validate/d1_aceita_zero` (2 amostras), `luhn_validate/d1` e `d2` (2 amostras cada). Das 9 falhas zeroshot sem raciocínio, 5 são da amostra s3.

### 3.3 Processo do agente

| | DS com raciocínio | DS sem raciocínio | Haiku ⁶ |
|---|---|---|---|
| Turnos por tarefa (média / mediana / máx.) | 7,5 / 7 / 15 | 6,1 / 5 / 15 | – |
| Chegaram ao limite de 15 turnos | 2 (ambas sucesso) | 1 (sucesso) | – |
| Execuções (pytest + python) por tarefa | 4,1 | 2,7 | 1,9 (Bash) |
| Rodou pytest antes de entregar | 100% | 100% | – |
| Viu o próprio teste falhar no código com defeito | 100% | 100% | – |
| Reescreveu o teste depois de ver um resultado | 18 tarefas, 100% sucesso | 20 tarefas, 100% sucesso | – |
| Simulou a correção numa cópia para checar o lado "passa" | 5 tarefas | 1 tarefa | relatado em notas |
| Custo médio por tarefa / por sucesso | US$ 0,0024 / 0,0025 | US$ 0,0009 / 0,0009 | n/d |

⁶ O Haiku rodou como subagente do Claude Code. Dele só existem a contagem de ferramentas e as notas, sem turnos, exit codes nem custo.

**Leitura:**

- Rodar o pytest e ver o teste falhar é o passo que garante F→P, e os dois DeepSeek fazem isso sempre. Por isso nenhum deles teve falha de "não reproduz".
- O que falta é o passo seguinte: confirmar que as asserções extras passariam com a correção.
  - As 3 falhas do agente sem raciocínio tiveram 1 ou 2 execuções, todas só contra o código com defeito.
  - Com raciocínio, o agente passou no `cpf_validate/d1` justamente porque testou numa cópia corrigida ("10 passed in a simulated fixed copy").
- O fato de o último pytest falhar não prevê o resultado: isso aconteceu em 67/69 e 69/69 tarefas, o que é esperado, porque o teste *deve* falhar no código com defeito.
- O agente melhora o DeepSeek sem raciocínio (87,0% → 95,7%) ao rodar o código em vez de chutar os valores esperados. Com raciocínio, o zeroshot já estava em 100%.

## 4. Resultados: TestGenEval

### 4.1 Geração completa (6 funções × 3 amostras)

| Medida | Haiku | DS com raciocínio | DS sem raciocínio |
|---|---|---|---|
| Utilizável | 100% | **33,3%** | 100% |
| all-pass pass@1 / pass@3 | 100% / 100% | 33,3% / 50,0% | 27,8% / 83,3% |
| any-pass pass@1 | 100% | 33,3% | 100% |
| Testes executados por arquivo (média; faixa) | 183 (103–550) | 95 (47–185) ⁷ | 46 (28–90) |
| Falsos alarmes | 0% | 0% ⁷ | 3,5% (29 de 824 testes) |
| Cobertura de linhas / ramos | 100% / 100% | 100% / 100% ⁷ | 99,7% / 99,6% |
| Mutation score | 99,6% | 98,6% ⁷ | 96,8% |
| Detecção de defeitos | 100% | 100% ⁷ | 97,2% |

⁷ Só as 6 suítes completas, que cobrem apenas `apnumber`, `luhn_validate` e `ordinal`. Para `cpf_validate`, `intword` e `naturalsize` não saiu nenhuma suíte avaliável.

**DeepSeek com raciocínio: o orçamento de saída acabou.**

- 12 das 18 respostas terminaram com `finish_reason=length` em 16.384 tokens.
- Em 8 delas, o raciocínio consumiu os 16.384 tokens inteiros e a resposta veio vazia.
- Nas outras 4, o código foi cortado no meio de uma string e deu `SyntaxError`.
- As 6 que terminaram normalmente são todas all-pass, sem falsos alarmes.
- Nos mesmos 6 jobs, o mutation score é Haiku 1,0, sem raciocínio 1,0 e com raciocínio 0,986. A diferença vem de `luhn_validate` s1.

Ou seja, o modelo escreve suítes corretas, mas o modo de raciocínio é inviável para essa tarefa com esse limite. Ele precisaria de mais orçamento de saída ou de um limite de raciocínio.

**DeepSeek sem raciocínio: suítes pequenas e com oráculos errados.**

- Todas as suítes são utilizáveis e passam em parte, mas 13 de 18 têm de 1 a 6 testes que falham na referência.
- As 29 falhas são todas asserções erradas sobre o comportamento:

| Tipo de erro | Testes |
|---|---|
| `ordinal` com negativos: espera `-1st`, mas o `%` do Python dá `-1th` | 6 |
| Aritmética do valor esperado (dígito do CPF, `naturalsize` além de QB) | 6 |
| Strings decimais (`"3.9"`): `int()` levanta erro e a função devolve a string | 5 |
| Arredondamento ou promoção de unidade no `intword` | 3 |
| Casos de Luhn (vazio, alfabeto esquecido) | 3 |
| `$` da regex aceita `\n` final | 2 |
| Singular `Byte` só vale para \|x\| == 1 exato | 2 |
| Base 1000 confundida com 1024 | 1 |
| Estrutura da constante `powers` | 1 |

- 6 das 29 testam funções auxiliares (`isdigits`, `_calc_check_digits`), não a função-alvo.
- As suítes têm ~4× menos casos que as do Haiku, que usa muito `parametrize`.

### 4.2 Completar testes

| Cenário | Modelo | pass@1 | pass@3 | Δ ramos | Δ mutation | Δ defeitos |
|---|---|---|---|---|---|---|
| first | Haiku | 100% | 100% | +20,8 | +25,6 | +25,0 |
| first | DS com raciocínio | 100% | 100% | **+37,1** | **+36,1** | **+38,0** |
| first | DS sem raciocínio | 66,7% | 100% | +18,3 | +22,2 | +21,3 |
| last | Haiku | 100% | 100% | +4,9 | +1,8 | 0 |
| last | DS com raciocínio | 94,4% | 100% | +5,2 | +2,2 | 0 |
| last | DS sem raciocínio | 94,4% | 100% | +4,9 | +1,8 | 0 |
| extra | Haiku | 100% | 100% | 0 | 0 | 0 |
| extra | DS com raciocínio | 100% | 100% | 0 | 0 | 0 |
| extra | DS sem raciocínio | 72,2% | 100% | 0 | 0 | 0 |

(Os Δ estão em pontos percentuais sobre o contexto. No *last* e no *extra*, o contexto já tem mutation e defeitos em ~100%, então o Δ é zero por limitação do instrumento.)

- **first é o cenário mais informativo.** Com raciocínio, o teste novo do DeepSeek traz mais ganho que o do Haiku, porque cobre mais ramos de uma vez.
- **Sem raciocínio:** as 12 falhas (6 no first, 1 no last, 5 no extra) vêm todas de uma única resposta de 38 a 455 tokens, sem execução. O modelo afirma comportamentos que o código do prompt não tem:
  - `ordinal(-1) == '-1st'`;
  - `apnumber(-0.5) == '0'`, quando a função devolve `'zero'`;
  - `naturalsize(10**30) == '1000.0 QB'`;
  - `InvalidChecksum` confundido com `InvalidFormat`.

  Com raciocínio, os mesmos jobs passaram. A única falha dele (*last*, `naturalsize` s3) foi outra vez estouro de tokens.

## 5. Custos (DeepSeek, preço fora do horário de pico)

| | Com raciocínio | Sem raciocínio |
|---|---|---|
| Total (210 tarefas) | US$ 0,509 | US$ 0,092 |
| Tokens de entrada / saída (dos quais raciocínio) | 2,20 M / 0,77 M (0,63 M) | 1,05 M / 0,10 M (0) |
| SWT zeroshot, por tarefa | US$ 0,0008 | US$ 0,0001 |
| SWT agente, por tarefa | US$ 0,0024 | US$ 0,0009 |
| TGE completa, por tarefa | US$ 0,0092 | US$ 0,0008 |
| TGE completar, por tarefa | US$ 0,0011–0,0031 | US$ 0,0001 |
| Respostas truncadas | 13 | 0 |

O raciocínio custa 5,6× mais no total. Gasta mais justamente nas tarefas longas, que são as que ele não consegue terminar.

## 6. Limitações

1. **Condições de execução diferentes.** O Haiku rodou como subagente do Claude Code, com o prompt de sistema e as ferramentas do harness. O DeepSeek rodou pela API crua, com o runner próprio e um limite de 15 turnos. A comparação mede "modelo + harness", não só o modelo.
2. **Limite de saída igual para todos (16.384 tokens), mas que inclui o raciocínio.** Isso penaliza o modo com raciocínio na geração completa. Com um limite maior, o resultado dele no TGE completo provavelmente subiria. Para comparar com justiça, seria preciso repetir só essas 18 tarefas com mais orçamento.
3. **Issues escritas à mão**, todas com exemplo de reprodução. Isso torna o SWT-Bench bem mais fácil que o original.
4. **Domínio pequeno:** 6 funções puras de 15 a 50 linhas.
5. **Suíte-ouro com mutation 1,0**, o que zera os Δ no *last* e no *extra*.
6. **n = 3 amostras por tarefa.** Diferenças de 1 ou 2 tarefas, como 98,6% contra 100%, estão dentro do ruído.
7. **Mutantes do próprio projeto** (39 por função), não de um gerador externo.

## 7. Como deixar o benchmark ainda mais discriminativo

O DeepSeek sem raciocínio já mostrou que as métricas separam modelos. Para separar modelos fortes entre si, por exemplo Haiku, Sonnet e DeepSeek com raciocínio:

- **Issues sem repro**, ou com sintoma indireto.
- **Ocultar também a docstring da função**, para que o modelo precise inferir o contrato pelo código. É aí que surgem os oráculos errados.
- **Pontuar os oráculos.** Relatar F→F e falsos alarmes como métrica de primeira linha: são o principal erro observado.
- **Contextos *last*/*extra* não saturados**, por exemplo uma suíte-ouro podada até ~70% de mutation.
- **Mais mutantes difíceis**, sobre constantes, conjuntos de caracteres e limites.
- **Módulos maiores**, para exigir leitura de contexto longo.
- **Penalizar tamanho:** relatar mutation score por teste.

## 8. Como reproduzir / rodar com outro modelo

```powershell
# 1. preparar dados, prompts e sandboxes
python benchmark/preparar.py --amostras 3 --sandbox <pasta-fora-do-repo> --modelo <rotulo>
```

**Via API (DeepSeek ou OpenRouter):**

```powershell
$env:DEEPSEEK_API_KEY = "<sua chave>"
python benchmark/gerar_openrouter.py --provedor deepseek --modelos deepseek-flash --teto-usd 1.0 --workers 10
python benchmark/gerar_openrouter.py --provedor deepseek --modelos deepseek-flash --sem-raciocinio --teto-usd 1.0 --workers 10
python benchmark/gerar_openrouter.py --provedor deepseek --modelos deepseek-flash --sem-raciocinio --harness v2 --teto-usd 1.0 --workers 10
python benchmark/avaliar.py --modelo deepseek-flash
python benchmark/avaliar.py --modelo deepseek-flash-sem-raciocinio
python benchmark/avaliar.py --modelo deepseek-flash-sem-raciocinio-v2
python benchmark/comparar.py
```

- O runner retoma de onde parou: tarefas com resposta são puladas.
- `--teto-usd` interrompe a rodada ao atingir o gasto.
- `--cota` mostra o saldo da conta.

**Vários modelos de graça (Groq):** crie uma chave em console.groq.com (sem cartão).

```powershell
$env:GROQ_API_KEY = "<sua chave>"
python benchmark/gerar_openrouter.py --provedor groq --harness v2 --amostras 1 --limite 2 --workers 2 `
    --modelos openai/gpt-oss-120b openai/gpt-oss-20b qwen/qwen3.8-27b
python benchmark/avaliar.py --modelo groq-gpt-oss-120b-v2 --amostras 1 --limite 2   # repita para cada rótulo groq-*
python benchmark/avaliar.py --modelo deepseek-flash-sem-raciocinio-v2 --amostras 1 --limite 2 --rotulo deepseek-v2-sub
python benchmark/comparar.py --modelos deepseek-v2-sub groq-gpt-oss-120b-v2 groq-gpt-oss-20b-v2 groq-qwen3.8-27b-v2
```

- **Quais ids existem.** Em 2026-11-22, a conta testada tinha estes três modelos com uso de ferramentas: `openai/gpt-oss-120b`, `openai/gpt-oss-20b` e `qwen/qwen3.8-27b`. Cada um tinha 1000 requisições por dia, 8 mil tokens por minuto e **200 mil tokens por dia**. A lista muda: se algum id não existir mais, o runner para logo no início e lista os modelos ativos da conta.
- **Geração inválida.** Às vezes o modelo gera os argumentos da ferramenta com JSON inválido (HTTP 400 `tool_use_failed`) ou uma resposta que a Groq não consegue interpretar (HTTP 400 `output_parse_failed`). Isso varia de uma chamada para outra, então o runner repete a chamada (até 6 tentativas) em vez de perder a tarefa.
- **Uma amostra não cabe num dia.** O limite que manda é o de 200 mil tokens por dia por modelo. Na amostra 1 o gpt-oss-120b gastou ~5 mil tokens por tarefa e parou com 36 de 70 tarefas prontas; o gpt-oss-20b parou com 28. O Qwen parou ainda no teste rápido de 12 tarefas. Ou seja, cada amostra de 70 tarefas leva uns 2 dias por modelo. O limite volta aos poucos (a Groq informa quantos segundos faltam), e o runner para quando a espera passa de `--espera-max`. Rode o mesmo comando no dia seguinte: as tarefas prontas são puladas e as que deram erro são refeitas. Os modelos podem rodar ao mesmo tempo, já que o limite é de cada modelo.
- **Por isso, use um subconjunto fixo.** `--amostras 1 --limite 2` roda 2 tarefas de cada tipo: 12 tarefas, cerca de 170 mil tokens por modelo. Avalie com os mesmos filtros no `avaliar.py` e reavalie no mesmo subconjunto o modelo de referência (a linha `--rotulo deepseek-v2-sub`), senão a comparação fica injusta.
- **Limites e esperas.** O limite é por modelo. Quando um modelo esgota a cota do dia, o runner segue para o próximo e, no fim, lista os que pararam. Rode o mesmo comando no dia seguinte: o que já foi feito é pulado. Esperas curtas, de até `--espera-max` (900 s), o runner resolve sozinho com o `Retry-After`.
- **HTTP 413.** Medido em 2026-11-22: o `max_tokens` pedido não conta no limite por minuto (8 mil tokens nos modelos da conta testada). Vem 413 quando a conversa do agente sozinha passa desse limite. Nesse caso a tarefa é marcada como erro e as outras continuam.
- **Raciocínio.** `--sem-raciocinio` só vale para a DeepSeek. Na Groq, cada modelo usa o modo de raciocínio que já vem nele.

**Via subagentes Claude:** rode o workflow [gerar_workflow.js](gerar_workflow.js) com `args = {root, sandbox_root, samples: 3, swt: [...], funcs: [...], model: 'sonnet'}`. Depois avalie:

```powershell
python benchmark/avaliar.py --modelo sonnet --journal <journal.jsonl> --transcricoes <pasta dos agent-*.jsonl>
```

## 9. Arquivos

| Caminho | O que é |
|---|---|
| [issues.json](issues.json) | 23 issues (título, corpo e repro) |
| [preparar.py](preparar.py) | gera instâncias, suítes-ouro, contextos, prompts, `jobs.json` e sandboxes |
| [gerar_workflow.js](gerar_workflow.js) | geração via subagentes Claude |
| [gerar_openrouter.py](gerar_openrouter.py) | geração via API (DeepSeek/OpenRouter): zeroshot e agente com ferramentas, custo e truncamentos |
| [avaliar.py](avaliar.py) | avaliação SWT e TGE, incluindo as métricas de processo do agente |
| [comparar.py](comparar.py) | tabela comparativa entre modelos |
| [resultados/comparativo.md](resultados/comparativo.md) | comparativo (também em `.csv`) |
| `resultados/<modelo>/` | `swt.csv`, `tge_full.csv`, `tge_compl.csv`, `resumo.json` e `resumo.md` |
| `saidas/<modelo>/<tarefa>/` | respostas brutas + `meta.json` (turnos, pytests, tokens, custo) |

## 10. Harness v2: DeepSeek Flash sem raciocínio

**Objetivo:** levar o modelo mais barato (US$ 0,09 na v1) o mais perto possível de 100%, sem trapaça. Nenhuma informação do gabarito (patch de correção, mutantes, suíte-ouro ou defeitos injetados) chega ao modelo. Só mudam as instruções e as ferramentas. A v2 grava com o rótulo `deepseek-flash-sem-raciocinio-v2` e não sobrescreve a v1.

### 10.1 O que mudou (`--harness v2`)

As falhas da v1 eram todas oráculos errados (seção 3.2). A v2 ataca exatamente essa causa:

| Modo | v1 | v2 |
|---|---|---|
| Todos | prompt do benchmark | + regras de oráculo: afirmar só o comportamento descrito, não calcular constantes de cabeça, atenção à semântica do Python (`%` com negativos, `int('3.9')`, `$` em regex) |
| SWT zeroshot | 1 chamada | análise antes do código + 2ª chamada de **autorrevisão** asserção por asserção (ainda sem executar nada) |
| SWT agente | escrever o teste e vê-lo falhar | + calcular os valores esperados com `run_python` e **verificar o lado corrigido**: copiar para `fixcheck/`, aplicar a correção mínima que o próprio modelo deduz da issue e confirmar que o teste passa; apagar asserções que falham lá. Limite de 20 turnos (era 15) |
| TGE (completo e completar) | 1 chamada, sem executar | **agente**: roda o pytest contra `alvo.py` (correto por definição, somente leitura) e corrige ou apaga cada teste que falha. No *completar*, o contexto fica somente leitura e o harness monta `test_alvo.py = contexto + teste novo`, igual ao avaliador |

**Por que não é trapaça:** o `fixcheck/` contém uma correção escrita pelo próprio modelo, não o patch real. O `alvo.py` do TGE já era entregue ao modelo na v1. Executá-lo é o que um desenvolvedor faria. Mutantes e defeitos nunca entram no sandbox.

**Ressalva de comparabilidade:** na v2 o TGE passa a ser agêntico. Compare a v2 com a v1 como "o que o mesmo modelo consegue com um harness melhor", não como o mesmo experimento.

### 10.2 Resultados (pass@1, média das 3 amostras)

| Medida | v1 | **v2** | Haiku |
|---|---|---|---|
| SWT zeroshot: S | 87,0% | **100%** | 100% |
| SWT agente: S | 95,7% | **98,6%** | 98,6% |
| TGE completo: all-pass | 27,8% | **100%** | 100% |
| TGE completo: falsos alarmes | 3,5% | **0%** | 0% |
| TGE completo: cobertura linhas / ramos | 99,7% / 99,6% | **100% / 100%** | 100% / 100% |
| TGE completo: mutation score | 96,8% | **99,3%** | 99,6% |
| TGE completo: detecção de defeitos | 97,2% | 97,2% | 100% |
| TGE *first*: pass@1 / Δ mutation | 66,7% / +22,2 | **94,4% / +53,9** | 100% / +25,6 |
| TGE *last* / *extra*: pass@1 | 94,4% / 72,2% | **100% / 100%** | 100% / 100% |
| pass@3 (todas as tarefas) | 100% | 100% | 100% |
| Custo das 210 tarefas | US$ 0,09 | US$ 0,17 | n/d |
| Tokens de entrada / saída | — | 2,75 M / 0,18 M | — |

### 10.3 O que ainda não é 100%

1. **SWT agente, 1 de 69** (`luhn_validate`, defeito `d2_sem_vai_um`, amostra 3). O agente bateu o limite de 20 turnos antes de terminar a verificação no `fixcheck/` e entregou 2 asserções que falham no código corrigido (P→F). Outras 3 tarefas também bateram o limite, mas entregaram teste correto.
2. **TGE *first*, 1 de 18** (`intword`, amostra 2). O teste passou no pytest do agente. Depois o modelo rodou `open('novo_teste.py','w').write(open('novo_teste.py').read())`, que trunca o arquivo antes de lê-lo, e entregou um arquivo vazio. É erro do modelo, não do avaliador.
3. **Detecção de defeitos em 97,2%:** é o mesmo valor da v1. As suítes da v2 pegam 99,3% dos mutantes, mas ainda deixam passar um dos defeitos injetados em algumas amostras.

**Possíveis ajustes legítimos para uma v3:** limite de 30 turnos, e impedir que `run_python` sobrescreva os arquivos de entrega (`test_issue.py`, `test_alvo.py`, `novo_teste.py`), deixando só `write_file` gravá-los. Como pass@3 já é 100% em tudo, o que resta é ruído de amostra única.
