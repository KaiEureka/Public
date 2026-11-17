"""Build the web edition: src/*.md -> site/, one HTML page per front section, part, chapter and appendix,
with a sidebar table of contents, full-text search, clickable figure references and (if built) the PDF.

site/_main.html contains the embeddable home page. site/publish_files.json lists its companion files.

    python3 build_web.py                 # uses build/book.pdf when it exists
    python3 build_web.py --pdf path.pdf  # link a specific PDF
"""
import argparse, html, json, os, re, shutil, subprocess

from build import ROOT, SRC, ORDER, MD_FORMAT, cjk_quotes, figures

SITE, WEB = os.path.join(ROOT, "site"), os.path.join(ROOT, "web")
TITLE = "从零造一个前沿大模型"
# the figures name the print fonts; on screen fall back to whatever CJK / serif fonts the reader has
SVG_SANS = "BookSans, -apple-system, PingFang SC, Hiragino Sans GB, Microsoft YaHei, Noto Sans CJK SC, Source Han Sans SC, sans-serif"
SVG_SERIF = "LatinSerif, STIX Two Text, Times New Roman, serif"
MM_PX = 4.2  # 165 mm (a full-width figure) -> 693 px, about the width of the text column


def pandoc_fragment(md):
    cmd = ["pandoc", "-f", MD_FORMAT, "-t", "html5", "--mathml", "--wrap=none", "--highlight-style=tango"]
    return subprocess.run(cmd, input=md, capture_output=True, text=True, check=True).stdout


def highlight_css():
    tpl = os.path.join(ROOT, "build", "hl.tpl")
    os.makedirs(os.path.dirname(tpl), exist_ok=True)
    open(tpl, "w").write("$highlighting-css$\n")
    cmd = ["pandoc", "-f", "markdown", "-t", "html5", "--standalone", "--template", tpl, "--highlight-style=tango",
           "--metadata", "title=x"]
    return subprocess.run(cmd, input="```python\nx = 1\n```\n", capture_output=True, text=True, check=True).stdout


def strip_tags(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def plain(h):
    """Searchable text of an HTML fragment: figures keep only their captions, formulas become their TeX."""
    h = re.sub(r"<svg\b.*?</svg>", " ", h, flags=re.S)
    h = re.sub(r'<math\b.*?<annotation encoding="application/x-tex">(.*?)</annotation>.*?</math>',
               lambda m: " " + m.group(1) + " ", h, flags=re.S)
    return strip_tags(h)


def web_svg(s):
    s = s.replace('font-family="BookSans"', f'font-family="{SVG_SANS}"').replace('font-family="LatinSerif"', f'font-family="{SVG_SERIF}"')
    # px width for the screen; drop the inline max-width so style.css can leave room for the white card's padding
    return re.sub(r'(<svg\b[^>]*style="width:)([0-9.]+)mm;max-width:100%', lambda m: f"{m.group(1)}{float(m.group(2)) * MM_PX:.0f}px", s)


def split_pages(name, h):
    """One page per source file, except the front matter, which has one page per top-level heading."""
    pieces = [h]
    if name == "00_front":
        cuts = [m.start() for m in re.finditer(r"<h1\b", h)]
        pieces = [h[a:b] for a, b in zip(cuts, cuts[1:] + [len(h)])]
    pages = []
    for p in pieces:
        m = re.search(r'<(h1|h2|section)\b[^>]*\bid="([^"]+)"[^>]*>', p)
        t = re.search(r"<(h1|h2)\b[^>]*>(.*?)</\1>", p, flags=re.S)
        kind = "front" if name == "00_front" else "part" if name.startswith("part") or name == "appendix" else "chapter"
        secs = [(i, strip_tags(x)) for i, x in re.findall(r'<h3\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h3>', p, flags=re.S)]
        pages.append(dict(slug=m.group(2), title=strip_tags(t.group(2)), kind=kind, body=p, secs=secs))
    return pages


def git(*args):
    try:
        env = dict(os.environ, TZ="Asia/Shanghai")
        return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, check=True, env=env).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def sidebar(groups, cur):
    out = ['<a class="side-home%s" href="index.html">封面与目录</a>' % (" current" if cur == "index" else "")]
    for head, items in groups:
        if head:
            out.append(f'<a class="side-part{" current" if head["slug"] == cur else ""}" href="{head["slug"]}.html">{html.escape(head["title"])}</a>')
        out.append('<ul class="side-list">')
        for p in items:
            here = p["slug"] == cur
            out.append(f'<li><a class="side-ch{" current" if here else ""}" href="{p["slug"]}.html">{html.escape(p["title"])}</a>')
            if here and p["secs"]:
                out.append('<ul class="side-secs">' + "".join(
                    f'<li><a href="#{i}" data-sec="{i}">{html.escape(t)}</a></li>' for i, t in p["secs"]) + "</ul>")
            out.append("</li>")
        out.append("</ul>")
    return "\n".join(out)


