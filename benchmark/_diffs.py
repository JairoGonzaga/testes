import difflib, re, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent / "funcoes"
def limpar(txt):
    linhas = txt.replace("\r\n", "\n").split("\n")
    while linhas and re.match(r"#\s*(DEFEITO INJETADO|Trecho original)", linhas[0]):
        linhas.pop(0)
    return "\n".join(linhas)
for f in sorted(R.iterdir()):
    ref = (f / "referencia.py").read_text(encoding="utf-8").replace("\r\n", "\n")
    for d in sorted((f / "defeitos").glob("*.py")):
        raw = d.read_text(encoding="utf-8").replace("\r\n", "\n")
        hdr = [l for l in raw.split("\n")[:3] if l.startswith("#")]
        bug = limpar(raw)
        print(f"=== {f.name}/{d.stem}  {' | '.join(hdr)}")
        for l in difflib.unified_diff(bug.split("\n"), ref.split("\n"), "buggy", "fixed", n=0, lineterm=""):
            if not l.startswith(("---", "+++")): print("   ", l)
