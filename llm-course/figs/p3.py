"""Figures for Part 3 (chapters 10-13). Run: python3 figs/p3.py"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import *

OUT = os.path.dirname(os.path.abspath(__file__))

# Epoch AI's corrected Chinchilla fit (chapter 10.4)
E_, A_, B_, AL, BE = 1.82, 482, 2085, 0.348, 0.366


def Lfit(N, D):
    return E_ + A_ / N ** AL + B_ / D ** BE


def save(f):
    f.save(os.path.join(OUT, f.name + ".svg"))


def clipped(c, xs, ys, color, sw=2, dash=None):
    """Draw a polyline, cutting it where it leaves the chart's y-range."""
    y0, y1 = c.ylim
    pts, seg = [], []
    for k in range(len(xs)):
        x, y = xs[k], ys[k]
        inside = y0 <= y <= y1
        if k > 0:
            px, py = xs[k - 1], ys[k - 1]
            pin = y0 <= py <= y1
            if pin != inside:
                yb = y1 if (y > y1 or py > y1) else y0
                t = (yb - py) / (y - py)
                xb = px + t * (x - px)
                seg.append((c.X(xb), c.Y(yb)))
                if pin:
                    pts.append(seg)
                    seg = []
        if inside:
            seg.append((c.X(x), c.Y(y)))
    if seg:
        pts.append(seg)
    for s in pts:
        if len(s) > 1:
            c.f.poly(s, color, sw, dash)


def lerp_col(t):
    t = max(0.0, min(1.0, t))
    return f"rgb({int(255 - t * (255 - 28))},{int(255 - t * (255 - 93))},{int(255 - t * (255 - 153))})"


# ----------------------------------------------------------------- chapter 10
def ch10_power():
    f = Fig("ch10_power", 660, 274)
    Ns = [10 ** (7 + i / 20) for i in range(121)]
    c = Chart(f, 52, 46, 240, 160, (1e7, 1e13), (1.5, 4.0), xlog=True)
    c.axes([1e7, 1e9, 1e11, 1e13], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0], xlabel="参数量 $N$（对数坐标）", ylabel="loss",
           xfmt=lambda v: f"$10^{{{int(round(math.log10(v)))}}}$", yfmt=lambda v: f"{v:.1f}")
    c.series(Ns, [E_ + A_ / n ** AL for n in Ns], BLUE)
    c.hline(E_, RED, "5 3", None)
    f.text(c.X(1e13) - 4, c.Y(E_) + 14, "$E$ = 1.82：不可约损失", 11, "end", RED)
    f.text(c.x0 + c.w / 2, 16, "loss 本身：越来越平，逼近 $E$", 12, "middle", INK, 700)
    c2 = Chart(f, 400, 46, 240, 160, (1e7, 1e13), (0.01, 3), xlog=True, ylog=True)
    c2.axes([1e7, 1e9, 1e11, 1e13], [0.01, 0.1, 1], xlabel="参数量 $N$（对数坐标）", ylabel="$L - E$（对数坐标）",
            xfmt=lambda v: f"$10^{{{int(round(math.log10(v)))}}}$", yfmt=lambda v: f"{v:g}")
    c2.series(Ns, [A_ / n ** AL for n in Ns], BLUE)
    f.text(c2.x0 + c2.w / 2, 16, "减去 $E$ 后：一条直线", 12, "middle", INK, 700)
    x1, x2 = 1e9, 1e10
    f.poly([(c2.X(x1), c2.Y(A_ / x1 ** AL)), (c2.X(x2), c2.Y(A_ / x1 ** AL)), (c2.X(x2), c2.Y(A_ / x2 ** AL))], INK3, 1, "3 2")
    f.text(c2.X(3e10), c2.Y(1.3), ["$N$ 每大 10 倍，", "$L - E$ 乘以 0.45"], 11, "start", INK2)
    f.text(330, 268, "示意：用 10.4 节的拟合常数 $E + A/N^{\\alpha}$ 画出（只看模型大小一项，数据视为无限多）", 11.5, "middle", INK2)
    save(f)


def ch10_isoflop():
    f = Fig("ch10_isoflop", 660, 286)
    c = Chart(f, 58, 30, 420, 190, (1e8, 1e12), (1.9, 2.75), xlog=True)
    c.axes([1e8, 1e9, 1e10, 1e11, 1e12], [1.9, 2.1, 2.3, 2.5, 2.7], xlabel="参数量 $N$（对数坐标）；每条曲线上 $D = C/(6N)$",
           ylabel="预测的 loss", xfmt=lambda v: f"$10^{{{int(round(math.log10(v)))}}}$", yfmt=lambda v: f"{v:.1f}")
    Ns = [10 ** (8 + i / 40) for i in range(161)]
    cols = [BLUE_M, "#5f8fc0", BLUE, NAVY]
    opt = []
    for k, C in enumerate([1e21, 1e22, 1e23, 1e24]):
        ys = [Lfit(n, C / 6 / n) for n in Ns]
        clipped(c, Ns, ys, cols[k], 2)
        j = min(range(len(ys)), key=lambda i: ys[i])
        opt.append((Ns[j], ys[j]))
        f.text(c.X(Ns[j]) - 8, c.Y(ys[j]) + 14, f"$10^{{{21 + k}}}$", 11, "end", INK)
    f.poly([(c.X(n), c.Y(l)) for n, l in opt], RED, 1.4, "4 3")
    for n, l in opt:
        f.circle(c.X(n), c.Y(l), 3.6, RED, "#ffffff", 1.5)
    f.text(496, 52, ["每条曲线固定计算量 $C$", "（数字是 FLOP），只改变", "模型和数据的分配比例。"], 11.5, "start", INK2)
    f.text(496, 116, ["“U”形的谷底就是", "计算最优的模型；", "红点连成的线：", "$N_{opt} \\propto C^{0.51}$"], 11.5, "start", INK2)
    f.text(496, 196, ["左侧：模型太小", "右侧：数据太少"], 11.5, "start", INK2)
    f.text(330, 280, "按 10.4 节的拟合公式计算（估算，不是训练实验）；谷底的数值与上表一致", 11.5, "middle", INK2)
    save(f)


