"""Figures for Part 1 (chapters 0-4). Run: python3 figs/p1.py  → writes figs/chNN_*.svg"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import *

OUT = os.path.dirname(os.path.abspath(__file__))


def save(f):
    f.save(os.path.join(OUT, f.name + ".svg"))


def mat(f, x, y, w, h, fill, stroke, label=None, below=True, size=11.5):
    f.rect(x, y, w, h, fill, stroke, 1.2, 2)
    if label:
        f.text(x + w / 2, (y + h + size + 3) if below else (y - 5), label, size, "middle", INK)


# ----------------------------------------------------------------- chapter 0
def ch00_6nd():
    f = Fig("ch00_6nd", 660, 300)
    cards = [("前向", "blue", "$y = xW$", "每个参数 2 FLOP"),
             ("反向①：传给前一层的梯度", "orange", "$dx = dy\\,W^{T}$", "每个参数 2 FLOP"),
             ("反向②：本层权重的梯度", "orange", "$dW = x^{T}dy$", "每个参数 2 FLOP")]
    cw, gap = 206, 11
    for i, (title, st, eq, cost) in enumerate(cards):
        x = 6 + i * (cw + gap)
        fill, stroke, _ = STYLE[st]
        f.rect(x, 6, cw, 196, fill, stroke, 1.2, 6)
        f.text(x + cw / 2, 30, title, 13, "middle", INK, 700)
        f.text(x + cw / 2, 58, eq, 15, "middle", INK)
        f.text(x + cw / 2, 190, cost, 12, "middle", INK2)
    # pictograms: d_in = 4 units tall, d_out = 3 units wide, unit = 16
    u = 15
    def eqrow(x, parts):
        """parts: list of (w, h, label, colour) or str operator"""
        cx = x
        base = 112
        for p in parts:
            if isinstance(p, str):
                f.text(cx + 7, base + 5, p, 15, "middle", INK2)
                cx += 16
            else:
                w, h, lab, col = p
                mat(f, cx, base - h / 2, w, h, col, NAVY if col != "#ffffff" else GRAY, lab, True, 11.5)
                cx += w + 4
    # card 1: x (1 x d_in) · W (d_in x d_out) = y (1 x d_out)
    eqrow(14, [(4 * u, u, "$x$", "#ffffff"), "×", (3 * u, 4 * u, "$W$", BLUE_M), "=", (3 * u, u, "$y$", "#ffffff")])
    eqrow(6 + cw + gap + 8, [(3 * u, u, "$dy$", ORANGE_M), "×", (4 * u, 3 * u, "$W^{T}$", BLUE_M), "=", (4 * u, u, "$dx$", "#ffffff")])
    eqrow(6 + 2 * (cw + gap) + 18, [(u, 4 * u, "$x^{T}$", "#ffffff"), "×", (3 * u, u, "$dy$", ORANGE_M), "=", (3 * u, 4 * u, "$dW$", ORANGE_M)])
    # total bar
    y = 226
    f.text(6, y + 14, "每个参数、每个 token：", 12.5, "start", INK)
    x0, unit = 150, 40
    for k, (lab, col) in enumerate([("前向 2", BLUE), ("反向 2", ORANGE), ("反向 2", ORANGE)]):
        f.rect(x0 + k * unit * 2, y, unit * 2 - 2, 22, col, "none", 0, 3)
        f.text(x0 + k * unit * 2 + unit - 1, y + 15.5, lab, 12, "middle", "#ffffff")
    f.text(x0 + 6 * unit + 10, y + 15.5, "= 6 FLOP，于是 $C \\approx 6ND$", 12.5, "start", INK)
    f.text(330, 288, "方块的形状表示矩阵的形状：三次乘法规模相同，都要做 $d_{in} \\times d_{out}$ 次乘加", 11.5, "middle", INK2)
    save(f)


def ch00_mem16():
    f = Fig("ch00_mem16", 660, 210)
    segs = [("bf16 权重", 2, BLUE), ("bf16 梯度", 2, "#5b8fc2"), ("fp32 主权重", 4, ORANGE),
            ("Adam $m$", 4, GREEN), ("Adam $v$", 4, "#5fa37a")]
    x0, y0, unit = 50, 34, 31
    f.text(6, 20, "每个参数要存的东西（字节）", 12.5, "start", INK, 700)
    cx = x0
    for lab, b, col in segs:
        w = b * unit
        f.rect(cx, y0, w - 2, 34, col, "none", 0, 2)
        f.text(cx + w / 2 - 1, y0 + 15, lab, 11.5, "middle", "#ffffff")
        f.text(cx + w / 2 - 1, y0 + 29, f"{b}", 11.5, "middle", "#ffffff")
        cx += w
    f.text(cx + 8, y0 + 22, "= 16 字节", 13, "start", INK, 700)
    for k in range(0, 17, 2):
        f.text(x0 + k * unit, y0 + 50, str(k), 10.5, "middle", INK3)
    # second row: 7B model vs one H100
    y1 = 120
    f.text(6, y1 - 8, "7B 模型的权重、梯度和优化器状态，与一张 H100 的显存相比（GB）", 12.5, "start", INK, 700)
    scale = 4.3
    f.rect(x0, y1, 112 * scale, 24, BLUE, "none", 0, 2)
    f.text(x0 + 6, y1 + 16.5, "7B × 16 字节 = 112 GB", 12, "start", "#ffffff")
    f.rect(x0, y1 + 32, 80 * scale, 24, GRAY_L, GRAY, 1, 2)
    f.text(x0 + 6, y1 + 48.5, "一张 H100：80 GB", 12, "start", INK)
    f.line(x0 + 80 * scale, y1 - 4, x0 + 80 * scale, y1 + 60, RED, 1.2, "4 3")
    f.text(x0 + 80 * scale + 6, y1 + 48.5, "放不下：要切分到多张卡上（第 20 章）", 11.5, "start", RED)
    f.text(6, y1 + 18, "", 12)
    f.text(330, 202, "这还不包括激活值，它随 batch 大小和序列长度增长", 11.5, "middle", INK2)
    save(f)


def ch00_decode():
    f = Fig("ch00_decode", 660, 200)
    f.rect(10, 30, 210, 120, BLUE_L, BLUE, 1.2, 6)
    f.text(115, 52, "显存（HBM）", 13, "middle", INK, 700)
    for k in range(5):
        f.rect(28 + k * 36, 66, 30, 44, BLUE_M, BLUE, 1, 2)
    f.text(115, 132, "全部权重：Llama 3 8B 约 16 GB", 11.5, "middle", INK2)
    f.rect(390, 30, 160, 120, ORANGE_L, ORANGE, 1.2, 6)
    f.text(470, 52, "计算单元", 13, "middle", INK, 700)
    f.text(470, 80, "989 TFLOP/s", 12, "middle", INK2)
    f.text(470, 104, "每个 token 只需", 11.5, "middle", INK2)
    f.text(470, 120, "约 $2N$ = 160 亿次运算", 11.5, "middle", INK2)
    f.arrow(224, 90, 386, 90, BLUE, 3)
    f.text(305, 80, "每生成 1 个 token", 12, "middle", INK)
    f.text(305, 110, "把 16 GB 全部读一遍", 12, "middle", INK)
    f.text(305, 126, "3.35 TB/s", 11.5, "middle", INK2)
    f.box(590, 74, 60, 32, "新 token", "Green", 12)
    f.arrow(552, 90, 588, 90, INK3)
    f.poly([(620, 108), (620, 168), (115, 168), (115, 154)], INK3, 1.3, "4 3", arrow=True)
    f.text(370, 190, "新 token 接到输入后面，再把全部权重读一遍，生成下一个", 11.5, "middle", INK2)
    f.text(330, 18, "瓶颈在读权重：最多 3,350 ÷ 16 ≈ 200 token/s，此时算力只用了峰值的 0.4%", 12.5, "middle", INK, 700)
    save(f)


# ----------------------------------------------------------------- chapter 1
def ch01_tree():
    f = Fig("ch01_tree", 660, 270)
    cols = {"root": 34, 1: 150, 2: 262, 3: 374, 4: 486}
    ys = {"cs": 64, "cp": 138, "ds": 222}
    # cylinder set highlight
    f.rect(118, 36, 528, 140, "#f4f8fc", BLUE, 1, 10, "5 4")
    f.text(640, 168, "柱集 {$X_1$ = 猫}：所有以“猫”开头的文档，概率 0.8", 11.5, "end", BLUE)
    node = lambda x, y, s, st="white": f.box(x - 22, y - 15, 44, 30, s, st, 14)
    node(cols["root"], 143, "开始", "gray")
    node(cols[1], 101, "猫", "Blue")
    node(cols[1], 222, "狗")
    paths = {"cs": ["睡", "了", "⟨eos⟩"], "cp": ["跑", "了", "⟨eos⟩"], "ds": ["睡", "了", "⟨eos⟩"]}
    for key, toks in paths.items():
        for k, t in enumerate(toks):
            st = "Blue" if key == "cs" else "white"
            node(cols[k + 2], ys[key], t, st)
    def edge(x1, y1, x2, y2, p, hl=False, pos=0.5):
        col = BLUE if hl else GRAY
        f.line(x1 + 23, y1, x2 - 23, y2, col, 2.2 if hl else 1.3)
        mx, my = x1 + 23 + (x2 - x1 - 46) * pos, y1 + (y2 - y1) * pos
        f.text(mx, my - 6, p, 11.5, "middle", BLUE if hl else INK2, 700 if hl else None)
    edge(cols["root"], 143, cols[1], 101, "0.8", True)
    edge(cols["root"], 143, cols[1], 222, "0.2")
    edge(cols[1], 101, cols[2], ys["cs"], "0.625", True)
    edge(cols[1], 101, cols[2], ys["cp"], "0.375")
    edge(cols[1], 222, cols[2], ys["ds"], "1")
    for key in paths:
        hl = key == "cs"
        edge(cols[2], ys[key], cols[3], ys[key], "1", hl)
        edge(cols[3], ys[key], cols[4], ys[key], "1", hl)
    for key, p in (("cs", "0.5"), ("cp", "0.3"), ("ds", "0.2")):
        f.text(cols[4] + 34, ys[key] + 5, f"文档概率 {p}", 12, "start", INK, 700 if key == "cs" else None)
    f.text(6, 262, "蓝色路径：$P$(猫睡了⟨eos⟩) = 0.8 × 0.625 × 1 × 1 = 0.5，每条边上是给定前缀时下一个 token 的条件概率",
           11.5, "start", INK2)
    save(f)


def ch01_autoreg():
    f = Fig("ch01_autoreg", 660, 205)
    toks = ["猫", "坐", "在"]
    for k, t in enumerate(toks):
        f.box(10 + k * 40, 70, 36, 32, t, "white", 14)
    f.text(70, 60, "前文", 11.5, "middle", INK2)
    f.arrow(132, 86, 168, 86)
    f.box(170, 56, 110, 60, "语言模型", "navy", 14, sub="给每个候选打分")
    f.arrow(282, 86, 316, 86)
    # distribution bars
    cands = [("垫", .42), ("地", .23), ("椅", .14), ("床", .09), ("……", .12)]
    bx, base = 330, 124
    for k, (c, p) in enumerate(cands):
        h = p * 150
        col = BLUE if k == 0 else BLUE_M
        f.rect(bx + k * 36, base - h, 26, h, col, "none", 0, 2)
        f.text(bx + k * 36 + 13, base + 16, c, 12.5, "middle", INK)
        f.text(bx + k * 36 + 13, base - h - 5, f"{p:.2f}", 10.5, "middle", INK2)
    f.line(bx - 4, base, bx + 5 * 36, base, AXIS, 1)
    f.text(bx + 88, 34, "softmax 得到下一个 token 的分布", 11.5, "middle", INK2)
    f.arrow(514, 86, 548, 86)
    f.box(550, 66, 100, 40, "抽样：垫", "Green", 13)
    f.path("M600,108 C600,185 120,185 120,106", INK3, 1.3, "4 3", arrow=True)
    f.text(360, 180, "把抽到的 token 接到前文后面，再预测下一个，直到抽到 ⟨eos⟩", 11.5, "middle", INK2)
    f.text(330, 16, "示意：概率数字是虚构的", 10.5, "middle", INK3)
    save(f)


def ch01_loss():
    f = Fig("ch01_loss", 660, 255)
    c = Chart(f, 60, 26, 420, 186, (0, 5), (0, 4.5))
    models = [("均匀分布", 4.174), ("unigram", 3.347), ("bigram", 2.482), ("5-gram", 1.770), ("MLP（第 2 章）", 1.711)]
    c.axes([], [0, 1, 2, 3, 4], ylabel="验证集 loss（nats/字符）", yfmt=lambda v: f"{v:g}")
    H = 1.2
    for k, (m, v) in enumerate(models):
        xc = c.X(k + 0.5)
        f.rect(xc - 22, c.Y(H), 44, c.Y(0) - c.Y(H), GRAY_L, "none", 0, 0)
        f.rect(xc - 22, c.Y(v), 44, c.Y(H) - c.Y(v), BLUE_M, "none", 0, 0)
        f.text(xc, c.Y(v) - 5, f"{v:.2f}", 11, "middle", INK)
        f.text(xc, c.Y(0) + 16, m, 11, "middle", INK2)
    c.hline(H, INK, "5 3", None)
    f.text(492, c.Y(H) + 4, "$H(p)$：数据本身的熵", 12, "start", INK)
    f.text(492, c.Y(H) + 20, "（真实值未知，", 11, "start", INK2)
    f.text(492, c.Y(H) + 34, "这里的位置是示意）", 11, "start", INK2)
    f.rect(492, 60, 14, 12, BLUE_M, "none", 0, 2)
    f.text(512, 70, "KL：模型与真实分布的差距", 11.5, "start", INK)
    f.text(512, 86, "训练只能压低这一段", 11, "start", INK2)
    f.rect(492, 100, 14, 12, GRAY_L, GRAY, 0.8, 2)
    f.text(512, 110, "不可约损失：永远降不掉", 11.5, "start", INK)
    f.text(330, 250, "交叉熵 loss = $H(p)$ + KL。柱高是本章和第 2 章模型的实测 loss", 11.5, "middle", INK2)
    save(f)


def ch01_grad():
    f = Fig("ch01_grad", 660, 218)
    toks = ["猫", "狗", "垫", "地", "上"]
    q = [0.10, 0.55, 0.20, 0.10, 0.05]
    y = 2  # index of the correct token
    panels = [("模型的分布 $q$ = softmax($z$)", q, BLUE_M), ("正确答案 onehot($y$)", [1 if i == y else 0 for i in range(5)], GREEN_M),
              ("梯度 $q$ − onehot($y$)", [q[i] - (1 if i == y else 0) for i in range(5)], None)]
    for p, (title, vals, col) in enumerate(panels):
        x0 = 14 + p * 218
        f.text(x0 + 95, 18, title, 12, "middle", INK, 700)
        base = 118 if p < 2 else 92
        f.line(x0, base, x0 + 190, base, AXIS, 1)
        for i, v in enumerate(vals):
            xc = x0 + 19 + i * 38
            h = v * 80
            colour = col if col else (ORANGE if v > 0 else GREEN)
            f.rect(xc - 11, base - max(h, 0), 22, abs(h), colour, "none", 0, 2)
            lab = f"{v:+.2f}" if p == 2 else f"{v:.2f}".rstrip("0").rstrip(".") if v else "0"
            ty = base - h - 5 if v >= 0 else base - h + 13
            f.text(xc, ty, lab, 10.5, "middle", INK2)
            f.text(xc, 138 if p < 2 else 186, toks[i], 12.5, "middle", INK, 700 if i == y else None)
    f.text(330, 210, "梯度下降沿梯度的反方向走：正确答案“垫”的 logit 被往上推 0.80，最自信的错误答案“狗”被往下推得最狠",
           11.5, "middle", INK2)
    f.text(14, 168, "正确答案是“垫”", 11.5, "start", INK2)
    save(f)


def ch01_teacher():
    f = Fig("ch01_teacher", 660, 215)
    inp = ["猫", "坐", "在", "垫", "上"]
    tgt = ["坐", "在", "垫", "上", "⟨eos⟩"]
    x0, dx = 92, 104
    f.text(8, 196, "输入", 12, "start", INK2)
    f.text(8, 30, "目标", 12, "start", INK2)
    f.rect(x0 - 30, 96, 4 * dx + 60, 46, BLUE_L, NAVY, 1.2, 6)
    f.text(x0 + 2 * dx, 116, "Transformer（因果：每个位置只看得到自己和前面的 token）", 12.5, "middle", INK)
    f.text(x0 + 2 * dx, 134, "一次前向，同时算出所有位置的预测", 11, "middle", INK2)
    for k in range(5):
        x = x0 + k * dx
        f.box(x - 20, 172, 40, 30, inp[k], "white", 14)
        f.arrow(x, 170, x, 144, GRAY)
        f.arrow(x, 94, x, 66, GRAY)
        f.box(x - 26, 36, 52, 30, tgt[k], "green", 13 if k < 4 else 11.5)
        f.text(x, 84, f"$-\\log q$", 11, "middle", ORANGE) if False else None
    f.text(x0 + 2 * dx, 18, "每个位置预测下一个 token，loss = 各位置 $-\\log q$(目标) 的平均", 12, "middle", INK)
    save(f)


def ch01_temp():
    f = Fig("ch01_temp", 660, 240)
    labels = ["h", "空格", "o", "e", "i", "其余 60 个"]
    counts = {"h": 20592, " ": 14879, "o": 5328, "e": 3918, "i": 2698}
    total = 60384
    rest = total - sum(counts.values())
    # treat the remaining 60 characters as spread evenly for the temperature transform (approximation shown as one bar)
    probs = [counts["h"], counts[" "], counts["o"], counts["e"], counts["i"]]
    p_main = [c / total for c in probs]
    rest_each = rest / total / 60
    def temper(t):
        w = [p ** (1 / t) for p in p_main] + [rest_each ** (1 / t)] * 60
        s = sum(w)
        return [x / s for x in w[:5]] + [sum(w[5:]) / s]
    temps = [(0.5, BLUE, "τ = 0.5"), (1.0, ORANGE, "τ = 1"), (2.0, GREEN, "τ = 2")]
    c = Chart(f, 50, 34, 560, 160, (0, 6), (0, 0.7))
    c.axes([], [0, 0.2, 0.4, 0.6], ylabel="概率", yfmt=lambda v: f"{v:g}")
    for i, lab in enumerate(labels):
        f.text(c.X(i + 0.5), c.Y(0) + 17, lab, 12, "middle", INK)
    for j, (t, col, name) in enumerate(temps):
        vals = temper(t)
        for i, v in enumerate(vals):
            xc = c.X(i + 0.5) + (j - 1) * 24
            c.bar(xc, v, 20, col)
            if i in (0, 5):
                f.text(xc, c.Y(v) - 4, f"{v:.2f}", 10, "middle", INK2)
    legend(f, 360, 22, [(n, col, "box") for _, col, n in temps])
    f.text(330, 234, "字符 t 后面的下一个字符（莎士比亚训练集的实测频率），按 $q^{1/τ}$ 重新归一化", 11.5, "middle", INK2)
    save(f)


def ch01_ngram():
    f = Fig("ch01_ngram", 660, 230)
    ns = [2, 3, 4, 5, 6, 7]
    loss = [2.488, 2.066, 1.796, 1.770, 2.007, 2.366]
    unseen = [0, 0.2, 1.4, 4.2, 10.1, 20.8]
    c1 = Chart(f, 50, 30, 250, 150, (1.6, 7.4), (1.6, 2.6))
    c1.axes(ns, [1.8, 2.0, 2.2, 2.4, 2.6], xlabel="$n$（看前 $n-1$ 个字符）", ylabel="验证集 loss", yfmt=lambda v: f"{v:.1f}")
    c1.series(ns, loss, BLUE, markers=True)
    f.circle(c1.X(5), c1.Y(1.770), 7, "none", ORANGE, 1.6)
    f.text(c1.X(5), c1.Y(1.770) + 22, "最好：5-gram", 11, "middle", INK)
    c2 = Chart(f, 390, 30, 250, 150, (1.6, 7.4), (0, 25))
    c2.axes(ns, [0, 5, 10, 15, 20, 25], xlabel="$n$", ylabel="上下文从没在训练集里出现过的位置（%）", yfmt=lambda v: f"{v:g}")
    c2.series(ns, unseen, ORANGE, markers=True)
    f.text(c2.X(6.75), c2.Y(21.5), "20.8% 的位置只能均匀乱猜", 11, "end", INK)
    save(f)


if __name__ == "__main__":
    for fn in [ch00_6nd, ch00_mem16, ch00_decode, ch01_tree, ch01_autoreg, ch01_loss, ch01_grad, ch01_teacher,
               ch01_temp, ch01_ngram]:
        fn()
    print("ok")


# ----------------------------------------------------------------- chapter 2
def ch02_onehot():
    f = Fig("ch02_onehot", 660, 225)
    # one-hot row vector (13 cells shown), times matrix, = selected row
    n, cw = 13, 15
    x0, y0 = 10, 92
    f.text(x0, 40, "onehot(c)：只有第 c 位是 1", 12, "start", INK2)
    for i in range(n):
        hot = i == 4
        f.rect(x0 + i * cw, y0, cw - 1, 18, BLUE if hot else "#ffffff", GRAY, 0.8, 1)
        if hot:
            f.text(x0 + i * cw + 7, y0 + 13.5, "1", 10.5, "middle", "#ffffff")
    f.text(x0 + n * cw / 2, y0 + 36, "1 × 65", 11, "middle", INK2)
    f.text(x0 + n * cw + 14, y0 + 14, "×", 15, "middle", INK2)
    mx, my, rh = x0 + n * cw + 30, 26, 11
    for i in range(n):
        hot = i == 4
        f.rect(mx, my + i * rh, 150, rh - 1, BLUE_M if hot else GRAY_L, BLUE if hot else "none", 1 if hot else 0, 1)
    f.text(mx + 75, my + n * rh + 16, "矩阵 $E$（65 × 16）", 11.5, "middle", INK2)
    f.text(mx - 6, my + 4 * rh + 8.5, "第 c 行", 10.5, "end", BLUE)
    f.text(mx + 172, y0 + 14, "=", 15, "middle", INK2)
    rx = mx + 190
    f.rect(rx, y0, 150, rh + 6, BLUE_M, BLUE, 1, 1)
    f.text(rx + 75, y0 + 36, "第 c 行：字符 c 的 embedding", 11.5, "middle", INK2)
    f.text(rx + 75, y0 + 52, "（1 × 16）", 11, "middle", INK2)
    f.text(330, 218, "乘法只是把第 c 行“取出来”：查表 = one-hot 乘矩阵 = 一个线性层", 12, "middle", INK)
    save(f)


def ch02_xor():
    f = Fig("ch02_xor", 660, 215)
    c = Chart(f, 50, 26, 170, 150, (-0.3, 1.3), (-0.3, 1.3))
    c.axes([0, 1], [0, 1], xlabel="输入 1", yfmt=lambda v: f"{v:g}", grid=False)
    f.text(20, 104, "输入 2", 11.5, "middle", INK2)
    for (a, b, out) in [(0, 0, 0), (1, 1, 0), (0, 1, 1), (1, 0, 1)]:
        if out:
            f.circle(c.X(a), c.Y(b), 9, BLUE, "#ffffff", 1.5)
        else:
            f.rect(c.X(a) - 8, c.Y(b) - 8, 16, 16, ORANGE, "#ffffff", 1.5, 2)
    f.line(c.X(-0.25), c.Y(0.6), c.X(1.25), c.Y(0.35), GRAY, 1.2, "5 4")
    legend(f, 236, 60, [("输出 1", BLUE, "dot")], horizontal=False)
    f.rect(238, 76, 14, 12, ORANGE, "none", 0, 2)
    f.text(259, 86, "输出 0", 11.5, "start", INK)
    f.text(236, 118, ["异或：没有一条直线能把", "圆点和方块分开，", "所以线性模型做不到"], 11.5, "start", INK2)
    c2 = Chart(f, 430, 26, 210, 150, (-4, 4), (-1.2, 1.2))
    c2.axes([-4, -2, 0, 2, 4], [-1, 0, 1], xlabel="输入", yfmt=lambda v: f"{v:g}")
    xs = [i / 10 for i in range(-40, 41)]
    c2.series(xs, [math.tanh(v) for v in xs], BLUE)
    c2.series([-1.2, 1.2], [-1.2, 1.2], GRAY, 1, "4 3")
    f.text(c2.X(1.3), c2.Y(1.1), "$y = x$", 11, "start", INK2)
    f.text(c2.X(-3.9), c2.Y(-0.75), "饱和", 11, "start", INK2)
    f.text(c2.X(2.2), c2.Y(0.8), "饱和", 11, "start", INK2)
    f.text(535, 16, "tanh：中间近似线性，两头被压平", 12, "middle", INK)
    save(f)


def ch02_matgrad():
    f = Fig("ch02_matgrad", 660, 312)
    u = 13
    rows = [("前向", "$Y = XW$", [("X", "B", "n", None), "×", ("W", "n", "m", BLUE_M), "=", ("Y", "B", "m", None)]),
            ("反向", "$dX = dY\\,W^{T}$", [("dY", "B", "m", ORANGE_M), "×", ("W^{T}", "m", "n", BLUE_M), "=", ("dX", "B", "n", ORANGE_M)]),
            ("反向", "$dW = X^{T}dY$", [("X^{T}", "n", "B", None), "×", ("dY", "B", "m", ORANGE_M), "=", ("dW", "n", "m", ORANGE_M)])]
    dims = {"B": 3, "n": 5, "m": 4}
    for r, (tag, eq, parts) in enumerate(rows):
        y = 22 + r * 92
        f.text(8, y + 40, tag, 12.5, "start", INK, 700)
        f.text(50, y + 40, eq, 13.5, "start", INK)
        cx = 196
        for p in parts:
            if isinstance(p, str):
                f.text(cx + 12, y + 41, p, 15, "middle", INK2)
                cx += 32
                continue
            name, rd, cd, col = p
            w, h = dims[cd] * u, dims[rd] * u
            top = y + 36 - h / 2
            f.rect(cx, top, w, h, col or "#ffffff", NAVY if col else GRAY, 1.2, 2)
            f.text(cx + w / 2, top + h / 2 + 4.5, f"${name}$", 12.5, "middle", INK)
            f.text(cx + w / 2, top - 4, cd, 10.5, "middle", INK3)
            f.text(cx - 4, top + h / 2 + 4, rd, 10.5, "end", INK3)
            cx += w + 4
        f.text(cx + 14, y + 40, ["形状：" + ("$B\\times m$" if r == 0 else "$B\\times n$，与 $X$ 相同" if r == 1 else "$n\\times m$，与 $W$ 相同")],
               11.5, "start", INK2)
    f.text(330, 304, "梯度的形状一定和原变量相同；满足这一点的矩阵乘法基本只有一种写法", 11.5, "middle", INK2)
    save(f)


def ch02_backflow():
    f = Fig("ch02_backflow", 660, 215)
    nodes = [("$x$ = E[字符]", 10), ("$a = xW_1 + b_1$", 140), ("$h$ = tanh($a$)", 290), ("logits = $hW_2 + b_2$", 418), ("loss", 580)]
    w = [116, 136, 112, 150, 66]
    y = 44
    xs = []
    for k, (lab, x) in enumerate(nodes):
        f.box(x, y, w[k], 36, lab, "navy" if k < 4 else "red", 12.5)
        xs.append((x, x + w[k]))
    for k in range(4):
        f.arrow(xs[k][1] + 2, y + 11, xs[k + 1][0] - 2, y + 11, NAVY, 1.4)
        f.arrow(xs[k + 1][0] - 2, y + 26, xs[k][1] + 2, y + 26, ORANGE, 1.4)
    f.text(330, 28, "前向（深蓝箭头）：从左往右算出每个中间结果", 12, "middle", NAVY)
    grads = ["$dx$：累加回 E 的对应行", "$da = dh\\odot(1-h^2)$", "$dh = d\\,$logits$\\,W_2^{T}$", "$d\\,$logits = softmax − onehot"]
    for k, g in enumerate(grads):
        cx = (xs[k][0] + xs[k][1]) / 2 if k < 3 else (xs[3][0] + xs[3][1]) / 2
        f.line(cx, 84, cx, 104, ORANGE, 1, "3 3")
        f.text(cx, 120, g, 11.5, "middle", INK)
    f.text((xs[1][0] + xs[1][1]) / 2, 144, "$dW_1 = x^{T}da$，$db_1 = \\sum da$", 11.5, "middle", INK2)
    f.text((xs[3][0] + xs[3][1]) / 2, 144, "$dW_2 = h^{T}d\\,$logits", 11.5, "middle", INK2)
    f.text(330, 184, "反向（橙色箭头）：从 loss 往回，按链式法则逐个求梯度；每个节点下方是它的梯度公式", 12, "middle", ORANGE)
    f.text(330, 206, "最后一步得到所有参数（E、$W_1$、$b_1$、$W_2$、$b_2$）的梯度，用来更新参数", 11.5, "middle", INK2)
    save(f)


def ch02_curve():
    f = Fig("ch02_curve", 660, 255)
    steps = [0, 100, 1000, 5000, 10000, 20000, 30000, 40000, 50000, 60000]
    tr = [4.1944, 2.8709, 2.4273, 2.0724, 1.8728, 1.7099, 1.6250, 1.5637, 1.5499, 1.5360]
    va = [4.1962, 2.9147, 2.4681, 2.1429, 1.9850, 1.8560, 1.7980, 1.7482, 1.7380, 1.7266]
    c = Chart(f, 50, 24, 470, 170, (0, 60000), (1.4, 3.0))
    c.axes([0, 10000, 20000, 30000, 40000, 50000, 60000], [1.5, 2.0, 2.5, 3.0], xlabel="step",
           ylabel="loss", xfmt=lambda v: f"{int(v/1000)}k" if v else "0", yfmt=lambda v: f"{v:.1f}")
    c.hline(2.482, GRAY, "4 3", "bigram 计数 2.48", anchor="end")
    c.hline(1.770, GRAY, "4 3", "5-gram 计数 1.77", anchor="start", dy=-4)
    for s in (36000, 51000):
        c.vline(s, "#c8d1db", "2 3", None)
    f.text(c.X(36000) + 3, c.Y(2.85), "学习率 0.1 → 0.03", 10.5, "start", INK3)
    f.text(c.X(51000) + 3, c.Y(2.7), "→ 0.01", 10.5, "start", INK3)
    c.series(steps[1:], tr[1:], ORANGE)
    c.series(steps[1:], va[1:], BLUE)
    f.text(c.X(60000) + 6, c.Y(1.536) + 4, "训练集 1.54", 11.5, "start", INK)
    f.text(c.X(60000) + 6, c.Y(1.7266) - 2, "验证集 1.73", 11.5, "start", INK)
    legend(f, 300, 16, [("训练集", ORANGE, "line"), ("验证集", BLUE, "line")])
    f.text(330, 250, "两条曲线之间的差距就是过拟合；初始 loss 4.19（图上未画出）≈ ln 65", 11.5, "middle", INK2)
    save(f)


def ch02_context():
    f = Fig("ch02_context", 660, 235)
    c = Chart(f, 50, 26, 420, 170, (0.8, 20), (1.5, 2.6), xlog=True)
    c.axes([1, 2, 4, 8, 16], [1.6, 1.8, 2.0, 2.2, 2.4, 2.6], xlabel="上下文长度（字符，对数坐标）", ylabel="验证集 loss",
           xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}")
    ctx = [1, 2, 3, 4, 5, 6]
    ng = [2.488, 2.066, 1.796, 1.770, 2.007, 2.366]
    c.series(ctx, ng, ORANGE, markers=True)
    c.series([4, 8, 16], [1.711, 1.727, 1.821], BLUE, markers=True)
    f.text(c.X(6) + 8, c.Y(2.366) + 4, "n-gram 计数（第 1 章）", 11.5, "start", INK)
    f.text(c.X(16) + 8, c.Y(1.821) + 4, "MLP", 11.5, "start", INK)
    f.text(c.X(4) + 4, c.Y(1.711) + 18, "MLP，$K$ = 4：1.711", 11, "start", INK)
    legend(f, 300, 16, [("n-gram 计数", ORANGE, "dot"), ("MLP", BLUE, "dot")])
    f.text(522, 70, ["同样看 4 个字符，", "MLP 比计数法更好：", "没见过的上下文也", "能泛化。", "", "上下文再加长，MLP", "也开始变差：每个", "位置各用一套权重，", "数据被分散了"], 11.5, "start", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 3
def ch03_signal():
    f = Fig("ch03_signal", 660, 262)
    layers = [1, 2, 5, 10, 15, 20]
    act = {"std = 1": [0.962, 0.963, 0.963, 0.963, 0.962, 0.963],
           "std = 1/√n": [0.606, 0.470, 0.316, 0.224, 0.194, 0.156],
           "std = (5/3)/√n": [0.742, 0.684, 0.654, 0.651, 0.657, 0.648]}
    grad = {"std = 1": [6.2e2, 2.9e2, 2.3e1, 2.2e-1, 1.8e-3, 1.9e-5],
            "std = 1/√n": [5.2e-6, 6.3e-6, 9.2e-6, 1.3e-5, 1.7e-5, 1.9e-5],
            "std = (5/3)/√n": [1.1e-4, 1.0e-4, 7.9e-5, 4.8e-5, 3.1e-5, 1.9e-5]}
    cols = [ORANGE, GREEN, BLUE]
    c1 = Chart(f, 46, 30, 230, 160, (0, 21), (0, 1.0))
    c1.axes([1, 5, 10, 15, 20], [0, 0.25, 0.5, 0.75, 1.0], xlabel="第几层", ylabel="激活值的标准差（前向）",
            xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    c2 = Chart(f, 380, 30, 230, 160, (0, 21), (1e-6, 1e3), ylog=True)
    c2.axes([1, 5, 10, 15, 20], [1e-6, 1e-4, 1e-2, 1, 1e2], xlabel="第几层", ylabel="权重梯度的大小（反向，对数坐标）",
            xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"$10^{{{int(round(math.log10(v)))}}}$")
    for (k, col) in zip(act, cols):
        c1.series(layers, act[k], col, markers=True, r=3)
        c2.series(layers, grad[k], col, markers=True, r=3)
    legend(f, 110, 256, [("std = 1：85% 饱和，梯度爆炸", ORANGE, "line"), ("std = 1/√n：逐层变小", GREEN, "line"),
                         ("std = (5/3)/√n：稳定", BLUE, "line")])
    save(f)


def ch03_residual():
    f = Fig("ch03_residual", 660, 270)
    titles = ["普通层", "Post-norm 残差（2017 年原始 Transformer）", "Pre-norm 残差（现代标准）"]
    xs = [40, 250, 470]
    for k, x in enumerate(xs):
        f.text(x + 70, 18, titles[k] if k == 0 else titles[k].split("（")[0], 13, "middle", INK, 700)
        if k:
            f.text(x + 70, 34, "（" + titles[k].split("（")[1], 11, "middle", INK2)
        f.box(x + 40, 226, 60, 26, "$h_l$", "white", 13)
        f.box(x + 40, 44, 60, 26, "$h_{l+1}$", "white", 13)
    # plain
    x = xs[0]
    f.box(x + 30, 126, 80, 34, "$f$", "blue", 13)
    f.arrow(x + 70, 224, x + 70, 162, INK3)
    f.arrow(x + 70, 124, x + 70, 72, INK3)
    f.text(x + 70, 196, "梯度只能穿过 $f$", 11, "middle", INK2) if False else None
    # post-norm
    x = xs[1]
    f.box(x + 6, 150, 70, 30, "$f$", "blue", 13)
    f.circle(x + 70, 116, 11, "#ffffff", NAVY, 1.2)
    f.text(x + 70, 121, "+", 15, "middle", INK)
    f.box(x + 30, 80, 80, 24, "Norm", "orange", 12.5)
    f.poly([(x + 70, 224), (x + 70, 206), (x + 41, 206), (x + 41, 182)], INK3, 1.3, arrow=True)
    f.poly([(x + 41, 148), (x + 41, 116), (x + 57, 116)], INK3, 1.3, arrow=True)
    f.poly([(x + 70, 206), (x + 112, 206), (x + 112, 116), (x + 83, 116)], GREEN, 2.2, arrow=True)
    f.arrow(x + 70, 104, x + 70, 106, INK3)
    f.arrow(x + 70, 78, x + 70, 72, INK3)
    f.line(x + 70, 105, x + 70, 106, INK3)
    f.text(x + 118, 170, ["恒等路径", "也要穿过 Norm"], 11, "start", RED)
    # pre-norm
    x = xs[2]
    f.box(x + 6, 172, 70, 24, "Norm", "orange", 12.5)
    f.box(x + 6, 124, 70, 30, "$f$", "blue", 13)
    f.circle(x + 70, 92, 11, "#ffffff", NAVY, 1.2)
    f.text(x + 70, 97, "+", 15, "middle", INK)
    f.poly([(x + 70, 224), (x + 70, 210), (x + 41, 210), (x + 41, 198)], INK3, 1.3, arrow=True)
    f.arrow(x + 41, 170, x + 41, 156, INK3)
    f.poly([(x + 41, 122), (x + 41, 92), (x + 57, 92)], INK3, 1.3, arrow=True)
    f.poly([(x + 70, 210), (x + 112, 210), (x + 112, 92), (x + 83, 92)], GREEN, 2.2, arrow=True)
    f.arrow(x + 70, 80, x + 70, 72, INK3)
    f.text(x + 118, 150, ["恒等路径畅通：", "梯度可以原封", "不动地传回去"], 11, "start", GREEN)
    f.text(330, 266, "绿色：残差连接提供的恒等路径。$\\partial h_{l+1}/\\partial h_l = I + \\partial f/\\partial h_l$，其中的 $I$ 就来自这条路", 11.5, "middle", INK2)
    save(f)


def ch03_optim():
    import random
    f = Fig("ch03_optim", 660, 260)
    ADAM_LR = 0.13
    a, b = 1.0, 25.0                      # loss = 0.5*(a x^2 + b y^2): a narrow valley
    def grad(x, y):
        return a * x, b * y
    def run(kind, steps=40):
        x, y = -4.5, 1.2
        pts = [(x, y)]
        mx = my = vx = vy = 0.0
        for t in range(1, steps + 1):
            gx, gy = grad(x, y)
            if kind == "sgd":
                x, y = x - 0.075 * gx, y - 0.075 * gy
            elif kind == "mom":
                mx, my = 0.85 * mx + gx, 0.85 * my + gy
                x, y = x - 0.012 * mx, y - 0.012 * my
            else:
                mx, my = 0.9 * mx + 0.1 * gx, 0.9 * my + 0.1 * gy
                vx, vy = 0.999 * vx + 0.001 * gx * gx, 0.999 * vy + 0.001 * gy * gy
                mh = (mx / (1 - 0.9 ** t), my / (1 - 0.9 ** t))
                vh = (vx / (1 - 0.999 ** t), vy / (1 - 0.999 ** t))
                x, y = x - ADAM_LR * mh[0] / (math.sqrt(vh[0]) + 1e-8), y - ADAM_LR * mh[1] / (math.sqrt(vh[1]) + 1e-8)
            pts.append((x, y))
        return pts
    c = Chart(f, 30, 20, 440, 200, (-5, 1.5), (-1.6, 1.6))
    f.rect(c.x0, c.y0, c.w, c.h, "#fbfcfd", AXIS, 1)
    for lv in [0.5, 2, 5, 10, 16]:
        rx, ry = math.sqrt(2 * lv / a), math.sqrt(2 * lv / b)
        pts = [(c.X(rx * math.cos(t / 60 * 2 * math.pi)), c.Y(ry * math.sin(t / 60 * 2 * math.pi))) for t in range(61)]
        f.poly([(px, py) for px, py in pts if c.x0 <= px <= c.x0 + c.w], GRID, 1)
    f.circle(c.X(0), c.Y(0), 4, INK, "#ffffff", 1)
    f.text(c.X(0) + 8, c.Y(0) + 16, "最低点", 11, "start", INK2)
    for kind, col in (("sgd", ORANGE), ("mom", GREEN), ("adam", BLUE)):
        pts = run(kind)
        c.series([p[0] for p in pts], [p[1] for p in pts], col, 1.6, markers=False)
        c.dots([p[0] for p in pts[::4]], [p[1] for p in pts[::4]], col, 2.6)
    f.text(490, 40, "40 步之后：", 12, "start", INK, 700)
    legend(f, 490, 64, [("SGD：在陡的方向来回震荡，", ORANGE, "line")], horizontal=False)
    f.text(513, 80, "平缓的方向走得很慢", 11.5, "start", INK)
    legend(f, 490, 104, [("动量：震荡被平均掉", GREEN, "line")], horizontal=False)
    legend(f, 490, 128, [("Adam：每个方向的步长", BLUE, "line")], horizontal=False)
    f.text(513, 144, "按梯度的典型大小归一化，", 11.5, "start", INK)
    f.text(513, 160, "两个方向同样快", 11.5, "start", INK)
    f.text(250, 250, "示意：一个“狭长山谷”形状的二次函数，竖直方向比水平方向陡 25 倍；椭圆是等高线", 11.5, "middle", INK2)
    save(f)


def ch03_sched():
    f = Fig("ch03_sched", 660, 250)
    T = 1000
    def cosine(t):
        if t < 50:
            return t / 50
        p = (t - 50) / (T - 50)
        return 0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * p))
    def wsd(t):
        if t < 50:
            return t / 50
        if t < 800:
            return 1.0
        return 1.0 - 0.9 * (t - 800) / 200
    c = Chart(f, 50, 24, 470, 160, (0, T), (0, 1.1))
    c.axes([0, 250, 500, 750, 1000], [0, 0.5, 1.0], xlabel="训练进度（步）", ylabel="学习率 / 峰值",
           xfmt=lambda v: f"{v / 10:g}%", yfmt=lambda v: f"{v:g}")
    ts = list(range(0, T + 1, 5))
    c.series(ts, [0.6] * len(ts), GRAY, 1.5, "5 4")
    c.series(ts, [cosine(t) for t in ts], BLUE)
    c.series(ts, [wsd(t) for t in ts], ORANGE)
    f.text(c.X(1000) + 6, c.Y(0.1) + 4, "warmup + cosine", 11.5, "start", INK)
    f.text(c.X(1000) + 6, c.Y(0.1) + 20, "WSD（两者都降到 10%）", 11.5, "start", INK)
    f.text(c.X(25), c.Y(1.05), "warmup", 11, "start", INK2)
    f.text(c.X(420), c.Y(1.06), "WSD 的稳定阶段", 11, "middle", INK2)
    f.text(c.X(900), c.Y(1.06), "快速衰减", 11, "middle", INK2)
    legend(f, 290, 16, [("warmup + cosine", BLUE, "line"), ("WSD", ORANGE, "line"), ("恒定", GRAY, "dash")])
    f.text(300, 244, "示意：warmup 占 5%，WSD 在最后 20% 衰减", 11.5, "middle", INK2)
    save(f)


def ch03_accum():
    f = Fig("ch03_accum", 660, 230)
    f.text(10, 20, "梯度累积：显存一次只放得下一个 micro-batch", 12.5, "start", INK, 700)
    for k in range(4):
        x = 10 + k * 90
        f.box(x, 36, 80, 30, f"micro-batch {k + 1}", "white", 11.5)
        f.arrow(x + 40, 68, x + 40, 92, GRAY)
        f.box(x, 94, 80, 26, "前向 + 反向", "blue", 11.5)
        f.arrow(x + 40, 122, x + 40, 146, GRAY)
    f.rect(10, 148, 350, 28, ORANGE_L, ORANGE, 1.2, 4)
    f.text(185, 166, "梯度加起来（累积在 .grad 里）", 12, "middle", INK)
    f.arrow(185, 178, 185, 198)
    f.box(110, 200, 150, 26, "优化器更新一次", "Orange", 12)
    # clipping panel
    cx, cy, r = 530, 130, 60
    f.text(430, 20, "梯度裁剪：方向不变，长度截到阈值", 12.5, "start", INK, 700)
    f.circle(cx, cy, r, "#f4f8fc", BLUE, 1)
    f.text(cx - r + 4, cy + r - 8, "‖g‖ = 1.0", 11, "start", BLUE)
    ang = math.radians(32)
    L = 112
    f.arrow(cx, cy, cx + L * math.cos(ang), cy - L * math.sin(ang), RED, 1.6, "5 4")
    f.text(cx + L * math.cos(ang) - 4, cy - L * math.sin(ang) - 6, "原始梯度（范数 1.9）", 11, "end", RED)
    f.arrow(cx, cy, cx + r * math.cos(ang), cy - r * math.sin(ang), GREEN, 2.4)
    f.text(cx + r * math.cos(ang) + 8, cy - r * math.sin(ang) + 20, "裁剪后", 11.5, "start", GREEN)
    f.circle(cx, cy, 2.5, INK)
    save(f)


# ----------------------------------------------------------------- chapter 4
def ch04_cpugpu():
    f = Fig("ch04_cpugpu", 660, 230)
    f.text(110, 18, "CPU：少量强大的核心", 12.5, "middle", INK, 700)
    f.rect(10, 28, 200, 150, GRAY_L, GRAY, 1, 6)
    for k in range(4):
        x, y = 22 + (k % 2) * 92, 40 + (k // 2) * 66
        f.box(x, y, 84, 56, "核心", "blue", 12, sub="复杂控制", sub_size=10.5)
    f.text(110, 196, "优化延迟：一串指令尽快跑完", 11.5, "middle", INK2)
    f.text(440, 18, "GPU（H100）：132 个 SM，每个 SM 里 4 个 Tensor Core", 12.5, "middle", INK, 700)
    f.rect(240, 28, 400, 150, GRAY_L, GRAY, 1, 6)
    for i in range(12):
        for j in range(5):
            x, y = 250 + i * 32.5, 38 + j * 22
            f.rect(x, y, 29, 18, BLUE_L, BLUE, 0.8, 2)
            for q in range(4):
                f.rect(x + 2 + q * 6.6, y + 9, 5.2, 6.5, ORANGE, "none", 0, 1)
    f.rect(250, 152, 380, 18, BLUE_M, "none", 0, 2)
    f.text(440, 165, "L2 缓存 50 MB，显存 80 GB", 11, "middle", INK)
    f.text(440, 196, "优化吞吐量：海量数据同时做同样的运算", 11.5, "middle", INK2)
    legend(f, 250, 222, [("SM（流式多处理器）", BLUE_L, "box"), ("Tensor Core：专做小矩阵乘加", ORANGE, "box")])
    save(f)


def ch04_memhier():
    f = Fig("ch04_memhier", 660, 250)
    levels = [("寄存器", "每个 SM 256 KB", "最快"), ("共享内存 / L1", "每个 SM ≤ 256 KB", "数十 TB/s"),
              ("L2 缓存", "50 MB", "介于两者之间"), ("HBM（显存）", "80 GB", "3.35 TB/s"),
              ("NVLink → 同机其他 GPU", "", "900 GB/s"), ("PCIe → CPU 内存", "", "约 64 GB/s"),
              ("InfiniBand → 其他机器", "", "每块网卡 50 GB/s")]
    cols = [BLUE, BLUE, "#3d7ab3", "#5b8fc2", GRAY, GRAY, GRAY]
    top, H = 20, 30
    for k, (name, cap, bw) in enumerate(levels):
        y = top + k * H
        half = 34 + k * 23
        cx = 210
        f.rect(cx - half, y, 2 * half, H - 4, cols[k] if k < 4 else GRAY_L, "none" if k < 4 else GRAY, 1, 2)
        f.text(cx, y + 17, name, 11.5, "middle", "#ffffff" if k < 4 else INK)
        f.text(420, y + 17, cap, 11.5, "start", INK2)
        f.text(545, y + 17, bw, 11.5, "start", INK)
    f.text(420, 12, "容量", 11.5, "start", INK3)
    f.text(545, 12, "带宽", 11.5, "start", INK3)
    f.line(12, 26, 12, 228, INK3, 1.2, arrow=True)
    f.text(20, 240, "越往下：越大、越慢、越远", 11.5, "start", INK2)
    f.line(400, 138, 650, 138, RED, 1, "4 3")
    f.text(420, 157, "以下在 GPU 芯片之外", 10.5, "start", RED)
    save(f)


def ch04_batch():
    f = Fig("ch04_batch", 660, 258)
    B = [1, 8, 32, 128, 512]
    per = [26.5, 16.5, 5.9, 2.4, 1.6]
    flops = [20.3, 32.5, 90.4, 228.9, 331.8]
    c1 = Chart(f, 50, 30, 230, 160, (0.7, 800), (1, 40), xlog=True, ylog=True)
    c1.axes(B, [1, 2, 5, 10, 20, 40], xlabel="batch 大小 $B$", ylabel="每个 token 的耗时（ms）",
            xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    c1.series(B, per, BLUE, markers=True)
    f.text(c1.X(1) + 8, c1.Y(26.5) + 4, "26.5", 11, "start", INK)
    f.text(c1.X(512), c1.Y(1.6) - 10, "1.6", 11, "middle", INK)
    c2 = Chart(f, 380, 30, 230, 160, (0.7, 800), (10, 600), xlog=True, ylog=True)
    c2.axes(B, [10, 30, 100, 300], xlabel="batch 大小 $B$", ylabel="实测算力（GFLOP/s）",
            xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    xs = [0.7 * 1.15 ** i for i in range(60)]
    xs = [x for x in xs if x <= 800]
    roof = [min(399, 0.5 * x * 40 / 1.0) for x in xs]
    c2.series(xs, roof, GRAY, 1.4, "5 4")
    c2.series(B, flops, ORANGE, markers=True)
    f.text(c2.X(20), c2.Y(399) - 8, "roofline：min(399, $B$ × 0.5 × 40 GB/s)", 10.5, "middle", INK2)
    f.text(330, 252, "实验 B：$B$ 个 token 共用一次 1 GB 权重的读取。$B$ 小时受限于内存，每个 token 的成本随 $B$ 增大而下降", 11.5, "middle", INK2)
    save(f)


def ch04_fusion():
    f = Fig("ch04_fusion", 660, 250)
    f.text(10, 18, "不融合：每个运算都把结果写回显存，下一个运算再读出来", 12.5, "start", INK, 700)
    ops = ["矩阵乘 $xW$", "加偏置", "GELU"]
    for k, op in enumerate(ops):
        x = 30 + k * 200
        f.box(x, 34, 110, 30, op, "orange", 12)
        f.arrow(x + 40, 66, x + 40, 98, RED, 1.3)
        if k < 2:
            f.poly([(x + 80, 98), (x + 80, 82), (x + 230, 82), (x + 230, 66)], RED, 1.3, arrow=True)
    f.rect(10, 100, 640, 26, BLUE_L, BLUE, 1, 3)
    f.text(330, 118, "HBM（显存）：写 3 次、读 2 次中间结果", 12, "middle", INK)
    y = 150
    f.text(10, y, "融合：一个 kernel 做完三件事，中间结果留在片上（寄存器 / SRAM）", 12.5, "start", INK, 700)
    f.rect(30, y + 14, 520, 40, GREEN_L, GREEN, 1.2, 6)
    for k, op in enumerate(ops):
        f.box(46 + k * 170, y + 20, 130, 28, op, "white", 12)
        if k < 2:
            f.arrow(178 + k * 170, y + 34, 214 + k * 170, y + 34, GREEN)
    f.arrow(500, y + 56, 500, y + 74, BLUE, 1.3)
    f.rect(10, y + 76, 640, 24, BLUE_L, BLUE, 1, 3)
    f.text(330, y + 93, "HBM：只写 1 次最终结果", 12, "middle", INK)
    save(f)


def ch04_batching():
    f = Fig("ch04_batching", 660, 258)
    W, BWt, F = 140e9, 26.8e12, 8 * 989e12
    def tput(B):
        t = max(W / BWt, 2 * 70e9 * B / F)
        return B / t
    c = Chart(f, 60, 26, 440, 170, (1, 4096), (100, 3e5), xlog=True, ylog=True)
    c.axes([1, 4, 16, 64, 256, 1024, 4096], [1e2, 1e3, 1e4, 1e5], xlabel="batch 大小 $B$（同时生成的序列数）",
           ylabel="总吞吐量（token/s）", xfmt=lambda v: f"{v:g}", yfmt=lambda v: {100: "100", 1000: "1K", 1e4: "10K", 1e5: "100K"}[v])
    xs = [2 ** (i / 4) for i in range(0, 49)]
    c.series(xs, [tput(x) for x in xs], BLUE)
    knee = 295 * 1.0
    c.vline(F / BWt * 140e9 / (2 * 70e9) / 1.0 * 1.0 / 1.0 if False else 295, GRAY, "4 3", "约 295：变成计算受限", dy=160, dx=6)
    f.text(c.X(1.2), c.Y(700), "$B$ = 1：约 190 token/s", 11, "start", INK)
    f.text(c.X(64) - 6, c.Y(tput(64)) - 10, "$B$ = 64：约 1.2 万", 11, "end", INK)
    f.text(520, 80, ["受限于读权重时，", "多加一条序列几乎", "不增加耗时，吞吐量", "随 $B$ 线性增长；", "变成计算受限后", "就不再增长"], 11.5, "start", INK2)
    f.text(330, 252, "估算：70B 模型（BF16）分到 8 张 H100 上，忽略 KV cache（第 33 章会把它加进来）", 11.5, "middle", INK2)
    save(f)


if __name__ == "__main__":
    for fn in [ch02_onehot, ch02_xor, ch02_matgrad, ch02_backflow, ch02_curve, ch02_context, ch03_signal,
               ch03_residual, ch03_optim, ch03_sched, ch03_accum, ch04_cpugpu, ch04_memhier, ch04_batch,
               ch04_fusion, ch04_batching]:
        fn()
    print("ok2")
