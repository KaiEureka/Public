"""Render pages a..b of a PDF side by side into one PNG, for checking layout at a glance.

    python3 tools/contact_sheet.py build/book.pdf 1 24 sheet.png [columns]
"""
import sys, pymupdf

pdf, a, b, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 4
doc = pymupdf.open(pdf)
pages = list(range(a - 1, min(b, len(doc))))
z = 0.55
w, h = doc[0].rect.width * z, doc[0].rect.height * z
rows = (len(pages) + cols - 1) // cols
sheet = pymupdf.open()
pg = sheet.new_page(width=w * cols, height=h * rows)
for k, i in enumerate(pages):
    r = pymupdf.Rect((k % cols) * w, (k // cols) * h, (k % cols + 1) * w, (k // cols + 1) * h)
    pg.show_pdf_page(r, doc, i)
    pg.draw_rect(r, color=(0.7, 0.7, 0.7), width=0.5)
    pg.insert_text((r.x0 + 4, r.y0 + 10), str(i + 1), fontsize=9, color=(1, 0, 0))
pg.get_pixmap(dpi=110).save(out)
print(out)
