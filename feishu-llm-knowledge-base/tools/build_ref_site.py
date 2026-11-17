"""把 reference/ 下导出的飞书知识库做成一个网站（可发布成 Claude Artifact），沿用本书网页版的样式与脚本。

    python3 tools/build_ref_site.py            # reference/飞书_LLMs知识库 -> ref_site/

- 每篇文档一页；图片以 data URI 内嵌进页面，所以发布的文件数很少（Artifact 一次最多 255 个文件）。
- 左侧是按九个部分分组的目录，顶部是全文搜索（复用 web/app.js，搜索索引按每道题一条）。
- PDF 附件单独成页：显示自动抽取的文字（Artifact 不允许嵌入 PDF，原件留在仓库）。
- ref_site/_main.html 是首页的 Artifact 形式，ref_site/publish_files.json 列出其余要发布的文件。
"""
import base64, html, json, mimetypes, os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "reference", "飞书_LLMs知识库")
OUT = os.path.join(ROOT, "ref_site")
WEB = os.path.join(ROOT, "web")
TITLE = "LLMs 知识库（飞书导出）"


def pandoc(md):
    cmd = ["pandoc", "-f", "markdown+tex_math_dollars-raw_html", "-t", "html5", "--mathml", "--wrap=none",
           "--highlight-style=tango", "--shift-heading-level-by=0"]
    return subprocess.run(cmd, input=md, capture_output=True, text=True, check=True).stdout


def strip_tags(h):
    h = re.sub(r"<annotation\b.*?</annotation>", "", h, flags=re.S)   # 公式只留显示文字，不带 LaTeX 源码
    return html.unescape(re.sub(r"<[^>]+>", "", h)).strip()


def inline_images(h, base):
    def rep(m):
        src = html.unescape(m.group(2))
        p = os.path.normpath(os.path.join(base, src))
        if src.startswith(("http:", "https:", "data:")) or not os.path.exists(p):
            return m.group(0)
        mime = mimetypes.guess_type(p)[0] or "image/png"
        return f'{m.group(1)}data:{mime};base64,{base64.b64encode(open(p, "rb").read()).decode()}{m.group(3)}'
    return re.sub(r'(<img\b[^>]*\bsrc=")([^"]+)(")', rep, h)


