#!/usr/bin/env python3
import json, os, re, collections, datetime, uuid
OUT="/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/full"
def L(n): return json.load(open(f"{OUT}/{n}.json"))["items"]
A=L("accounts"); C=L("cards"); T=L("transactions"); S=L("statements")
CU=L("invoicing_customers_incl_deleted"); CU_pub=L("invoicing_customers"); IV=L("invoicing_invoices")

print("="*20,"ID FORMAT")
def uinfo(s):
    try: u=uuid.UUID(s)
    except Exception: return ("NOT-UUID", None, None)
    return ("uuid", u.version, u.variant)
groups = {"account.id":[a["id"] for a in A], "card.id":[c["id"] for c in C],
  "transaction.id":[t["id"] for t in T], "transaction.money_movement_id":sorted({t["money_movement_id"] for t in T}),
  "statement.id":[s["id"] for s in S], "customer.id":[c["id"] for c in CU],
  "invoice.id":[i["id"] for i in IV], "invoice.file_id":[i["file_id"] for i in IV if i.get("file_id")],
  "txn.attachment.file_id":sorted({a["file_id"] for t in T for a in t["attachments"]}),
  "txn.user_id":sorted({t["user_id"] for t in T if t.get("user_id")}),
  "card.cardholder.user_id":sorted({c["cardholder"]["user_id"] for c in C}),
  "txn.card_id":sorted({t["card_id"] for t in T if t.get("card_id")}),
  "invoice.activities[].user_id":sorted({a["user_id"] for i in IV for a in i["activities"] if a.get("user_id")}),
  "invoice.payments[].transaction_id":sorted({p["transaction_id"] for i in IV for p in i["payments"] if p.get("transaction_id")}),
  "statement.accounts[].account_id":sorted({x["account_id"] for s in S for x in s["accounts"] if x.get("account_id")}),
}
for k,v in groups.items():
    vers=collections.Counter(uinfo(x)[1] for x in v)
    prefixes=collections.Counter(x.split("-")[0] for x in v)
    print(f"{k:38s} n={len(v):3d} versions={dict(vers)} prefixes={dict(prefixes)}")
    print(f"    sample: {v[:2]}")

print()
print("="*20,"UUIDv7 TIMESTAMP DECODE (transactions)")
def v7ts(s):
    h=s.replace("-","")
    ms=int(h[:12],16)
    return datetime.datetime.fromtimestamp(ms/1000, datetime.timezone.utc)
rows=[]
for t in sorted(T,key=lambda x:x["id"]):
    ts=v7ts(t["id"])
    init=datetime.datetime.fromisoformat(t["initiated_at"].replace("Z","+00:00"))
    rows.append((t["id"], ts.isoformat(), t["initiated_at"], (ts-init).total_seconds()))
print(f"{'id':40s} {'v7-embedded-ts':28s} {'initiated_at':22s} delta_s")
for r in rows[:8]+rows[-5:]: print(f"{r[0]:40s} {r[1]:28s} {r[2]:22s} {r[3]:.0f}")
deltas=[r[3] for r in rows]
print("delta seconds: min",min(deltas),"max",max(deltas),"nonzero:",sum(1 for d in deltas if abs(d)>0.5))
suffixes=collections.Counter(t["id"].split("-")[-1] for t in T)
print("v7 suffix (node) distinct:", len(suffixes), "sample:", list(suffixes)[:6])
print("v7 clock-seq segment values:", collections.Counter(t["id"].split("-")[2]+"/"+t["id"].split("-")[3] for t in T))
seqs=sorted(int(t["id"].split("-")[-1],16) for t in T)
print("suffix ints sorted:", seqs)

print()
print("="*20,"CURRENCY")
def walk(o,p=""):
    if isinstance(o,dict):
        for k,v in o.items(): yield from walk(v,f"{p}.{k}" if p else k)
    elif isinstance(o,list):
        for i in o: yield from walk(i,p+"[]")
    else: yield p,o
cur=collections.Counter()
for coll in (A,C,T,S,CU,IV):
    for r in coll:
        for p,v in walk(r):
            if p.endswith("currency"): cur[v]+=1
print("currency values:", dict(cur))

