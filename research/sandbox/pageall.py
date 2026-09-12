import json, os, sys, time, urllib.parse, urllib.request

BASE = "https://rhoapi-sandbox.rho.co/api/v1"
OUT  = "/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/full"
os.makedirs(OUT, exist_ok=True)

def get(path, params):
    url = BASE + path + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": "Bearer sandbox",
                                               "Accept": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode()), dict(r.headers), r.status
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code == 429:
                wait = float(e.headers.get("Retry-After") or 5) or 5
                time.sleep(max(wait, 5)); continue
            return {"__error__": body, "__status__": e.code}, dict(e.headers), e.code
        except Exception as ex:
            time.sleep(3)
            if attempt == 5:
                return {"__error__": str(ex)}, {}, -1
    return {"__error__": "retries exhausted"}, {}, -1

def page_all(path, key, extra=None, page_size=100, name=None):
    name = name or key
    items, tokens, pages = [], [], []
    tok = None
    n = 0
    while True:
        p = dict(extra or {})
        p["page_size"] = page_size
        if tok: p["page_token"] = tok
        body, hdrs, status = get(path, p)
        n += 1
        pages.append({"request_params": p, "status": status, "body": body})
        if "__error__" in body:
            print(f"  !! {name} page {n} error {status}: {str(body)[:200]}")
            break
        got = body.get(key, [])
        items.extend(got)
        tok = (body.get("page") or {}).get("next_page_token")
        tokens.append(tok)
        print(f"  {name} page {n}: {len(got)} items, next={str(tok)[:32]}")
        if not tok: break
        if n > 200:
            print("  !! bail at 200 pages"); break
        time.sleep(1.1)
    json.dump({"endpoint": path, "key": key, "extra": extra, "page_size": page_size,
               "total": len(items), "pages": len(pages), "tokens": tokens,
               "items": items},
              open(f"{OUT}/{name}.json", "w"), indent=1)
    json.dump(pages, open(f"{OUT}/{name}.raw_pages.json", "w"), indent=1)
    print(f"== {name}: {len(items)} items over {len(pages)} pages")
    return items

if __name__ == "__main__":
    jobs = [
        ("/accounts", "accounts", None, "accounts"),
        ("/cards", "cards", None, "cards"),
        ("/transactions", "transactions", None, "transactions"),
        ("/statements", "statements", None, "statements"),
        ("/invoicing/customers", "customers", None, "invoicing_customers"),
        ("/invoicing/customers", "customers", {"include_deleted": "true"}, "invoicing_customers_incl_deleted"),
        ("/invoicing/invoices", "invoices", None, "invoicing_invoices"),
    ]
    for path, key, extra, name in jobs:
        print(f"--- {path} {extra or ''}")
        page_all(path, key, extra, 100, name)
        time.sleep(1.2)
