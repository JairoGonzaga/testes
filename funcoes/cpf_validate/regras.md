# validate (CPF)

Valida um número de CPF (Cadastro de Pessoas Físicas). O CPF tem 11 dígitos, dos quais os
dois últimos são dígitos verificadores.

Exceções (todas podem ser importadas de `alvo`):

- `ValidationError` — base de todas, subclasse de `ValueError`;
- `InvalidFormat` — subclasse de `ValidationError`;
- `InvalidLength` — subclasse de `InvalidFormat`;
- `InvalidChecksum` — subclasse de `ValidationError`.

## Regras

- **R1** — Antes de validar, o número é compactado: removem-se espaços, hífens (`-`) e
  pontos (`.`), além de espaços em branco nas pontas. `"390.533.447-05"` é tratado como
  `"39053344705"`.
- **R2** — Se o número compactado tiver qualquer caractere que não seja dígito de 0 a 9,
  for vazio, ou for igual a zero (todos os dígitos `0`), levanta `InvalidFormat`.
  Exemplo: `"390.533.447=0"` → `InvalidFormat`. Valores que não são strings (por exemplo
  `None`) também levantam `InvalidFormat`.
- **R3** — Se o número compactado (só com dígitos) não tiver exatamente 11 dígitos,
  levanta `InvalidLength`.
- **R4** — Os dois últimos dígitos são verificadores. Sendo `n0…n8` os nove primeiros dígitos:
  - `d1 = (11 − Σ (10 − i)·n_i) mod 11 mod 10`, para i = 0…8;
  - `d2 = (11 − (Σ (11 − i)·n_i + 2·d1)) mod 11 mod 10`, para i = 0…8.

  Se o 10º e o 11º dígitos não forem `d1` e `d2`, levanta `InvalidChecksum`. Exemplo:
  `"231.002.999-00"` → `InvalidChecksum`.
- **R5** — As verificações seguem a ordem R2 → R3 → R4: a primeira que falhar define a
  exceção.
- **R6** — Se o número for válido, retorna o número compactado (11 dígitos, sem
  separadores): `"390.533.447-05"` → `"39053344705"`.
- **R7** — Números com todos os dígitos iguais não recebem tratamento especial: são válidos
  se os dígitos verificadores conferirem (por exemplo, `"111.111.111-11"` →
  `"11111111111"`).

## Fora do escopo

- Traços Unicode parecidos com o hífen (por exemplo `–` e `—`).
