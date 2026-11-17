"""Figures for Part 8-9 (chapters 32-39). Run: python3 figs/p7.py"""
import json, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import *

OUT = os.path.dirname(os.path.abspath(__file__))


def save(f):
    f.save(os.path.join(OUT, f.name + ".svg"))


def shade(t, a=(0xe8, 0xef, 0xf6), b=(0x1c, 0x5d, 0x99)):
    t = max(0.0, min(1.0, t))
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ----------------------------------------------------------------- chapter 32
def ch32_superpos():
    f = Fig("ch32_superpos", 660, 262)
    cx, cy, r = 120, 132, 76
    f.text(cx, 18, "2 维空间里放 5 个特征方向", 12, "middle", INK, 700)
    f.line(cx - r - 10, cy, cx + r + 10, cy, GRID, 1)
    f.line(cx, cy - r - 10, cx, cy + r + 10, GRID, 1)
    names = ["引用", "韩文", "HTTP", "诗歌", "代码"]
    cols = [BLUE, ORANGE, GREEN, PURPLE, RED]
    for k in range(5):
        a = math.pi / 2 + 2 * math.pi * k / 5
        x2, y2 = cx + r * math.cos(a), cy - r * math.sin(a)
        f.arrow(cx, cy, x2, y2, cols[k], 2)
        f.text(cx + (r + 16) * math.cos(a), cy - (r + 16) * math.sin(a) + 4, names[k], 10.5, "middle", cols[k])
    f.text(cx, 234, ["方向之间不正交，会互相干扰；", "但特征很稀疏，很少同时出现"], 10.5, "middle", INK2)
    rnd = random.Random(1)
    c = Chart(f, 300, 34, 250, 160, (-1, 1), (0, 1.05))
    c.axes([-1, -0.5, 0, 0.5, 1], [], xlabel="两个随机方向的余弦相似度", ylabel=None, xfmt=lambda v: f"{v:g}", size=11)
    f.text(c.x0 + c.w / 2, 18, "维度越高，随机方向越接近正交", 12, "middle", INK, 700)
    for d, col in ((2, ORANGE), (16, BLUE_M), (128, BLUE)):
        bins = [0] * 40
        for _ in range(20000):
            u = [rnd.gauss(0, 1) for _ in range(d)]
            v = [rnd.gauss(0, 1) for _ in range(d)]
            cs = sum(a * b for a, b in zip(u, v)) / math.sqrt(sum(a * a for a in u) * sum(b * b for b in v))
            bins[min(39, int((cs + 1) * 20))] += 1
        m = max(bins)
        xs = [-1 + (i + 0.5) / 20 for i in range(40)]
        c.series(xs, [b / m for b in bins], col, 2)
    legend(f, 566, 60, [("$d$ = 2", ORANGE, "line"), ("$d$ = 16", BLUE_M, "line"), ("$d$ = 128", BLUE, "line")], horizontal=False, size=11, gap=22)
    f.text(566, 140, ["$d$ = 128 时", "标准差约 0.09"], 10.5, "start", INK2)
    f.text(425, 256, "右：随机抽样 2 万对方向的分布（纵轴按各自最大值归一化）", 10.5, "middle", INK3)
    save(f)


