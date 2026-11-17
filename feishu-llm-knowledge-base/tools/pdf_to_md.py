"""把一个目录下所有 PDF 的文字抽出来，存成同名的 .pdf.md，方便检索。
用法：python3 tools/pdf_to_md.py <目录>"""
import pathlib, sys
import pymupdf

root = pathlib.Path(sys.argv[1])
for pdf in sorted(root.rglob("*.pdf")):
    out = pdf.with_name(pdf.name + ".md")
    if out.exists():
        continue
    with pymupdf.open(pdf) as doc:
        pages = [f"<!-- 第 {i + 1} 页 -->\n{p.get_text().strip()}" for i, p in enumerate(doc)]
    out.write_text(f"# {pdf.stem}\n\n（由 PDF 自动抽取的文字，排版和公式可能有损，原件见同目录的 PDF）\n\n" + "\n\n".join(pages) + "\n")
    print(out.relative_to(root), len(pages), "pages")
