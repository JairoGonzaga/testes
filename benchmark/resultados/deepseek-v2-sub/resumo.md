# Benchmark SWT-Bench + TestGenEval (adaptado) — modelo: deepseek-flash-sem-raciocinio-v2

## SWT-Bench (reprodução de issue, 23 instâncias × 3 amostras)

| Modo | W (aplicável) | S (sucesso) | pass@1 | pass@3 | algum F→P | algum P→F | ΔC patch | ΔC (sucessos) |
|---|---|---|---|---|---|---|---|---|
| zeroshot | 100.0% | 100.0% | 100.0% | — | 100.0% | 0.0% | 100.0% | 100.0% |
| agente | 100.0% | 100.0% | 100.0% | — | 100.0% | 0.0% | 100.0% | 100.0% |

## Processo do agente (SWT modo agente)

- turnos por tarefa: 5.5; bateu o limite de turnos: 0; argumentos de ferramenta inválidos: 0
- rodou pytest antes de entregar: 100.0%; viu o próprio teste falhar no código com defeito: 100.0%; último pytest falhando (o esperado): 0.0%
- S quando rodou pytest: 100.0%; S quando não rodou: —; entregou via arquivo: 100.0%
- custo por sucesso: US$ 0.0007

## TestGenEval — geração completa (6 funções × 3 amostras)

- utilizável: 100.0%; all-pass pass@1 100.0%, pass@3 —; any-pass pass@1 100.0%
- testes por arquivo: 66.0; falsos alarmes: 0.0%
- cobertura de linhas 100.0%, de ramos 100.0%; mutation score 97.4%; detecção de defeitos 100.0%

## TestGenEval — completar testes (6 funções × 3 amostras por cenário)

| Cenário | pass@1 | pass@3 | Δ linhas | Δ ramos | Δ mutation | Δ defeitos |
|---|---|---|---|---|---|---|
| first | 100.0% | — | 29.8% | 60.0% | 30.1% | 58.3% |
| last | 100.0% | — | 2.5% | 5.0% | 2.5% | 0.0% |
| extra | 100.0% | — | 0.0% | 0.0% | 0.0% | 0.0% |
