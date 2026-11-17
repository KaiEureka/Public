"""Build the textbook: Markdown (src/) -> pandoc HTML (MathML) -> Chromium PDF, with page numbers in the TOC."""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, BUILD = os.path.join(ROOT, "src"), os.path.join(ROOT, "build")
ORDER = (["00_front"]
         + ["part1"] + [f"ch{i:02d}" for i in range(0, 5)]
         + ["part2"] + [f"ch{i:02d}" for i in range(5, 10)]
         + ["part3"] + [f"ch{i:02d}" for i in range(10, 14)]
         + ["part4"] + [f"ch{i:02d}" for i in range(14, 18)]
         + ["part5"] + [f"ch{i:02d}" for i in range(18, 24)]
         + ["part6"] + [f"ch{i:02d}" for i in range(24, 30)]
         + ["part7"] + [f"ch{i:02d}" for i in range(30, 33)]
         + ["part8"] + [f"ch{i:02d}" for i in range(33, 36)]
         + ["part9"] + [f"ch{i:02d}" for i in range(36, 40)]
         + ["appendix", "appA", "appB", "appC", "appD", "appE"])


MD_FORMAT = "markdown+fenced_divs+pipe_tables+tex_math_dollars+header_attributes-implicit_figures-smart"
CODE_SPAN = re.compile(r"(`+)(.+?)\1")


def cjk_quotes(md, name=""):
    """Turn ASCII double quotes in prose into Chinese curly quotes (pandoc's 'smart' gets CJK context wrong).
    Code fences, inline code, raw HTML lines and lines with HTML attributes are left untouched."""
    out, in_fence = [], False
    for no, line in enumerate(md.split("\n"), 1):
        st = line.lstrip()
        if st.startswith("```"):
            in_fence = not in_fence
            out.append(line); continue
        if in_fence or st.startswith("<") or '="' in line or '"' not in line:
            out.append(line); continue
        pieces, pos, opened = [], 0, False
        for m in CODE_SPAN.finditer(line):
            pieces.append((False, line[pos:m.start()])); pieces.append((True, m.group(0))); pos = m.end()
        pieces.append((False, line[pos:]))
        res = []
        for is_code, txt in pieces:
            if is_code:
                res.append(txt); continue
            buf = []
            for ch in txt:
                if ch == '"':
                    buf.append("\u201d" if opened else "\u201c"); opened = not opened
                else:
                    buf.append(ch)
            res.append("".join(buf))
        if opened:
            print(f"warning: unbalanced quotes in {name}.md line {no}: {line[:60]}")
        out.append("".join(res))
    return "\n".join(out)


def assemble():
    parts, missing = [], []
    for name in ORDER:
        p = os.path.join(SRC, name + ".md")
        if os.path.exists(p):
            parts.append(cjk_quotes(open(p, encoding="utf-8").read().strip(), name))
        else:
            missing.append(name)
    md = "\n\n".join(parts) + "\n"
    path = os.path.join(BUILD, "book.md")
    open(path, "w", encoding="utf-8").write(md)
    return path, missing


def pandoc(md_path, html_path):
    cmd = ["pandoc", md_path, "-f", MD_FORMAT,
           "-t", "html5", "--standalone", "--template", os.path.join(ROOT, "template.html"), "--mathml",
           "--toc", "--toc-depth=2", "--highlight-style=tango", "--metadata", "title=从零造一个前沿大模型",
           "-o", html_path]
    subprocess.run(cmd, check=True)


def figures(s, link=False):
    """Inline figs/*.svg into <figure data-svg=...>, number figures per chapter, resolve {{fig-id}} references
    (as links to the figure when link=True, for the web edition)."""
    def inline(m):
        svg = open(os.path.join(ROOT, "figs", m.group(2)), encoding="utf-8").read()
        sc = re.search(r'\bdata-scale="([0-9.]+)"', m.group(1))
        if sc:  # shrink a figure slightly when it decides whether a chapter's last lines spill onto a new page
            svg = re.sub(r'width:([0-9.]+)mm', lambda w: f"width:{float(w.group(1)) * float(sc.group(1)):.1f}mm", svg, count=1)
        return m.group(1) + "\n" + svg
    s = re.sub(r'(<figure\b[^>]*\bdata-svg="([^"]+)"[^>]*>)', inline, s)
    ids, out, pos, chap, k, pending = {}, [], 0, None, 0, None
    for m in re.finditer(r'<h2\b[^>]*\bid="(?:ch(\d+)|app([A-E]))"|<figure\b([^>]*)>|<figcaption>', s):
        if m.group(1) or m.group(2):
            chap, k = (str(int(m.group(1))) if m.group(1) else m.group(2)), 0
        elif m.group(0).startswith("<figure"):
            attrs = m.group(3) or ""
            if "nonum" in attrs or chap is None:
                pending = None
                continue
            k += 1
            pending = f"图 {chap}.{k}"
            fid = re.search(r'\bid="([^"]+)"', attrs)
            if fid:
                ids[fid.group(1)] = pending
        elif pending:
            out.append(s[pos:m.end()] + pending + "\u3000")
            pos, pending = m.end(), None
    out.append(s[pos:])
    s = "".join(out)
    missing = set()
    def ref(m):
        if m.group(1) not in ids:
            missing.add(m.group(1))
        label = ids.get(m.group(1), "图 ?")
        return f'<a class="figref" href="#{m.group(1)}">{label}</a>' if link and m.group(1) in ids else label
    s = re.sub(r"\{\{(fig-[\w-]+)\}\}", ref, s)
    if missing:
        print("warning: unresolved figure references:", ", ".join(sorted(missing)))
    return s