def ch32_sae():
    f = Fig("ch32_sae", 660, 206)
    f.box(10, 36, 80, 70, ["激活 $x$", "128 维"], "white", 11)
    f.arrow(92, 71, 120, 71)
    f.box(122, 48, 80, 46, ["编码器", "+ ReLU"], "blue", 11)
    f.arrow(204, 71, 232, 71)
    rnd = random.Random(5)
    on = set(rnd.sample(range(48), 5))
    for i in range(48):
        x = 236 + (i % 24) * 9.5
        y = 42 + (i // 24) * 30
        f.rect(x, y, 7.5, 26, ORANGE if i in on else GRAY_L, "none", 0, 1)
    f.text(236 + 114, 116, "特征 $f$：1,024 个，大多数为 0", 10.5, "middle", INK2)
    f.arrow(468, 71, 496, 71)
    f.box(498, 48, 66, 46, ["解码器", "（字典）"], "blue", 11)
    f.arrow(566, 71, 584, 71)
    f.box(586, 36, 64, 70, ["重建 $\\hat x$", "128 维"], "white", 11)
    f.text(330, 150, "loss = $\\lVert x - \\hat x\\rVert^{2}$（重建得准）+ $\\lambda\\sum\\lvert f_i\\rvert$（足够稀疏）", 12, "middle", INK)
    f.text(330, 176, "第 6 章小 GPT 上的实测：$\\lambda$ = 3e-3 时方差解释 97.5%、L0 = 128；$\\lambda$ = 3e-2 时 73.5%、L0 = 13.8", 11, "middle", INK2)
    f.text(330, 196, "两者不可兼得", 11, "middle", INK2)
    save(f)


def ch32_steer():
    f = Fig("ch32_steer", 660, 230)
    sets = ["不干预", "加特征 148", "加特征 352"]
    cols = [GRAY, ORANGE, BLUE]
    for p, (title, vals, fmt, ymax) in enumerate((("每 600 个字符中的破折号数", [0.2, 9.2, 0.0], "{:g}", 10),
                                                  ("字母中大写字母的比例", [9.8, 8.7, 15.0], "{:g}%", 16))):
        c = Chart(f, 70 + p * 320, 36, 220, 140, (0, 3), (0, ymax))
        c.axes([], [0, ymax / 2, ymax], yfmt=lambda v: f"{v:g}", size=11)
        f.text(c.x0 + c.w / 2, 18, title, 12, "middle", INK, 700)
        for i, v in enumerate(vals):
            c.bar(c.X(i + 0.5), max(v, ymax * 0.005), 40, cols[i])
            f.text(c.X(i + 0.5), c.Y(v) - 6, fmt.format(v), 11, "middle", INK, 700 if i == p + 1 else None)
            f.text(c.X(i + 0.5), c.Y(0) + 16, sets[i], 10.5, "middle", INK2)
    f.text(330, 216, "32.6 节的干预实验（实测）：特征 148 是“句末破折号”，特征 352 是“正在写说话人名字”", 11.5, "middle", INK2)
    save(f)


def ch32_induction():
    f = Fig("ch32_induction", 660, 196)
    toks = ["…", "Mr", "Dur", "sley", "said", "…", "…", "Mr", "Dur", "?"]
    x0, w = 30, 60
    for i, t in enumerate(toks):
        st = "orange" if t == "Dur" else ("green" if t == "sley" else "white")
        if i == 9:
            st = "Blue"
        f.box(x0 + i * w, 110, 50, 28, t, st, 12)
    a, b = x0 + 2 * w + 25, x0 + 8 * w + 25
    f.path(f"M{b},108 C{b},40 {a},40 {a},108", ORANGE, 1.6, "5 3", arrow=True)
    f.text((a + b) / 2, 48, "① 在前文中找到和当前 token 相同的位置（Dur）", 11, "middle", ORANGE)
    s = x0 + 3 * w + 25
    f.path(f"M{s},140 C{s},176 {x0 + 9 * w + 25},176 {x0 + 9 * w + 25},140", GREEN, 1.6, arrow=True)
    f.text((s + x0 + 9 * w + 25) / 2, 190, "② 把它的下一个 token（sley）复制过来作为预测", 11, "middle", GREEN)
    f.text(10, 20, "归纳头：[A][B] … [A] → 预测 [B]（示意）", 12, "start", INK, 700)
    save(f)


# ----------------------------------------------------------------- chapter 33
def ch33_phases():
    f = Fig("ch33_phases", 660, 222)
    f.text(10, 18, "Prefill：提示词的 8 个 token 一次并行处理", 12, "start", INK, 700)
    for i in range(8):
        f.rect(20 + i * 22, 30, 19, 24, BLUE_M, "none", 0, 2)
    f.rect(16, 26, 180, 32, "none", BLUE, 1.4, 4)
    f.arrow(200, 42, 228, 42)
    f.box(230, 28, 150, 28, "大矩阵乘法：受限于算力", "blue", 10.5)
    f.text(10, 92, "Decode：每一步只生成 1 个 token，但每步都要读一遍全部权重和 KV cache", 12, "start", INK, 700)
    for s in range(5):
        x = 20 + s * 126
        for i in range(8):
            f.rect(x + i * 9, 104, 7.5, 18, GRAY_L, "none", 0, 1)
        for j in range(s):
            f.rect(x + 72 + j * 9, 104, 7.5, 18, ORANGE_M, "none", 0, 1)
        f.rect(x + 72 + s * 9, 104, 7.5, 18, ORANGE, "none", 0, 1)
        f.text(x + 50, 140, f"第 {s + 1} 步", 10.5, "middle", INK2)
    a, b, c = 16, 20 + 72 + 7.5, 20 + 126 + 72 + 9 + 7.5
    for xx in (a, b, c):
        f.line(xx, 158, xx, 178, INK3, 1)
    f.line(a, 168, b, 168, INK3, 1, arrow=True, arrow_start=True)
    f.text((a + b) / 2, 192, "TTFT", 11, "middle", INK, 700)
    f.line(b, 168, c, 168, INK3, 1, arrow=True, arrow_start=True)
    f.text((b + c) / 2, 192, "TPOT", 11, "middle", INK, 700)
    f.text(c + 10, 172, "TTFT：等到第一个 token；TPOT：之后每个 token 的间隔", 10.5, "start", INK2)
    f.text(330, 214, "灰色：缓存里已有的 K、V；橙色：本步新生成的 token。示意", 11, "middle", INK3)
    save(f)


def ch33_kvspeed():
    f = Fig("ch33_kvspeed", 660, 240)
    n = [128, 256, 512, 960]
    no = [1.17, 3.27, 13.0, 50.0]
    yes = [0.28, 0.58, 1.56, 2.61]
    c = Chart(f, 60, 26, 400, 160, (0, 1000), (0, 52))
    c.axes([0, 250, 500, 750, 1000], [0, 10, 20, 30, 40, 50], xlabel="生成的 token 数 $n$", ylabel="耗时（秒）", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", size=11)
    c.series(n, no, RED, 2.2, markers=True)
    c.series(n, yes, GREEN, 2.2, markers=True)
    f.text(c.X(960) - 10, c.Y(50) + 4, "不用缓存：随 $n^{2}$ 增长", 11, "end", RED)
    f.text(c.X(960), c.Y(2.61) - 10, "KV cache：近似线性", 11, "end", GREEN)
    f.text(480, 60, ["加速倍数：", "128 → 4.2 倍", "256 → 5.7 倍", "512 → 8.3 倍", "960 → 19.1 倍"], 11, "start", INK2)
    f.text(330, 234, "33.2 节的实验（实测，数据同上表）：生成得越长，差距越大", 11.5, "middle", INK2)
    save(f)


def ch33_batching():
    f = Fig("ch33_batching", 660, 232)
    lens = [6, 3, 9, 4]
    new = [5, 7, 3]
    u = 21
    def lane_box(y, x, w, col, txt=""):
        f.rect(130 + x * u, y, w * u - 2, 20, col, "none", 0, 3)
        if txt:
            f.text(130 + x * u + (w * u - 2) / 2, y + 14, txt, 10, "middle", "#ffffff")
    f.text(10, 18, "静态 batching：等整批都结束才换下一批", 11.5, "start", INK, 700)
    cols = [BLUE, ORANGE, GREEN, PURPLE]
    for i, L in enumerate(lens):
        y = 28 + i * 24
        f.text(122, y + 14, f"槽位 {i}", 10.5, "end", INK2)
        lane_box(y, 0, L, cols[i], f"请求 {i + 1}")
        if L < 9:
            f.rect(130 + L * u, y, (9 - L) * u - 2, 20, "#f1f4f7", "#d5dde5", 1, 3)
    f.text(130 + 9 * u + 6, 70, "空等", 10.5, "start", INK3)
    f.text(10, 140, "continuous batching：每一步都可以换人", 11.5, "start", INK, 700)
    starts = [[(0, 6, 0), (6, 5, 4)], [(0, 3, 1), (3, 7, 5)], [(0, 9, 2)], [(0, 4, 3), (4, 3, 6)]]
    cols2 = [BLUE, ORANGE, GREEN, PURPLE, "#3d6f9e", "#a0620a", "#55407a"]
    for i, segs in enumerate(starts):
        y = 150 + i * 18
        f.text(122, y + 12, f"槽位 {i}", 10, "end", INK2)
        for x, w, k in segs:
            f.rect(130 + x * u, y, w * u - 2, 15, cols2[k], "none", 0, 3)
            f.text(130 + x * u + (w * u - 2) / 2, y + 11.5, f"请求 {k + 1}", 9, "middle", "#ffffff")
    f.text(130 + 11 * u + 6, 186, ["结束的请求立刻离开，", "新请求立刻加入；", "GPU 几乎不空闲（示意）"], 10.5, "start", INK2)
    save(f)


def ch33_paged():
    f = Fig("ch33_paged", 660, 236)
    f.text(10, 18, "两条序列（同一个提示，各自采样不同的回答）", 11.5, "start", INK, 700)
    seqA = [("提示 0–15", 0), ("提示 16–31", 1), ("回答 A", 2)]
    seqB = [("提示 0–15", 0), ("提示 16–31", 1), ("回答 B", 3)]
    phys = {0: 5, 1: 2, 2: 7, 3: 0}
    for r, (name, blocks, col) in enumerate((("序列 A 的逻辑块", seqA, BLUE), ("序列 B 的逻辑块", seqB, ORANGE))):
        y = 36 + r * 90
        f.text(10, y + 18, name, 11, "start", INK)
        for k, (lab, lb) in enumerate(blocks):
            x = 120 + k * 76
            f.box(x, y, 70, 28, lab, "blue" if lb < 2 else ("Blue" if lb == 2 else "Orange"), 10)
            f.text(x + 35, y + 42, f"→ 物理块 {phys[lb]}", 9.5, "middle", INK2)
    f.text(470, 18, "显存中的物理块（每块 16 个 token）", 11.5, "middle", INK, 700)
    owner = {5: ("共享", BLUE_M), 2: ("共享", BLUE_M), 7: ("A", BLUE), 0: ("B", ORANGE)}
    for p in range(8):
        x, y = 360 + (p % 4) * 58, 36 + (p // 4) * 64
        lab, col = owner.get(p, ("空闲", "#f1f4f7"))
        f.rect(x, y, 52, 46, col, "#d5dde5" if lab == "空闲" else "none", 1, 4)
        f.text(x + 26, y + 20, f"块 {p}", 10.5, "middle", "#ffffff" if lab in ("A", "B") else INK)
        f.text(x + 26, y + 36, lab, 10, "middle", "#ffffff" if lab in ("A", "B") else INK2)
    f.text(330, 200, "块表把逻辑位置映射到不连续的物理块；用到才分配，浪费不到 4%；", 11.5, "middle", INK2)
    f.text(330, 218, "相同的提示前缀只存一份，谁要修改才复制（写时复制）。示意", 11.5, "middle", INK2)
    save(f)


def ch33_cost():
    f = Fig("ch33_cost", 660, 276)
    Bs = [1 * 2 ** (i / 8) for i in range(70)]
    Bs = [b for b in Bs if b <= 380]
    step = lambda b: (140 + b * 1.31) / 26.8
    c = Chart(f, 64, 30, 230, 160, (1, 400), (0, 16000), xlog=True)
    c.axes([1, 4, 16, 64, 256], [0, 4000, 8000, 12000, 16000], xlabel="batch 大小 $B$（对数坐标）", ylabel="总吞吐量（token/秒）", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:,.0f}", size=10.5)
    c.series(Bs, [b / step(b) * 1000 for b in Bs], BLUE, 2.2)
    c.vline(380, RED, "4 3", None)
    f.text(c.X(380) - 4, c.Y(2500), ["显存", "上限", "≈ 380"], 10, "end", RED)
    c2 = Chart(f, 400, 30, 230, 160, (1, 400), (0, 200), xlog=True)
    c2.axes([1, 4, 16, 64, 256], [0, 50, 100, 150, 200], xlabel="batch 大小 $B$（对数坐标）", ylabel="每条序列的速度（token/秒）", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", size=10.5)
    c2.series(Bs, [1000 / step(b) for b in Bs], ORANGE, 2.2)
    for b in (1, 32, 64, 256):
        c.dots([b], [b / step(b) * 1000], BLUE, 3.6)
        c2.dots([b], [1000 / step(b)], ORANGE, 3.6)
    f.text(c.X(1.2), c.Y(1500), "$B$ = 1：约 29 美元 / 百万 token", 10, "start", INK2)
    f.text(c.X(150), c.Y(14433) + 4, "$B$ = 256：约 0.38 美元", 10, "end", INK2)
    f.text(330, 252, "Llama 3 70B、8 张 H100、每条 4K 上下文：每步耗时 ≈（140 GB 权重 + $B$ × 1.31 GB KV cache）÷ 26.8 TB/s", 11, "middle", INK2)
    f.text(330, 270, "（估算，数据同上表）。吞吐量和每个用户的速度此消彼长", 11, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 34
def ch34_quant():
    f = Fig("ch34_quant", 660, 250)
    rows = [("FP32", 32, 1.8894), ("INT8 每通道", 8, 1.8895), ("INT4 每通道", 4, 1.9077), ("INT4 每 32 个一组", 4.5, 1.8984),
            ("INT3 每通道", 3, 1.9726), ("INT3 每 32 个一组", 3.5, 1.9330)]
    c = Chart(f, 160, 20, 380, 168, (1.88, 1.98), (0, len(rows)))
    for t in [1.88, 1.90, 1.92, 1.94, 1.96, 1.98]:
        f.line(c.X(t), c.y0, c.X(t), c.y0 + c.h, GRID, 1)
        f.text(c.X(t), c.y0 + c.h + 16, f"{t:.2f}", 10.5, "middle", INK2)
    f.text(c.x0 + c.w / 2, c.y0 + c.h + 34, "验证集 loss（越低越好）", 11, "middle", INK2)
    for i, (lab, bits, loss) in enumerate(rows):
        yc = c.y0 + (i + 0.5) * c.h / len(rows)
        f.text(c.x0 - 8, yc + 4, lab, 11, "end", INK)
        col = GRAY if i == 0 else (GREEN if "组" in lab else BLUE)
        f.rect(c.x0, yc - 10, c.X(loss) - c.x0, 20, col, "none", 0, 2)
        f.text(c.X(loss) + 6, yc + 4, f"{loss:.4f}", 10.5, "start", INK)
        f.text(650, yc + 4, f"{bits:g} 位", 10.5, "end", INK2)
    f.text(650, 14, "每个权重", 10, "end", INK3)
    f.text(330, 244, "34.1 节量化实验（实测，数据同上表）：绿色是分组量化，挽回了大部分损失", 11.5, "middle", INK2)
    save(f)


def ch34_spec():
    f = Fig("ch34_spec", 660, 214)
    f.text(10, 18, "① 草稿模型（便宜）连续猜 $\\gamma$ = 4 个 token", 11.5, "start", INK, 700)
    ctx = ["To", " be", ","]
    draft = [" or", " not", " to", " go"]
    x = 20
    for t in ctx:
        f.box(x, 30, 44, 26, t.replace(" ", "␣"), "white", 11)
        x += 48
    xs = []
    for t in draft:
        f.box(x, 30, 50, 26, t.replace(" ", "␣"), "orange", 11)
        xs.append(x)
        x += 54
    f.text(10, 84, "② 大模型调用一次，同时检查这 4 个位置", 11.5, "start", INK, 700)
    marks = ["✓", "✓", "✓", "✗"]
    for k, xx in enumerate(xs):
        ok = marks[k] == "✓"
        f.box(xx, 94, 50, 26, marks[k], "Green" if ok else "Red", 12)
    f.text(10, 148, "③ 接受前 3 个；第 4 个位置按 normalize(max(0, $p - q$)) 重新采样", 11.5, "start", INK, 700)
    x = 20
    for t in ctx + draft[:3]:
        f.box(x, 158, 44 if t in ctx else 50, 26, t.replace(" ", "␣"), "white" if t in ctx else "green", 11)
        x += 48 if t in ctx else 54
    f.box(x, 158, 50, 26, "␣be", "Blue", 11)
    f.text(x + 60, 176, "← 一次大模型调用，得到 4 个 token", 11, "start", INK2)
    f.text(330, 208, "接受的规则保证输出分布与直接用大模型采样完全相同（示意）", 11, "middle", INK3)
    save(f)


def ch34_gamma():
    f = Fig("ch34_gamma", 660, 262)
    c = Chart(f, 60, 26, 400, 170, (0, 10), (1, 7.5))
    c.axes([0, 2, 4, 6, 8, 10], [1, 2, 3, 4, 5, 6, 7], xlabel="草稿长度 $\\gamma$", ylabel="每次大模型调用产生的 token 数 $E$", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", size=11)
    gs = [i / 10 for i in range(101)]
    for a, col in ((0.58, BLUE_M), (0.8, BLUE), (0.9, NAVY)):
        ys = [(1 - a ** (g + 1)) / (1 - a) for g in gs]
        c.series(gs, ys, col, 2)
        f.text(c.X(10) + 6, c.Y(ys[-1]) + 4, f"$\\alpha$ = {a:g}" + (f"（上限 {1 / (1 - a):g}）" if a > 0.6 else ""), 11, "start", col)
    c.dots([2, 4, 8], [1.89, 2.24, 2.40], ORANGE, 4.4)
    f.text(c.X(5), c.Y(2.24) + 24, "圆点：实测，bigram 草稿（接受率约 0.58）", 11, "start", ORANGE)
    f.text(330, 256, "期望加速 $E = (1 - \\alpha^{\\gamma+1})/(1 - \\alpha)$：$\\gamma$ 越大收益越递减；草稿越准（$\\alpha$ 越大），上限越高", 11, "middle", INK2)
    save(f)


def ch34_disagg():
    f = Fig("ch34_disagg", 660, 200)
    f.box(10, 70, 90, 50, ["新请求", "（长提示）"], "white", 11)
    f.arrow(102, 95, 130, 95)
    f.rect(132, 40, 170, 110, BLUE_L, BLUE, 1.4, 6)
    f.text(217, 60, "Prefill 集群", 12, "middle", INK, 700)
    f.text(217, 78, "受限于算力；保证 TTFT", 10.5, "middle", INK2)
    for i in range(6):
        f.rect(150 + (i % 3) * 46, 90 + (i // 3) * 26, 40, 20, BLUE, "none", 0, 3)
    f.arrow(304, 95, 376, 95, ORANGE, 2)
    f.text(340, 86, "KV cache", 10.5, "middle", ORANGE, 700)
    f.text(340, 112, "RDMA", 10.5, "middle", INK2)
    f.rect(378, 40, 170, 110, ORANGE_L, ORANGE, 1.4, 6)
    f.text(463, 60, "Decode 集群", 12, "middle", INK, 700)
    f.text(463, 78, "受限于带宽；保证 TPOT", 10.5, "middle", INK2)
    for i in range(6):
        f.rect(396 + (i % 3) * 46, 90 + (i // 3) * 26, 40, 20, ORANGE, "none", 0, 3)
    f.arrow(550, 95, 578, 95)
    f.box(580, 70, 70, 50, ["逐个", "输出"], "white", 11)
    f.text(330, 184, "prefill 与 decode 分离部署：两组 GPU 各自选择并行方式和规模，互不干扰（示意）", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 35
def ch35_vit():
    f = Fig("ch35_vit", 660, 222)
    rnd = random.Random(2)
    n, s = 6, 22
    f.text(76, 18, "图片切成 6 × 6 个小块", 11.5, "middle", INK, 700)
    for i in range(n):
        for j in range(n):
            t = 0.25 + 0.5 * math.exp(-((i - 2.5) ** 2 + (j - 3) ** 2) / 6) + rnd.uniform(-0.08, 0.08)
            f.rect(10 + j * s, 30 + i * s, s - 2, s - 2, shade(t), "none", 0, 1)
    f.arrow(150, 96, 180, 96)
    f.text(165, 86, "展平", 10, "middle", INK2)
    for k in range(12):
        f.rect(186 + k * 15, 84, 12, 24, shade(0.3 + 0.05 * (k % 6)), "none", 0, 2)
    f.text(186 + 90, 124, "…… 共 36 个“视觉 token”", 10.5, "middle", INK2)
    f.text(186 + 90, 72, "线性投影 + 位置嵌入", 10.5, "middle", INK2)
    f.arrow(370, 96, 398, 96)
    f.box(400, 70, 150, 52, ["Transformer 编码器", "（没有因果掩码）"], "blue", 11)
    f.arrow(552, 96, 578, 96)
    f.box(580, 76, 70, 40, "图像特征", "white", 11)
    f.text(330, 188, "224×224 的图、16×16 的块 → 196 个 token；336×336 的图、14×14 的块 → 576 个 token", 11.5, "middle", INK2)
    f.text(330, 208, "（图中为示意，只画了 6 × 6 块）", 11, "middle", INK3)
    save(f)


def ch35_clip():
    f = Fig("ch35_clip", 660, 236)
    B, cs, x0, y0 = 6, 26, 200, 40
    caps = ["一只狗", "海边日落", "红色汽车", "一碗面", "雪山", "猫"]
    f.text(x0 + B * cs / 2, 18, "文字编码 $T_1$ … $T_6$", 11, "middle", INK2)
    f.text(x0 - 10, y0 - 6, "图片编码", 11, "end", INK2)
    rnd = random.Random(9)
    for i in range(B):
        f.text(x0 - 10, y0 + i * cs + cs / 2 + 4, f"$I_{i + 1}$", 11, "end", INK)
        f.text(x0 + i * cs + cs / 2, y0 - 6 + 0, "", 10)
        for j in range(B):
            v = 0.85 + rnd.uniform(-0.05, 0.08) if i == j else rnd.uniform(0.0, 0.35)
            f.rect(x0 + j * cs, y0 + i * cs, cs - 2, cs - 2, shade(v), "none", 0, 2)
        f.text(x0 + B * cs + 10, y0 + i * cs + cs / 2 + 4, caps[i], 10.5, "start", INK2)
    for j in range(B):
        f.text(x0 + j * cs + cs / 2, y0 + B * cs + 14, f"{j + 1}", 10, "middle", INK3)
    f.text(20, 80, ["每一行：在 6 段文字中", "找出配对的那一段", "（交叉熵，答案在对角线）"], 10.5, "start", INK2)
    f.text(420, 80, ["每一列也做一遍，", "两个方向的 loss 取平均：", "对称的 InfoNCE"], 10.5, "start", INK2)
    f.text(330, 228, "CLIP 的 $B\\times B$ 相似度矩阵：拉近对角线上的真配对，推开其余所有组合（颜色深浅为示意）", 11, "middle", INK2)
    save(f)


def ch35_llava():
    f = Fig("ch35_llava", 660, 196)
    f.box(10, 36, 70, 46, "图片", "white", 12)
    f.arrow(82, 59, 104, 59)
    f.box(106, 30, 120, 58, ["视觉编码器", "CLIP / SigLIP"], "blue", 11)
    f.text(166, 102, "阶段 1、2 都冻结", 10, "middle", BLUE)
    f.arrow(228, 59, 250, 59)
    f.box(252, 36, 80, 46, ["MLP", "连接层"], "Orange", 11)
    f.text(292, 102, "阶段 1 只训练它", 10, "middle", ORANGE)
    f.arrow(334, 59, 356, 59)
    for k in range(6):
        f.rect(360 + k * 13, 44, 10, 30, ORANGE_M, "none", 0, 2)
    f.text(398, 92, "576 个视觉 token", 10, "middle", INK2)
    f.box(360, 120, 80, 28, "文字 token", "white", 10.5)
    f.arrow(440, 59, 466, 90, INK3, 1.2)
    f.arrow(442, 134, 466, 108, INK3, 1.2)
    f.box(468, 74, 104, 52, ["语言模型"], "Blue", 12)
    f.text(520, 140, "阶段 2 解冻", 10, "middle", BLUE)
    f.arrow(574, 100, 596, 100)
    f.box(598, 82, 52, 36, "回答", "white", 11)
    f.text(330, 184, "LLaVA 式视觉语言模型：阶段 1 用约 55.8 万对图片说明对齐连接层，阶段 2 做视觉指令微调", 11, "middle", INK2)
    save(f)


def ch35_rvq():
    f = Fig("ch35_rvq", 660, 196)
    f.text(10, 18, "残差向量量化：每一层码本编码上一层留下的误差", 12, "start", INK, 700)
    errs = [1.0, 0.45, 0.2, 0.09]
    for k in range(4):
        y = 34 + k * 34
        f.text(10, y + 17, f"第 {k + 1} 层码本", 11, "start", INK)
        f.rect(100, y + 4, 300 * errs[k], 20, shade(0.4 + 0.15 * k, b=(0x2e, 0x7d, 0x4f)), "none", 0, 2)
        f.box(430, y + 2, 60, 24, f"id {[143, 7, 921, 58][k]}", "white", 10.5)
    f.text(460, 186, "每帧的离散 token", 10.5, "middle", INK2)
    f.text(510, 60, ["层数越多，", "还原的音质越好；", "token 数也越多"], 11, "start", INK2)
    f.text(250, 186, "条形长度：每一层编码前剩下的误差（示意）", 10.5, "middle", INK3)
    save(f)


def ch35_diffusion():
    d = json.load(open(os.path.join(OUT, "data", "ch35_diffusion.json")))
    f = Fig("ch35_diffusion", 660, 196)
    panels = [("100", "纯噪声（起点）"), ("60", "去噪 40 步"), ("30", "70 步"), ("10", "90 步"), ("0", "100 步：生成结果"), ("data", "真实数据")]
    w = 104
    for k, (key, title) in enumerate(panels):
        x0 = 10 + k * (w + 4)
        cx, cy, sc = x0 + w / 2, 96, 24
        f.rect(x0, 34, w, w + 20, "#fbfcfd", GRID, 1, 4)
        f.text(cx, 24, title, 10.5, "middle", INK, 700 if key in ("0", "data") else None)
        f.circle(cx, cy, sc, "none", GRID, 1)
        col = GREEN if key == "data" else BLUE
        pts = d[key][:700]
        for a, b in pts:
            px, py = cx + a * sc, cy - b * sc
            if x0 + 2 < px < x0 + w - 2 and 36 < py < 34 + w + 18:
                f.raw(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="0.9" fill="{col}" fill-opacity="0.55"/>')
    f.text(330, 182, "35.5 节二维扩散模型的去噪过程（实测：同一个训练好的模型重新采样 1,500 个点，图中画出其中 700 个）", 10.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 36
def ch36_budget():
    f = Fig("ch36_budget", 660, 236)
    rows = [("最终预训练", 6, 6), ("研究与消融实验", 10, 30), ("后训练（含强化学习）", 3, 10), ("数据（授权 + 标注 + 合成）", 10, 15), ("人员（约 100 人）", 50, 50)]
    c = Chart(f, 200, 20, 380, 150, (0, 60), (0, len(rows)))
    for t in [0, 10, 20, 30, 40, 50, 60]:
        f.line(c.X(t), c.y0, c.X(t), c.y0 + c.h, GRID, 1)
        f.text(c.X(t), c.y0 + c.h + 16, f"{t}", 10.5, "middle", INK2)
    f.text(c.x0 + c.w / 2, c.y0 + c.h + 34, "百万美元（按每卡时 2 美元租用算力估算）", 11, "middle", INK2)
    for i, (lab, lo, hi) in enumerate(rows):
        yc = c.y0 + (i + 0.5) * c.h / len(rows)
        f.text(c.x0 - 8, yc + 4, lab, 11, "end", INK)
        f.rect(c.x0, yc - 9, c.X(lo) - c.x0, 18, BLUE, "none", 0, 2)
        if hi > lo:
            f.rect(c.X(lo), yc - 9, c.X(hi) - c.X(lo), 18, BLUE_M, "none", 0, 2)
        txt = {0: "约 6", 1: "10–30", 2: "数百万到上千万", 3: "10 以上", 4: "约 50"}[i]
        f.text(c.X(hi) + 6, yc + 4, txt, 10.5, "start", INK)
    f.text(330, 230, "做一个 DeepSeek-V3 级别的模型，第一年的示意预算：合计约 1 亿到 2 亿美元（浅色是估算区间的上半段）", 11, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 37
def ch37_timeline():
    f = Fig("ch37_timeline", 660, 236)
    x0, x1 = 30, 640
    t0, t1 = 2017.0, 2022.75
    X = lambda t: x0 + (t - t0) / (t1 - t0) * (x1 - x0)
    ya = 128
    f.line(x0, ya, x1, ya, INK3, 2)
    for y in range(2017, 2023):
        f.line(X(y), ya - 5, X(y), ya + 5, INK3, 1.4)
    hw = [(2017.0, "P100（已有）", 5), (2017.37, "TPU v2 发布（bf16）", 4), (2017.6, "V100 出货（FP16 Tensor Core）", 3), (2018.2, "V100 32 GB", 2),
          (2018.37, "TPU v3", 1), (2018.6, "DGX-2 / NVSwitch", 0), (2020.37, "A100：bf16、80 GB", 0), (2022.2, "H100：FP8", 0)]
    for t, lab, lvl in hw:
        y = 112 - lvl * 16
        f.line(X(t), y + 3, X(t), ya, BLUE, 1)
        f.circle(X(t), ya, 3.6, BLUE, "#ffffff", 1.2)
        f.text(X(t) + 4, y, lab, 10.5, "start", BLUE)
    al = [(2017.45, "Transformer", 2), (2017.8, "混合精度训练论文", 1), (2018.45, "GPT-1（1.17 亿参数）", 0), (2020.4, "GPT-3", 0), (2022.2, "Chinchilla", 1)]
    for t, lab, lvl in al:
        y = 154 + lvl * 16
        f.line(X(t), ya, X(t), y - 10, ORANGE, 1)
        f.circle(X(t), ya, 3, ORANGE, "#ffffff", 1)
        f.text(X(t) + 4, y, lab, 10.5, "start", ORANGE)
    for y in range(2017, 2023):
        f.line(X(y), ya + 5, X(y), ya + 62, GRID, 1, "2 2")
        f.text(X(y), ya + 76, str(y), 11, "middle", INK, 700)
    f.text(640, 230, "蓝色在上：硬件；橙色在下：算法与模型的历史节点（数据见本章与第 0 章）", 10.5, "end", INK2)
    save(f)


def ch37_compare():
    f = Fig("ch37_compare", 660, 208)
    rows = [("低精度峰值算力", 125, 989, "TFLOP/s", "约 8 倍"), ("显存容量", 16, 80, "GB", "5 倍"), ("显存带宽", 0.9, 3.35, "TB/s", "约 3.7 倍"),
            ("每卡的跨机带宽", 6.25, 50, "GB/s", "8 倍")]
    for i, (lab, v, h, unit, ratio) in enumerate(rows):
        y = 20 + i * 40
        f.text(130, y + 20, lab, 11.5, "end", INK)
        w = 380
        f.rect(140, y + 4, w * v / h, 14, ORANGE, "none", 0, 2)
        f.rect(140, y + 20, w, 14, BLUE, "none", 0, 2)
        f.text(140 + w * v / h + 6, y + 15, f"V100：{v:g} {unit}", 10, "start", ORANGE)
        f.text(140 + w - 6, y + 31, f"H100：{h:g} {unit}", 10, "end", "#ffffff")
        f.text(650, y + 24, ratio, 11.5, "end", INK, 700)
    f.text(330, 200, "V100（2017 年底）与 H100 的对比。另外 V100 只支持 FP16，没有 BF16 和 FP8", 11.5, "middle", INK2)
    save(f)


def ch37_days():
    f = Fig("ch37_days", 660, 232)
    rows = [("GPT-3 级别", 9, 4), ("Chinchilla 级别", 17, 7), ("8B 训练 15T token", 21, 8), ("DeepSeek-V3 级别", 95, 38), ("Llama 3 405B 级别", 1095, 438)]
    c = Chart(f, 170, 24, 400, 160, (1, 2000), (0, len(rows)), xlog=True)
    for t, lab in ((1, "1 天"), (7, "1 周"), (30, "1 个月"), (365, "1 年")):
        f.line(c.X(t), c.y0, c.X(t), c.y0 + c.h, GRID, 1)
        f.text(c.X(t), c.y0 + c.h + 16, lab, 10.5, "middle", INK2)
    for i, (lab, d1, d2) in enumerate(rows):
        yc = c.y0 + (i + 0.5) * c.h / len(rows)
        f.text(c.x0 - 8, yc + 4, lab, 11, "end", INK)
        f.rect(c.x0, yc - 10, c.X(d1) - c.x0, 9, BLUE, "none", 0, 2)
        f.rect(c.x0, yc + 1, c.X(d2) - c.x0, 9, BLUE_M, "none", 0, 2)
        f.text(c.X(d1) + 5, yc - 2, f"{d1:g} 天" if d1 < 1000 else "约 3 年", 10, "start", INK)
    legend(f, 170, 220, [("1 万张 V100", BLUE, "box"), ("2.5 万张 V100", BLUE_M, "box")])
    f.text(640, 220, "每卡有效 40 TFLOP/s（估算）", 10.5, "end", INK3)
    save(f)


# ----------------------------------------------------------------- chapter 38
def ch38_ratio():
    f = Fig("ch38_ratio", 660, 222)
    rows = [("H100：有效算力 ÷ 每卡跨机带宽", 8000, BLUE), ("V100（DGX-1）", 6400, BLUE_M), ("V3 式 MoE 层：最多发往 4 台机器", 6900, ORANGE), ("MoE 层：最多发往 2 台机器", 13800, GREEN)]
    c = Chart(f, 250, 20, 330, 140, (0, 15000), (0, 4))
    for t in [0, 5000, 10000, 15000]:
        f.line(c.X(t), c.y0, c.X(t), c.y0 + c.h, GRID, 1)
        f.text(c.X(t), c.y0 + c.h + 16, f"{t:,}", 10.5, "middle", INK2)
    f.text(c.x0 + c.w / 2, c.y0 + c.h + 34, "FLOP / 字节", 11, "middle", INK2)
    for i, (lab, v, col) in enumerate(rows):
        yc = c.y0 + (i + 0.5) * c.h / 4
        f.text(c.x0 - 8, yc + 4, lab, 10.5, "end", INK)
        f.rect(c.x0, yc - 11, c.X(v) - c.x0, 22, col, "none", 0, 2)
        f.text(c.X(v) + 6, yc + 4, f"{v:,}", 10.5, "start", INK)
    c.vline(6400, RED, "4 3", None)
    f.text(330, 216, "计算与通信之比要高于硬件的“算力 ÷ 带宽”（红线，V100），通信才藏得住（估算，数据同 38.1、38.2 节）", 10.5, "middle", INK2)
    save(f)


def ch38_memory():
    f = Fig("ch38_memory", 660, 210)
    rows = [("不做重新计算", [(4.6, BLUE, "模型状态 4.6"), (11.4, ORANGE, "激活值 11.4"), (1.5, GRAY, "缓冲")]),
            ("做重新计算", [(4.6, BLUE, "模型状态 4.6"), (0.7 + 0.2, ORANGE, ""), (1.0, GRAY, "")])]
    sc = 26
    for i, (lab, parts) in enumerate(rows):
        y = 40 + i * 60
        f.text(110, y + 20, lab, 11.5, "end", INK)
        x = 120
        for v, col, t in parts:
            f.rect(x, y + 4, v * sc - 1, 26, col, "none", 0, 2)
            if t:
                f.text(x + v * sc / 2, y + 22, t, 10, "middle", "#ffffff")
            x += v * sc
        tot = sum(v for v, _, _ in parts)
        f.text(x + 8, y + 22, f"合计约 {tot:.0f} GB" if i else "超过 16 GB", 11, "start", RED if i == 0 else GREEN, 700)
    f.line(120 + 16 * sc, 30, 120 + 16 * sc, 140, RED, 1.4, "5 3")
    f.text(120 + 16 * sc + 4, 26, "V100 显存 16 GB", 10.5, "start", RED)
    f.text(330, 168, "70B 稠密模型、4,096 张 V100（TP 8 × PP 8 × DP 64 + ZeRO-1）、4K 序列：每张卡的显存（估算，数据同上表）", 11, "middle", INK2)
    f.text(330, 186, "16 GB 的显存是 2017 年最紧的约束之一，所以必须做激活重计算", 11, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 39
def ch39_roadmap():
    f = Fig("ch39_roadmap", 660, 262)
    x0, x1 = 110, 650
    q = (x1 - x0) / 12
    X = lambda qi: x0 + qi * q
    for y in range(3):
        f.rect(X(y * 4), 14, 4 * q - 2, 20, NAVY if y == 0 else ("#3d6f9e" if y == 1 else BLUE), "none", 0, 2)
        f.text(X(y * 4) + 2 * q, 28, f"{2017 + y} 年", 11, "middle", "#ffffff", 700)
    for k in range(13):
        f.line(X(k), 36, X(k), 232, GRID, 1)
    for k in range(12):
        f.text(X(k) + q / 2, 46, f"Q{k % 4 + 1}", 9, "middle", INK3)
    lanes = [("组织与硬件", [(0, 1, "P100", GRAY), (2, 4, "V100 上线", GRAY), (5, 8, "扩到 1–2.5 万卡、DGX-2", GRAY)]),
             ("数据", [(0, 4, "清洗、去重、私有评测集", GREEN), (4, 8, "用一代模型打分与合成", GREEN_M)]),
             ("系统", [(0, 1, "FP16+DP", PURPLE), (1, 2, "TP、PP", PURPLE), (2, 4, "推理引擎", PURPLE), (4, 8, "强化学习基础设施", PURPLE)]),
             ("研究", [(1, 2, "规模阶梯", ORANGE_M), (5, 8, "小规模验证 MoE", ORANGE_M)]),
             ("正式训练", [(2, 3, "7B", BLUE_M), (3, 4, "70B 稠密", BLUE), (8, 11, "第二代 MoE（约 3×10²⁴）", BLUE)]),
             ("后训练与发布", [(3, 4, "SFT+DPO", ORANGE), (4, 5, "发布一代", RED), (5, 8, "RLVR、蒸馏", ORANGE), (10, 12, "R1 式、Agent", ORANGE)])]
    for i, (name, bars) in enumerate(lanes):
        y = 54 + i * 30
        f.text(x0 - 8, y + 15, name, 11, "end", INK)
        for a, b, lab, col in bars:
            f.rect(X(a) + 1, y, (b - a) * q - 3, 22, col, "none", 0, 3)
            tc = "#ffffff" if col in (BLUE, PURPLE, RED, GREEN, ORANGE, GRAY) else INK
            f.text(X(a) + (b - a) * q / 2, y + 15, lab, 10 if b - a > 1 else 9.5, "middle", tc)
    f.text(330, 252, "39.1 节路线图的概览（每格一个季度；这是计划，不是史实）", 11, "middle", INK3)
    save(f)


if __name__ == "__main__":
    for fn in [ch32_superpos, ch32_sae, ch32_steer, ch32_induction,
               ch33_phases, ch33_kvspeed, ch33_batching, ch33_paged, ch33_cost,
               ch34_quant, ch34_spec, ch34_gamma, ch34_disagg,
               ch35_vit, ch35_clip, ch35_llava, ch35_rvq, ch35_diffusion,
               ch36_budget, ch37_timeline, ch37_compare, ch37_days,
               ch38_ratio, ch38_memory, ch39_roadmap]:
        fn()
    print("ok")
