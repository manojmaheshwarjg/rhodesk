import json, sys, time
sys.path.insert(0,"/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox")
from pageall import get, OUT

txns = json.load(open(f"{OUT}/transactions.json"))["items"]
out = []
for t in txns:
    for a in t.get("attachments") or []:
        b,h,s = get(f"/transactions/{t['id']}/files/{a['file_id']}", None)
        out.append({"transaction_id": t["id"], "file_id": a["file_id"], "status": s, "body": b})
        time.sleep(1.05)
json.dump(out, open(f"{OUT}/transaction_files.json","w"), indent=1)
print("transaction files:", len(out), "errors:", sum(1 for o in out if "__error__" in o["body"]))

inv = json.load(open(f"{OUT}/invoicing_invoices.json"))["items"]
out2 = []
for i in inv:
    fid = i.get("file_id")
    if not fid: continue
    b,h,s = get(f"/invoicing/invoices/{i['id']}/files/{fid}", None)
    out2.append({"invoice_id": i["id"], "file_id": fid, "status": s, "body": b})
    time.sleep(1.05)
json.dump(out2, open(f"{OUT}/invoice_files.json","w"), indent=1)
print("invoice files:", len(out2), "errors:", sum(1 for o in out2 if "__error__" in o["body"]))
