"""Blank space at the bottom of each page in the given ranges (finds large gaps left by a figure pushed to the next page).

    python3 tools/page_gaps.py 100-120 200-205
"""
import sys, pymupdf

doc = pymupdf.open("build/book.pdf")
for a, b in [tuple(map(int, r.split("-"))) for r in sys.argv[1:]]:
    for pn in range(a, b + 1):
        page = doc[pn - 1]
        blocks = [bl for bl in page.get_text("blocks") if bl[4].strip() and bl[3] < page.rect.height - 40]
        draws = page.get_drawings()
        ys = [bl[3] for bl in blocks] + [d["rect"].y1 for d in draws if d["rect"].y1 < page.rect.height - 40]
        bottom = max(ys) if ys else 0
        first = min([bl[1] for bl in blocks] + [d["rect"].y0 for d in draws]) if ys else 0
        print(pn, "bottom gap (pt):", round(page.rect.height - 57 - bottom), " first item y:", round(first))
