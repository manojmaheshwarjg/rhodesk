import json, sys, time, os
sys.path.insert(0,"/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox")
from pageall import get, OUT

def L(n): return json.load(open(f"{OUT}/{n}.json"))["items"]

jobs = [
 ("accounts_detail",   "/accounts/{}",            [a["id"] for a in L("accounts")]),
 ("cards_detail",      "/cards/{}",               [c["id"] for c in L("cards")]),
 ("transactions_detail","/transactions/{}",       [t["id"] for t in L("transactions")]),
 ("statements_detail", "/statements/{}",          [s["id"] for s in L("statements")]),
 ("invoicing_customers_detail","/invoicing/customers/{}", [c["id"] for c in L("invoicing_customers_incl_deleted")]),
 ("invoicing_invoices_detail","/invoicing/invoices/{}",   [i["id"] for i in L("invoicing_invoices")]),
]
for name, tmpl, ids in jobs:
    out = {}
    for i, _id in enumerate(ids):
        b, h, s = get(tmpl.format(_id), None)
        out[_id] = {"status": s, "body": b}
        if "__error__" in b: print(f"  !! {name} {_id} -> {s} {str(b)[:120]}")
        time.sleep(1.05)
    json.dump(out, open(f"{OUT}/{name}.json","w"), indent=1)
    print(f"== {name}: {len(out)} fetched")