def postprocess(html_path, pages=None):
    s = figures(open(html_path, encoding="utf-8").read())
    # invisible page markers right after part/chapter/front headings (outside the heading -> not in the PDF outline)
    s = re.sub(r'(<h([12])\b[^>]*\bid="([^"]+)"[^>]*>.*?</h\2>)', lambda m: m.group(1) + f'<div class="pnmark">@@PN:{m.group(3)}@@</div>', s, flags=re.S)
    # part pages: pandoc moves the heading id onto the wrapping <section class="partpage">
    s = re.sub(r'(<section id="([^"]+)" class="[^"]*\bpartpage\b[^"]*">\s*<h1\b[^>]*>.*?</h1>)', lambda m: m.group(1) + f'<div class="pnmark">@@PN:{m.group(2)}@@</div>', s, flags=re.S)
    # toc entries: title + dotted leader + page number
    def toc_link(m):
        href, rest, text = m.group(1), m.group(2), m.group(3)
        pn = (pages or {}).get(href, "")
        return f'<a href="#{href}"{rest}><span class="t">{text}</span><span class="dots"></span><span class="pn">{pn}</span></a>'
    head, sep, tail = s.partition('<nav id="TOC"')
    toc, sep2, body = tail.partition("</nav>")
    toc = re.sub(r'<a href="#([^"]+)"([^>]*)>(.*?)</a>', toc_link, toc, flags=re.S)
    s = head + sep + toc + sep2 + body
    open(html_path, "w", encoding="utf-8").write(s)


def render(html_path, pdf_path):
    subprocess.run(["node", os.path.join(ROOT, "render.js"), html_path, pdf_path], check=True)


def find_pages(pdf_path):
    import pymupdf
    doc = pymupdf.open(pdf_path)
    pages = {}
    for i, pg in enumerate(doc):
        # markers are 2 px text; some machines extract them with stray spaces ("pref ace"), so drop all whitespace
        for m in re.finditer(r"@@PN:([^@\s]+)@@", re.sub(r"\s+", "", pg.get_text())):
            pages.setdefault(m.group(1), i + 1)
    return pages, len(doc)


if __name__ == "__main__":
    os.makedirs(BUILD, exist_ok=True)
    md, missing = assemble()
    if missing:
        print("missing sources:", ", ".join(missing))
    out_html = os.path.join(BUILD, "book.html")
    out_pdf = os.path.join(BUILD, "book.pdf")
    pandoc(md, out_html); postprocess(out_html); render(out_html, out_pdf)
    pages, n = find_pages(out_pdf)
    pandoc(md, out_html); postprocess(out_html, pages); render(out_html, out_pdf)   # second pass: TOC page numbers
    pages2, n2 = find_pages(out_pdf)
    changed = {k: (pages[k], pages2.get(k)) for k in pages if pages[k] != pages2.get(k)}
    print(f"pages: {n2}; headings located: {len(pages2)}; page numbers changed in pass 2: {changed or 'none'}")
    lost = [k for k in re.findall(r"@@PN:([^@\s]+)@@", open(out_html, encoding="utf-8").read()) if k not in pages2]
    if lost:
        print("warning: headings not found in the PDF (no TOC page number):", ", ".join(lost))
    json.dump(pages2, open(os.path.join(BUILD, "pages.json"), "w"), ensure_ascii=False, indent=0)
    # lossless re-save (shared objects merged, streams compressed): about 22 MB -> 12 MB, same pages and text
    import pymupdf
    with pymupdf.open(out_pdf) as doc:
        doc.save(out_pdf + ".tmp", garbage=4, deflate=True, deflate_fonts=True, deflate_images=True, use_objstms=1)
    os.replace(out_pdf + ".tmp", out_pdf)
