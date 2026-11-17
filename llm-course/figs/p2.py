"""Figures for Part 2 (chapters 5-9). Run: python3 figs/p2.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import *

OUT = os.path.dirname(os.path.abspath(__file__))


def save(f):
    f.save(os.path.join(OUT, f.name + ".svg"))


def tokrow(f, x, y, toks, style="white", size=12, h=24, pad=7, gap=3, mono=False):
    """Draw a row of token boxes; returns the x after the last box."""
    for t in toks:
        shown = t.replace(" ", "␣")
        w = max(text_width(shown, size) + 2 * pad, 18)
        f.box(x, y, w, h, shown, style, size, rx=3, sw=1)
        x += w + gap
    return x


# ----------------------------------------------------------------- chapter 5
def ch05_split():
    f = Fig("ch05_split", 660, 205)
    rows = [("按字符", list("The unmannerly courtiers whisper."), "33 个 token", "gray"),
            ("按单词", ["The", "unmannerly", "courtiers", "whisper", "."], "5 个 token，但“unmannerly”这样的罕见词会让词表无限膨胀", "orange"),
            ("按子词（BPE）", ["The", " un", "man", "ner", "ly", " court", "iers", " whisper", "."], "9 个 token：常见词整个保留，罕见词拆成几块", "blue")]
    for k, (name, toks, note, st) in enumerate(rows):
        y = 14 + k * 62
        f.text(8, y + 17, name, 12.5, "start", INK, 700)
        if k == 0:
            x = 104
            for ch in toks:
                f.box(x, y, 13.4, 24, ch.replace(" ", "␣"), "white", 11, rx=2, sw=0.8)
                x += 15.2
        else:
            tokrow(f, 104, y, toks, st, 12.5)
        f.text(104, y + 42, note, 11.5, "start", INK2)
    f.text(330, 200, "子词的切分来自本章在莎士比亚文本上训练的 BPE（词表 8,192，实测）；␣ 表示空格", 11, "middle", INK3)
    save(f)


def ch05_utf8():
    f = Fig("ch05_utf8", 660, 175)
    items = [("A", "U+0041", ["41"]), ("é", "U+00E9", ["C3", "A9"]), ("中", "U+4E2D", ["E4", "B8", "AD"]),
             ("😀", "U+1F600", ["F0", "9F", "98", "80"])]
    f.text(10, 50, "字符", 12, "start", INK2)
    f.text(10, 94, "码点", 12, "start", INK2)
    f.text(10, 138, "UTF-8 字节", 12, "start", INK2)
    for k, (ch, cp, bs) in enumerate(items):
        cx = 140 + k * 140
        f.box(cx - 24, 28, 48, 34, ch, "white", 18 if k < 3 else 16)
        f.arrow(cx, 64, cx, 78, GRAY)
        f.text(cx, 96, cp, 12, "middle", INK, family="LatinSerif")
        f.arrow(cx, 102, cx, 116, GRAY)
        bw = 30
        x0 = cx - len(bs) * (bw + 3) / 2
        for j, b in enumerate(bs):
            f.box(x0 + j * (bw + 3), 120, bw, 26, b, "Blue", 12, rx=2)
        f.text(cx, 164, f"{len(bs)} 个字节", 11.5, "middle", INK2)
    f.text(330, 14, "Unicode 给每个字符一个编号（码点），UTF-8 再把码点变成 1 到 4 个字节", 12, "middle", INK)
    save(f)


def ch05_bpe():
    f = Fig("ch05_bpe", 660, 250)
    words = [("low", 5), ("lower", 2), ("newest", 6), ("widest", 3)]
    states = [
        [["l", "o", "w"], ["l", "o", "w", "e", "r"], ["n", "e", "w", "e", "s", "t"], ["w", "i", "d", "e", "s", "t"]],
        [["l", "o", "w"], ["l", "o", "w", "e", "r"], ["n", "e", "w", "es", "t"], ["w", "i", "d", "es", "t"]],
        [["l", "o", "w"], ["l", "o", "w", "e", "r"], ["n", "e", "w", "est"], ["w", "i", "d", "est"]],
        [["lo", "w"], ["lo", "w", "e", "r"], ["n", "e", "w", "est"], ["w", "i", "d", "est"]],
        [["low"], ["low", "e", "r"], ["n", "e", "w", "est"], ["w", "i", "d", "est"]],
    ]
    heads = ["开始：单个字符", "① e + s → es", "② es + t → est", "③ l + o → lo", "④ lo + w → low"]
    newtok = [set(), {"es"}, {"est"}, {"lo"}, {"low"}]
    colw = 124
    for c in range(5):
        x0 = 82 + c * colw - 50
        f.text(x0 + 52 + 6, 20, heads[c], 11.5, "middle", INK, 700 if c else None)
        for r, toks in enumerate(states[c]):
            y = 34 + r * 46
            x = x0 + 4
            for t in toks:
                w = 13 + 7.2 * (len(t) - 1)
                st = "Blue" if t in newtok[c] else ("blue" if len(t) > 1 else "white")
                f.box(x, y, w, 22, t, st, 11.5, rx=2, sw=0.8)
                x += w + 2
    for r, (w, n) in enumerate(words):
        f.text(8, 34 + r * 46 + 15, f"×{n}", 11.5, "start", INK2)
    f.text(330, 226, "每一轮在整个语料中找出现次数最多的相邻一对（按词频加权），把它合并成一个新 token", 11.5, "middle", INK2)
    f.text(330, 244, "四轮之后，语料里没有的 lowest 也能切成 low | est", 11.5, "middle", INK2)
    save(f)


def ch05_vocab():
    f = Fig("ch05_vocab", 660, 252)
    V = [256, 512, 1024, 2048, 4096, 8192]
    bpt = [1.00, 1.99, 2.44, 2.81, 3.24, 3.59]
    c = Chart(f, 50, 26, 440, 160, (200, 10000), (0, 4), xlog=True)
    c.axes(V, [0, 1, 2, 3, 4], xlabel="词表大小 $V$（对数坐标）", ylabel="每个 token 平均几个字节", xfmt=lambda v: f"{v:,}", yfmt=lambda v: f"{v:g}")
    c.series(V, bpt, BLUE, markers=True)
    for v, b in zip(V, bpt):
        f.text(c.X(v), c.Y(b) - 9, f"{b:.2f}", 11, "middle", INK)
    f.text(510, 70, ["收益递减：", "256 → 512，序列减半；", "4,096 → 8,192，", "只缩短了 10%"], 11.5, "start", INK2)
    f.text(330, 246, "在莎士比亚训练集上训练、在验证集上测量（实测，数据同上表）", 11.5, "middle", INK2)
    save(f)


def ch05_zh():
    f = Fig("ch05_zh", 660, 205)
    groups = [("每个汉字要几个 token（《孟子》）", [2.97, 1.16], 3.3), ("英文每个 token 几个字节", [3.59, 3.37], 4.0)]
    names = ["只用莎士比亚训练", "莎士比亚 + 唐诗"]
    for g, (title, vals, ymax) in enumerate(groups):
        c = Chart(f, 70 + g * 320, 34, 220, 120, (0, 2), (0, ymax))
        c.axes([], [0, 1, 2, 3] if ymax < 4 else [0, 1, 2, 3, 4], ylabel=title, yfmt=lambda v: f"{v:g}")
        for i, v in enumerate(vals):
            c.bar(c.X(i + 0.5), v, 44, [ORANGE, BLUE][i])
            f.text(c.X(i + 0.5), c.Y(v) - 6, f"{v:.2f}", 11.5, "middle", INK)
            f.text(c.X(i + 0.5), c.Y(0) + 16, names[i], 11, "middle", INK2)
    f.text(330, 198, "两个分词器的词表都是 8,192（实测）。照顾中文之后，中文的 token 数降到约 40%，英文的压缩率略有下降", 11.5, "middle", INK2)
    save(f)


def ch05_pipeline():
    f = Fig("ch05_pipeline", 660, 250)
    f.box(6, 22, 150, 30, "To be, or not to be:", "white", 12.5)
    f.text(81, 70, "原始文本", 11, "middle", INK2)
    f.arrow(158, 37, 196, 37)
    toks = ["To", " be", ",", " or", " not", " to", " be", ":"]
    ids = [403, 308, 44, 538, 325, 291, 308, 58]
    x, cen = 200, []
    for t in toks:
        w = max(text_width(t.replace(" ", "␣"), 12) + 12, 28)
        f.box(x, 22, w, 30, t.replace(" ", "␣"), "white", 12, rx=3, sw=1)
        cen.append((x + w / 2, w))
        x += w + 4
    f.text(x + 6, 42, "① 预切分", 11.5, "start", INK, 700)
    for (c, w), i in zip(cen, ids):
        f.arrow(c, 54, c, 82, GRAY, 1)
        f.box(c - w / 2, 84, w, 26, str(i), "Blue", 11, rx=2)
    cen = [c for c, w in cen]
    f.text(x + 6, 102, "② 片段内做 BPE，得到 id", 11.5, "start", INK, 700)
    for c in cen:
        f.arrow(c, 112, c, 136, GRAY, 1)
        for k in range(5):
            f.rect(c - 7, 138 + k * 9, 14, 8, BLUE_M if k % 2 else BLUE_L, BLUE, 0.6, 1)
    f.text(x + 6, 166, ["③ 查 embedding 表：", "每个 id → 一个 $d$ 维向量"], 11.5, "start", INK, 700)
    f.text(cen[0] + (cen[-1] - cen[0]) / 2, 212, "送进 Transformer", 12, "middle", INK, 700)
    f.arrow(cen[0] + (cen[-1] - cen[0]) / 2, 186, cen[0] + (cen[-1] - cen[0]) / 2, 194)
    f.text(8, 108, ["分词器在预训练开始前训练好，", "之后冻结：一改，embedding", "就对不上了。", "整个语料会事先编码成", "token id，存成二进制文件"], 11.5, "start", INK2)
    f.text(330, 240, "正则先切出片段（空格归入后面的单词，标点单独成段），BPE 只在片段内部合并（id 为实测）", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 6
def ch06_rnn():
    f = Fig("ch06_rnn", 660, 215)
    toks = ["猫", "坐", "在", "垫", "上"]
    f.text(160, 18, "RNN：所有信息挤进一个记忆向量，逐步传递", 12.5, "middle", INK, 700)
    for k, t in enumerate(toks):
        x = 20 + k * 62
        f.box(x, 160, 36, 28, t, "white", 13)
        f.arrow(x + 18, 158, x + 18, 132, GRAY)
        f.box(x - 2, 96, 40, 34, "$h$", "orange", 13)
        if k < 4:
            f.arrow(x + 39, 113, x + 59, 113, ORANGE, 1.6)
    f.text(160, 76, "第 $t$ 步必须等第 $t-1$ 步算完，无法并行", 11.5, "middle", INK2)
    f.text(160, 208, "越早的 token，信息被转手的次数越多", 11.5, "middle", INK2)
    ox = 345
    f.text(ox + 150, 18, "注意力：每个位置直接查看前面所有位置", 12.5, "middle", INK, 700)
    xs = [ox + 10 + k * 56 for k in range(5)]
    for k, t in enumerate(toks):
        f.box(xs[k], 160, 36, 28, t, "white", 13)
    tgt = xs[4] + 18
    for k in range(5):
        sx = xs[k] + 18
        w = [0.4, 0.8, 1.2, 2.6, 1.2][k]
        f.path(f"M{sx},158 C{sx},{110 - k * 4} {tgt},{100} {tgt},{92}", BLUE, w, arrow=(k == 4))
    f.box(tgt - 46, 58, 92, 32, "位置 5 的输出", "Blue", 12)
    f.text(ox + 150, 208, "线条粗细 = 注意力权重（示意）；所有位置可以同时计算", 11.5, "middle", INK2)
    save(f)


def ch06_qkv():
    f = Fig("ch06_qkv", 660, 250)
    keys = [([2, 0], [10, 0], 1.414, 0.576), ([0, 1], [0, 10], 0.0, 0.140), ([1, 1], [5, 5], 0.707, 0.284)]
    f.box(12, 104, 92, 40, "query $q$ = [1, 0]", "Orange", 12)
    f.text(58, 160, "位置 3 提出的“问题”", 11, "middle", INK2)
    for k, (key, val, s, w) in enumerate(keys):
        y = 30 + k * 66
        f.box(150, y, 94, 32, f"key $k_{k + 1}$ = [{key[0]}, {key[1]}]", "white", 12)
        f.arrow(106, 124, 148, y + 16, GRAY, 1)
        f.text(258, y + 13, f"$q\\cdot k_{k + 1}/\\sqrt{{2}}$ = {s:.3f}", 11.5, "start", INK)
        # weight bar
        f.rect(258, y + 20, 110 * w, 10, BLUE, "none", 0, 2)
        f.text(262 + 110 * w, y + 29, f"{w:.3f}", 11, "start", INK, 700 if k == 0 else None)
        f.box(420, y, 100, 32, f"value $v_{k + 1}$ = [{val[0]}, {val[1]}]", "green", 12)
        f.arrow(372 + 30, y + 16, 418, y + 16, GRAY, 1)
        f.arrow(522, y + 16, 556, 124, GREEN, 0.6 + 3 * w)
    f.text(320, 228, "softmax 权重（和为 1）", 11, "middle", INK2)
    f.box(558, 104, 96, 40, "输出 [7.18, 2.82]", "Green", 12)
    f.text(606, 160, "value 的加权平均", 11, "middle", INK2)
    f.text(330, 246, "6.4 节的手算例子：位置 1 的 key 与 query 最匹配，它的 value 贡献最多", 11.5, "middle", INK2)
    save(f)


def ch06_mask():
    f = Fig("ch06_mask", 660, 250)
    T, cs = 6, 26
    toks = ["猫", "坐", "在", "垫", "上", "了"]
    import random
    rnd = random.Random(3)
    S = [[rnd.uniform(-1.5, 2.0) for _ in range(T)] for _ in range(T)]
    A = []
    for i in range(T):
        row = [math.exp(S[i][j]) for j in range(i + 1)]
        s = sum(row)
        A.append([v / s for v in row] + [0] * (T - i - 1))
    def grid(x0, y0, title, val, kind):
        f.text(x0 + T * cs / 2, y0 - 26, title, 12, "middle", INK, 700)
        for j in range(T):
            f.text(x0 + j * cs + cs / 2, y0 - 6, toks[j], 11, "middle", INK2)
        for i in range(T):
            f.text(x0 - 6, y0 + i * cs + cs / 2 + 4, toks[i], 11, "end", INK2)
            for j in range(T):
                v = val(i, j)
                if kind == "S":
                    fill = BLUE_L
                    lab = f"{v:.1f}"
                elif kind == "M":
                    fill = "#ffffff" if j <= i else GRAY_L
                    lab = "0" if j <= i else "−∞"
                else:
                    t = min(1, v)
                    fill = "#ffffff" if j > i else f"rgb({int(255 - t * (255 - 28))},{int(255 - t * (255 - 93))},{int(255 - t * (255 - 153))})"
                    lab = f"{v:.2f}" if j <= i else ""
                f.rect(x0 + j * cs, y0 + i * cs, cs - 1, cs - 1, fill, "none", 0, 1)
                col = "#ffffff" if (kind == "A" and v > 0.55) else INK2
                f.text(x0 + j * cs + cs / 2, y0 + i * cs + cs / 2 + 3.5, lab, 8.5 if kind != "M" else 10, "middle", col)
    grid(40, 60, "分数 $S = QK^{T}/\\sqrt{d_h}$", lambda i, j: S[i][j], "S")
    f.text(214, 140, "+", 18, "middle", INK2)
    grid(250, 60, "因果掩码 $M$", lambda i, j: 0, "M")
    f.text(424, 140, "→", 18, "middle", INK2)
    grid(466, 60, "softmax：权重 $A$", lambda i, j: A[i][j], "A")
    f.text(330, 236, "第 $i$ 行是位置 $i$ 的 query；它只能看到 $j \\le i$ 的位置，每行权重之和为 1，输出 $O = AV$（数字为示意）", 11.5, "middle", INK2)
    save(f)


def ch06_multihead():
    f = Fig("ch06_multihead", 660, 218)
    f.box(10, 82, 70, 36, "$X$（$d$ 维）", "white", 12)
    cols = [BLUE, ORANGE, GREEN, PURPLE]
    for h in range(4):
        y = 14 + h * 46
        f.arrow(82, 100, 120, y + 18, GRAY, 1)
        f.box(122, y, 150, 36, f"头 {h + 1}：$Q_{h + 1}, K_{h + 1}, V_{h + 1}$", "white", 11.5)
        f.rect(122, y, 6, 36, cols[h], "none", 0, 2)
        f.arrow(274, y + 18, 300, y + 18, GRAY, 1)
        f.box(302, y, 110, 36, "注意力", "blue", 12, sub=f"$d_h = d/n_h$ 维输出", sub_size=10.5)
        f.arrow(414, y + 18, 446, 100, GRAY, 1)
    for h in range(4):
        f.rect(448 + h * 16, 84, 14, 32, cols[h], "none", 0, 2)
    f.text(480, 132, "拼接（$d$ 维）", 11, "middle", INK2)
    f.arrow(514, 100, 540, 100)
    f.box(542, 82, 110, 36, "乘 $W_o$ → 输出", "Navy", 12)
    f.text(330, 212, "每个头有自己的投影矩阵，各自关注一种模式；总计算量与一个 $d$ 维的单头注意力相同", 11.5, "middle", INK2)
    save(f)


def ch06_ctx():
    f = Fig("ch06_ctx", 660, 250)
    buckets = ["1", "2–3", "4–7", "8–15", "16–31", "32–63", "64–128"]
    loss = [2.563, 2.145, 1.927, 1.892, 1.869, 1.865, 1.865]
    c = Chart(f, 50, 30, 300, 160, (0, 7), (1.8, 2.7))
    c.axes([], [1.8, 2.0, 2.2, 2.4, 2.6], ylabel="验证集 loss", yfmt=lambda v: f"{v:.1f}")
    for i, (b, v) in enumerate(zip(buckets, loss)):
        c.bar(c.X(i + 0.5), v, 28, BLUE)
        f.text(c.X(i + 0.5), c.Y(v) - 5, f"{v:.2f}", 10, "middle", INK)
        f.text(c.X(i + 0.5), c.Y(1.8) + 15, b, 10.5, "middle", INK2)
    f.text(200, 226, "当前位置前面有几个字符的上下文", 11.5, "middle", INK2)
    dist = [[33.4, 19.3, 23.2, 20.7], [3.0, 16.8, 2.6, 2.0], [2.6, 3.0, 4.6, 3.0], [14.5, 13.7, 14.0, 16.0]]
    x0, y0, cs = 450, 50, 40
    f.text(x0 + 80, 22, "每个头平均往回看多少个字符", 12, "middle", INK, 700)
    for h in range(4):
        f.text(x0 + h * cs + cs / 2, y0 - 8, f"头 {h}", 11, "middle", INK2)
    for l in range(4):
        f.text(x0 - 8, y0 + l * cs + cs / 2 + 4, f"第 {l} 层", 11, "end", INK2)
        for h in range(4):
            v = dist[l][h]
            t = min(1, math.log(v) / math.log(34))
            fill = f"rgb({int(255 - t * (255 - 28))},{int(255 - t * (255 - 93))},{int(255 - t * (255 - 153))})"
            f.rect(x0 + h * cs, y0 + l * cs, cs - 2, cs - 2, fill, "none", 0, 2)
            f.text(x0 + h * cs + cs / 2 - 1, y0 + l * cs + cs / 2 + 4, f"{v:.1f}", 11, "middle", "#ffffff" if t > 0.6 else INK)
    f.text(x0 + 80, 228, "颜色越深看得越远；有的头只看相邻字符", 11, "middle", INK2)
    save(f)


def ch06_encdec():
    f = Fig("ch06_encdec", 660, 215)
    f.text(165, 18, "2017 年原版：编码器–解码器（翻译）", 12.5, "middle", INK, 700)
    f.box(20, 60, 120, 90, "编码器", "green", 13, sub=["双向查看", "整段原文"])
    f.box(190, 60, 120, 90, "解码器", "blue", 13, sub=["只看已生成的", "译文 + 交叉注意力"])
    f.arrow(142, 105, 188, 105, GREEN, 1.6)
    f.text(165, 98, "", 11)
    f.box(20, 168, 120, 26, "原文：猫坐在垫上", "white", 11.5)
    f.box(190, 168, 120, 26, "译文：The cat sat", "white", 11.5)
    f.arrow(80, 166, 80, 152, GRAY)
    f.arrow(250, 166, 250, 152, GRAY)
    f.text(495, 18, "今天：只有解码器（decoder-only）", 12.5, "middle", INK, 700)
    f.box(435, 60, 120, 90, "解码器", "blue", 13, sub=["因果注意力：", "只看前面"])
    f.box(380, 168, 230, 26, "提示词和回答拼成一条序列", "white", 11.5)
    f.arrow(495, 166, 495, 152, GRAY)
    f.arrow(495, 58, 495, 36, BLUE)
    f.text(560, 44, "预测下一个 token", 11.5, "start", INK2)
    f.text(330, 210, "所有任务都写成“续写”，一种结构、一个训练目标，便于扩大规模", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 7
def ch07_rope():
    f = Fig("ch07_rope", 660, 235)
    th = math.radians(14)
    def dial(cx, cy, r, m, n, title):
        f.text(cx, cy - r - 30, title, 12, "middle", INK, 700)
        f.circle(cx, cy, r, "#fbfcfd", GRID, 1)
        f.line(cx - r - 6, cy, cx + r + 6, cy, GRID, 1)
        f.line(cx, cy - r - 6, cx, cy + r + 6, GRID, 1)
        aq, ak = m * th + math.radians(10), n * th + math.radians(-15)
        for a, col, lab in ((aq, ORANGE, f"$q$ 转 {m} 格"), (ak, BLUE, f"$k$ 转 {n} 格")):
            x2, y2 = cx + r * math.cos(a), cy - r * math.sin(a)
            f.arrow(cx, cy, x2, y2, col, 2.2)
            f.text(x2 + (10 if math.cos(a) >= 0 else -10), y2 - 4, lab, 11.5, "start" if math.cos(a) >= 0 else "end", INK)
        # angle arc between
        a1, a2 = sorted((aq, ak))
        rr = r * 0.35
        f.path(f"M{cx + rr * math.cos(a1):.1f},{cy - rr * math.sin(a1):.1f} A{rr:.1f},{rr:.1f} 0 0 0 {cx + rr * math.cos(a2):.1f},{cy - rr * math.sin(a2):.1f}",
               GREEN, 2)
    dial(150, 128, 70, 5, 3, "位置 $m$ = 5，$n$ = 3")
    dial(420, 128, 70, 9, 7, "两者都往后挪 4 个位置")
    f.text(285, 132, "→", 20, "middle", INK2)
    f.text(560, 92, ["绿色夹角相同：", "点积只取决于", "相对位置 $m - n$"], 12, "start", GREEN)
    f.text(330, 228, "示意：位置每加 1，向量多转一格（一个固定角度）。实际有 $d_h/2$ 个平面，每个平面的一格大小不同", 11.5, "middle", INK2)
    save(f)


def ch07_swiglu():
    f = Fig("ch07_swiglu", 660, 255)
    f.text(140, 18, "普通 MLP（GPT-2）", 12.5, "middle", INK, 700)
    f.box(90, 206, 100, 26, "$x$", "white", 13)
    f.arrow(140, 204, 140, 186)
    f.box(70, 152, 140, 32, "$W_{up}$：$d \\to 4d$", "blue", 12)
    f.arrow(140, 150, 140, 130)
    f.box(90, 104, 100, 24, "GELU", "orange", 12)
    f.arrow(140, 102, 140, 84)
    f.box(70, 50, 140, 32, "$W_{down}$：$4d \\to d$", "blue", 12)
    f.text(450, 18, "SwiGLU（现代标准）", 12.5, "middle", INK, 700)
    f.box(400, 206, 100, 26, "$x$", "white", 13)
    f.line(450, 204, 450, 194, INK3, 1.3)
    f.poly([(380, 194), (520, 194)], INK3, 1.3)
    f.arrow(380, 194, 380, 186)
    f.arrow(520, 194, 520, 186)
    f.box(320, 152, 120, 32, "$W_{gate}$", "blue", 12)
    f.box(460, 152, 120, 32, "$W_{up}$", "blue", 12)
    f.arrow(380, 150, 380, 130)
    f.box(340, 104, 80, 24, "SiLU", "orange", 12)
    f.circle(450, 116, 12, "#ffffff", NAVY, 1.2)
    f.text(450, 121, "×", 15, "middle", INK)
    f.arrow(422, 116, 436, 116)
    f.poly([(520, 150), (520, 116), (464, 116)], INK3, 1.3, arrow=True)
    f.arrow(450, 102, 450, 84)
    f.box(380, 50, 140, 32, "$W_{down}$", "blue", 12)
    f.text(588, 164, ["隐藏层宽", "约 $\\frac{8}{3}d$"], 11.5, "start", INK2)
    f.text(468, 104, "逐元素相乘", 10.5, "start", INK2)
    f.text(330, 248, "SwiGLU 用 SiLU 算出的“门”逐元素调节 $W_{up}$ 的输出。它多一个矩阵，所以隐藏层从 $4d$ 缩到约 $\\frac{8}{3}d$，参数量不变", 11, "middle", INK2)
    save(f)


def ch07_gqa():
    f = Fig("ch07_gqa", 660, 245)
    schemes = [("MHA", 8), ("GQA", 2), ("MQA", 1)]
    for s, (name, nkv) in enumerate(schemes):
        x0 = 14 + s * 160
        f.text(x0 + 66, 18, name, 13, "middle", INK, 700)
        f.text(x0 + 66, 34, f"{nkv} 个 KV 头" if nkv > 1 else "1 个 KV 头", 11, "middle", INK2)
        qx = [x0 + 4 + i * 16.5 for i in range(8)]
        for x in qx:
            f.rect(x, 56, 13, 30, ORANGE, "none", 0, 2)
        kv_w = 132 / nkv
        kvx = [x0 + 4 + j * kv_w for j in range(nkv)]
        for j, x in enumerate(kvx):
            w = min(13, kv_w - 3) if nkv == 8 else kv_w - 6
            f.rect(x if nkv == 8 else x + 1, 136, w, 30, BLUE, "none", 0, 2)
        for i, x in enumerate(qx):
            j = i * nkv // 8
            tx = kvx[j] + (6.5 if nkv == 8 else (kv_w - 6) / 2 + 1)
            f.line(x + 6.5, 88, tx, 134, GRAY, 0.9)
    # bar chart of cache per token (Llama 3 8B dims)
    c = Chart(f, 520, 40, 120, 130, (0, 3), (0, 600))
    c.axes([], [0, 256, 512], ylabel="每 token 缓存（KB）", yfmt=lambda v: f"{v:g}", size=10.5)
    for i, (lab, v) in enumerate([("MHA", 512), ("GQA", 128), ("MQA", 16)]):
        c.bar(c.X(i + 0.5), v, 26, BLUE)
        f.text(c.X(i + 0.5), c.Y(v) - 4, str(v), 10.5, "middle", INK)
        f.text(c.X(i + 0.5), c.Y(0) + 14, lab, 10.5, "middle", INK2)
    f.text(330, 202, "上排是 8 个 Q 头，下排是 K/V 头，连线表示共用。右侧：Llama 3 8B（32 个 Q 头）分别用 32、8、1 个", 11.5, "middle", INK2)
    f.text(330, 220, "KV 头时，每个 token 在 32 层里的缓存总量（bf16）。KV 头越少，推理时要存、要读的数据越少；", 11.5, "middle", INK2)
    f.text(330, 238, "GQA（Llama 3 用 8 个 KV 头）在效果和缓存之间取了折中", 11.5, "middle", INK2)
    save(f)


def ch07_params():
    f = Fig("ch07_params", 660, 165)
    parts = [("32 层 MLP：56.4 亿", 5.64, BLUE), ("注意力 13.4 亿", 1.34, ORANGE), ("嵌入 + 输出层 10.5 亿", 1.05, GREEN)]
    x0, scale, y = 10, 640 / 8.03, 36
    f.text(10, 22, "Llama 3 8B 的 80.3 亿个参数在哪里", 12.5, "start", INK, 700)
    x = x0
    for k, (lab, v, col) in enumerate(parts):
        w = v * scale
        f.rect(x, y, w - 2, 34, col, "none", 0, 2)
        if k == 0:
            f.text(x + w / 2, y + 22, lab, 12, "middle", "#ffffff")
        elif k == 1:
            f.text(x, y + 52, lab, 11.5, "start", ORANGE)
        else:
            f.text(x + w - 2, y + 52, lab, 11.5, "end", GREEN)
        x += w
    f.text(10, 122, "约七成参数在 MLP 里；GQA 让注意力只占 17%。$d_{ff}$ = 14,336 = 3.5$d$，比 $\\frac{8}{3}d$ 宽一些", 11.5, "start", INK2)
    f.text(10, 144, "（按 7.6 节的配置计算：每层 MLP 3 × 4,096 × 14,336 = 1.76 亿，每层注意力 0.42 亿）", 11, "start", INK3)
    save(f)


def ch07_block():
    f = Fig("ch07_block", 660, 280)
    def row(yb, title, labs, st, bold, note):
        f.text(10, yb - 72, title, 12.5, "start", INK, 700)
        f.box(10, yb - 13, 60, 26, "输入", "white", 12)
        f.line(70, yb, 321, yb, INK3, 1.6)
        f.line(339, yb, 581, yb, INK3, 1.6)
        f.arrow(599, yb, 610, yb, INK3, 1.6)
        f.box(612, yb - 13, 44, 26, "输出", "white", 12)
        for k, bx in enumerate((85, 345)):
            px = 330 if k == 0 else 590
            f.poly([(bx, yb), (bx, yb - 40), (bx + 13, yb - 40)], INK3, 1.2, arrow=True)
            f.box(bx + 15, yb - 52, 90, 24, labs[2 * k], st, 11.5, weight=bold)
            f.arrow(bx + 105, yb - 40, bx + 115, yb - 40, INK3, 1.2)
            f.box(bx + 117, yb - 52, 108, 24, labs[2 * k + 1], st, 11.5, weight=bold)
            f.poly([(bx + 225, yb - 40), (px, yb - 40), (px, yb - 10)], INK3, 1.2, arrow=True)
            f.circle(px, yb, 9, "#ffffff", NAVY, 1.2)
            f.text(px, yb + 5, "+", 14, "middle", INK)
        f.text(10, yb + 30, note, 11, "start", INK2)
    row(96, "GPT-2 的 block", ["LayerNorm", "多头注意力", "LayerNorm", "GELU MLP"], "blue", None,
        "输入 = token 嵌入 + 可学习的位置嵌入")
    row(228, "现代（Llama 式）block", ["RMSNorm", "GQA + RoPE", "RMSNorm", "SwiGLU"], "orange", 700,
        "输入 = token 嵌入（位置信息由 RoPE 在注意力里加入）；线性层不带偏置")
    f.text(330, 274, "骨架相同：Pre-norm 残差结构，“+”把子层的输出加回主干。橙色是现代模型换掉的组件", 11.5, "middle", INK2)
    save(f)


def ch08_params():
    f = Fig("ch08_params", 660, 272)
    models = [("Llama 3 70B（稠密）", 70, 70), ("Mixtral 8×7B", 47, 13), ("DeepSeek-V2", 236, 21), ("Qwen3-235B-A22B", 235, 22),
              ("DeepSeek-V3", 671, 37), ("Kimi K2", 1000, 32)]
    c = Chart(f, 160, 30, 380, 180, (5, 2000), (0, len(models)), xlog=True)
    for t in [10, 30, 100, 300, 1000]:
        f.line(c.X(t), c.y0, c.X(t), c.y0 + c.h, GRID, 1)
        f.text(c.X(t), c.y0 + c.h + 16, f"{t:,}", 11, "middle", INK2)
    f.text(c.X(80), c.y0 + c.h + 34, "参数量（十亿，对数坐标）", 11.5, "middle", INK2)
    for i, (name, tot, act) in enumerate(models):
        yc = c.y0 + (i + 0.5) * c.h / len(models)
        f.text(c.x0 - 8, yc + 4, name, 11.5, "end", INK)
        f.rect(c.x0, yc - 9, c.X(tot) - c.x0, 9, BLUE_M, "none", 0, 2)
        f.rect(c.x0, yc + 1, c.X(act) - c.x0, 9, BLUE, "none", 0, 2)
        f.text(c.X(tot) + 5, yc - 1, ("约 " if tot == 1000 else "") + f"{tot:,}", 10.5, "start", INK2)
        f.text(c.X(act) + 5, yc + 9, f"{act}", 10.5, "start", INK2)
        r = tot / act
        f.text(600, yc + 4, "1×" if r == 1 else (f"{r:.1f}×" if r < 10 else f"{r:.0f}×"), 11.5, "middle", INK)
    f.text(600, 22, "总 ÷ 激活", 11, "middle", INK3)
    legend(f, 160, 266, [("总参数：决定容量（要全部放进显存）", BLUE_M, "box"), ("激活参数：决定每个 token 的计算量", BLUE, "box")])
    save(f)


def ch08_balance():
    f = Fig("ch08_balance", 660, 250)
    before = [176, 489, 677, 502, 669, 648, 771, 1454, 1272, 1190, 1356, 1052, 1341, 1657, 1787, 1343]
    after = [977, 1047, 1018, 1024, 1009, 1097, 1025, 1046, 1061, 915, 1090, 1032, 940, 1145, 969, 989]
    for p, (title, vals) in enumerate([("不做均衡", before), ("偏置调节 1,000 步后", after)]):
        c = Chart(f, 50 + p * 320, 44, 270, 150, (0, 16), (0, 2000))
        c.axes([], [0, 500, 1000, 1500, 2000], ylabel="每个专家每批处理的 token 数" if p == 0 else None, yfmt=lambda v: f"{v:,}")
        f.text(c.x0 + c.w / 2, 14, title, 12, "middle", INK, 700)
        for i, v in enumerate(vals):
            col = RED if (p == 0 and v > 1280) else BLUE
            c.bar(c.X(i + 0.5), v, 12, col)
        c.hline(1024, INK, "4 3", "理想值 1,024" if p == 0 else "虚线：理想值 1,024", anchor="start" if p == 0 else "end", dy=-4 if p == 0 else -32)
        if p == 0:
            c.hline(1280, RED, "2 3", None)
            f.text(c.x0 + 4, c.Y(1280) - 5, "容量上限（系数 1.25）", 10.5, "start", RED)
        f.text(c.x0 + c.w / 2, c.Y(0) + 16, "16 个专家", 11, "middle", INK2)
    f.text(330, 244, "模拟实验（实测）：16 个专家选 2 个，每批 8,192 个 token。红色的专家超出容量，多出的 token 在旧方案里会被丢弃", 11.5, "middle", INK2)
    save(f)


def ch08_fine():
    f = Fig("ch08_fine", 660, 205)
    f.text(140, 18, "16 个专家选 2 个：120 种组合", 12.5, "middle", INK, 700)
    for i in range(16):
        x, y = 40 + (i % 8) * 26, 40 + (i // 8) * 52
        sel = i in (3, 12)
        f.rect(x, y, 22, 46, BLUE if sel else GRAY_L, "none" if sel else GRAY, 1, 3)
    f.text(140, 162, "每个专家的隐藏层宽度为 $h$", 11.5, "middle", INK2)
    f.text(470, 18, "拆细成 64 个选 8 个，再加 1 个共享专家：约 44 亿种组合", 12.5, "middle", INK, 700)
    f.rect(330, 40, 30, 98, GREEN, "none", 0, 3)
    f.text(345, 156, "共享", 11, "middle", INK2)
    sel = {2, 9, 17, 22, 35, 41, 50, 63}
    for i in range(64):
        x, y = 372 + (i % 16) * 17, 40 + (i // 16) * 25
        on = i in sel
        f.rect(x, y, 14, 22, BLUE if on else GRAY_L, "none" if on else GRAY, 0.8, 2)
    f.text(508, 156, "每个专家的宽度为 $h/4$，每个 token 的计算量不变", 11.5, "middle", INK2)
    f.text(330, 194, "组合越多，模型越能为不同 token 拼出合适的专家组合；共享专家承载所有 token 都需要的通用知识", 11.5, "middle", INK2)
    save(f)


def ch08_a2a():
    f = Fig("ch08_a2a", 660, 250)
    gpus = 4
    cols = [BLUE, ORANGE, GREEN, PURPLE]
    for g in range(gpus):
        x = 20 + g * 160
        f.rect(x, 30, 140, 50, GRAY_L, GRAY, 1, 4)
        f.text(x + 70, 22, f"GPU {g}", 11.5, "middle", INK2)
        for t in range(4):
            dest = (g * 3 + t * 5) % 4
            f.rect(x + 8 + t * 32, 44, 26, 24, cols[dest], "none", 0, 2)
        f.rect(x, 150, 140, 46, BLUE_L, BLUE, 1, 4)
        f.text(x + 70, 170, f"专家 {2 * g + 1}、{2 * g + 2}", 12, "middle", INK)
        f.text(x + 70, 187, "处理收到的 token", 10.5, "middle", INK2)
    for g in range(gpus):
        for d in range(gpus):
            x1, x2 = 20 + g * 160 + 70, 20 + d * 160 + 70
            f.line(x1, 84, x2, 146, cols[d], 1.2 if g != d else 2, None)
    f.text(10, 118, "① 分发", 12, "start", INK, 700)
    f.text(10, 216, "② 专家计算之后，再做一次 all-to-all，把结果送回 token 原来所在的 GPU（汇总）", 12, "start", INK)
    f.text(330, 244, "颜色表示 token 被路由去的 GPU。每个 MoE 层都要做两次 all-to-all，跨机器时很容易成为瓶颈", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 9
def ch09_share():
    f = Fig("ch09_share", 660, 262)
    c = Chart(f, 60, 26, 440, 170, (1024, 1048576), (0, 1), xlog=True)
    ticks = [1024, 4096, 16384, 65536, 262144, 1048576]
    c.axes(ticks, [0, 0.25, 0.5, 0.75, 1.0], xlabel="上下文长度 $T$（对数坐标）", ylabel="注意力占每层计算量的比例",
           xfmt=lambda v: {1024: "1K", 4096: "4K", 16384: "16K", 65536: "64K", 262144: "256K", 1048576: "1M"}[v],
           yfmt=lambda v: f"{v:.0%}")
    xs = [1024 * 2 ** (i / 8) for i in range(81)]
    for d, col, lab in ((4096, BLUE, "$d$ = 4096"), (16384, ORANGE, "$d$ = 16384")):
        ys = [T / (T + 6 * d) for T in xs]
        c.series(xs, ys, col)
        f.text(c.X(xs[-1]) + 6, c.Y(ys[-1]) + 4, lab, 11.5, "start", INK)
    for T, v in ((8192, .25), (32768, .57), (131072, .84), (1048576, .98)):
        c.dots([T], [v], BLUE)
    c.hline(0.5, GRAY, "3 3", None)
    f.text(c.X(1100), c.Y(0.5) - 5, "过半", 11, "start", INK2)
    f.text(330, 256, "比例 = $4Td$ / ($4Td + 24d^2$) = $T$ / ($T + 6d$)。圆点是正文表格中的四个数", 11.5, "middle", INK2)
    save(f)


def ch09_mla():
    f = Fig("ch09_mla", 660, 230)
    f.box(10, 92, 80, 40, "$x_t$（$d$ 维）", "white", 12)
    f.arrow(92, 112, 128, 112)
    f.box(130, 92, 80, 40, "$W_{DKV}$", "blue", 12, sub="压缩", sub_size=10.5)
    f.arrow(212, 112, 248, 112)
    f.rect(250, 84, 98, 56, ORANGE_L, ORANGE, 1.6, 4)
    f.text(299, 106, "潜在向量 $c_t$", 12, "middle", INK, 700)
    f.text(299, 124, "512 维", 11, "middle", INK2)
    f.text(299, 160, "只缓存它", 11.5, "middle", ORANGE, 700)
    for k, (lab, yy) in enumerate((("$W_{UK}$ → 128 个头的 K", 52), ("$W_{UV}$ → 128 个头的 V", 150))):
        f.arrow(350, 112, 400, yy + 18, GRAY)
        f.box(402, yy, 170, 36, lab, "white", 11.5)
    f.text(487, 34, "需要时再“解压”（或吸收进其他矩阵）", 11, "middle", INK2)
    f.rect(250, 186, 98, 30, PURPLE_L, PURPLE, 1.2, 4)
    f.text(299, 206, "RoPE 部分 64 维", 11, "middle", INK)
    f.text(360, 206, "解耦 RoPE：另存 64 维带位置的 key，各头共享", 11, "start", INK2)
    f.text(10, 20, "每层每个 token 只缓存 512 + 64 = 576 个数（MHA 要 32,768 个）", 12.5, "start", INK, 700)
    save(f)


def ch09_kvbars():
    f = Fig("ch09_kvbars", 660, 150)
    rows = [("MHA", 32768), ("GQA（8 组）", 2048), ("MLA", 576)]
    x0, w = 120, 470
    for k, (lab, v) in enumerate(rows):
        y = 24 + k * 36
        f.text(x0 - 8, y + 16, lab, 12, "end", INK)
        f.rect(x0, y + 2, w * v / 32768, 22, BLUE if k < 2 else ORANGE, "none", 0, 2)
        f.text(x0 + w * v / 32768 + 6, y + 18, f"{v:,}", 11.5, "start", INK)
    f.text(330, 140, "DeepSeek-V3 的规格（128 个头，$d_h$ = 128）下，每层每个 token 要缓存的数", 11.5, "middle", INK2)
    save(f)


def ch09_patterns():
    f = Fig("ch09_patterns", 660, 215)
    T, cs = 16, 8.5
    def grid(x0, title, sub, allowed):
        f.text(x0 + T * cs / 2, 18, title, 12, "middle", INK, 700)
        for i in range(T):
            for j in range(T):
                ok = j <= i and allowed(i, j)
                fill = BLUE if ok else (GRAY_L if j <= i else "#ffffff")
                f.rect(x0 + j * cs, 30 + i * cs, cs - 1, cs - 1, fill, "none", 0, 0.5)
        f.text(x0 + T * cs / 2, 30 + T * cs + 18, sub, 11, "middle", INK2)
    grid(20, "全注意力", "计算量 ∝ $T^2$", lambda i, j: True)
    grid(185, "滑动窗口", "只看最近 $W$ 个", lambda i, j: i - j < 4)
    sel = {(i, j) for i in range(T) for j in range(T) if (j // 4) in {0, (i // 4)} or i - j < 2}
    grid(350, "块稀疏（示意）", "按内容为每个 query 挑块", lambda i, j: (i, j) in sel)
    grid(515, "注意力汇聚点 + 窗口", "保留开头几个 token", lambda i, j: j < 2 or i - j < 4)
    f.text(330, 208, "每个格子表示“第 $i$ 行的 query 能否看到第 $j$ 列的 key”；深蓝 = 计算，浅灰 = 跳过（$T$ = 16，示意）", 11.5, "middle", INK2)
    save(f)


def ch09_state():
    f = Fig("ch09_state", 660, 200)
    f.text(160, 18, "softmax 注意力：KV cache 随序列增长", 12.5, "middle", INK, 700)
    for k in range(12):
        f.rect(20 + k * 24, 40, 20, 46, BLUE_M, "none", 0, 2)
    f.text(20 + 12 * 24 + 4, 68, "…", 14, "start", INK2)
    f.text(160, 108, "每个位置的 K、V 都保留：能精确找回", 11.5, "middle", INK2)
    f.text(160, 126, "1,000 个 token 之前的任何内容，但成本随 $T$ 增长", 11.5, "middle", INK2)
    f.text(500, 18, "线性注意力 / SSM：固定大小的状态", 12.5, "middle", INK, 700)
    f.rect(450, 40, 100, 46, ORANGE, "none", 0, 4)
    f.text(500, 68, "状态 $S$", 12.5, "middle", "#ffffff")
    f.path("M552,60 C600,40 600,90 552,72", ORANGE, 1.5, arrow=True)
    f.text(500, 108, "每来一个 token 就更新一次状态：", 11.5, "middle", INK2)
    f.text(500, 126, "成本不随 $T$ 增长，但旧信息会被挤掉", 11.5, "middle", INK2)
    f.text(330, 168, "混合架构：大量线性层 / SSM 层降低成本，少量全注意力层负责精确检索", 12, "middle", INK)
    f.text(330, 190, "$S_t = S_{t-1} + \\phi(k_t)^{T}v_t$，$o_t = \\phi(q_t)S_t$", 11.5, "middle", INK2)
    save(f)


def ch09_wave():
    f = Fig("ch09_wave", 660, 264)
    c = Chart(f, 60, 26, 440, 170, (0, 64), (1, 1e7), ylog=True)
    c.axes([0, 16, 32, 46, 64], [1e1, 1e3, 1e5, 1e7], xlabel="维度对的编号 $i$（$d_h$ = 128，共 64 对）",
           ylabel="波长：转一整圈需要的位置数（对数坐标）", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"$10^{{{int(round(math.log10(v)))}}}$")
    for base, col, lab in ((10000, BLUE, "base = 10,000"), (500000, ORANGE, "base = 500,000（Llama 3）")):
        xs = list(range(64))
        ys = [2 * math.pi * base ** (2 * i / 128) for i in xs]
        c.series(xs, ys, col)
        f.text(c.X(63) + 6, c.Y(ys[-1]) + 4, lab, 11, "start", INK)
    c.hline(4096, RED, "5 3", None)
    f.text(c.x0 + 4, c.Y(4096) - 5, "训练长度 4,096", 11, "start", RED)
    xs = [i for i in range(64) if 2 * math.pi * 10000 ** (2 * i / 128) > 4096]
    c.dots(xs, [2 * math.pi * 10000 ** (2 * i / 128) for i in xs], BLUE, 2.8)
    f.text(c.X(47), c.Y(900), ["圆点：第 46–63 对（18 对），", "在 4,096 个位置内一圈都没转完"], 11, "start", BLUE)
    f.text(330, 258, "高频的维度对在训练长度内转了很多圈；低频的维度对在外推时会遇到没见过的角度", 11.5, "middle", INK2)
    save(f)


def ch09_packing():
    f = Fig("ch09_packing", 660, 215)
    docs = [(0, 5, BLUE), (5, 9, ORANGE), (9, 16, GREEN)]
    T, cs = 16, 9.5
    f.text(10, 18, "打包：三篇文档拼成一条 16 个 token 的训练序列", 12.5, "start", INK, 700)
    for a, b, col in docs:
        for k in range(a, b):
            f.rect(10 + k * 17, 30, 15, 22, col, "none", 0, 2)
    f.text(10 + 2.5 * 17, 70, "文档 A", 11, "middle", INK2)
    f.text(10 + 7 * 17, 70, "文档 B", 11, "middle", INK2)
    f.text(10 + 12.5 * 17, 70, "文档 C", 11, "middle", INK2)
    for p, (title, block) in enumerate((("只用因果掩码", False), ("因果掩码 + 文档掩码", True))):
        x0 = 330 + p * 170
        f.text(x0 + T * cs / 2, 18, title, 12, "middle", INK, 700)
        for i in range(T):
            di = next(k for k, (a, b, _) in enumerate(docs) if a <= i < b)
            for j in range(T):
                dj = next(k for k, (a, b, _) in enumerate(docs) if a <= j < b)
                ok = j <= i and (not block or di == dj)
                cross = j <= i and di != dj
                fill = docs[di][2] if ok and di == dj else ("#f2c4be" if ok and cross else ("#ffffff" if j > i else GRAY_L))
                f.rect(x0 + j * cs, 30 + i * cs, cs - 1, cs - 1, fill, "none", 0, 0.5)
    f.text(330 + T * cs / 2, 30 + T * cs + 16, "浅红：看到了别的文档", 11, "middle", RED)
    f.text(500 + T * cs / 2, 30 + T * cs + 16, "每篇只看自己", 11, "middle", INK2)
    f.text(10, 110, ["不加文档掩码时，文档 C 的 token", "能“看到”毫不相关的文档 A、B，", "学到虚假的依赖关系。", "加上文档掩码，注意力矩阵变成", "块对角的形状。"], 11.5, "start", INK2)
    save(f)


if __name__ == "__main__":
    for fn in [ch05_split, ch05_utf8, ch05_bpe, ch05_vocab, ch05_zh, ch05_pipeline,
               ch06_rnn, ch06_qkv, ch06_mask, ch06_multihead, ch06_ctx, ch06_encdec,
               ch07_rope, ch07_swiglu, ch07_gqa, ch07_params, ch07_block,
               ch08_params, ch08_balance, ch08_fine, ch08_a2a,
               ch09_share, ch09_mla, ch09_kvbars, ch09_patterns, ch09_state, ch09_wave, ch09_packing]:
        fn()
    print("ok")
