import re, sys, pathlib
SP = pathlib.Path("/private/tmp/claude-501/-Users-manojmaheshwarjagadeesan-Desktop-Vivpro-Codebase-regain-frontend/32689851-de1d-4894-8a66-652780dfadbf/scratchpad/rho")
OUT = pathlib.Path.home()/"Desktop"/"project"

def slug(h):
    s = h.strip().lower()
    s = re.sub(r'[`*_\[\]()]', '', s)
    s = re.sub(r'[^\w\s-]', '', s)
    return re.sub(r'\s+', '-', s).strip('-')

def toc(body):
    lines = []
    for ln in body.splitlines():
        m = re.match(r'^(##|###)\s+(.*)$', ln)
        if not m: continue
        lvl, txt = len(m.group(1)), m.group(2).strip()
        if txt.startswith(('About this document','Contents','The short version','How this was researched')): continue
        indent = '' if lvl == 2 else '    '
        lines.append(f"{indent}- [{txt}](#{slug(txt)})")
    return "\n".join(lines)

def build(header, parts_glob, out_name):
    head = (SP/header).read_text()
    body = "".join(p.read_text() for p in sorted(SP.glob(parts_glob)))
    head = head.replace("{{TOC}}", toc(body))
    (OUT/out_name).write_text(head + body)
    n = (OUT/out_name)
    print(f"{out_name}: {len(n.read_text().split())} words, {n.stat().st_size} bytes")

build("dossier-header.md", "dossier/sec-*.md", "RHO_PRODUCT_DOSSIER.md")
build("api-header.md", "draft/sec-*.md", "RHO_API_REFERENCE.md")
