#!/usr/bin/env python3
"""Walk the captured Rho sandbox JSON and emit a field-path census per resource."""
import json, os, re, collections

OUT = "/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/full"

def jtype(v):
    if v is None: return "null"
    if isinstance(v, bool): return "bool"
    if isinstance(v, int): return "int"
    if isinstance(v, float): return "float"
    if isinstance(v, str): return "string"
    if isinstance(v, list): return "array"
    if isinstance(v, dict): return "object"
    return type(v).__name__

class Census:
    def __init__(self):
        self.present = collections.Counter()   # path -> records where path key exists
        self.nulls   = collections.Counter()   # path -> times value was null
        self.types   = collections.defaultdict(collections.Counter)
        self.values  = collections.defaultdict(set)   # path -> observed scalar values
        self.toobig  = set()
        self.parents = collections.Counter()   # path -> times parent container existed
        self.n = 0

    def walk(self, obj, prefix, parent_seen=True):
        if isinstance(obj, dict):
            for k, v in obj.items():
                p = f"{prefix}.{k}" if prefix else k
                self.present[p] += 1
                self.types[p][jtype(v)] += 1
                if v is None: self.nulls[p] += 1
                if isinstance(v, (str, int, float, bool)) and not isinstance(v, bool) or isinstance(v, bool):
                    if len(self.values[p]) <= 400:
                        self.values[p].add(v)
                    else:
                        self.toobig.add(p)
                self.walk(v, p)
        elif isinstance(obj, list):
            self.arraylen(prefix, len(obj))
            for it in obj:
                self.walk(it, prefix + "[]")

    def arraylen(self, path, n):
        self.values[path + "#len"].add(n)

    def add(self, rec):
        self.n += 1
        self.walk(rec, "")

def load(name):
    p = f"{OUT}/{name}.json"
    if not os.path.exists(p): return None
    return json.load(open(p))

def records_from_list(name):
    d = load(name)
    return d["items"] if d else []

def records_from_detail(name, key=None):
    d = load(name)
    if not d: return []
    out = []
    for _id, wrap in d.items():
        b = wrap["body"]
        if "__error__" in b: continue
        # detail bodies are wrapped: {"transaction": {...}} or bare
        if isinstance(b, dict) and len(b) == 1 and isinstance(list(b.values())[0], dict):
            out.append(list(b.values())[0])
        else:
            out.append(b)
    return out

RESOURCES = {
  "accounts":            ("accounts", "accounts_detail"),
  "cards":               ("cards", "cards_detail"),
  "transactions":        ("transactions", "transactions_detail"),
  "statements":          ("statements", "statements_detail"),
  "invoicing_customers": ("invoicing_customers_incl_deleted", "invoicing_customers_detail"),
  "invoicing_invoices":  ("invoicing_invoices", "invoicing_invoices_detail"),
}

def fmt_values(vals, limit=40):
    vs = sorted(vals, key=lambda x: (str(type(x)), x if isinstance(x,(int,float)) else str(x)))
    if len(vs) > limit: return f"({len(vs)} distinct)"
    return ", ".join("`"+str(v)+"`" for v in vs)

report = []
def emit(s=""): report.append(s)

summary_rows = []
for res, (lname, dname) in RESOURCES.items():
    for mode, recs in (("list", records_from_list(lname)), ("detail", records_from_detail(dname))):
        c = Census()
        for r in recs: c.add(r)
        globals().setdefault("CEN", {})[(res, mode)] = c
        summary_rows.append((res, mode, c.n, len(c.present)))

CEN = globals()["CEN"]

emit("## A. Record counts and field-path counts\n")
emit("| resource | surface | records | distinct field paths |")
emit("|---|---|---|---|")
for r in summary_rows:
    emit(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
emit()

for res, (lname, dname) in RESOURCES.items():
    lc, dc = CEN[(res,"list")], CEN[(res,"detail")]
    emit(f"\n## {res}\n")
    emit(f"list records: {lc.n} | detail records: {dc.n}\n")
    paths = sorted(set(lc.present) | set(dc.present))
    emit("| field path | list present | list null | detail present | detail null | types | distinct | values / range |")
    emit("|---|---|---|---|---|---|---|---|")
    for p in paths:
        if p.endswith("#len"): continue
        lp, dp = lc.present.get(p,0), dc.present.get(p,0)
        ln, dn = lc.nulls.get(p,0), dc.nulls.get(p,0)
        tt = "+".join(sorted(set(list(lc.types.get(p,{}).keys()) + list(dc.types.get(p,{}).keys()))))
        allv = set(lc.values.get(p,set())) | set(dc.values.get(p,set()))
        allv = {v for v in allv if v is not None}
        nd = len(allv)
        if nd == 0: shown = ""
        elif nd <= 25: shown = fmt_values(allv)
        elif all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in allv):
            shown = f"min `{min(allv)}` max `{max(allv)}`"
        else:
            sv = sorted(str(v) for v in allv)
            shown = f"e.g. `{sv[0]}` … `{sv[-1]}`"
        lpct = f"{lp}/{lc.n}" if lc.n else "-"
        dpct = f"{dp}/{dc.n}" if dc.n else "-"
        emit(f"| `{p}` | {lpct} | {ln} | {dpct} | {dn} | {tt} | {nd} | {shown} |")
    # array lengths
    lens = {k:(set(lc.values.get(k,set()))|set(dc.values.get(k,set()))) for k in set(lc.values)|set(dc.values) if k.endswith("#len")}
    if lens:
        emit("\nArray cardinality:\n")
        emit("| array path | observed lengths |")
        emit("|---|---|")
        for k in sorted(lens):
            vs = sorted(lens[k])
            emit(f"| `{k[:-4]}` | min {min(vs)}, max {max(vs)}, set {{{', '.join(str(v) for v in vs)}}} |")

open(f"{OUT}/../census_tables.md","w").write("\n".join(report))
print("\n".join(report))