print()
print("="*20,"AMOUNT SIGN CONVENTION BY transaction_type")
bt=collections.defaultdict(lambda: [0,0,0,[]])
for t in T:
    a=t["amount"]["amount"]; k=t["transaction_type"]
    if a<0: bt[k][0]+=1
    elif a>0: bt[k][1]+=1
    else: bt[k][2]+=1
    bt[k][3].append(a)
print(f"{'transaction_type':34s} {'neg':>4s} {'pos':>4s} {'zero':>4s}  min..max")
for k in sorted(bt):
    n,p,z,vals=bt[k]
    print(f"{k:34s} {n:4d} {p:4d} {z:4d}  {min(vals)}..{max(vals)}")

print()
print("="*20,"SIGN BY account_type")
bt2=collections.defaultdict(lambda:[0,0,0])
for t in T:
    a=t["amount"]["amount"]; k=t["account_type"]
    bt2[k][0 if a<0 else (1 if a>0 else 2)]+=1
for k,v in sorted(bt2.items()): print(f"{k:12s} neg={v[0]:3d} pos={v[1]:3d} zero={v[2]:3d}")

print()
print("="*20,"DATE RANGES")
def rng(vals):
    vs=sorted(v for v in vals if v)
    return (vs[0], vs[-1], len(vs)) if vs else None
print("txn.initiated_at ", rng([t["initiated_at"] for t in T]))
print("txn.posted_at    ", rng([t.get("posted_at") for t in T]))
print("stmt.period_start", rng([s["period_start"] for s in S]))
print("stmt.period_end  ", rng([s["period_end"] for s in S]))
print("stmt.available_at", rng([s["available_at"] for s in S]))
print("cust.created_at  ", rng([c["created_at"] for c in CU]))
print("cust.updated_at  ", rng([c["updated_at"] for c in CU]))
print("inv.created_at   ", rng([i["created_at"] for i in IV]))
print("inv.date         ", rng([i["date"] for i in IV]))
print("inv.due_date     ", rng([i["due_date"] for i in IV]))
print("card.spend_period_start", rng([c.get("spend_period_start") for c in C]))
print("card.usage_starts_at   ", rng([c.get("usage_starts_at") for c in C]))
print("card.usage_ends_at     ", rng([c.get("usage_ends_at") for c in C]))
ts_re=re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")
d_re=re.compile(r"^\d{4}-\d{2}-\d{2}$")
allts=collections.Counter()
for coll,name in ((A,"accounts"),(C,"cards"),(T,"transactions"),(S,"statements"),(CU,"customers"),(IV,"invoices")):
    for r in coll:
        for p,v in walk(r):
            if isinstance(v,str):
                if ts_re.match(v): allts[(name,p,"datetime-Z")]+=1
                elif d_re.match(v): allts[(name,p,"date-only")]+=1
print("\ntemporal field shapes:")
for k,v in sorted(allts.items()): print(f"  {k[0]:12s} {k[1]:34s} {k[2]:12s} x{v}")

print()
print("="*20,"MONEY MOVEMENT GROUPS")
mm=collections.defaultdict(list)
for t in T: mm[t["money_movement_id"]].append(t)
multi={k:v for k,v in mm.items() if len(v)>1}
print("distinct money_movement_id:", len(mm), " with >1 entry:", len(multi))
for k,v in sorted(multi.items()):
    print(f"  {k}: {len(v)} legs")
    for t in sorted(v,key=lambda x:x["id"]):
        print(f"     {t['id']}  {t['transaction_type']:26s} {t['account_name'][:20]:20s} {t['amount']['amount']:>12d} {t['status']}")

print()
print("="*20,"REFERENTIAL INTEGRITY")
acct_ids={a["id"] for a in A}; card_ids={c["id"] for c in C}; txn_ids={t["id"] for t in T}
cust_ids={c["id"] for c in CU}; inv_ids={i["id"] for i in IV}
def chk(label, refs, universe):
    refs=set(r for r in refs if r)
    missing=refs-universe
    print(f"{label:44s} refs={len(refs):3d} resolve={len(refs&universe):3d} DANGLING={len(missing)} {sorted(missing)[:4]}")