def main():
    tree = json.load(open(os.path.join(SRC, "tree.json"), encoding="utf-8"))
    root = tree[0]
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    shutil.copy(os.path.join(WEB, "style.css"), os.path.join(OUT, "assets", "style.css"))
    shutil.copy(os.path.join(WEB, "app.js"), os.path.join(OUT, "assets", "app.js"))
    tpl = open(os.path.join(WEB, "page.html"), encoding="utf-8").read().replace("搜索全书", "搜索知识库")
    tpl = tpl.replace("</head>", "<style>details.ocr-src{margin:-.4em 0 1.2em;font-size:.85em;color:var(--muted,#888)}"
                      "details.ocr-src summary{cursor:pointer}details.ocr-src img{display:block;margin-top:.5em}</style>\n</head>")

    # 页面：每个节点一页；部分（有子节点的）作为侧栏的分组标题
    pages, groups, by_token = [], [], {}
    for k, n in enumerate(tree):
        n["title"] = n["title"].replace("dkdk", "√dₖ")                    # 原标题里复制坏的公式
        n["slug"] = "home" if k == 0 else f"p{k:03d}"
        by_token[n["token"]] = n
    for n in tree[1:]:
        if n["depth"] == 1:
            groups.append((n, []))
        elif groups:
            groups[-1][1].append(n)
    order = [n for g, items in groups for n in [g] + items]

    for n in tree:
        path = os.path.join(SRC, n["file"])
        base = os.path.dirname(path)
        if n["obj_type"] == 22:
            md = open(path, encoding="utf-8").read()
            md = re.sub(r"^#### ", "### ", md, flags=re.M)          # 每道题是 h3：进侧栏、进搜索
            body = pandoc(md)
            # feishu_polish.py 把已识别成文字的截图标成 .ocr-src：收进可展开的“查看原图”
            body = re.sub(r'<figure>\s*(<img\b[^>]*class="ocr-src"[^>]*>)\s*(?:<figcaption[^>]*>.*?</figcaption>)?\s*</figure>',
                          r'<details class="ocr-src"><summary>查看原图</summary>\1</details>', body, flags=re.S)
            body = re.sub(r'<p>(<img\b[^>]*class="ocr-src"[^>]*>)</p>', r'<details class="ocr-src"><summary>查看原图</summary>\1</details>', body)
        else:                                                     # PDF 附件
            name = os.path.basename(path)
            txt = path + ".md"
            body = (f'<h1>{html.escape(n["title"])}</h1><p>原文是 PDF 附件（原件在仓库的 reference/ 目录：{html.escape(name)}）。'
                    "下面是自动抽取的文字，排版与公式可能有损。</p>"
                    + (f"<pre style='white-space:pre-wrap'>{html.escape(open(txt, encoding='utf-8').read())}</pre>" if os.path.exists(txt) else ""))
        body = inline_images(body, base)
        body = re.sub(r"<table\b", '<div class="tw"><table', body).replace("</table>", "</table></div>")
        n["body"] = body
        n["secs"] = [(m.group(1), strip_tags(m.group(2))) for m in re.finditer(r'<h3\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h3>', body, re.S)]

    def sidebar(cur):
        out = [f'<a class="side-home{" current" if cur == "home" else ""}" href="index.html">首页与目录</a>']
        for g, items in groups:
            out.append(f'<a class="side-part{" current" if g["slug"] == cur else ""}" href="{g["slug"]}.html">{html.escape(g["title"])}</a>')
            out.append('<ul class="side-list">')
            for p in items:
                here = p["slug"] == cur
                out.append(f'<li><a class="side-ch{" current" if here else ""}" href="{p["slug"]}.html">{html.escape(p["title"])}</a>')
                if here and p["secs"]:
                    out.append('<ul class="side-secs">' + "".join(f'<li><a href="#{i}" data-sec="{i}">{html.escape(t)}</a></li>' for i, t in p["secs"]) + "</ul>")
                out.append("</li>")
            out.append("</ul>")
        return "\n".join(out)

    def pager(prev, nxt):
        card = lambda p, cls, label: f'<a class="{cls}" href="{p["slug"]}.html"><small>{label}</small>{html.escape(p["title"])}</a>' if p else "<span></span>"
        return f'<nav class="pager">{card(prev, "prev", "上一页")}{card(nxt, "next", "下一页")}</nav>'

    def write(fname, slug, title, body, cls):
        page = (tpl.replace("{{title}}", html.escape(title)).replace("{{book}}", TITLE).replace("{{pdf}}", "")
                .replace("{{sidebar}}", sidebar(slug)).replace("{{class}}", cls).replace("{{body}}", body))
        open(os.path.join(OUT, fname), "w", encoding="utf-8").write(page)

    for k, p in enumerate(order):
        prev = order[k - 1] if k else None
        nxt = order[k + 1] if k + 1 < len(order) else None
        write(p["slug"] + ".html", p["slug"], f'{p["title"]} · {TITLE}', p["body"] + pager(prev, nxt), "page-chapter")

    toc = [f'<h1 class="front">{html.escape(root["title"])}</h1>',
           f'<p>飞书知识库的离线副本，共 {len(tree) - 1} 篇（{len(groups)} 个部分）。左上角按钮打开目录，顶部可以全文搜索。</p>',
           root["body"].split("</h1>", 1)[-1], '<div class="home-toc"><h2>目　录</h2>']
    for g, items in groups:
        toc.append(f'<h3><a href="{g["slug"]}.html">{html.escape(g["title"])}</a></h3>')
        toc.append("<ul>" + "".join(f'<li><a href="{c["slug"]}.html">{html.escape(c["title"])}</a></li>' for c in items) + "</ul>")
    toc.append("</div>")
    write("index.html", "home", TITLE, "".join(toc), "page-home")
    write("404.html", "", f"页面不存在 · {TITLE}", '<h1 class="front">页面不存在</h1><p><a href="index.html">回到首页</a></p>', "page-front")

    # 搜索索引：每道题一条
    index = []
    for p in order:
        b = re.sub(r'<img\b[^>]*>', "", p["body"])
        cuts = [(m.end(), m.group(1), strip_tags(m.group(2))) for m in re.finditer(r'<h3\b[^>]*\bid="([^"]+)"[^>]*>(.*?)</h3>', b, re.S)]
        spans = [(0, "", "")] + cuts
        for (a, sid, st), (e, _, _) in zip(spans, spans[1:] + [(len(b), "", "")]):
            text = re.sub(r"\s+", " ", strip_tags(re.sub(r"<h3\b.*", "", b[a:e], flags=re.S)))
            if text:
                index.append([p["slug"], sid, p["title"] + (" › " + st if st else ""), text[:4000]])
    json.dump(index, open(os.path.join(OUT, "assets", "search.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

    home = open(os.path.join(OUT, "index.html"), encoding="utf-8").read()
    head = re.search(r"<title>.*?</title>", home, re.S).group(0) + "\n" + re.search(r'<link rel="stylesheet"[^>]*>', home).group(0)
    open(os.path.join(OUT, "_main.html"), "w", encoding="utf-8").write(head + "\n" + re.search(r"<body[^>]*>\n?(.*)</body>", home, re.S).group(1))
    files = sorted(f for f in os.listdir(OUT) if f not in ("index.html", "_main.html", "publish_files.json", "assets")) + \
        ["assets/" + f for f in sorted(os.listdir(os.path.join(OUT, "assets")))]
    json.dump(files, open(os.path.join(OUT, "publish_files.json"), "w"), indent=0)
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in files)
    print(f"ref site: {len(order) + 1} pages, {len(index)} search entries, {len(files)} files, {total / 2**20:.1f} MB -> {OUT}")


if __name__ == "__main__":
    main()
