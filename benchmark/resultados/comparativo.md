# Comparativo entre modelos

S = sucesso SWT (falha no código com defeito, passa no corrigido); ΔC = cobertura das linhas do patch; ag = modo agente (turnos, % que rodou pytest, % que viu o próprio teste falhar no código com defeito); TGE = suíte completa (pass@1 da amostra); first/last/extra = completar testes.

| Modelo | Custo (US$) | SWT zs S | SWT zs pass@3 | SWT zs ΔC | SWT ag S | SWT ag pass@3 | SWT ag W | SWT ag execuções | ag turnos | ag rodou pytest | ag viu falhar | TGE all-pass | TGE any-pass | TGE linhas | TGE ramos | TGE mutação | TGE defeitos | TGE falsos alarmes | first pass@1 | first Δmut | last pass@1 | extra pass@1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| haiku | – | 100.0% | 100.0% | 100.0% | 98.6% | 100.0% | 98.6% | 1.9 | – | – | – | 100.0% | 100.0% | 100.0% | 100.0% | 99.6% | 100.0% | 0.0% | 100.0% | 25.6% | 100.0% | 100.0% |
| deepseek-flash | 0.509 | 100.0% | 100.0% | 100.0% | 98.6% | 100.0% | 100.0% | 4.1 | 7.5 | 100.0% | 100.0% | 33.3% | 33.3% | 100.0% | 100.0% | 98.6% | 100.0% | 0.0% | 100.0% | 36.1% | 94.4% | 100.0% |
| deepseek-flash-sem-raciocinio | 0.092 | 87.0% | 100.0% | 100.0% | 95.7% | 100.0% | 100.0% | 2.7 | 6.1 | 100.0% | 100.0% | 27.8% | 100.0% | 99.7% | 99.6% | 96.8% | 97.2% | 3.5% | 66.7% | 22.2% | 94.4% | 72.2% |
| deepseek-flash-sem-raciocinio-v2 | 0.167 | 100.0% | 100.0% | 100.0% | 98.6% | 100.0% | 100.0% | 4.8 | 8.0 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 99.3% | 97.2% | 0.0% | 94.4% | 53.9% | 100.0% | 100.0% |