def pager(prev, nxt):
    def card(p, cls, label):
        if not p:
            return '<span></span>'
        return f'<a class="{cls}" href="{p["slug"]}.html"><small>{label}</small>{html.escape(p["title"])}</a>'
    return f'<nav class="pager">{card(prev, "prev", "上一页")}{card(nxt, "next", "下一页")}</nav>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default=os.path.join(ROOT, "build", "book.pdf"))
    args = ap.parse_args()

    # 1. markdown -> html per source file; number figures over the whole book so references resolve across chapters
    frags = []
    for name in ORDER:
        md = cjk_quotes(open(os.path.join(SRC, name + ".md"), encoding="utf-8").read().strip(), name)
        frags.append((name, pandoc_fragment(md)))
    joined = "".join(f"<!--@@FILE:{n}@@-->\n{h}" for n, h in frags)
    joined = re.sub(r'\sdata-scale="[^"]*"', "", joined)  # print-only pagination tweak
    joined = web_svg(figures(joined, link=True))
    joined = re.sub(r"<table\b", '<div class="tw"><table', joined).replace("</table>", "</table></div>")
    parts = re.split(r"<!--@@FILE:([\w]+)@@-->\n", joined)[1:]
    pages = [pg for name, h in zip(parts[0::2], parts[1::2]) for pg in split_pages(name, h)]

    # 2. reading order and sidebar groups: front pages, then each part (or the appendix) with its chapters
    groups = [(None, [])]
    for p in pages:
        if p["kind"] == "part":
            groups.append((p, []))
        else:
            groups[-1][1].append(p)
    for head, items in groups[1:]:
        lis = "".join(f'<li><a href="{c["slug"]}.html">{html.escape(c["title"])}</a></li>' for c in items)
        label = "各附录" if head["slug"] == "appendix" else "本篇各章"
        head["body"] += f'<div class="part-chapters"><h3>{label}</h3><ul>{lis}</ul></div>'

    # 3. links to ids on other pages (figure references across chapters)
    owner = {}
    for p in pages:
        for i in re.findall(r'\bid="([^"]+)"', p["body"]):
            owner.setdefault(i, p["slug"])
    for p in pages:
        own = set(re.findall(r'\bid="([^"]+)"', p["body"]))
        p["body"] = re.sub(r'href="#([^"]+)"', lambda m: m.group(0) if m.group(1) in own or m.group(1) not in owner
                           else f'href="{owner[m.group(1)]}.html#{m.group(1)}"', p["body"])

    # 4. site skeleton
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    shutil.copytree(os.path.join(WEB, "fonts"), os.path.join(SITE, "fonts"))
    os.makedirs(os.path.join(SITE, "assets"))
    shutil.copy(os.path.join(WEB, "app.js"), os.path.join(SITE, "assets", "app.js"))
    css = open(os.path.join(WEB, "style.css"), encoding="utf-8").read() + "\n/* pandoc syntax highlighting (tango) */\n" + highlight_css()
    open(os.path.join(SITE, "assets", "style.css"), "w", encoding="utf-8").write(css)
    has_pdf = os.path.exists(args.pdf)
    if has_pdf:
        shutil.copy(args.pdf, os.path.join(SITE, "book.pdf"))
    tpl = open(os.path.join(WEB, "page.html"), encoding="utf-8").read()
    pdf_link = '<button class="bar-btn pdf-dl" type="button" title="下载 PDF 版">PDF</button>' if has_pdf else ""

    def write(slug, title, body, cls):
        page = (tpl.replace("{{title}}", html.escape(title)).replace("{{book}}", TITLE).replace("{{pdf}}", pdf_link)
                .replace("{{sidebar}}", sidebar(groups, slug)).replace("{{class}}", cls).replace("{{body}}", body))
        open(os.path.join(SITE, slug + ".html"), "w", encoding="utf-8").write(page)

    for k, p in enumerate(pages):
        prev = pages[k - 1] if k else None
        nxt = pages[k + 1] if k + 1 < len(pages) else None
        write(p["slug"], f'{p["title"]} · {TITLE}', p["body"] + pager(prev, nxt), "page-" + p["kind"])

    # 5. home page: cover, last update, table of contents
    cover = re.search(r'<section class="cover">.*?</section>', open(os.path.join(ROOT, "template.html"), encoding="utf-8").read(), re.S).group(0)
    skip = ("--invert-grep", "--grep=^归档对话记录")  # conversation backups are not changes to the book
    last = git("log", "-1", *skip, "--format=%cd|%h|%s", "--date=format-local:%Y-%m-%d %H:%M")
    when = ""
    if last:
        d, hsh, subj = last.split("|", 2)
        when = f'<p class="updated">最近更新：{d}（UTC+8）· {html.escape(subj)} · <a href="changelog.html">全部更新记录</a></p>'
    actions = ('<div class="cover-actions"><a class="btn primary" href="preface.html">开始阅读</a>'
               + ('<button class="btn pdf-dl" type="button">下载 PDF</button>' if has_pdf else "") + "</div>")
    toc = ['<div class="home-toc"><h2>目　录</h2>']
    for head, items in groups:
        toc.append(f'<h3><a href="{head["slug"]}.html">{html.escape(head["title"])}</a></h3>' if head else "<h3>前言与说明</h3>")
        toc.append("<ul>" + "".join(f'<li><a href="{c["slug"]}.html">{html.escape(c["title"])}</a></li>' for c in items) + "</ul>")
    toc.append("</div>")
    write("index", TITLE, cover.replace("</section>", actions + "</section>") + when + "".join(toc), "page-home")

    # 6. update log from git history
    log = git("log", "-n", "200", *skip, "--format=%cd|%h|%s", "--date=format-local:%Y-%m-%d %H:%M")
    rows = "".join(f"<tr><td>{d}</td><td><code>{h}</code></td><td>{html.escape(s)}</td></tr>"
                   for d, h, s in (l.split("|", 2) for l in log.splitlines() if l))
    write("changelog", f"更新记录 · {TITLE}", '<h1 class="front" id="changelog">更新记录</h1>'
          '<p>每次修订书稿后，网页版与 PDF 一起重新发布。时间为 UTC+8。</p>'
          f'<div class="tw"><table><thead><tr><th>时间</th><th>版本</th><th>说明</th></tr></thead><tbody>{rows}</tbody></table></div>',
          "page-front")
    write("404", f"页面不存在 · {TITLE}", '<h1 class="front">页面不存在</h1><p><a href="index.html">回到目录</a></p>', "page-front")

    # 7. search index: one entry per section (and per page intro)
    index = []
    for p in pages:
        cuts = [(m.end(), m.group(1), strip_tags(m.group(2))) for m in re.finditer(r'<h3\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h3>', p["body"], flags=re.S)]
        spans = [(0, "", "")] + cuts
        for (a, sid, st), (b, _, _) in zip(spans, spans[1:] + [(len(p["body"]), "", "")]):
            text = plain(re.sub(r"<h3\b.*", "", p["body"][a:b], flags=re.S))  # section text up to the next heading
            if text:
                index.append([p["slug"], sid, p["title"] + (" › " + st if st else ""), text])
    json.dump(index, open(os.path.join(SITE, "assets", "search.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

    # 8. artifact form of the home page, and the list of files published next to it
    home = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    head = re.search(r"<title>.*?</title>", home, re.S).group(0) + "\n" + re.search(r'<link rel="stylesheet"[^>]*>', home).group(0)
    open(os.path.join(SITE, "_main.html"), "w", encoding="utf-8").write(head + "\n" + re.search(r"<body[^>]*>\n?(.*)</body>", home, re.S).group(1))
    files = sorted(os.path.relpath(os.path.join(d, f), SITE) for d, _, fs in os.walk(SITE) for f in fs)
    files = [f for f in files if f not in ("index.html", "_main.html", "publish_files.json")]
    json.dump(files, open(os.path.join(SITE, "publish_files.json"), "w"), indent=0)
    print(f"web: {len(pages)} pages, {len(index)} search entries, pdf: {'yes' if has_pdf else 'no'} -> {SITE}")


if __name__ == "__main__":
    main()
