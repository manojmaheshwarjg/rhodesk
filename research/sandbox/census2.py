#!/usr/bin/env python3
"""Rho sandbox field-path census, v2: correct presence denominators."""
import json, os, collections

OUT = "/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/full"

def jtype(v):
    if v is None: return "null"
    if isinstance(v, bool): return "bool"
    if isinstance(v, int): return "int"
    if isinstance(v, float): return "float"
    if isinstance(v, str): return "string"
    if isinstance(v, list): return "array"
    if isinstance(v, dict): return "object"
    return "?"

class Census:
    def __init__(self):
        self.container = collections.Counter()  # path of the OBJECT -> how many such objects seen ("" = root record)
        self.present   = collections.Counter()
        self.nulls     = collections.Counter()
        self.types     = collections.defaultdict(collections.Counter)
        self.values    = collections.defaultdict(set)
        self.lens      = collections.defaultdict(collections.Counter)
        self.n = 0
    def walk(self, obj, prefix):
        if isinstance(obj, dict):
            self.container[prefix] += 1
            for k, v in obj.items():
                p = f"{prefix}.{k}" if prefix else k
                self.present[p] += 1
                self.types[p][jtype(v)] += 1
                if v is None: self.nulls[p] += 1
                elif isinstance(v, (str, int, float, bool)):
                    if len(self.values[p]) < 500: self.values[p].add(v)
                self.walk(v, p)
        elif isinstance(obj, list):
            self.lens[prefix][len(obj)] += 1
            for it in obj: self.walk(it, prefix + "[]")
    def add(self, rec):
        self.n += 1; self.walk(rec, "")
    def denom(self, path):
        parent = path.rsplit(".", 1)[0] if "." in path else ""
        return self.container.get(parent, self.n)

def L(name):
    p = f"{OUT}/{name}.json"
    return json.load(open(p))["items"] if os.path.exists(p) else []

def D(name):
    p = f"{OUT}/{name}.json"
    if not os.path.exists(p): return []
    out = []
    for _id, w in json.load(open(p)).items():
        b = w["body"]
        if "__error__" in b: continue
        if isinstance(b, dict) and len(b) == 1 and isinstance(list(b.values())[0], dict):
            out.append(list(b.values())[0])
        else: out.append(b)
    return out

RES = [
 ("accounts","accounts","accounts_detail"),
 ("cards","cards","cards_detail"),
 ("transactions","transactions","transactions_detail"),
 ("statements","statements","statements_detail"),
 ("invoicing_customers","invoicing_customers_incl_deleted","invoicing_customers_detail"),
 ("invoicing_invoices","invoicing_invoices","invoicing_invoices_detail"),
]

def vfmt(vals, cap=30):
    if not vals: return ""
    nums = all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in vals)
    if len(vals) <= cap:
        vs = sorted(vals, key=lambda x: (x if isinstance(x,(int,float)) and not isinstance(x,bool) else 0, str(x)))
        return ", ".join("`"+("<empty string>" if v=="" else str(v))+"`" for v in vs)
    if nums: return f"{len(vals)} distinct, min `{min(vals)}` max `{max(vals)}`"
    sv = sorted(str(v) for v in vals)
    return f"{len(vals)} distinct, `{sv[0]}` … `{sv[-1]}`"

rep = []
def e(s=""): rep.append(s)

e("| resource | list records | detail records | distinct field paths |")
e("|---|---|---|---|")
C = {}
for res, ln, dn in RES:
    lc, dc = Census(), Census()
    for r in L(ln): lc.add(r)
    for r in D(dn): dc.add(r)
    C[res] = (lc, dc)
    e(f"| {res} | {lc.n} | {dc.n} | {len(set(lc.present)|set(dc.present))} |")
e()

for res, ln, dn in RES:
    lc, dc = C[res]
    e(f"\n### `{res}` field census\n")
    e("`present` = occurrences of the key / occurrences of its containing object. "
      "A ratio below 1.0 means the key is **omitted** (not null) on some records.\n")
    e("| field path | JSON types | list present | list null | detail present | detail null | n distinct | observed values |")
    e("|---|---|---|---|---|---|---|---|")
    for p in sorted(set(lc.present)|set(dc.present)):
        t = "+".join(sorted(set(lc.types.get(p,{}))|set(dc.types.get(p,{}))))
        ld, dd = lc.denom(p), dc.denom(p)
        lp, dp = lc.present.get(p,0), dc.present.get(p,0)
        vals = (lc.values.get(p,set())|dc.values.get(p,set()))
        # skip giant signed URLs
        if p == "pdf_url":
            shown = "signed GCS URL, see §PDF analysis"
            nd = "n/a"
        else:
            shown = vfmt(vals); nd = len(vals)
        e(f"| `{p}` | {t} | {lp}/{ld} | {lc.nulls.get(p,0)} | {dp}/{dd} | {dc.nulls.get(p,0)} | {nd} | {shown} |")
    if lc.lens or dc.lens:
        e("\n**Array lengths**\n")
        e("| array path | length distribution (list surface) |")
        e("|---|---|")
        for p in sorted(set(lc.lens)|set(dc.lens)):
            dist = lc.lens.get(p) or dc.lens.get(p)
            e(f"| `{p}` | " + ", ".join(f"len {k} x{v}" for k,v in sorted(dist.items())) + " |")

open(f"{OUT}/../census_tables.md","w").write("\n".join(rep))
print("wrote", len(rep), "lines")
