import json, sys, time
sys.path.insert(0,"/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox")
from pageall import get, page_all, OUT

accts = json.load(open(f"{OUT}/accounts.json"))["items"]
txns  = json.load(open(f"{OUT}/transactions.json"))["items"]
seen = {t["id"] for t in txns}
print("baseline txns:", len(seen))

extra = {}
# by account
for a in accts:
    b,_,s = get("/transactions", {"account_id": a["id"], "page_size":100})
    got = b.get("transactions", [])
    new = [t for t in got if t["id"] not in seen]
    print(f"acct {a['id'][-4:]} {a['account_type']:10s} {a['account_name'][:22]:22s} -> {len(got):3d} txns, {len(new)} new")
    for t in new: seen.add(t["id"]); extra[t["id"]]=t
    time.sleep(1.05)

for st in ["pending","settled","failed","awaiting_approval"]:
    b,_,s = get("/transactions", {"status": st, "page_size":100})
    got = b.get("transactions", [])
    new = [t for t in got if t["id"] not in seen]
    print(f"status {st:18s} -> {len(got):3d}, {len(new)} new, nextpg={(b.get('page') or {}).get('next_page_token')}")
    for t in new: seen.add(t["id"]); extra[t["id"]]=t
    time.sleep(1.05)

for at in ["checking","credit","investment","savings","rewards"]:
    b,_,s = get("/transactions", {"account_type": at, "page_size":100})
    got = b.get("transactions", [])
    new = [t for t in got if t["id"] not in seen]
    print(f"acct_type {at:12s} -> {len(got):3d}, {len(new)} new")
    for t in new: seen.add(t["id"]); extra[t["id"]]=t
    time.sleep(1.05)

json.dump(list(extra.values()), open(f"{OUT}/transactions_extra_from_filters.json","w"), indent=1)
print("TOTAL distinct txn ids:", len(seen))
