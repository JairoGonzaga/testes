# Benchmark SWT-Bench + TestGenEval (adaptado) — modelo: deepseek-flash

## SWT-Bench (reprodução de issue, 23 instâncias × 3 amostras)

| Modo | W (aplicável) | S (sucesso) | pass@1 | pass@3 | algum F→P | algum P→F | ΔC patch | ΔC (sucessos) |
|---|---|---|---|---|---|---|---|---|
| zeroshot | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |
| agente | 100.0% | 98.6% | 98.6% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |

## Processo do agente (SWT modo agente)

- turnos por tarefa: 7.5; bateu o limite de turnos: 2; argumentos de ferramenta inválidos: 0
- rodou pytest antes de entregar: 100.0%; viu o próprio teste falhar no código com defeito: 100.0%; último pytest falhando (o esperado): 97.1%
- S quando rodou pytest: 98.6%; S quando não rodou: —; entregou via arquivo: 100.0%
- custo por sucesso: US$ 0.0025

## TestGenEval — geração completa (6 funções × 3 amostras)

- utilizável: 33.3%; all-pass pass@1 33.3%, pass@3 50.0%; any-pass pass@1 33.3%
- testes por arquivo: 95.2; falsos alarmes: 0.0%
- cobertura de linhas 100.0%, de ramos 100.0%; mutation score 98.6%; detecção de defeitos 100.0%

## TestGenEval — completar testes (6 funções × 3 amostras por cenário)

| Cenário | pass@1 | pass@3 | Δ linhas | Δ ramos | Δ mutation | Δ defeitos |
|---|---|---|---|---|---|---|
| first | 100.0% | 100.0% | 27.4% | 37.1% | 36.1% | 38.0% |
| last | 94.4% | 100.0% | 2.3% | 5.2% | 2.2% | 0.0% |
| extra | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
