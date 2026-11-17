"""飞书导出的可读性修补（在 feishu_export.js、feishu_sheets.js 之后运行；可重复运行）。

1. 公式碎片：原文的行内公式是从网页上复制来的，变成了“纯文本 + 斜体”两份，例如
   `s*s*`、`*λU*`、`*dmodel*`。还原成 LaTeX：`$s$`、`$λ_U$`、`$d_{model}$`。
2. 截图转文字：原文很多段落（尤其含公式的）是截图。若 _ocr/<图片名>.md 里有识别结果
   （tools/feishu_ocr.py 生成），就用识别出的 Markdown + LaTeX 替换图片，原图以 `{.ocr-src}` 标记
   保留（网页版收进可展开的“查看原图”），便于核对。没有识别结果的图片保持原样。

3. 排版：飞书块内的换行（如“4. 小标题⏎解释”）在 Markdown 里会被并成一行，改成硬换行，
   列表项的续行缩进到列表内容下；去掉空列表项、零宽字符；写在代码格式里的 LaTeX（含 \text、
   \frac、_{…} 等）改成公式。

用法：python3 tools/feishu_polish.py reference/飞书_LLMs知识库
"""
import glob, os, re, sys

ROOT = sys.argv[1]
OCR = os.path.join(ROOT, "_ocr")
FIXES = [l.split("\t", 1) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "feishu_fixes.tsv"), encoding="utf-8").read().split("\n")
         if l.strip() and not l.startswith("#")]
MATHCH = r"A-Za-z0-9α-ωΑ-Ωϵϕϑ∇′'"
KEEP = {"SFT", "RL", "KL", "OR", "BA", "AB", "LoRA", "PPO", "DPO", "RM", "IO", "AI", "GPU", "PPL", "RLHF"}


def to_tex(tok):
    """把复制坏的公式片段猜回 LaTeX：首字母作主体，其余作下标。"""
    if tok in KEEP or len(tok) == 1 or not re.fullmatch(f"[{MATHCH}]+", tok):
        return tok
    m = re.fullmatch(r"([A-Za-zα-ωΑ-Ωϵϕϑ])([a-z0-9]+|[A-Z])", tok)
    if m:
        base, sub = m.groups()
        return f"{base}_{{{sub}}}" if len(sub) > 1 else f"{base}_{sub}"
    return tok


def fix_math(t):
    """只改公式以外的部分：$$…$$、$…$ 和代码块原样保留（重复运行时不会改坏转写好的 LaTeX）。"""
    t = t.replace("\u200b", "")
    for old, new in FIXES:                                                     # 逐条手写的改正（tools/feishu_fixes.tsv）
        t = t.replace(old, new)
    parts = re.split(r"(\$\$.*?\$\$|```.*?```|`[^`\n]*`|\$[^$\n]+\$)", t, flags=re.S)
    return "".join(p if i % 2 else _fix_math(p) for i, p in enumerate(parts))


def tex(name):
    """把一个变量名转成 LaTeX：Δ 和希腊字母转成命令；首字母作主体，其余作下标。"""
    greek = {"Δ": r"\Delta ", "π": r"\pi", "λ": r"\lambda", "α": r"\alpha", "β": r"\beta", "γ": r"\gamma", "τ": r"\tau", "θ": r"\theta"}
    if name in ("BA", "AB"):
        return name
    head, rest = name[0], name[1:]
    head = greek.get(head, head)
    return head + (f"_{{{rest}}}" if len(rest) > 1 else f"_{rest}" if rest else "")


def _garbled(t):
    """飞书里从网页复制来的公式会变成“两份残缺拷贝”，按固定形态还原。"""
    t = re.sub(r"(?<![\w*])([A-Za-zα-ωΔ][A-Za-z0-9]{0,4})=([\w.]{1,8})\*\1\*=\2(?!\w)",         # n=8*n*=8
               lambda m: f"${tex(m.group(1))}={m.group(2)}$", t)
    t = re.sub(r"(?<![\w*])([A-Za-zα-ωΔ])([A-Za-z0-9]{1,6})\*\1\*\2(?!\w)",                   # πref*π*ref、B0*B*0
               lambda m: f"${tex(m.group(1) + m.group(2))}$", t)
    t = re.sub(r"(?<![A-Za-z0-9_.*])(\d+)\*([A-Za-z])\*(?![*A-Za-z0-9])", r"$\1\2$", t)          # 2*i*、4*d*
    t = re.sub(r"Δ\*([A-Za-z])\*", lambda m: f"$\\Delta {m.group(1)}$", t)                     # Δ*W*
    t = re.sub(r"(?<![\w*])\*([A-Za-zα-ωΑ-Ω])\*([0-9]+|max|min|ref|out|recent|heavy)(?![\w])",  # *W*0、*L*max
               lambda m: f"${tex(m.group(1) + m.group(2))}$", t)
    t = re.sub(r"(?<![\w*$])([A-Za-z])\*([A-Za-z])\*(?![\w*])",                                # W*K*、S*t*、L*D*
               lambda m: f"${tex(m.group(1) + m.group(2))}$", t)
    return t


