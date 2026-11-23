# Benchmark: SWT-Bench + TestGenEval (adaptados)

Mede quão bem um modelo de IA escreve testes pytest para as funções deste projeto. Usa duas metodologias de artigos, reimplementadas sobre o nosso código (os datasets originais, como Django e SymPy, não são usados):

- **[SWT-Bench](https://arxiv.org/abs/2406.12952)**: o modelo recebe uma *issue* e o código com defeito e precisa escrever um teste que **falhe agora e passe depois da correção**. Roda em dois modos: *zeroshot* (uma resposta) e *agente* (sandbox onde o modelo pode rodar `pytest`).
- **[TestGenEval](https://arxiv.org/abs/2410.00752)**: o modelo escreve uma suíte inteira, ou completa uma suíte existente (*first*, *last*, *extra*). A suíte é medida por cobertura, mutation score, defeitos detectados e falsos alarmes.

**Base:** 6 funções (`apnumber`, `cpf_validate`, `intword`, `luhn_validate`, `naturalsize`, `ordinal`), 23 defeitos injetados e 39 mutantes por função. São 210 tarefas por modelo: 70 tarefas × 3 amostras.

📄 **Relatório completo:** [RELATORIO.md](RELATORIO.md) · **Resumo em PDF (3 páginas):** [RESUMO_benchmark.pdf](RESUMO_benchmark.pdf)

## Resultados

pass@1, média das 3 amostras:

| Medida | Haiku | DeepSeek Flash (com raciocínio) | DeepSeek Flash (sem raciocínio) | DeepSeek Flash (sem raciocínio, harness v2) |
|---|:-:|:-:|:-:|:-:|
| SWT zeroshot: sucesso | **100%** | **100%** | 87,0% | **100%** |
| SWT agente: sucesso | 98,6% | 98,6% | 95,7% | 98,6% |
| TGE suíte completa: all-pass | **100%** | 33,3%¹ | 27,8% | **100%** |
| TGE suíte completa: mutation score | **99,6%** | 98,6% | 96,8% | 99,3% |
| TGE suíte completa: falsos alarmes | 0% | 0% | 3,5% | 0% |
| TGE completar *first*: pass@1 / ganho de mutation | 100% / +25,6 | 100% / +36,1 | 66,7% / +22,2 | 94,4% / **+53,9** |
| TGE completar *last* / *extra*: pass@1 | 100% / 100% | 94,4% / 100% | 94,4% / 72,2% | 100% / 100% |
| Custo das 210 tarefas | n/d² | US$ 0,51 | **US$ 0,09** | US$ 0,17 |

¹ O raciocínio estourou o limite de 16.384 tokens de saída antes de terminar a suíte.
² O Haiku rodou como subagente do Claude Code, que não informa custo por chamada.

**O que os números mostram:**

1. **O benchmark separa os modelos.** O modelo mais fraco cai bastante, então as tarefas têm dificuldade real.
2. **O erro típico é o oráculo errado, não a reprodução.** Os testes que falham reproduzem a issue, mas trazem um valor esperado calculado de cabeça que também quebra no código corrigido.
3. **O harness v2 leva o modelo barato ao nível do Haiku.** Ele exige conferir os oráculos executando o código e não dá ao modelo nenhum dado do gabarito. O DeepSeek sem raciocínio ficou quase todo em 100%, por US$ 0,17.

**Modelos gratuitos (Groq):** gpt-oss-120b, gpt-oss-20b e Qwen. A rodada está em andamento e vai devagar por causa do limite de 200 mil tokens por dia em cada modelo (veja a [seção 8 do relatório](RELATORIO.md#8-como-reproduzir--rodar-com-outro-modelo)).

A tabela com todas as métricas, por modelo, está em [resultados/comparativo.md](resultados/comparativo.md) (também em [CSV](resultados/comparativo.csv)).

## Como rodar

Use Python 3.10 ou mais novo, com as dependências do [requirements.txt](../requirements.txt) da raiz. Os comandos rodam a partir da raiz do repositório.

```bash
# 1. Gerar instâncias, suítes-ouro, prompts, jobs.json e sandboxes
python benchmark/preparar.py --amostras 3 --sandbox <pasta-fora-do-repo> --modelo <rotulo>

# 2. Gerar os testes com o modelo (DeepSeek, OpenRouter ou Groq)
export DEEPSEEK_API_KEY=...   # PowerShell: $env:DEEPSEEK_API_KEY = "..."
python benchmark/gerar_openrouter.py --provedor deepseek --modelos deepseek-flash \
    --sem-raciocinio --harness v2 --teto-usd 1.0 --workers 10

# 3. Avaliar e comparar
python benchmark/avaliar.py --modelo deepseek-flash-sem-raciocinio-v2
python benchmark/comparar.py
```

- **Retomada:** o gerador continua de onde parou. Tarefas com `meta.json` são puladas e as que deram erro (`erro.json`) são refeitas.
- **Gasto:** `--teto-usd` interrompe a rodada ao atingir o valor e `--cota` mostra o saldo da conta.
- **Groq de graça:** use `--provedor groq --amostras 1 --limite 2`, que roda um subconjunto fixo de 12 tarefas.
- **Outros provedores:** os detalhes, incluindo como gerar via subagentes Claude com [gerar_workflow.js](gerar_workflow.js), estão na [seção 8 do relatório](RELATORIO.md#8-como-reproduzir--rodar-com-outro-modelo).

> As chaves de API vêm só de variáveis de ambiente (ou do `.env`, que está no `.gitignore`). Nada é gravado nos arquivos de saída.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| [issues.json](issues.json) | as 23 issues (título, corpo e chamada que reproduz o defeito) |
| [preparar.py](preparar.py) | monta instâncias, suítes-ouro, contextos, prompts, `jobs.json` e sandboxes |
| [gerar_openrouter.py](gerar_openrouter.py) | gerador via API: zeroshot e agente com ferramentas, harness v1/v2, custo e retomada |
| [gerar_workflow.js](gerar_workflow.js) | gerador via subagentes Claude (Workflow do Claude Code) |
| [avaliar.py](avaliar.py) | métricas SWT (S, W, F→P, ΔC, pass@k) e TGE (cobertura, mutação, defeitos, falsos alarmes) |
| [comparar.py](comparar.py) | tabela comparativa entre modelos |
| [dados/](dados/) | instâncias SWT (`buggy.py`/`fixed.py`), material TGE, prompts e `jobs.json` |
| [saidas/](saidas/) | resposta de cada modelo por tarefa, com `meta.json` (turnos, pytests, tokens e custo) |
| [resultados/](resultados/) | por modelo: `swt.csv`, `tge_full.csv`, `tge_compl.csv`, `resumo.json` e `resumo.md` |
