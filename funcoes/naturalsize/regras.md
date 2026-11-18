# naturalsize

Formata uma quantidade de bytes como tamanho de arquivo legível (por exemplo `"10.0 kB"`).

## Regras

- **R1** — O valor (`int`, `float` ou `str` numérica) é convertido com `float()`. Se a
  conversão falhar, a exceção de `float()` é propagada: string não numérica →
  `ValueError`; `None` → `TypeError`.
- **R2** — Valor absoluto exatamente 1, fora do modo GNU: `"1 Byte"` (singular), com o
  sinal preservado (`-1` → `"-1 Byte"`).
- **R3** — Valor absoluto menor que a base (1000 no modo decimal, 1024 nos modos binário e
  GNU): retorna a parte inteira seguida de `" Bytes"` (`0` → `"0 Bytes"`, `999` →
  `"999 Bytes"`, `naturalsize(1023, binary=True)` → `"1023 Bytes"`). No modo GNU, o
  formato é `"<n>B"`, sem espaço, inclusive para 1 (`naturalsize(300, gnu=True)` → `"300B"`).
- **R4** — Modo decimal (padrão): base 1000 e sufixos `kB`, `MB`, `GB`, `TB`, `PB`, `EB`,
  `ZB`, `YB`, `RB`, `QB`, separados do número por um espaço. O número é formatado com
  `format` (padrão `"%.1f"`) e o sinal é preservado. Exemplos: `3000000` → `"3.0 MB"`,
  `10**28` → `"10.0 RB"`.
- **R5** — `binary=True`: base 1024 e sufixos `KiB`, `MiB`, `GiB`, `TiB`, `PiB`, `EiB`,
  `ZiB`, `YiB`, `RiB`, `QiB`. Exemplos: `naturalsize(3000, True)` → `"2.9 KiB"`,
  `naturalsize(-4096, True)` → `"-4.0 KiB"`.
- **R6** — `gnu=True`: base 1024, sufixos de uma letra (`K`, `M`, `G`, `T`, `P`, `E`, `Z`,
  `Y`, `R`, `Q`) sem espaço. Quando `gnu=True`, o parâmetro `binary` é ignorado.
  Exemplo: `naturalsize(3000, False, True)` → `"2.9K"`.
- **R7** — O parâmetro `format` define a formatação do número:
  `naturalsize(3000, False, True, "%.3f")` → `"2.930K"`.
- **R8** — Se o arredondamento levar o número a alcançar a base, usa-se o sufixo
  seguinte: `999_999` → `"1.0 MB"` (e não `"1000.0 kB"`).
- **R9** — Acima do maior sufixo (`QB`, `QiB`, `Q`), o número continua crescendo com esse
  sufixo: `10**34 * 3` → `"30000.0 QB"`.

## Fora do escopo

- Valores não inteiros abaixo da base (por exemplo, `1.5`).
- Valores não finitos (`inf`, `nan`).