def _fix_math(t):
    t = t.replace("****", "")                                            # 空的加粗标记
    # 先去掉“纯文本 + 斜体”的重复：W*W* -> $W$。
    # 必须早于 _garbled 的 W*K* 下标规则，否则会被误写成 $W_W$。
    t = re.sub(rf"(?<![{MATHCH}*])([{MATHCH}]{{1,12}})\*\1\*", lambda m: f"${to_tex(m.group(1))}$", t)
    t = _garbled(t)
    # 单独的斜体公式片段：*x* -> $x$（只处理拉丁/希腊字母和数字，不碰中文强调）
    t = re.sub(rf"(?<![*A-Za-z0-9_$])\*([{MATHCH}]{{1,12}})\*(?![*A-Za-z0-9_])",
               lambda m: m.group(0) if m.group(1) in KEEP else f"${to_tex(m.group(1))}$", t)
    return t


def use_ocr(t, mdfile):
    def rep(m):
        alt, src = m.group(1), m.group(2)
        name = os.path.splitext(os.path.basename(src))[0]
        f = os.path.join(OCR, name + ".md")
        if not os.path.exists(f):
            return m.group(0)
        text = open(f, encoding="utf-8").read().strip()
        if not text:
            return m.group(0)
        if text.startswith("[[图]]"):                                  # 示意图：保留图片，把一句话说明当图注（可搜索）
            return f"![{text[5:].strip()}]({src})"
        return f"{text}\n\n![原图]({src}){{.ocr-src}}"                    # 网页版把它收进“查看原图”
    return re.sub(r"^!\[([^\]]*)\]\((media/[^)]+)\)$", rep, t, flags=re.M)


TEXCODE = re.compile(r"\\(?:text|frac|sqrt|mathrm|mathbf|operatorname|alpha|beta|gamma|theta|lambda|sigma|sum|prod|cdot|times|log|exp|hat|tilde|left|right)\b|[_^]\{")
BLOCK = re.compile(r"^\s*(?:[-*+] |\d+[.)] |#|\||>|!\[|\$\$|```|---\s*$|<)")
ITEM = re.compile(r"^(\s*)(?:[-*+]|\d+[.)]) ")


def layout(t):
    t = t.replace("​", "")
    t = re.sub(r"^[ \t]*[-*+][ \t]*$\n?", "", t, flags=re.M)                     # 空列表项
    t = re.sub(r"^([^\n*#|>!$`\-][^\n]{0,39}?)\\?\n\n(\*\*\1[:：]?\*\*)", r"\2", t, flags=re.M)  # 原文标题 + 截图里同样的加粗标题：只留一个
    t = re.sub(r"`([^`\n]*)`", lambda m: f"${m.group(1)}$" if TEXCODE.search(m.group(1)) and not re.search(r"[<>|\"']", m.group(1))
               and not re.fullmatch(r"\\[a-zA-Z]+(?:\{\})*", m.group(1))
               else m.group(0), t)                                                # 代码格式里的 LaTeX
    lines, out, fence, item_indent = t.split("\n"), [], None, None
    for i, l in enumerate(lines):
        st = l.strip()
        if fence:
            out.append(l)
            if st.startswith(fence):
                fence = None
            continue
        if st.startswith(("```", "$$")) and not (st.startswith("$$") and st.endswith("$$") and len(st) > 2):
            fence = st[:3] if st.startswith("```") else "$$"
            out.append(l)
            continue
        m = ITEM.match(l)
        if not st:
            item_indent = None
        elif m:
            item_indent = len(m.group(0))
        elif item_indent is not None and not l.startswith(" "):
            l = " " * item_indent + l                                         # 列表项的续行
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if (st and nxt.strip() and not BLOCK.match(nxt) and not st.startswith(("|", ">", "#", "$$", "![", "<"))
                and not st.endswith("\\")):
            l += "\\"                                                         # 段内换行 -> 硬换行
        out.append(l)
    return "\n".join(out)


n = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
    if f.endswith(".pdf.md") or os.sep + "_ocr" + os.sep in f:
        continue
    t0 = open(f, encoding="utf-8").read()
    t = layout(use_ocr(fix_math(t0), f))
    if t != t0:
        open(f, "w", encoding="utf-8").write(t)
        n += 1
print("polished", n, "files")
