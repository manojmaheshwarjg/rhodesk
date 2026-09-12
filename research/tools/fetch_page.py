import sys, re, html, subprocess, pathlib
url, out = sys.argv[1], sys.argv[2]
try:
    raw = subprocess.run(["curl","-sL","--max-time","40","-A","Mozilla/5.0 (compatible; research)",url],
                         capture_output=True, timeout=60).stdout.decode("utf-8","ignore")
except Exception as e:
    raw = ""
t = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', raw)
t = re.sub(r'(?is)<br\s*/?>', '\n', t)
t = re.sub(r'(?is)</(p|div|li|h[1-6]|tr|section)>', '\n', t)
t = re.sub(r'(?s)<[^>]+>', ' ', t)
t = html.unescape(t)
t = re.sub(r'[ \t ]+', ' ', t)
t = re.sub(r'\n\s*\n\s*\n+', '\n\n', t)
t = "\n".join(line.strip() for line in t.splitlines())
p = pathlib.Path(out); p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(f"SOURCE: {url}\n\n{t.strip()}\n", encoding="utf-8")
print(f"{len(t):7d}  {url}")
