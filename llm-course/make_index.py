"""Build INDEX.md: a compact map of the whole book (sections, experiments, figures, line numbers) for quick lookup."""
import os, re
ROOT = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(ROOT, "build", "book.html"), encoding="utf-8").read()
fignum = {m.group(1): m.group(2) for m in re.finditer(r'<figure id="([^"]+)"[^>]*>.*?<figcaption>(图 [0-9A-E]+\.\d+)', html, re.S)}
order = ["00_front"] + [f"ch{i:02d}" for i in range(40)] + [f"app{c}" for c in "ABCDE"]
out = ["# 全书索引（自动生成：python3 make_index.py）", "", "格式：`文件:行号` 标题。实验框只列第一句，图只列编号和图注。", ""]
for name in order:
    path = os.path.join(ROOT, "src", name + ".md")
    lines = open(path, encoding="utf-8").read().split("\n")
    in_exp = in_svg = False
    n_ex = 0
    for i, l in enumerate(lines, 1):
        if l.startswith("<svg") or (l.startswith("<figure") and "data-svg" not in l and not l.startswith('<figure class="nonum" data-svg')):
            in_svg = True
        if in_svg:
            if l.startswith("</figure>"):
                in_svg = False
            m = re.match(r"<figcaption>(.*)</figcaption>", l)
            if m and not l.startswith("<figure"):
                pass
        if re.match(r"^(#|##) ", l) and "{#" in l:
            out.append("")
            out.append(f"## {re.sub(r' *\{#.*', '', l.lstrip('# '))}  `{name}.md:{i}`")
        elif l.startswith("### "):
            out.append(f"- {l[4:]}  `:{i}`")
        elif l.startswith("#### "):
            out.append(f"  - {l[5:]}  `:{i}`")
        elif l.startswith("::: experiment"):
            in_exp = True
        elif in_exp and l.strip():
            out.append(f"  - 【实验】{l.strip()[:90]}  `:{i}`")
            in_exp = False
        elif l.startswith("::: exercises"):
            n_ex = sum(1 for x in lines[i:] if re.match(r"^\d+\. ", x))
            out.append(f"  - 【习题】{n_ex} 道  `:{i}`")
        m = re.match(r'<figure id="([^"]+)"', l)
        if m:
            cap = next((re.sub(r"</?figcaption>", "", x) for x in lines[i:i + 200] if x.startswith("<figcaption>")), "")
            out.append(f"  - 【{fignum.get(m.group(1), '图')}】{cap[:80]}  `:{i}`")
open(os.path.join(ROOT, "INDEX.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out), "lines")