def ch10_flat():
    f = Fig("ch10_flat", 660, 252)
    N0, C = 96e9, 1e24
    L0 = Lfit(N0, C / 6 / N0)
    c = Chart(f, 60, 30, 400, 160, (1 / 16, 4), (0, 0.08), xlog=True)
    ticks = [1 / 16, 1 / 8, 1 / 4, 1 / 2, 1, 2, 4]
    c.axes(ticks, [0, 0.02, 0.04, 0.06, 0.08], xlabel="模型大小 ÷ 最优大小 $N_0$（对数坐标；计算量固定为 $10^{24}$）",
           ylabel="loss 比最优点高出多少", xfmt=lambda v: {1 / 16: "1/16", 1 / 8: "1/8", 1 / 4: "1/4", 1 / 2: "1/2"}.get(v, f"{v:g}"),
           yfmt=lambda v: f"{v:.2f}")
    f.rect(c.X(0.5), c.y0, c.X(2) - c.X(0.5), c.h, GREEN_L, "none", 0, 0)
    xs = [2 ** (-4 + i / 20) for i in range(121)]
    c.series(xs, [Lfit(N0 * x, C / 6 / N0 / x) - L0 for x in xs], BLUE)
    for x, v in zip(ticks, [0.074, 0.041, 0.018, 0.004, 0, 0.004, 0.018]):
        c.dots([x], [v], BLUE)
        f.text(c.X(x) + (8 if x < 1 else -8), c.Y(v) - 6, f"+{v:.3f}" if v else "0", 10.5, "start" if x < 1 else "end", INK)
    f.text(c.X(1), c.y0 + 16, "2 倍以内：几乎无损", 11, "middle", GREEN)
    f.text(478, 70, ["往左：小模型、多数据。", "在 1/16 处，loss 只高", "出 0.074，却换来一个", "推理便宜 16 倍的模型", "——这就是“过度训练”", "的空间（10.6 节）"], 11.5, "start", INK2)
    f.text(330, 246, "按 10.4 节的拟合公式估算（数据同上表）", 11.5, "middle", INK2)
    save(f)


def ch10_tokens():
    f = Fig("ch10_tokens", 660, 252)
    rows = [("MT-NLG 530B（2022）", 270 / 530), ("Gopher 280B（2021）", 300 / 280), ("GPT-3 175B（2020）", 300 / 175),
            ("Chinchilla 70B（2022）", 1400 / 70), ("Llama 3 405B（2024）", 15600 / 405), ("Llama 3 8B（2024）", 15000 / 8)]
    c = Chart(f, 170, 22, 400, 168, (0.3, 3000), (0, len(rows)), xlog=True)
    for t in [1, 10, 100, 1000]:
        f.line(c.X(t), c.y0, c.X(t), c.y0 + c.h, GRID, 1)
        f.text(c.X(t), c.y0 + c.h + 16, f"{t:,}", 11, "middle", INK2)
    f.text(c.x0 + c.w / 2, c.y0 + c.h + 34, "训练 token 数 ÷ 参数量（对数坐标）", 11.5, "middle", INK2)
    for i, (name, r) in enumerate(rows):
        yc = c.y0 + (i + 0.5) * c.h / len(rows)
        f.text(c.x0 - 8, yc + 4, name, 11.5, "end", INK)
        col = ORANGE if i < 3 else (GREEN if i == 3 else BLUE)
        f.rect(c.x0, yc - 9, c.X(r) - c.x0, 18, col, "none", 0, 2)
        f.text(c.X(r) + 6, yc + 4, f"{r:,.1f}" if r < 10 else f"{r:,.0f}", 11, "start", INK)
    c.vline(20, GREEN, "4 3", None)
    f.text(c.X(20) + 4, c.y0 - 6, "Chinchilla：约 20", 11, "start", GREEN)
    f.text(330, 246, "橙色：Kaplan 时代“参数多、数据少”；蓝色：考虑推理成本后的“过度训练”（数据见本章与第 0 章）", 11.5, "middle", INK2)
    save(f)


