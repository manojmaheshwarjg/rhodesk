import json, sys, time
sys.path.insert(0,"/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox")
from pageall import get, OUT
res={}
def probe(label, path, params):
    b,h,s = get(path, params)
    key = [k for k in b if k not in ("page",)] if isinstance(b,dict) else []
    n = None
    for k in key:
        if isinstance(b.get(k), list): n = len(b[k]); break
    res[label] = {"params":params,"status":s,"count":n,"body_head":json.dumps(b)[:200]}
    print(f"{label:48s} {s} n={n} {'' if s==200 else json.dumps(b)[:120]}")
    time.sleep(1.05)

for st in ["printing","shipped","out_for_delivery","activate_card","delivery_canceled","active","expiring","locked","canceled","suspended","expired"]:
    probe(f"cards.status={st}", "/cards", {"status":st,"page_size":100})
for t in ["physical","virtual"]:
    probe(f"cards.type={t}", "/cards", {"type":t,"page_size":100})
for st in ["paid","unpaid","cancelled","overdue","confirm_payment","pending_payout"]:
    probe(f"invoices.status={st}", "/invoicing/invoices", {"status":st,"page_size":100})
for t in ["account","credit","treasury","checking","savings"]:
    probe(f"statements.type={t}", "/statements", {"statement_type":t,"page_size":100})
# bogus enum behaviour
probe("cards.status=bogus", "/cards", {"status":"bogus"})
probe("txn.status=bogus", "/transactions", {"status":"bogus"})
probe("txn.sort_by=amount", "/transactions", {"sort_by":"amount","order":"asc","page_size":3})
probe("txn.sort_by=bogus", "/transactions", {"sort_by":"bogus"})
probe("acct.sort_by=bogus", "/accounts", {"sort_by":"bogus"})
probe("stmt.sort_by=bogus", "/statements", {"sort_by":"bogus"})
probe("cust.sort_by=bogus", "/invoicing/customers", {"sort_by":"bogus"})
probe("txn.unknown_param", "/transactions", {"nonsense":"x","page_size":2})
probe("txn.id.notfound", "/transactions/00000000-0000-4000-8000-000000000000", None)
probe("acct.id.notfound", "/accounts/00000000-0000-4000-8000-000000000000", None)
probe("acct.id.malformed", "/accounts/not-a-uuid", None)
probe("unknown.resource", "/payments", None)
probe("unknown.resource2", "/users", None)
probe("unknown.resource3", "/webhooks", None)
probe("unknown.resource4", "/counterparties", None)
probe("unknown.resource5", "/business", None)
probe("txn.badtoken", "/transactions", {"page_token":"garbage"})
json.dump(res, open(f"{OUT}/probe_enums.json","w"), indent=1)
