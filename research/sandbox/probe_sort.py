import json,sys,time,base64
sys.path.insert(0,"/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox")
from pageall import get, OUT
res={}
def p(label,path,params,show=None):
    b,h,s=get(path,params)
    ok = s==200
    note=""
    if ok and show:
        k=show; arr=b.get(k,[])
        note=f"n={len(arr)} first={arr[0].get('id') if arr else None}"
    elif not ok:
        note=json.dumps(b)[:130]
    res[label]={"params":params,"status":s,"note":note}
    print(f"{label:52s} {s} {note}")
    time.sleep(1.05)

cands=["id","name","created_at","updated_at","amount","balance","account_name","account_type",
       "legal_name","email","total_revenue","initiated_at","posted_at","period_end","period_start",
       "available_at","due_date","date","status","invoice_number","last_4","counterparty_name"]
for c in cands: p(f"accounts sort_by={c}","/accounts",{"sort_by":c,"page_size":2},"accounts")
for c in cands: p(f"customers sort_by={c}","/invoicing/customers",{"sort_by":c,"page_size":2},"customers")
for c in ["asc","desc","ASC","up","1"]:
    p(f"accounts order={c}","/accounts",{"sort_by":"balance","order":c,"page_size":2},"accounts")
p("cards sort_by=name","/cards",{"sort_by":"name","page_size":2},"cards")
p("invoices sort_by=date","/invoicing/invoices",{"sort_by":"date","page_size":2},"invoices")
# cursor semantics
b,_,_=get("/transactions",{"page_size":5})
tok=b["page"]["next_page_token"]
print("tok1:", tok, base64.urlsafe_b64decode(tok+"==").decode())
time.sleep(1.1)
p("txn cross-endpoint token on /statements","/statements",{"page_size":5,"page_token":tok},"statements")
p("txn token with different page_size","/transactions",{"page_size":10,"page_token":tok},"transactions")
p("txn token with added filter","/transactions",{"page_size":5,"page_token":tok,"status":"settled"},"transactions")
b2,_,_=get("/transactions",{"page_size":5,"status":"settled"})
print("filtered tok:", b2["page"]["next_page_token"], base64.urlsafe_b64decode(b2["page"]["next_page_token"]+"==").decode())
time.sleep(1.1)
b3,_,_=get("/accounts",{"page_size":5})
print("accounts tok:", b3["page"]["next_page_token"], base64.urlsafe_b64decode(b3["page"]["next_page_token"]+"==").decode() if b3["page"]["next_page_token"] else None)
json.dump(res,open(f"{OUT}/probe_sort.json","w"),indent=1)