def ch10_breakeven():
    f = Fig("ch10_breakeven", 660, 258)
    c = Chart(f, 60, 30, 400, 170, (0, 25), (0, 20))
    c.axes([0, 5, 10, 15, 20, 25], [0, 5, 10, 15, 20], xlabel="上线后生成的 token 总数（万亿，即 T）",
           ylabel="训练 + 推理的总计算量（$10^{23}$ FLOP）", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    xs = [0, 25]
    c.series(xs, [7.2 + 0.16 * x for x in xs], BLUE, 2.2)
    c.series(xs, [1.32 + 0.68 * x for x in xs], ORANGE, 2.2)
    xb = 5.88 / 0.52
    c.vline(xb, INK3, "4 3", None)
    c.dots([xb], [7.2 + 0.16 * xb], RED)
    f.text(c.X(xb) + 6, c.Y(0) - 8, "约 11T", 11, "start", INK)
    f.text(c.X(25) + 6, c.Y(7.2 + 4) + 4, ["8B，训练 15T token", "（过度训练）"], 11.5, "start", BLUE)
    f.text(c.X(25) + 6, c.Y(1.32 + 17) + 4, ["34B，训练 0.65T token", "（计算最优）"], 11.5, "start", ORANGE)
    f.line(c.X(0.6), c.Y(1.32) - 2, c.X(0.6), c.Y(7.2) + 2, INK3, 1.2, arrow=True, arrow_start=True)
    f.text(c.X(0.6) + 6, c.Y(6.0) + 4, "多花的训练算力", 11, "start", INK2)
    f.text(330, 252, "两个模型的预测 loss 相同（2.022）。斜率是推理成本：每个 token 约 $2N$ FLOP（示意，按 10.4 节公式外推）", 11.5, "middle", INK2)
    save(f)


def ch10_emerge():
    f = Fig("ch10_emerge", 660, 248)
    lc = [18 + i / 20 for i in range(121)]  # log10 C from 18 to 24
    nll = [0.25 + 2.2 * 10 ** (-0.18 * (x - 18)) for x in lc]
    acc = lambda z: 0.25 + 0.7 / (1 + math.exp((z - 0.75) / 0.07))
    c1 = Chart(f, 46, 46, 160, 130, (18, 24), (0, 2.6))
    c1.axes([18, 20, 22, 24], [0, 1, 2], xlabel="$\\log_{10}$ 计算量", ylabel="正确答案的 NLL", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", size=10.5)
    c1.series(lc, nll, BLUE)
    f.text(126, 16, "① 计算量 → NLL：平滑的幂律", 11.5, "middle", INK, 700)
    zs = [i / 40 for i in range(101)]
    c2 = Chart(f, 266, 46, 160, 130, (2.5, 0), (0, 1))
    c2.axes([2, 1, 0], [0, 0.25, 0.5, 0.75, 1], xlabel="NLL（向右越小）", ylabel="准确率", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0%}", size=10.5)
    c2.series(zs, [acc(z) for z in zs], ORANGE)
    f.text(346, 16, "② NLL → 准确率：S 形", 11.5, "middle", INK, 700)
    c3 = Chart(f, 486, 46, 160, 130, (18, 24), (0, 1))
    c3.axes([18, 20, 22, 24], [0, 0.25, 0.5, 0.75, 1], xlabel="$\\log_{10}$ 计算量", ylabel="准确率", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0%}", size=10.5)
    c3.series(lc, [acc(z) for z in nll], GREEN)
    f.text(566, 16, "合起来：像是“突然涌现”", 11.5, "middle", INK, 700)
    f.text(330, 240, "示意。连续的指标（NLL）平稳变化；“对就 1 分、错就 0 分”的准确率在某个阈值附近陡升", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 11
def ch11_sum():
    f = Fig("ch11_sum", 660, 256)
    n = 256
    rnd = random.Random(7)
    walk, s = [0], 0
    for _ in range(n):
        s += rnd.choice((-1, 1))
        walk.append(s)
    js = list(range(n + 1))
    c = Chart(f, 50, 40, 240, 160, (0, n), (0, 256))
    c.axes([0, 128, 256], [0, 64, 128, 192, 256], xlabel="相加的项数 $n$", ylabel="累加和", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", size=11)
    c.series(js, js, ORANGE, 2.2)
    f.text(c.x0 + c.w / 2, 16, "同号相加：增长到 $n$ = 256", 12, "middle", INK, 700)
    c2 = Chart(f, 390, 40, 240, 160, (0, n), (-24, 24))
    c2.axes([0, 128, 256], [-24, -16, -8, 0, 8, 16, 24], xlabel="相加的项数 $n$", ylabel="累加和（注意纵轴小了 10 倍）", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", size=11)
    c2.series(js, [math.sqrt(j) for j in js], GRAY, 1, "3 3")
    c2.series(js, [-math.sqrt(j) for j in js], GRAY, 1, "3 3")
    c2.series(js, walk, BLUE, 1.6)
    f.text(c2.x0 + c2.w / 2, 16, "随机正负相加：只有 $\\sqrt{n}$ = 16 的量级", 12, "middle", INK, 700)
    f.text(c2.X(140), c2.Y(20), "虚线：±$\\sqrt{n}$", 11, "start", INK3)
    f.text(330, 250, "每项大小为 1（一次随机模拟）。初始化时的输出是“随机正负相加”，Adam 更新带来的输出变化是“同号相加”", 11.5, "middle", INK2)
    save(f)


def ch11_lrsweep():
    f = Fig("ch11_lrsweep", 660, 280)
    xs = list(range(-12, -2))
    sp = {64: [3.19, 2.95, 2.65, 2.42, 2.28, 2.21, 2.26, 2.45, 2.79, 3.27],
          256: [2.79, 2.59, 2.43, 2.28, 2.22, 2.27, 2.46, 3.03, 4.22, 7.43],
          1024: [2.50, 2.38, 2.28, 2.27, 2.38, 2.82, 3.79, 6.16, 11.71, 26.57]}
    mu = {64: [3.19, 2.95, 2.65, 2.42, 2.28, 2.21, 2.26, 2.42, 2.73, 3.32],
          256: [3.09, 2.82, 2.52, 2.31, 2.18, 2.11, 2.16, 2.31, 2.59, 3.28],
          1024: [3.11, 2.80, 2.49, 2.28, 2.15, 2.08, 2.10, 2.21, 2.45, 2.99]}
    cols = {64: BLUE_M, 256: "#4f86bd", 1024: NAVY}
    for p, (title, data) in enumerate((("常规参数化（SP）", sp), ("μP", mu))):
        c = Chart(f, 50 + p * 320, 34, 260, 160, (-12, -3), (2.0, 3.4))
        c.axes(xs[::3] + [-3], [2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4], xlabel="学习率（$\\log_2$）",
               ylabel="验证集 loss" if p == 0 else None, xfmt=lambda v: f"$2^{{{int(v)}}}$", yfmt=lambda v: f"{v:.1f}", size=11)
        f.text(c.x0 + c.w / 2, 16, title, 12.5, "middle", INK, 700)
        for H, ys in data.items():
            clipped(c, xs, ys, cols[H], 2)
            j = min(range(10), key=lambda i: ys[i])
            c.dots([xs[j]], [ys[j]], cols[H], 4.2)
        if p == 0:
            f.text(c.X(-11.8), c.Y(3.33), "大学习率一侧迅速崩溃 →", 10.5, "start", INK2)
            f.text(c.X(-8), c.Y(2.03), "最优点随宽度左移", 10.5, "middle", RED)
        else:
            c.vline(-7, RED, "4 3", None)
            f.text(c.X(-7) + 5, c.Y(3.3), "三种宽度的最优都在 $2^{-7}$", 10.5, "start", RED)
    legend(f, 190, 252, [("$H$ = 64", BLUE_M, "line"), ("$H$ = 256", "#4f86bd", "line"), ("$H$ = 1024", NAVY, "line")])
    f.text(330, 274, "11.3 节的实验（实测，数据同上表）；圆点是每种宽度的最优学习率，超出图框的点没有画出", 11.5, "middle", INK2)
    save(f)


def ch11_bcrit():
    f = Fig("ch11_bcrit", 660, 246)
    c = Chart(f, 60, 26, 330, 160, (1, 6.5), (1, 6.5))
    c.axes([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], xlabel="用掉的数据 $E/E_{min}$", ylabel="训练步数 $S/S_{min}$",
           xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
    xs = [1 + 1 / (5.5) + i * 0.02 for i in range(300)]
    xs = [x for x in xs if x <= 6.5]
    c.series(xs, [1 + 1 / (x - 1) for x in xs], BLUE, 2.2)
    pts = [(1.2, 6.0, "$B \\ll B_{crit}$"), (2, 2, "$B = B_{crit}$"), (6.0, 1.2, "$B \\gg B_{crit}$")]
    for x, y, lab in pts:
        c.dots([x], [y], ORANGE, 4.2)
    f.text(c.X(1.2) + 8, c.Y(6.0) + 4, "①", 12, "start", ORANGE)
    f.text(c.X(2) + 8, c.Y(2) - 6, "②", 12, "start", ORANGE)
    f.text(c.X(6.0), c.Y(1.2) - 10, "③", 12, "middle", ORANGE)
    f.text(410, 50, "① $B$ 远小于 $B_{crit}$：", 12, "start", INK, 700)
    f.text(410, 68, "数据几乎不浪费，但步数多", 11.5, "start", INK2)
    f.text(410, 104, "② $B = B_{crit}$：", 12, "start", INK, 700)
    f.text(410, 122, "步数和数据都是最小值的 2 倍", 11.5, "start", INK2)
    f.text(410, 158, "③ $B$ 远大于 $B_{crit}$：", 12, "start", INK, 700)
    f.text(410, 176, "步数接近最少，数据大量浪费", 11.5, "start", INK2)
    f.text(330, 240, "达到同一个 loss 的各种做法都落在这条双曲线上：$(S/S_{min} - 1)(E/E_{min} - 1) = 1$", 11.5, "middle", INK2)
    save(f)


def ch11_wsd():
    f = Fig("ch11_wsd", 660, 288)
    T = 400
    ts = [i / T for i in range(T + 1)]
    cosine = [0.5 * (1 + math.cos(math.pi * t)) for t in ts]
    def wsd(t, start, length):
        if t < start:
            return 1.0
        return max(0.0, 1 - (t - start) / length)
    w = [wsd(t, 0.8, 0.2) for t in ts]
    br_ts = [t for t in ts if 0.4 <= t <= 0.5]
    br = [wsd(t, 0.4, 0.1) for t in br_ts]
    def loss(lrs, t0=0.0, p0=0.0):
        out, p = [], p0
        for lr in lrs:
            p += lr / T
            out.append(1.9 + 0.5 / (1 + 8 * p) + 0.25 * lr)
        return out
    c1 = Chart(f, 60, 26, 420, 60, (0, 1), (0, 1.1))
    c1.axes([], [0, 1], ylabel="学习率", yfmt=lambda v: "峰值" if v else "0", size=11)
    c1.series(ts, cosine, ORANGE, 2)
    c1.series(ts, w, BLUE, 2)
    c1.series(br_ts, br, BLUE, 1.5, "4 3")
    c2 = Chart(f, 60, 118, 420, 108, (0, 1), (1.9, 2.7))
    c2.axes([0, 0.2, 0.4, 0.6, 0.8, 1.0], [1.9, 2.1, 2.3, 2.5, 2.7], xlabel="训练进度", ylabel="loss（示意）",
            xfmt=lambda v: f"{v:.0%}", yfmt=lambda v: f"{v:.1f}", size=11)
    lc, lw = loss(cosine), loss(w)
    p40 = sum(w[:int(0.4 * T) + 1]) / T
    lb = loss(br, p0=p40)
    c2.series(ts[4:], lc[4:], ORANGE, 2)
    c2.series(ts[4:], lw[4:], BLUE, 2)
    c2.series(br_ts, lb, BLUE, 1.5, "4 3")
    c2.dots([br_ts[-1]], [lb[-1]], BLUE, 3.4)
    legend(f, 496, 40, [("余弦调度", ORANGE, "line"), ("WSD", BLUE, "line"), ("从中途检查点分出的衰减", BLUE, "dash")], horizontal=False, size=11)
    f.text(496, 128, ["WSD 的稳定阶段 loss 偏高", "（参数在“河谷”两壁之间", "弹跳），一进入衰减阶段", "就急剧下降，最终与余弦", "调度相当。", "", "虚线：从 40% 处的检查点", "单独衰减，就能得到一个", "较短训练的终点"], 11, "start", INK2)
    f.text(330, 282, "示意：曲线形状按“loss = 与已走路程有关的项 + 与当前学习率成正比的项”画出，不是实测", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 12
def ch12_spike():
    f = Fig("ch12_spike", 660, 254)
    c = Chart(f, 60, 26, 440, 170, (0, 1000), (2.0, 4.0))
    c.axes([0, 200, 400, 600, 800, 1000], [2.0, 2.5, 3.0, 3.5, 4.0], xlabel="训练步数（示意）", ylabel="训练 loss",
           xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.1f}")
    rnd = random.Random(5)
    base = lambda s: 2.3 + 1.2 * math.exp(-s / 160)
    xs, ys = [], []
    for s in range(0, 1001, 4):
        y = base(s) + rnd.gauss(0, 0.015)
        if 300 <= s <= 360:
            y += 0.9 * math.exp(-((s - 312) / 14) ** 2) if s < 312 else 0.9 * math.exp(-(s - 312) / 16)
        xs.append(s)
        ys.append(y)
    c.series(xs[:166], ys[:166], BLUE, 1.6)
    # divergence branch after a second spike at ~660
    dx, dy = [], []
    for s in range(660, 1001, 4):
        dx.append(s)
        dy.append(min(4.0, base(s) + 0.002 * (s - 660) + (0.8 if s >= 672 else 0.4 * (s - 660) / 12) + rnd.gauss(0, 0.02)))
    c.series([xs[165]] + dx, [ys[165]] + dy, RED, 1.6)
    rx = [600 + k * 4 for k in range(101)]
    c.series(rx, [base(s) + rnd.gauss(0, 0.012) for s in rx], GREEN, 1.6, "4 3")
    f.text(c.X(318) + 8, c.Y(3.25), "尖峰，随后自行恢复", 11.5, "start", INK)
    f.text(c.X(690), c.Y(3.78), "发散：loss 居高不下", 11.5, "start", RED)
    f.circle(c.X(600), c.Y(base(600)), 4, "#ffffff", GREEN, 1.6)
    f.text(c.X(600) - 6, c.Y(base(600)) + 22, "回滚到这个检查点", 11, "end", GREEN)
    f.text(c.X(860), c.Y(base(860)) + 20, "跳过数据、调低学习率后重新训练", 11, "middle", GREEN)
    f.text(330, 248, "示意图（不是实测）。有的尖峰会自己恢复；有的不会，只能回滚到更早的检查点重来", 11.5, "middle", INK2)
    save(f)


def adam_sim(beta2, steps=1100, jump=1000, beta1=0.9, eps=1e-8):
    rnd = random.Random(1)
    m = v = 0.0
    out = []
    for t in range(1, steps + 1):
        g = 0.1 if t >= jump else 0.001 * rnd.choice((-1, 1))
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * g * g
        mh, vh = m / (1 - beta1 ** t), v / (1 - beta2 ** t)
        out.append(abs(mh) / (math.sqrt(vh) + eps))
    return out


def ch12_adam():
    f = Fig("ch12_adam", 660, 272)
    lo, hi = 950, 1080
    steps = list(range(lo, hi + 1))
    c0 = Chart(f, 60, 22, 380, 46, (lo, hi), (0, 0.11))
    c0.axes([], [0, 0.1], ylabel=None, yfmt=lambda v: f"{v:g}", size=10.5)
    c0.series([lo, 999.5, 999.5, hi], [0.001, 0.001, 0.1, 0.1], INK2, 1.8)
    f.text(520, c0.y0 + 18, ["梯度大小：长期 0.001，", "第 1,000 步起为 0.1"], 11, "start", INK2)
    c = Chart(f, 60, 92, 380, 120, (lo, hi), (0, 8))
    c.axes([950, 1000, 1050], [0, 2, 4, 6, 8], xlabel="训练步数", ylabel=None, xfmt=lambda v: f"{v:,}", yfmt=lambda v: f"{v:g}", size=11)
    f.text(c.x0 + 6, c.y0 + 12, "每步更新量 ÷ 学习率", 11, "start", INK2)
    for b2, col, lab in ((0.999, RED, "$\\beta_2$ = 0.999"), (0.95, BLUE, "$\\beta_2$ = 0.95")):
        u = adam_sim(b2)
        ys = [u[s - 1] for s in steps]
        c.series(steps, ys, col, 2)
        k = max(range(len(ys)), key=lambda i: ys[i])
        f.text(c.X(hi) + 6, c.Y(ys[-1]) + 4, f"{lab}", 11.5, "start", col)
        if b2 == 0.999:
            f.text(c.X(steps[k]) + 6, c.Y(ys[k]) - 4, f"最大 {ys[k]:.1f}", 11, "start", RED)
    c.hline(1, INK3, "3 3", None)
    f.text(520, 120, ["$\\beta_2$ 大：$v$ 记得太久，", "仍停留在“梯度很小”的", "旧印象里，$m/\\sqrt{v}$ 被", "放大好几倍，形成尖峰。", "", "$\\beta_2$ = 0.95：约 20 步", "就跟上了新的梯度尺度"], 11, "start", INK2)
    f.text(330, 266, "按 Adam 公式的数值模拟（$\\beta_1$ = 0.9，含偏差修正）：一个长期“冷门”的参数突然收到大梯度", 11.5, "middle", INK2)
    save(f)


def ch12_ortho():
    f = Fig("ch12_ortho", 660, 222)
    def panel(cx, cy, s1, s2, ang, title, col, sub):
        f.text(cx, 18, title, 12, "middle", INK, 700)
        f.line(cx - 80, cy, cx + 80, cy, GRID, 1)
        f.line(cx, cy - 80, cx, cy + 80, GRID, 1)
        pts = []
        for k in range(73):
            t = 2 * math.pi * k / 72
            x, y = s1 * math.cos(t), s2 * math.sin(t)
            xr = x * math.cos(ang) - y * math.sin(ang)
            yr = x * math.sin(ang) + y * math.cos(ang)
            pts.append((cx + 26 * xr, cy - 26 * yr))
        f.poly(pts, col, 2, fill=col + "22" if col.startswith("#") else "none")
        for s, a in ((s1, ang), (s2, ang + math.pi / 2)):
            f.arrow(cx, cy, cx + 26 * s * math.cos(a), cy - 26 * s * math.sin(a), col, 1.6)
        f.text(cx, 200, sub, 11.5, "middle", INK2)
    f.text(70, 18, "输入：单位圆", 12, "middle", INK, 700)
    f.circle(70, 110, 26, BLUE_L, BLUE, 1.6)
    f.line(10, 110, 130, 110, GRID, 1)
    f.line(70, 50, 70, 170, GRID, 1)
    f.text(70, 200, "所有方向的长度都是 1", 11.5, "middle", INK2)
    f.arrow(140, 110, 176, 110)
    panel(290, 110, 2.9, 0.35, math.radians(25), "乘以动量 $m$", ORANGE, ["被拉成细长的椭圆：", "更新几乎全在一个方向上"])
    f.arrow(408, 110, 444, 110)
    panel(545, 110, 1, 1, math.radians(25), "乘以 $UV^{T}$（正交化后）", GREEN, ["又变回圆：每个方向的", "幅度都是 1，方向被保留"])
    save(f)


def ch12_sv():
    f = Fig("ch12_sv", 660, 250)
    idx = ["0", "1", "2", "10", "50", "128", "255"]
    g = [50.0, 20.0, 8.0, 0.825, 0.276, 0.033, 0.001]
    o = [1.202, 1.202, 1.200, 1.178, 0.906, 0.286, 0.009]
    c = Chart(f, 60, 26, 440, 160, (0, 7), (0.0005, 100), ylog=True)
    c.axes([], [0.001, 0.01, 0.1, 1, 10, 100], ylabel="奇异值（对数坐标）", yfmt=lambda v: f"{v:g}")
    for i in range(7):
        x = c.X(i + 0.5)
        f.rect(x - 17, c.Y(g[i]), 16, c.Y(0.0005) - c.Y(g[i]), GRAY, "none", 0, 1.5)
        f.rect(x + 1, c.Y(o[i]), 16, c.Y(0.0005) - c.Y(o[i]), BLUE, "none", 0, 1.5)
        f.text(x, c.Y(0.0005) + 15, idx[i], 11, "middle", INK2)
    f.text(c.x0 + c.w / 2, c.Y(0.0005) + 33, "第几个奇异值（从大到小排序）", 11.5, "middle", INK2)
    legend(f, 516, 50, [("原始梯度 $G$", GRAY, "box"), ("5 次迭代之后", BLUE, "box")], horizontal=False)
    f.text(516, 110, ["最强 3 个方向的份额", "（按奇异值平方计）：", "99.4% → 4.6%"], 11.5, "start", INK2)
    f.text(330, 244, "Newton–Schulz 正交化的数值演示（实测，数据同上表）：大和中等的奇异值都被拉到 1 附近", 11.5, "middle", INK2)
    save(f)


def ch12_flow():
    f = Fig("ch12_flow", 660, 236)
    f.box(10, 92, 86, 40, "发现尖峰", "Red", 12.5)
    f.arrow(98, 112, 120, 112)
    f.poly([(176, 82), (232, 112), (176, 142), (120, 112), (176, 82)], ORANGE, 1.4, fill=ORANGE_L)
    f.text(176, 108, "几百步内", 11, "middle", INK)
    f.text(176, 122, "自行恢复？", 11, "middle", INK)
    f.poly([(176, 80), (176, 40), (260, 40)], INK3, 1.3, arrow=True)
    f.text(182, 58, "是", 11, "start", GREEN, 700)
    f.box(262, 22, 150, 36, "继续训练，记录在案", "green", 12)
    f.arrow(234, 112, 262, 112)
    f.text(240, 106, "否", 11, "start", RED, 700)
    f.box(264, 90, 114, 44, ["回滚到尖峰前", "几十到几百步"], "blue", 11.5)
    f.arrow(380, 112, 402, 112)
    f.box(404, 90, 112, 44, ["跳过附近的 batch；", "临时调低学习率"], "blue", 11.5)
    f.arrow(518, 112, 540, 112)
    f.box(542, 90, 108, 44, ["继续训练"], "blue", 12)
    f.poly([(596, 136), (596, 166), (520, 166)], INK3, 1.3, arrow=True)
    f.text(602, 156, "反复出现", 11, "start", RED)
    f.box(250, 150, 268, 54, ["从结构上找原因：看注意力和输出", "logits 的统计量，加 QK-norm 或", "z-loss，排查数据和硬件"], "orange", 11)
    f.text(330, 228, "12.6 节的处理流程。每一次处理都要记录下来，成为团队的运维知识", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 13
def ch13_bits():
    f = Fig("ch13_bits", 660, 252)
    rows = [("FP32", 8, 23, ["最大 3.4e38", "间隔 1.2e-7"]), ("BF16", 8, 7, ["最大 3.4e38", "间隔 7.8e-3"]),
            ("FP16", 5, 10, ["最大 65,504", "间隔 9.8e-4"]), ("FP8 E4M3", 4, 3, ["最大 448", "间隔 0.125"]),
            ("FP8 E5M2", 5, 2, ["最大 57,344", "间隔 0.25"])]
    bw = 13.6
    x0 = 82
    for r, (name, e, m, note) in enumerate(rows):
        y = 18 + r * 40
        f.text(x0 - 8, y + 16, name, 12, "end", INK, 700)
        cols = [GRAY] + [BLUE] * e + [ORANGE] * m
        for k, col in enumerate(cols):
            f.rect(x0 + k * bw, y, bw - 1.5, 22, col, "none", 0, 1.5)
        xe = x0 + 32 * bw
        f.text(xe + 10, y + 9, note[0], 10.5, "start", INK2)
        f.text(xe + 10, y + 22, note[1], 10.5, "start", INK2)
    # bf16 = top half of fp32
    f.poly([(x0 + 16 * bw, 14), (x0 + 16 * bw, 62)], RED, 1.2, "3 2")
    f.text(x0 + 16 * bw + 8, 74, ["← BF16 就是 FP32 的前 16 位：", "范围相同，尾数少了 16 位"], 10.5, "start", RED)
    legend(f, x0, 222, [("符号位", GRAY, "box"), ("指数位：决定范围", BLUE, "box"), ("尾数位：决定精度", ORANGE, "box")])
    f.text(330, 246, "“间隔”指 1.0 附近相邻两个可表示数的相对间隔（数据同上表）", 11.5, "middle", INK2)
    save(f)


def ch13_accum():
    import torch
    f = Fig("ch13_accum", 660, 272)
    # left: the bf16 grid around 4
    f.text(150, 18, "BF16 在 4 附近能表示的数", 12, "middle", INK, 700)
    lx0, lx1, v0, v1 = 20, 280, 3.94, 4.07
    X = lambda v: lx0 + (v - v0) / (v1 - v0) * (lx1 - lx0)
    f.line(lx0, 80, lx1, 80, INK3, 1.2)
    grid = [4 - 3 * 2 ** -6, 4 - 2 * 2 ** -6, 4 - 2 ** -6, 4.0, 4 + 2 ** -5, 4 + 2 * 2 ** -5]
    for g in grid:
        f.line(X(g), 72, X(g), 88, NAVY, 1.6)
    f.text(X(4.0), 104, "4", 12, "middle", INK, 700)
    f.text(X(4 + 2 ** -5), 104, "4.03125", 11, "middle", INK2)
    f.text(X(4 - 2 ** -6), 104, "3.984", 11, "middle", INK2)
    f.circle(X(4.01), 80, 4.5, RED, "#ffffff", 1.3)
    f.path(f"M{X(4.01):.1f},72 C{X(4.01):.1f},50 {X(4.0):.1f},50 {X(4.0) + 1:.1f},68", RED, 1.3, arrow=True)
    f.text(X(4.01) + 6, 48, "4 + 0.01：离 4 更近，舍入回 4", 11, "start", RED)
    f.text(150, 134, ["4 以上相邻两数相差 0.03125，", "加 0.01 不到半个间隔，", "结果永远停在 4"], 11.5, "middle", INK2)
    # right: accumulation curves (computed with torch, same setting as demo 3)
    n = 10000
    xs = list(range(0, n + 1, 50))
    curves = {}
    for dt in (torch.float32, torch.float16, torch.bfloat16):
        s = torch.zeros((), dtype=dt)
        a = torch.tensor(0.01, dtype=dt)
        vals = [0.0]
        for i in range(1, n + 1):
            s = s + a
            if i % 50 == 0:
                vals.append(float(s))
        curves[dt] = vals
    c = Chart(f, 360, 44, 220, 166, (0, n), (0, 110))
    c.axes([0, 5000, 10000], [0, 25, 50, 75, 100], xlabel="加了多少次 0.01", ylabel="累加结果", xfmt=lambda v: f"{v:,}", yfmt=lambda v: f"{v:g}", size=11)
    f.text(470, 18, "把 0.01 连续加 10,000 次", 12, "middle", INK, 700)
    for dt, col, lab in ((torch.float32, GREEN, "fp32：100.003"), (torch.float16, ORANGE, "fp16：停在 32"), (torch.bfloat16, RED, "bf16：停在 4")):
        c.series(xs, curves[dt], col, 2)
        f.text(c.X(n) + 6, c.Y(curves[dt][-1]) + 4, lab, 11, "start", col)
    f.text(330, 266, "大数吞小数（13.2 节演示 ③，曲线由 PyTorch 逐步累加得到）：所以矩阵乘法的累加必须用 fp32", 11.5, "middle", INK2)
    save(f)


def ch13_mixed():
    f = Fig("ch13_mixed", 660, 236)
    f.box(14, 30, 120, 44, ["fp32 主权重"], "Orange", 12.5)
    f.arrow(136, 52, 166, 52)
    f.text(151, 44, "转换", 10.5, "middle", INK2)
    f.box(168, 30, 104, 44, ["bf16 权重副本"], "blue", 12)
    f.arrow(274, 52, 304, 52)
    f.box(306, 26, 170, 52, ["前向：bf16 矩阵乘法、", "fp32 累加；softmax 等", "保留 fp32"], "blue", 11)
    f.arrow(478, 52, 508, 52)
    f.box(510, 30, 136, 44, ["loss（fp32）"], "orange", 12)
    f.arrow(578, 76, 578, 126)
    f.box(470, 128, 176, 44, ["反向：得到 bf16 梯度"], "blue", 12)
    f.arrow(468, 150, 412, 150)
    f.box(222, 128, 188, 44, ["fp32 优化器：Adam 的", "$m$、$v$ 都是 fp32"], "orange", 11.5)
    f.poly([(220, 150), (74, 150), (74, 76)], INK3, 1.4, arrow=True)
    f.text(148, 144, "更新主权重", 11, "middle", INK2)
    legend(f, 14, 206, [("fp32", ORANGE, "box"), ("bf16", BLUE_M, "box")])
    f.text(150, 206, "如果用 fp16：还要把 loss 乘以缩放因子 $S$，梯度再除回来（动态 loss scaling）", 11.5, "start", INK2)
    f.text(330, 230, "每个参数：bf16 权重 2 + bf16 梯度 2 + fp32 主权重 4 + $m$ 4 + $v$ 4 = 16 字节", 11.5, "middle", INK2)
    save(f)


def ch13_fp8():
    f = Fig("ch13_fp8", 660, 262)
    Ks = [1e2, 1e3, 1e4, 3e4, 1e5]
    tensor = [2.66, 2.65, 2.71, 3.97, 12.59]
    block = [2.57, 2.57, 2.57, 2.57, 2.64]
    c = Chart(f, 56, 30, 270, 170, (60, 1.6e5), (0, 14), xlog=True)
    c.axes(Ks[:3] + [1e5], [0, 4, 8, 12], xlabel="离群值大小 $K$（对数坐标）", ylabel="普通值的相对误差（%）",
           xfmt=lambda v: f"$10^{{{int(round(math.log10(v)))}}}$", yfmt=lambda v: f"{v:g}", size=11)
    c.series(Ks, tensor, RED, 2, markers=True)
    c.series(Ks, block, BLUE, 2, markers=True)
    f.text(c.X(1e5) - 8, c.Y(12.59) + 4, "整个张量共用一个缩放因子", 11, "end", RED)
    f.text(c.X(1e2), c.Y(2.6) + 16, "每 1×128 一块各用一个缩放因子", 11, "start", BLUE)
    # right: blocks schematic
    x0, y0 = 370, 40
    f.text(510, 22, "一行 1,024 个数，切成 8 块，每块 128 个", 11.5, "middle", INK, 700)
    for b in range(8):
        f.rect(x0 + b * 35, y0, 33, 26, RED_L if b == 5 else BLUE_L, RED if b == 5 else BLUE, 1, 2)
    f.circle(x0 + 5 * 35 + 16, y0 + 13, 5, RED, "none")
    f.text(x0 + 5 * 35 + 16, y0 + 44, "离群值", 11, "middle", RED)
    f.text(370, 112, ["共用一个缩放因子：为了装下离群值，", "缩放因子只能很小，普通值全被挤进", "FP8 的最低端，精度大量丢失。", "", "按块缩放：只有离群值所在的那一块", "受影响，其余 7 块照常使用全部精度"], 11.5, "start", INK2)
    f.text(330, 256, "FP8（E4M3）量化实验（实测，数据同上表）。DeepSeek-V3 对激活值用 1×128、对权重用 128×128 的块", 11.5, "middle", INK2)
    save(f)


def ch13_sround():
    import torch
    f = Fig("ch13_sround", 660, 272)
    # left: number line
    f.text(150, 18, "真实值落在两个可表示数之间", 12, "middle", INK, 700)
    a, b = 40, 260
    f.line(a - 10, 70, b + 10, 70, INK3, 1.2)
    for x, lab in ((a, "$a$"), (b, "$b$")):
        f.line(x, 62, x, 78, NAVY, 2)
        f.text(x, 96, lab, 13, "middle", INK)
    xv = a + 0.3 * (b - a)
    f.circle(xv, 70, 5, RED, "#ffffff", 1.3)
    f.text(xv, 52, "$x$（距 $a$ 30%）", 11.5, "middle", RED)
    f.text(20, 128, "就近舍入：总是得到 $a$", 12, "start", INK, 700)
    f.text(20, 146, "每次都往同一个方向偏，误差会累积", 11, "start", INK2)
    f.text(20, 176, "随机舍入：70% 得 $a$，30% 得 $b$", 12, "start", INK, 700)
    f.text(20, 194, "期望恰好等于 $x$，没有系统偏差", 11, "start", INK2)
    # right: demo 4 re-simulated
    torch.manual_seed(0)
    nw, steps = 10000, 1000
    def bf16_sr(x):
        u = x.view(torch.int32)
        r = torch.randint(0, 65536, u.shape, dtype=torch.int32)
        return ((u + r) & -65536).view(torch.float32)
    w_rn = torch.ones(1, dtype=torch.bfloat16)
    w_sr = torch.ones(nw, dtype=torch.float32)
    tr_fp, tr_rn, tr_sr = [1.0], [1.0], [1.0]
    w_fp = 1.0
    for s in range(1, steps + 1):
        w_fp -= 1e-4
        w_rn = (w_rn.float() - 1e-4).to(torch.bfloat16)
        w_sr = bf16_sr(w_sr - 1e-4)
        if s % 10 == 0:
            tr_fp.append(w_fp)
            tr_rn.append(float(w_rn[0]))
            tr_sr.append(float(w_sr.mean()))
    xs = list(range(0, steps + 1, 10))
    c = Chart(f, 350, 44, 180, 166, (0, steps), (0.88, 1.01))
    c.axes([0, 500, 1000], [0.88, 0.92, 0.96, 1.0], xlabel="更新次数（每次 $-10^{-4}$）", ylabel="权重", xfmt=lambda v: f"{v:,}", yfmt=lambda v: f"{v:.2f}", size=11)
    f.text(440, 18, "13.2 节演示 ④ 的过程", 12, "middle", INK, 700)
    c.series(xs, tr_rn, RED, 2)
    c.series(xs, tr_fp, GREEN, 3.2)
    c.series(xs, tr_sr, BLUE, 1.6, "4 3")
    f.text(c.X(steps) + 6, c.Y(tr_rn[-1]) + 4, ["bf16 就近舍入：", "停在 1.0"], 11, "start", RED)
    f.text(c.X(steps) + 6, c.Y(0.955), ["fp32（实线）与", "bf16 随机舍入", "（虚线，1 万个", "权重的平均）", "几乎重合"], 11, "start", INK2)
    f.text(330, 266, f"右图按演示 ④ 的设置重新模拟（随机舍入的平均终值 {tr_sr[-1]:.4f}，与正文的 0.9001 一致）", 11.5, "middle", INK2)
    save(f)


if __name__ == "__main__":
    for fn in [ch10_power, ch10_isoflop, ch10_flat, ch10_tokens, ch10_breakeven, ch10_emerge,
               ch11_sum, ch11_lrsweep, ch11_bcrit, ch11_wsd,
               ch12_spike, ch12_adam, ch12_ortho, ch12_sv, ch12_flow,
               ch13_bits, ch13_accum, ch13_mixed, ch13_fp8, ch13_sround]:
        fn()
    print("ok")
