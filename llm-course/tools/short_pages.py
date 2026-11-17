"""List chapters whose last page holds only a few lines (a 'spill' page worth fixing). Run after build.py.

    python3 tools/short_pages.py
"""
import json, pymupdf

doc = pymupdf.open("build/book.pdf")
p = json.load(open("build/pages.json"))
starts = sorted(set(p.values()))
for k, s in enumerate(starts):
    end = (starts[k + 1] - 1) if k + 1 < len(starts) else len(doc)
    page = doc[end - 1]
    blocks = [b for b in page.get_text("blocks") if b[4].strip() and b[3] < page.rect.height - 40]
    if not blocks:
        continue
    frac = (max(b[3] for b in blocks) - 50) / (page.rect.height - 110)
    name = [kk for kk, v in p.items() if v == s]
    if frac < 0.3 and end > s:
        print(f"{name} start {s} last page {end}: fill {frac:.0%}")
