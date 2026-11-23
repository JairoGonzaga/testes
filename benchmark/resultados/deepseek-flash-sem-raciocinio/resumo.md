# Benchmark SWT-Bench + TestGenEval (adaptado) — modelo: deepseek-flash-sem-raciocinio

## SWT-Bench (reprodução de issue, 23 instâncias × 3 amostras)

| Modo | W (aplicável) | S (sucesso) | pass@1 | pass@3 | algum F→P | algum P→F | ΔC patch | ΔC (sucessos) |
|---|---|---|---|---|---|---|---|---|
| zeroshot | 100.0% | 87.0% | 87.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |
| agente | 100.0% | 95.7% | 95.7% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |

## Processo do agente (SWT modo agente)

- turnos por tarefa: 6.1; bateu o limite de turnos: 1; argumentos de ferramenta inválidos: 0
- rodou pytest antes de entregar: 100.0%; viu o próprio teste falhar no código com defeito: 100.0%; último pytest falhando (o esperado): 100.0%
- S quando rodou pytest: 95.7%; S quando não rodou: —; entregou via arquivo: 100.0%
- custo por sucesso: US$ 0.0009

## TestGenEval — geração completa (6 funções × 3 amostras)

- utilizável: 100.0%; all-pass pass@1 27.8%, pass@3 83.3%; any-pass pass@1 100.0%
- testes por arquivo: 45.8; falsos alarmes: 3.5%
- cobertura de linhas 99.7%, de ramos 99.6%; mutation score 96.8%; detecção de defeitos 97.2%

## TestGenEval — completar testes (6 funções × 3 amostras por cenário)

| Cenário | pass@1 | pass@3 | Δ linhas | Δ ramos | Δ mutation | Δ defeitos |
|---|---|---|---|---|---|---|
| first | 66.7% | 100.0% | 17.7% | 18.3% | 22.2% | 21.3% |
| last | 94.4% | 100.0% | 2.2% | 4.9% | 1.8% | 0.0% |
| extra | 72.2% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
