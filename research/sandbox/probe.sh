#!/bin/bash
# probe.sh LABEL PATH_AND_QUERY [extra curl args...]
D=/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/probe-filters
B=https://rhoapi-sandbox.rho.co/api/v1
probe() {
  local label="$1"; shift
  local pq="$1"; shift
  local st
  st=$(curl -s -o "$D/$label.body" -D "$D/$label.hdr" -w '%{http_code}' --max-time 40 \
      -H "Authorization: Bearer sandbox" "$B$pq" "$@")
  echo "$pq" > "$D/$label.url"
  python3 - "$label" "$st" "$pq" <<'PY'
import sys,json,base64,hashlib,os
D="/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho/sandbox/probe-filters"
label,st,pq=sys.argv[1],sys.argv[2],sys.argv[3]
raw=open(os.path.join(D,label+".body"),"rb").read()
ct=""
for l in open(os.path.join(D,label+".hdr")):
    if l.lower().startswith("content-type:"): ct=l.split(":",1)[1].strip()
def d(s):
    s+="="*(-len(s)%4)
    try: return base64.urlsafe_b64decode(s).decode()
    except Exception: return "?"
try:
    j=json.loads(raw)
except Exception:
    print(f"{label}\t{st}\t{ct}\tNON-JSON\t{raw[:120]!r}"); sys.exit()
if isinstance(j,dict) and any(k in j for k in ("accounts","cards","transactions","statements","customers","invoices")):
    k=[k for k in ("accounts","cards","transactions","statements","customers","invoices") if k in j][0]
    items=j[k]; ids=[str(i.get("id")) for i in items]
    h=hashlib.sha1("|".join(ids).encode()).hexdigest()[:8]
    tok=(j.get("page") or {}).get("next_page_token")
    f=t=""
    if tok:
        try:
            o=json.loads(d(tok)); f=o.get("f",""); t=d(o.get("t",""))
        except Exception: f="?"
    print(f"{label}\t{st}\t{k}={len(items)}\tids={h}\tf={f}\tt={t}\tfirst={ids[0] if ids else '-'}")
else:
    print(f"{label}\t{st}\t{ct}\t{json.dumps(j)[:300]}")
PY
  sleep 1
}
