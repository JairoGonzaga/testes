# Benchmark SWT-Bench + TestGenEval (adaptado) — modelo: deepseek-flash-sem-raciocinio-v2

## SWT-Bench (reprodução de issue, 23 instâncias × 3 amostras)

| Modo | W (aplicável) | S (sucesso) | pass@1 | pass@3 | algum F→P | algum P→F | ΔC patch | ΔC (sucessos) |
|---|---|---|---|---|---|---|---|---|
| zeroshot | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |
| agente | 100.0% | 98.6% | 98.6% | 100.0% | 100.0% | 1.4% | 100.0% | 100.0% |

## Processo do agente (SWT modo agente)

- turnos por tarefa: 8.0; bateu o limite de turnos: 4; argumentos de ferramenta inválidos: 0
- rodou pytest antes de entregar: 100.0%; viu o próprio teste falhar no código com defeito: 100.0%; último pytest falhando (o esperado): 13.0%
- S quando rodou pytest: 98.6%; S quando não rodou: —; entregou via arquivo: 100.0%
- custo por sucesso: US$ 0.0010

## TestGenEval — geração completa (6 funções × 3 amostras)

- utilizável: 100.0%; all-pass pass@1 100.0%, pass@3 100.0%; any-pass pass@1 100.0%
- testes por arquivo: 58.8; falsos alarmes: 0.0%
- cobertura de linhas 100.0%, de ramos 100.0%; mutation score 99.3%; detecção de defeitos 97.2%

## TestGenEval — completar testes (6 funções × 3 amostras por cenário)

| Cenário | pass@1 | pass@3 | Δ linhas | Δ ramos | Δ mutation | Δ defeitos |
|---|---|---|---|---|---|---|
| first | 94.4% | 100.0% | 44.5% | 65.0% | 53.9% | 73.5% |
| last | 100.0% | 100.0% | 2.2% | 4.9% | 2.1% | 0.0% |
| extra | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
