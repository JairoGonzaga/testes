# Benchmark SWT-Bench + TestGenEval (adaptado) — modelo: haiku

## SWT-Bench (reprodução de issue, 23 instâncias × 3 amostras)

| Modo | W (aplicável) | S (sucesso) | pass@1 | pass@3 | algum F→P | algum P→F | ΔC patch | ΔC (sucessos) |
|---|---|---|---|---|---|---|---|---|
| zeroshot | 100.0% | 100.0% | 100.0% | — | 100.0% | 0.0% | 100.0% | 100.0% |
| agente | 100.0% | 100.0% | 100.0% | — | 100.0% | 0.0% | 100.0% | 100.0% |

## TestGenEval — geração completa (6 funções × 3 amostras)

- utilizável: 100.0%; all-pass pass@1 100.0%, pass@3 —; any-pass pass@1 100.0%
- testes por arquivo: 139.2; falsos alarmes: 0.0%
- cobertura de linhas 100.0%, de ramos 100.0%; mutation score 99.6%; detecção de defeitos 100.0%

## TestGenEval — completar testes (6 funções × 3 amostras por cenário)

| Cenário | pass@1 | pass@3 | Δ linhas | Δ ramos | Δ mutation | Δ defeitos |
|---|---|---|---|---|---|---|
| first | 100.0% | — | 19.5% | 19.7% | 27.9% | 26.4% |
| last | 100.0% | — | 2.2% | 4.9% | 1.8% | 0.0% |
| extra | 100.0% | — | 0.0% | 0.0% | 0.0% | 0.0% |