chk("transaction.account_id -> accounts", [t["account_id"] for t in T], acct_ids)
chk("transaction.card_id -> cards", [t.get("card_id") for t in T], card_ids)
chk("statement.accounts[].account_id -> accounts", [x.get("account_id") for s in S for x in s["accounts"]], acct_ids)
chk("customer.last_invoice_id -> invoices", [c.get("last_invoice_id") for c in CU], inv_ids)
chk("invoice.customer.id -> customers", [i["customer"]["id"] for i in IV], cust_ids)
chk("invoice.payments[].transaction_id -> txns", [p.get("transaction_id") for i in IV for p in i["payments"]], txn_ids)
chk("card.cardholder.user_id -> txn.user_id set", [c["cardholder"]["user_id"] for c in C], {t["user_id"] for t in T if t.get("user_id")})
chk("invoice.activities[].user_id -> txn user ids", [a.get("user_id") for i in IV for a in i["activities"]], {t["user_id"] for t in T if t.get("user_id")})
print("accounts never referenced by any transaction:", sorted(acct_ids-{t["account_id"] for t in T}))
print("accounts never in any statement:", sorted(acct_ids-{x.get("account_id") for s in S for x in s["accounts"]}))
print("customers with no invoice:", sorted(cust_ids-{i["customer"]["id"] for i in IV}))
print("cards with no transaction:", sorted(card_ids-{t.get("card_id") for t in T}))

print()
print("="*20,"CARD / USER CROSS-CHECK")
u_from_txn={t["user_id"]:t["user_full_name"] for t in T if t.get("user_id")}
u_from_card={c["cardholder"]["user_id"]:c["cardholder"]["first_name"]+" "+c["cardholder"]["last_name"] for c in C}
for uid in sorted(set(u_from_txn)|set(u_from_card)):
    print(f"  {uid}  txn={u_from_txn.get(uid,'-'):18s} card={u_from_card.get(uid,'-')}")

print()
print("="*20,"CARD SPEND MATH")
for c in sorted(C,key=lambda x:x["id"]):
    sl=c["spending_limit"]; cs=c["current_spend"]; ps=c["pending_spend"]
    print(f"  {c['id'][-2:]} {c['name'][:26]:26s} {c['type']:8s} {c['status']:9s} {c['spending_limit_type']:8s} limit={sl['amount']:>9d} cur={cs['amount']:>9d} pend={ps['amount']:>7d} util={cs['amount']/sl['amount']*100:5.1f}% start={c['spend_period_start']} end={c['spend_period_end']}")

print()
print("="*20,"STATEMENTS DETAIL")
bytype=collections.Counter(s["statement_type"] for s in S)
print("by type:", dict(bytype))
print("accounts[] length dist:", collections.Counter(len(s["accounts"]) for s in S))
print("credit stmts with non-null account_id:", sum(1 for s in S if s["statement_type"]=="credit" and all(x.get("account_id") for x in s["accounts"])), "of", bytype["credit"])
pairs=collections.Counter((s["statement_type"], x["account_type"], x.get("account_id")) for s in S for x in s["accounts"])
for k,v in sorted(pairs.items(), key=lambda z:str(z)): print("  ",k,v)
import urllib.parse
blobs=collections.Counter(urllib.parse.urlparse(s["pdf_url"]).path for s in S if s.get("pdf_url"))
print("distinct pdf blob paths:", len(blobs), dict(blobs))
print("null pdf_url:", sum(1 for s in S if s.get("pdf_url") is None))
# statement id numeric?
sids=sorted(int(s["id"]) for s in S)
print("statement ids numeric sorted:", sids)
print("id len set:", {len(s["id"]) for s in S})

print()
print("="*20,"ACCOUNTS")
for a in sorted(A,key=lambda x:x["id"]):
    print(f"  {a['id']} {a['account_type']:9s} {a['account_name'][:20]:20s} bal={a['balance']['amount']:>10d} acct4={a.get('account_number_last_4','-')} rout4={a.get('routing_number_last_4','-')}")
print("sum of balances:", sum(a["balance"]["amount"] for a in A))
print("routing last4 distinct:", collections.Counter(a.get("routing_number_last_4") for a in A))
