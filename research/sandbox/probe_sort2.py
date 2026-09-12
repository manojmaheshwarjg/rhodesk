import json,sys,time,base64
sys.path.insert(0,"/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox")
from pageall import get, OUT
def dec(t):
    if not t: return None
    o=json.loads(base64.urlsafe_b64decode(t+"=="))
    try: o["t_decoded"]=base64.urlsafe_b64decode(o["t"]+"===").decode()
    except Exception: pass
    return o
print("=== cursor shape per endpoint (page_size=1)")
for path,key in [("/accounts","accounts"),("/cards","cards"),("/transactions","transactions"),
                 ("/statements","statements"),("/invoicing/customers","customers"),("/invoicing/invoices","invoices")]:
    b,_,s=get(path,{"page_size":1})
    print(f"{path:24s} {s} tok={dec((b.get('page') or {}).get('next_page_token'))}")
    time.sleep(1.05)
print()
print("=== accounts sort_by extra candidates")
for c in ["balance","account_name","account_number_last_4","routing_number_last_4","type","account_balance","name"]:
    b,_,s=get("/accounts",{"sort_by":c,"page_size":1}); print(f"  {c:26s} {s}"); time.sleep(1.05)
print("=== customers sort_by extra candidates")
for c in ["created_at","legal_name","company_name","customer_name","revenue","total","deleted_at","last_invoice_id"]:
    b,_,s=get("/invoicing/customers",{"sort_by":c,"page_size":1}); print(f"  {c:26s} {s}"); time.sleep(1.05)
print("=== cards sort_by candidates (does it validate?)")
for c in ["name","bogus","last_4","status"]:
    b,_,s=get("/cards",{"sort_by":c,"page_size":1}); print(f"  {c:26s} {s}"); time.sleep(1.05)
print("=== invoices sort_by candidates")
for c in ["date","bogus","due_date","total"]:
    b,_,s=get("/invoicing/invoices",{"sort_by":c,"page_size":1}); print(f"  {c:26s} {s}"); time.sleep(1.05)
print()
print("=== does transactions sort_by actually sort?")
for sb,od in [("amount","asc"),("amount","desc"),("initiated_at","asc"),("posted_at","desc"),("bogus","asc")]:
    b,_,s=get("/transactions",{"sort_by":sb,"order":od,"page_size":4})
    arr=b.get("transactions",[])
    print(f"  sort_by={sb:14s} order={od:5s} -> " + " | ".join(f"{t['amount']['amount']}@{t['initiated_at'][:10]}" for t in arr))
    time.sleep(1.05)
print("=== statements sort_by")
for sb,od in [("period_end","asc"),("period_end","desc"),("period_start","asc"),("available_at","asc"),("bogus","asc")]:
    b,_,s=get("/statements",{"sort_by":sb,"order":od,"page_size":4})
    arr=b.get("statements",[])
    print(f"  sort_by={sb:14s} order={od:5s} {s} -> " + " | ".join(f"{x['period_end']}" for x in arr))
    time.sleep(1.05)
print("=== default order per endpoint (first 3 ids)")
for path,key in [("/accounts","accounts"),("/cards","cards"),("/transactions","transactions"),
                 ("/statements","statements"),("/invoicing/customers","customers"),("/invoicing/invoices","invoices")]:
    b,_,s=get(path,{"page_size":3}); arr=b.get(key,[])
    print(f"  {path:24s} " + " | ".join(str(x.get('id')) for x in arr))
    time.sleep(1.05)
