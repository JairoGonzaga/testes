import importlib.util, re, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent / "funcoes"
def load(path, name):
    src = path.read_text(encoding="utf-8")
    spec = importlib.util.spec_from_loader(name, loader=None); m = importlib.util.module_from_spec(spec)
    exec(compile(src, str(path), "exec"), m.__dict__); return m
def run(m, call):
    try: return "returns " + repr(eval(call, m.__dict__))
    except Exception as e: return f"raises {type(e).__name__}"
PROBES = {
 "apnumber": {"d1": "apnumber(0)", "d2": "apnumber(9)", "d3": "apnumber(None)"},
 "cpf_validate": {"d1": "validate('00000000000')", "d2": "validate('111444777350')", "d3": "validate('111.444.777-35')", "d4": "validate('11144477735')"},
 "intword": {"d1": "intword(1000)", "d2": "intword(999999)", "d3": "intword(-1000000)", "d4": "intword(1000000)"},
 "luhn_validate": {"d1": "validate('79927398713')", "d2": "validate('79927398713')", "d3": "validate('')", "d4": "validate(79927398713)"},
 "naturalsize": {"d1": "naturalsize(1000)", "d2": "naturalsize(3000000, binary=True)", "d3": "naturalsize(-1)", "d4": "naturalsize(999999)"},
 "ordinal": {"d1": "ordinal(13)", "d2": "ordinal(11)", "d3": "ordinal(111)", "d4": "ordinal('something else')"},
}
for f, probes in PROBES.items():
    ref = load(R / f / "referencia.py", "ref")
    for d in sorted((R / f / "defeitos").glob("*.py")):
        k = d.stem.split("_")[0]; bug = load(d, "bug"); c = probes[k]
        a, b = run(bug, c), run(ref, c)
        print(f"{'OK ' if a!=b else 'XX '} {f}/{d.stem}: {c} -> buggy {a} | fixed {b}")
