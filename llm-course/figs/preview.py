"""Preview figures: python3 figs/preview.py out.png name1.svg name2.svg ... (renders with the book's fonts)."""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out, names = sys.argv[1], sys.argv[2:]
body = "".join(f'<div class="f"><div class="n">{n}</div>{open(os.path.join(ROOT, "figs", n), encoding="utf-8").read()}</div>'
               for n in names)
html = f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{ROOT}/book.css">
<style>body{{width:174mm;margin:6mm;background:#fff}} .f{{margin:0 0 8mm}} .n{{font:9pt monospace;color:#999}}</style>
</head><body>{body}</body></html>"""
path = os.path.join(ROOT, "build", "preview.html")
open(path, "w", encoding="utf-8").write(html)
js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage({{deviceScaleFactor: 1.6}});
await p.goto('file://{path}'); await p.evaluate(async () => {{ await document.fonts.ready; }});
await p.screenshot({{ path: '{os.path.abspath(out)}', fullPage: true }}); await b.close(); }})();"""
subprocess.run(["node", "-e", js], check=True, cwd=ROOT)
print("wrote", out)
