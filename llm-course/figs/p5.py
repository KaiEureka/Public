"""Figures for Part 5 (chapters 18-23). Run: python3 figs/p5.py"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import *

OUT = os.path.dirname(os.path.abspath(__file__))
IDLE, IDLE_S = "#f1f4f7", "#d5dde5"
GPUC = [BLUE, ORANGE, GREEN, PURPLE]


def clipped(c, xs, ys, color, sw=2, dash=None):
    """Polyline restricted to the chart's (log) y-range."""
    lo, hi = c.ylim
    pts = [(x, y) for x, y in zip(xs, ys) if lo <= y <= hi]
    if len(pts) > 1:
        c.f.poly([(c.X(x), c.Y(y)) for x, y in pts], color, sw, dash)


def save(f):
    f.save(os.path.join(OUT, f.name + ".svg"))


def shade(t):
    a, b = (0xe8, 0xef, 0xf6), (0x0f, 0x27, 0x40)
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ----------------------------------------------------------------- chapter 18
def ch18_bw():
    f = Fig("ch18_bw", 660, 196)
    rows = [("GPU ↔ 自己的显存（HBM）", 3350, "约 67 倍"), ("GPU ↔ 本机其他 GPU（NVLink）", 450, "约 9 倍"),
            ("GPU ↔ CPU、网卡（PCIe Gen5）", 64, "约 1.3 倍"), ("GPU ↔ 其他机器（网卡）", 50, "1 倍")]
    c = Chart(f, 210, 14, 360, 136, (10, 5000), (0, 4), xlog=True)
    for t in [10, 100, 1000]:
        f.line(c.X(t), c.y0, c.X(t), c.y0 + c.h, GRID, 1)
        f.text(c.X(t), c.y0 + c.h + 16, f"{t:,}", 11, "middle", INK2)
    f.text(c.x0 + c.w / 2, c.y0 + c.h + 34, "单方向带宽（GB/s，对数坐标）", 11.5, "middle", INK2)
    for i, (lab, v, rel) in enumerate(rows):
        yc = c.y0 + (i + 0.5) * c.h / 4
        f.text(c.x0 - 8, yc + 4, lab, 11.5, "end", INK)
        f.rect(c.x0, yc - 11, c.X(v) - c.x0, 22, BLUE if i < 2 else ORANGE, "none", 0, 2)
        f.text(c.X(v) + 6, yc + 4, f"{v:,}", 11.5, "start", INK, 700)
        f.text(650, yc + 4, rel, 11, "end", INK2)
    f.text(650, 10, "相对跨机网络", 10.5, "end", INK3)
    save(f)


def ch18_rail():
    f = Fig("ch18_rail", 660, 272)
    nsv, ng = 4, 4
    spine_x = [230, 430]
    for x in spine_x:
        f.box(x - 50, 14, 100, 28, "脊交换机", "Navy", 11.5)
    leaf_x = [100 + k * 153 for k in range(ng)]
    for k, x in enumerate(leaf_x):
        f.box(x - 52, 82, 104, 30, f"轨道 {k} 叶交换机", "white", 11)
        f.rect(x - 52, 82, 6, 30, GPUC[k], "none", 0, 2)
        for sx in spine_x:
            f.line(x, 82, sx, 42, GRAY, 1)
    for s in range(nsv):
        x0 = 14 + s * 160
        f.rect(x0, 168, 150, 62, GRAY_L, GRAY, 1, 4)
        f.text(x0 + 75, 246, f"服务器 {s}", 11, "middle", INK2)
        f.line(x0 + 14, 216, x0 + 136, 216, NAVY, 3)
        for g in range(ng):
            gx = x0 + 12 + g * 34
            f.rect(gx, 178, 26, 30, GPUC[g], "none", 0, 3)
            f.text(gx + 13, 198, f"{g}", 11, "middle", "#ffffff", 700)
            f.line(gx + 13, 176, leaf_x[g], 114, GPUC[g], 1.2)
    f.text(14 + 3 * 160 + 140, 226, "NVLink", 10, "end", NAVY)
    f.text(330, 266, "示意：每台服务器只画了 4 张卡（实际 8 张）。编号相同的 GPU 接到同一条轨道，跨机通信一跳就到", 11.5, "middle", INK2)
    save(f)


def ch18_fail():
    f = Fig("ch18_fail", 660, 266)
    rate = 419 / (54 * 24 * 16384)  # unexpected interruptions per GPU-hour, Llama 3 405B
    c = Chart(f, 64, 30, 340, 170, (1000, 200000), (0.2, 100), xlog=True, ylog=True)
    c.axes([1000, 10000, 100000], [1, 10, 100], xlabel="集群的 GPU 数（对数坐标）", ylabel="平均多少小时中断一次（对数坐标）",
           xfmt=lambda v: f"{v:,}", yfmt=lambda v: f"{v:g}", size=11)
    xs = [1000 * 10 ** (i / 20) for i in range(47)]
    c.series(xs, [1 / (rate * n) for n in xs], BLUE, 2)
    c.dots([16384], [1 / (rate * 16384)], RED, 4.4)
    f.text(c.X(16384) + 8, c.Y(1 / (rate * 16384)) - 6, "Llama 3：1.6 万卡，约 3 小时", 11, "start", RED)
    f.text(c.X(1024) + 10, c.Y(1 / (rate * 1024)) - 4, f"1,024 卡：约 {1 / (rate * 1024):.0f} 小时", 11, "start", INK2)
    f.text(c.X(100000) - 6, c.Y(1 / (rate * 100000)) + 18, f"10 万卡：约 {60 / (rate * 100000):.0f} 分钟", 11, "end", INK2)
    # causes
    x0, y0, w = 440, 46, 200
    f.text(x0, 30, "419 次意外中断的原因", 11.5, "start", INK, 700)
    parts = [("GPU 故障 约 30%", 30, RED), ("显存故障 约 17%", 17, ORANGE), ("其他硬件 约 31%", 31, ORANGE_M), ("非硬件 约 22%", 22, GRAY)]
    y = y0
    for lab, v, col in parts:
        h = 1.4 * v
        f.rect(x0, y, 26, h - 2, col, "none", 0, 2)
        f.text(x0 + 34, y + h / 2 + 4, lab, 11, "start", INK)
        y += h
    f.text(x0, y + 18, ["确认或怀疑是硬件问题的", "合计约 78%"], 11, "start", INK2)
    f.text(330, 260, "左：按 Llama 3 405B 的中断率（每 GPU 每小时相同）线性外推的估算；右：Llama 3 报告的原因分布", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 19
def mini(f, x, y, cols, cw=15, ch=11, gap=3):
    """cols: list of 4 lists of (fill, text)."""
    for g, cells in enumerate(cols):
        for k, (fill, txt) in enumerate(cells):
            cx, cy = x + g * (cw + gap), y + (3 - k) * (ch + 2)
            f.rect(cx, cy, cw, ch, fill, "none", 0, 1.5)
            if txt:
                f.text(cx + cw / 2, cy + ch - 2, txt, 8.5, "middle", "#ffffff")
    for g in range(4):
        f.text(x + g * (cw + gap) + cw / 2, y + 4 * (ch + 2) + 10, str(g), 9, "middle", INK3)


def ch19_ops():
    f = Fig("ch19_ops", 660, 300)
    S = (NAVY, "Σ")
    E = []
    ops = [
        ("broadcast", [[(BLUE, "")], [], [], []], [[(BLUE, "")]] * 4),
        ("reduce", [[(c, "")] for c in GPUC], [[S], [], [], []]),
        ("all-reduce", [[(c, "")] for c in GPUC], [[S]] * 4),
        ("reduce-scatter", [[(c, "")] * 4 for c in GPUC], [[S if k == g else (IDLE, "") for k in range(4)] for g in range(4)]),
        ("all-gather", [[(GPUC[g], "") if k == g else (IDLE, "") for k in range(4)] for g in range(4)], [[(GPUC[k], "") for k in range(4)]] * 4),
        ("all-to-all", [[(GPUC[g], str(k)) for k in range(4)] for g in range(4)], [[(GPUC[k], str(g)) for k in range(4)] for g in range(4)]),
    ]
    descs = ["GPU 0 的数据复制到每张卡", "求和，只有 GPU 0 得到结果", "求和，每张卡都得到结果", "求和后切成 4 份，每卡一份",
             "每卡一份，拼成完整的给每张卡", "每卡把第 k 份发给 GPU k"]
    for i, (name, before, after) in enumerate(ops):
        px, py = 10 + (i % 3) * 218, 14 + (i // 3) * 140
        f.text(px + 100, py + 8, name, 12, "middle", INK, 700)
        f.text(px + 100, py + 24, descs[i], 10, "middle", INK2)
        mini(f, px + 10, py + 34, before)
        f.arrow(px + 92, py + 60, px + 112, py + 60, INK3, 1.2)
        mini(f, px + 120, py + 34, after)
    f.text(330, 292, "4 张 GPU（每列一张，编号在下方）。颜色表示数据来自哪张卡，Σ 表示多张卡的数据求和；all-to-all 里的数字是目的地", 11, "middle", INK2)
    save(f)


def ring_states(n=4):
    cnt = [[{r} for _ in range(n)] for r in range(n)]
    states = [[[len(c) for c in row] for row in cnt]]
    for s in range(n - 1):
        new = [[set(c) for c in row] for row in cnt]
        for r in range(n):
            c = (r - s) % n
            new[(r + 1) % n][c] |= cnt[r][c]
        cnt = new
        states.append([[len(c) for c in row] for row in cnt])
    for s in range(n - 1):
        new = [[set(c) for c in row] for row in cnt]
        for r in range(n):
            c = (r + 1 - s) % n
            new[(r + 1) % n][c] = set(cnt[r][c])
        cnt = new
        states.append([[len(c) for c in row] for row in cnt])
    return states


def ch19_ring():
    f = Fig("ch19_ring", 660, 214)
    st = ring_states()
    titles = ["初始", "第 1 步", "第 2 步", "第 3 步", "第 1 步", "第 2 步", "第 3 步"]
    cw = 15
    for i, grid in enumerate(st):
        x0 = 48 + i * 88
        f.text(x0 + 2 * cw + 2, 50, titles[i], 11, "middle", INK, 700)
        for r in range(4):
            if i == 0:
                f.text(x0 - 6, 70 + r * 18, f"GPU {r}", 10, "end", INK2)
            for c in range(4):
                v = grid[r][c]
                fill = shade((v - 1) / 3)
                f.rect(x0 + c * (cw + 1), 59 + r * 18, cw, 16, fill, "none", 0, 1.5)
                f.text(x0 + c * (cw + 1) + cw / 2, 71 + r * 18, str(v), 10, "middle", "#ffffff" if v >= 3 else INK)
        if i < 6:
            f.arrow(x0 + 66, 95, x0 + 82, 95, INK3, 1.1)
    f.brace_h(48 + 88, 48 + 3 * 88 + 64, 40, None, BLUE, up=True)
    f.text(48 + 2 * 88 + 32, 22, "reduce-scatter：把一块传给下一张卡，对方累加", 11, "middle", BLUE)
    f.brace_h(48 + 4 * 88, 48 + 6 * 88 + 64, 40, None, GREEN, up=True)
    f.text(48 + 5 * 88 + 32, 22, "all-gather：传递求和完毕的块，对方覆盖", 11, "middle", GREEN)
    f.text(330, 160, "每个格子：这张 GPU（行）上这一块数据（列）已经累加了几张卡的贡献。4 = 求和完毕", 11.5, "middle", INK2)
    f.text(330, 180, "reduce-scatter 3 步后，每张卡恰好有一块是 4；all-gather 3 步后全部是 4", 11.5, "middle", INK2)
    f.text(330, 202, "与 19.4 节实验表中的数值逐格对应（例如 GPU 0 第 3 步后第 1 块 = 2222，即 4 张卡的和）", 11, "middle", INK3)
    save(f)


def ch19_ab():
    f = Fig("ch19_ab", 660, 268)
    n, alpha, beta = 512, 5e-6, 50e9
    c = Chart(f, 64, 26, 400, 180, (1e3, 1e10), (0.01, 1000), xlog=True, ylog=True)
    lab = {1e3: "1 KB", 1e4: "", 1e5: "", 1e6: "1 MB", 1e7: "", 1e8: "", 1e9: "1 GB", 1e10: "10 GB"}
    c.axes(list(lab), [0.01, 0.1, 1, 10, 100, 1000], xlabel="每张卡要 all-reduce 的数据量", ylabel="耗时（毫秒，对数坐标）",
           xfmt=lambda v: lab[v], yfmt=lambda v: f"{v:g}", size=11)
    xs = [10 ** (3 + i / 10) for i in range(71)]
    lat = 2 * (n - 1) * alpha * 1e3
    bw = [2 * (n - 1) / n * s / beta * 1e3 for s in xs]
    c.series(xs, [lat] * len(xs), GRAY, 1.4, "5 3")
    clipped(c, xs, bw, ORANGE, 1.4, "5 3")
    c.series(xs, [lat + b for b in bw], BLUE, 2.4)
    for s in (1e6, 1e9):
        t = lat + 2 * (n - 1) / n * s / beta * 1e3
        c.dots([s], [t], RED, 4)
    f.text(c.X(1e6), c.Y(5.15) - 10, "1 MB：5.15 ms，延迟占主导", 11, "middle", RED)
    f.text(c.X(1e9) - 6, c.Y(45) - 10, "1 GB：45 ms，带宽占主导", 11, "end", RED)
    f.text(c.X(1e3) + 4, c.Y(lat) + 16, "延迟项 $2(n-1)\\alpha$ = 5.11 ms", 11, "start", INK2)
    f.text(c.X(1e8) + 8, c.Y(2), "带宽项 ∝ 数据量", 11, "start", ORANGE)
    f.text(480, 60, ["环形 all-reduce：", "$n$ = 512 张卡，", "$\\alpha$ = 5 μs，", "带宽 50 GB/s"], 11.5, "start", INK2)
    f.text(480, 140, ["小消息：耗时几乎不随", "数据量变化；", "大消息：耗时与数据量", "成正比"], 11.5, "start", INK2)
    f.text(330, 262, "按 α-β 模型计算（数据同附录 D 习题答案）", 11.5, "middle", INK2)
    save(f)


def ch19_hier():
    f = Fig("ch19_hier", 660, 264)
    for m in range(2):
        y0 = 30 + m * 76
        f.rect(10, y0, 300, 54, GRAY_L, GRAY, 1, 4)
        f.text(16, y0 + 14, f"机器 {m}", 10.5, "start", INK2)
        for g in range(8):
            gx = 24 + g * 34
            f.rect(gx, y0 + 20, 26, 24, BLUE if g != 3 else ORANGE, "none", 0, 3)
            f.text(gx + 13, y0 + 37, str(g), 10.5, "middle", "#ffffff", 700)
        f.line(22, y0 + 50, 298, y0 + 50, NAVY, 2.5)
    f.text(160, 96, "……共 8 台机器……", 10.5, "middle", INK3)
    f.line(24 + 3 * 34 + 13, 74, 24 + 3 * 34 + 13, 126, ORANGE, 2, "4 2")
    steps = [("① 机器内 reduce-scatter", "NVLink 450 GB/s，约 27 ms", BLUE),
             ("② 编号相同的卡跨机 all-reduce", "网卡 50 GB/s，每组只处理 1/8，约 61 ms", ORANGE),
             ("③ 机器内 all-gather", "NVLink 450 GB/s，约 27 ms", BLUE)]
    for k, (a, b, col) in enumerate(steps):
        y = 188 + k * 22
        f.text(10, y, a, 11.5, "start", col, 700)
        f.text(206, y, b, 11, "start", INK2)
    # comparison bars
    c = Chart(f, 400, 40, 240, 110, (0, 600), (0, 2))
    for t in [0, 200, 400, 600]:
        f.line(c.X(t), c.y0, c.X(t), c.y0 + c.h, GRID, 1)
        f.text(c.X(t), c.y0 + c.h + 14, f"{t}", 10.5, "middle", INK2)
    f.text(c.x0 + c.w / 2, c.y0 + c.h + 30, "耗时（毫秒）", 11, "middle", INK2)
    y1 = c.y0 + 0.5 * c.h / 2
    x = c.x0
    for v, col in ((27, BLUE), (61, ORANGE), (27, BLUE)):
        f.rect(x, y1 - 14, c.X(v) - c.x0, 28, col, "#ffffff", 1, 0)
        x += c.X(v) - c.x0
    f.text(x + 6, y1 + 4, "分层：约 115 ms", 11.5, "start", INK, 700)
    y2 = c.y0 + 1.5 * c.h / 2
    f.rect(c.x0, y2 - 14, c.X(551) - c.x0, 28, RED, "none", 0, 0)
    f.text(c.X(551) - 6, y2 + 4, "全走网络：约 551 ms", 11.5, "end", "#ffffff", 700)
    f.text(520, 22, "64 张卡 all-reduce 14 GB", 11.5, "middle", INK, 700)
    f.text(330, 258, "分层 all-reduce：重活交给机器内部的 NVLink，跨机器的链路只承担 1/8 的数据（估算同上表）", 11.5, "middle", INK2)
    save(f)


def ch19_overlap():
    f = Fig("ch19_overlap", 660, 230)
    u = 22
    def row(y, items, label):
        f.text(118, y + 15, label, 11, "end", INK2)
        for x, w, txt, col in items:
            f.rect(126 + x * u, y, w * u - 2, 22, col, "none", 0, 3)
            if txt:
                f.text(126 + x * u + (w * u - 2) / 2, y + 15, txt, 10, "middle", "#ffffff")
    f.text(10, 18, "不重叠：算完全部梯度再通信", 11.5, "start", INK, 700)
    row(26, [(k, 1, f"L{8 - k}", GREEN) for k in range(8)], "计算")
    row(52, [(8, 8, "all-reduce 全部梯度", ORANGE)], "通信")
    f.text(10, 108, "分桶重叠：每个桶的梯度一算好就开始通信", 11.5, "start", INK, 700)
    row(116, [(k, 1, f"L{8 - k}", GREEN) for k in range(8)], "计算")
    row(142, [(2 + 2 * k, 2, f"桶 {k + 1}", ORANGE) for k in range(4)], "通信")
    f.line(126 + 16 * u, 20, 126 + 16 * u, 80, RED, 1.2, "4 3")
    f.line(126 + 10 * u, 110, 126 + 10 * u, 170, RED, 1.2, "4 3")
    f.text(126 + 10 * u + 6, 182, "这一步结束", 11, "start", RED)
    f.text(126 + 16 * u + 6, 92, "这一步结束", 11, "start", RED)
    f.text(330, 208, "反向传播从最后一层算起（L8 → L1）。通信在另一条 CUDA stream 上运行，可以和计算同时进行；", 11.5, "middle", INK2)
    f.text(330, 224, "PyTorch DDP 默认每个桶约 25 MB（示意，时间长度为假设）", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 20
def ch20_dp():
    f = Fig("ch20_dp", 660, 222)
    f.text(46, 16, "全局 batch", 11.5, "middle", INK, 700)
    for g in range(4):
        y = 26 + g * 44
        f.rect(16, y, 60, 36, GPUC[g], "none", 0, 2)
        f.text(46, y + 22, f"数据 {g + 1}", 11, "middle", "#ffffff")
        f.arrow(78, y + 18, 104, y + 18, INK3, 1.2)
        f.box(106, y, 150, 36, f"GPU {g}：完整的模型副本", "blue", 11)
        f.arrow(258, y + 18, 284, y + 18, INK3, 1.2)
        f.box(286, y, 70, 36, f"梯度 $g_{g + 1}$", "white", 11.5)
        f.arrow(358, y + 18, 384, y + 18, INK3, 1.2)
        f.arrow(442, y + 18, 468, y + 18, INK3, 1.2)
        f.box(470, y, 180, 36, "用平均梯度做相同的更新", "green", 11)
    f.rect(386, 26, 54, 168, ORANGE_L, ORANGE, 1.4, 4)
    f.text(413, 100, "all-", 11.5, "middle", INK, 700)
    f.text(413, 116, "reduce", 11.5, "middle", INK, 700)
    f.text(413, 134, "求平均", 11, "middle", INK2)
    f.text(330, 216, "数据并行：每张卡存一份完整的模型，各算各的数据，梯度求平均后同步更新，所以模型始终一致", 11.5, "middle", INK2)
    save(f)


def ch20_zero():
    f = Fig("ch20_zero", 660, 250)
    rows = [("普通数据并行", (0, 0, 0), "1,120 GB"), ("ZeRO-1", (0, 0, 1), "293 GB"), ("ZeRO-2", (0, 1, 1), "155 GB"), ("ZeRO-3", (1, 1, 1), "17.5 GB")]
    comps = [(2, BLUE), (2, ORANGE), (12, GREEN)]
    unit = 6
    f.text(570, 18, ["70B，64 张卡时", "每张卡的模型状态"], 10.5, "middle", INK2)
    for r, (name, shard, gb) in enumerate(rows):
        y = 44 + r * 44
        f.text(98, y + 16, name, 11.5, "end", INK, 700)
        for g in range(4):
            x = 108 + g * 112
            for (sz, col), sh in zip(comps, shard):
                w = sz * unit
                if sh:
                    f.rect(x, y, w, 22, GRAY_L, "none", 0, 1)
                    f.rect(x + g * w / 4, y, w / 4, 22, col, "none", 0, 1)
                else:
                    f.rect(x, y, w, 22, col, "none", 0, 1)
                x += w
        f.text(570, y + 16, gb, 12, "middle", INK, 700)
    for g in range(4):
        f.text(108 + g * 112 + 48, 36, f"GPU {g}", 10.5, "middle", INK2)
    legend(f, 108, 226, [("参数 2Ψ", BLUE, "box"), ("梯度 2Ψ", ORANGE, "box"), ("优化器状态 12Ψ", GREEN, "box"), ("切分后不存的部分", GRAY_L, "box")])
    f.text(330, 246, "每张卡要存什么（4 张卡示意）：ZeRO 逐步把优化器状态、梯度、参数切成 n 份，每张卡只存自己那一份", 11, "middle", INK2)
    save(f)


def ch20_zero3():
    f = Fig("ch20_zero3", 660, 196)
    u = 46
    def blk(row, x, w, txt, col, y0=0):
        y = 34 + row * 34 + y0
        f.rect(130 + x * u, y, w * u - 3, 26, col, "none", 0, 3)
        f.text(130 + x * u + (w * u - 3) / 2, y + 17, txt, 10.5, "middle", "#ffffff")
    f.text(122, 51, "通信", 11, "end", INK2)
    f.text(122, 85, "计算", 11, "end", INK2)
    for k in range(4):
        blk(0, k * 1.2, 1.2, f"拼参数 {k + 1}", ORANGE)
        blk(1, (k + 1) * 1.2, 1.2, f"前向 {k + 1}", BLUE)
    f.text(130, 22, "前向：all-gather 第 k 层的完整参数 → 计算 → 立即释放；算第 k 层时预取第 k+1 层", 11, "start", INK)
    f.text(130, 140, "反向：再 all-gather 一次参数 → 算梯度 → reduce-scatter 把梯度分给各卡 → 释放", 11, "start", INK)
    f.text(130, 162, "通信量约 3Ψ，是数据并行的 1.5 倍；显存峰值 ≈ 自己的切片 + 一两个完整 block", 11, "start", INK2)
    f.text(330, 190, "ZeRO-3 / FSDP 的前向过程（示意）：拼参数和计算错开一步，通信被计算掩盖", 11.5, "middle", INK2)
    save(f)


def ch20_recompute():
    f = Fig("ch20_recompute", 660, 250)
    L = 8
    for r, (title, full) in enumerate((("不重新计算：每层内部的中间结果都存着", True), ("重新计算：只存每层的输入", False))):
        y = 30 + r * 96
        f.text(10, y - 10, title, 11.5, "start", INK, 700)
        for k in range(L):
            x = 10 + k * 50
            f.box(x, y + 40, 42, 22, f"层 {k + 1}", "white", 10.5)
            if full:
                for j in range(4):
                    f.rect(x + 4, y + 32 - j * 9, 34, 7, ORANGE, "none", 0, 1)
            else:
                f.rect(x + 4, y + 32, 34, 7, ORANGE, "none", 0, 1)
            if k < L - 1:
                f.arrow(x + 42, y + 51, x + 50, y + 51, INK3, 1)
        if not full:
            f.path(f"M{10 + 5 * 50 + 21},{y + 64} C{10 + 5 * 50 + 21},{y + 82} {10 + 5 * 50 + 61},{y + 82} {10 + 5 * 50 + 61},{y + 64}", RED, 1.3, arrow=True)
            f.text(10 + 5 * 50 + 41, y + 98, "反向算到这层时，用存下的输入把它重算一遍", 10.5, "middle", RED)
    c = Chart(f, 440, 40, 200, 120, (0, 100), (0, 2))
    for i, (lab, v, col) in enumerate((("不重算", 91, ORANGE), ("重算", 6.5, GREEN))):
        yc = c.y0 + (i + 0.5) * c.h / 2
        f.rect(c.x0 + 40, yc - 14, (v / 100) * (c.w - 90), 28, col, "none", 0, 2)
        f.text(c.x0 + 34, yc + 4, lab, 11, "end", INK)
        f.text(c.x0 + 40 + (v / 100) * (c.w - 90) + 4, yc + 4, f"{v:g} GB", 11.5, "start", INK, 700)
    f.text(c.x0 + 20, 26, ["70B 级模型，一条 4K 序列", "的激活值"], 10.5, "start", INK2)
    f.text(330, 244, "代价：多做一次前向，总计算量从 $6ND$ 变成约 $8ND$（每层激活值约 $34Tbd$ 字节，数据同正文）", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 21
def ch21_tp():
    f = Fig("ch21_tp", 660, 238)
    f.box(10, 92, 50, 40, "$X$", "white", 13)
    for g, y in ((0, 30), (1, 140)):
        col = GPUC[g]
        f.poly([(62, 112), (80, 112), (80, y + 26), (94, y + 26)], INK3, 1.2, arrow=True)
        f.text(96, y - 4, f"GPU {g}", 11, "start", col, 700)
        f.box(96, y + 6, 92, 40, f"$XA_{g + 1}$", "white", 12)
        f.rect(96, y + 6, 6, 40, col, "none", 0, 2)
        f.arrow(190, y + 26, 210, y + 26, INK3, 1.2)
        f.box(212, y + 6, 70, 40, "GELU", "orange", 11.5)
        f.arrow(284, y + 26, 304, y + 26, INK3, 1.2)
        f.box(306, y + 6, 92, 40, f"乘 $B_{g + 1}$", "white", 12)
        f.rect(306, y + 6, 6, 40, col, "none", 0, 2)
        f.arrow(400, y + 26, 420, y + 26, INK3, 1.2)
        f.box(422, y + 6, 76, 40, f"部分和 $Y_{g + 1}$", "white", 11)
        f.poly([(500, y + 26), (516, y + 26), (516, 112), (528, 112)], INK3, 1.2, arrow=True)
    f.box(530, 88, 120, 48, ["all-reduce", "$Y = Y_1 + Y_2$"], "Orange", 11.5)
    f.text(240, 112, "中间不需要任何通信", 11, "middle", GREEN, 700)
    f.text(140, 214, "$A$ 按列切：每张卡得到隐藏层中不重叠的一段", 11, "middle", INK2)
    f.text(450, 214, "$B$ 按行切：每张卡用自己那段去乘对应的行", 11, "middle", INK2)
    f.text(330, 232, "张量并行切分 MLP（$t$ = 2 示意）：每层前向只在最后做一次 all-reduce", 11.5, "middle", INK2)
    save(f)


def ch21_cp():
    f = Fig("ch21_cp", 660, 222)
    n, cs = 8, 17
    for p, (title, owner) in enumerate((("按顺序切：第 i 张卡拿第 2i、2i+1 块", lambda r: r // 2),
                                         ("一前一后搭配：第 i 张卡拿第 i 块和第 7−i 块", lambda r: r if r < 4 else 7 - r))):
        x0 = 30 + p * 330
        f.text(x0 + 130, 18, title, 11.5, "middle", INK, 700)
        for r in range(n):
            g = owner(r)
            for c in range(n):
                fill = GPUC[g] if c <= r else "#ffffff"
                f.rect(x0 + c * cs, 30 + r * cs, cs - 2, cs - 2, fill, "none" if c <= r else IDLE_S, 0.6, 1.5)
            f.text(x0 + n * cs + 6, 30 + r * cs + 12, f"GPU {g}", 9.5, "start", INK3)
        work = [0] * 4
        for r in range(n):
            work[owner(r)] += r + 1
        bx = x0 + 200
        f.text(bx, 40, "计算量（块数）", 10.5, "start", INK2)
        for g in range(4):
            y = 52 + g * 24
            f.rect(bx, y, work[g] * 5, 16, GPUC[g], "none", 0, 2)
            f.text(bx + work[g] * 5 + 4, y + 12, str(work[g]), 10.5, "start", INK)
    f.text(330, 194, "因果注意力矩阵按行切成 2 × CP = 8 块（CP = 4）。每行越往下，要看的 K/V 越多，计算量越大。", 11.5, "middle", INK2)
    f.text(330, 212, "按顺序切，最后一张卡的活是第一张的 5 倍；一前一后搭配，每张卡都是 9 块", 11.5, "middle", INK2)
    save(f)


def sched_1f1b(p, m):
    ops = []
    for s in range(p):
        w = min(p - s - 1, m)
        seq = [("F", i) for i in range(w)]
        fi, bi = w, 0
        while fi < m:
            seq.append(("F", fi)); fi += 1
            seq.append(("B", bi)); bi += 1
        while bi < m:
            seq.append(("B", bi)); bi += 1
        ops.append(seq)
    end, pos, free = {}, [0] * p, [0] * p
    done = 0
    while done < p * 2 * m:
        progress = False
        for s in range(p):
            if pos[s] >= len(ops[s]):
                continue
            kind, i = ops[s][pos[s]]
            dep = ("F", s - 1, i) if kind == "F" and s > 0 else (("B", s + 1, i) if kind == "B" and s < p - 1 else ("F", s, i) if kind == "B" else None)
            if dep is not None and dep not in end:
                continue
            t0 = max(free[s], end[dep] if dep else 0)
            end[(kind, s, i)] = t0 + 1
            free[s] = t0 + 1
            pos[s] += 1
            done += 1
            progress = True
        assert progress
    return end


def ch21_1f1b():
    p, m = 4, 8
    end = sched_1f1b(p, m)
    T = max(end.values())
    f = Fig("ch21_1f1b", 660, 212)
    u, x0 = 26, 76
    for t in range(T + 1):
        f.text(x0 + t * u, 16, str(t), 9.5, "middle", INK3) if t % 2 == 0 else None
    for s in range(p):
        y = 24 + s * 32
        f.text(x0 - 8, y + 18, f"阶段 {s}", 11, "end", INK)
        busy = set()
        for (kind, ss, i), e in end.items():
            if ss != s:
                continue
            busy.add(e - 1)
            f.rect(x0 + (e - 1) * u, y, u - 3, 26, BLUE if kind == "F" else GREEN, "none", 0, 3)
            f.text(x0 + (e - 1) * u + (u - 3) / 2, y + 17, f"{kind}{i + 1}", 10, "middle", "#ffffff")
        for t in range(T):
            if t not in busy:
                f.rect(x0 + t * u, y, u - 3, 26, IDLE, IDLE_S, 1, 3)
    f.text(x0, 170, f"总长 {T} 个单位，其中每个阶段空等 {T - 2 * m} 个：气泡 = {T - 2 * m}/{T} ≈ {(T - 2 * m) / T:.0%}，与 GPipe 相同", 11.5, "start", INK2)
    f.text(x0, 190, "但阶段 0 同一时刻最多只保存 4 个 micro-batch 的激活值（= $p$），GPipe 要存 8 个（= $m$）", 11.5, "start", INK2)
    f.text(330, 208, "1F1B 调度（4 个阶段，8 个 micro-batch，前向和反向都按 1 个单位时间计）", 11, "middle", INK3)
    save(f)


def ch21_bubble():
    f = Fig("ch21_bubble", 660, 262)
    c = Chart(f, 60, 26, 400, 180, (1, 128), (0, 1), xlog=True)
    c.axes([1, 2, 4, 8, 16, 32, 64, 128], [0, 0.25, 0.5, 0.75, 1], xlabel="每步的 micro-batch 数 $m$（对数坐标）",
           ylabel="气泡占总时间的比例", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0%}", size=11)
    ms = [2 ** (i / 10) for i in range(71)]
    for pp, col in ((4, BLUE_M), (8, BLUE), (16, NAVY)):
        ys = [(pp - 1) / (m + pp - 1) for m in ms]
        c.series(ms, ys, col, 2)
        v6 = (pp - 1) / (6 + pp - 1)
        f.text(c.X(6) + 6, c.Y(v6) - 6, f"$p$ = {pp}", 11, "start", col)
    ys = [(8 - 1) / (4 * m + 8 - 1) for m in ms]
    c.series(ms, ys, ORANGE, 2, "5 3")
    f.text(c.X(1.08), c.Y(0.3), "$p$ = 8，交错调度 $v$ = 4", 11, "start", ORANGE)
    for m, pp in ((64, 16), (32, 8)):
        v = (pp - 1) / (m + pp - 1)
        c.dots([m], [v], RED, 4)
    f.text(c.X(64), c.Y(15 / 79) - 10, "$p$ = 16，$m$ = 64：19%", 10.5, "middle", RED)
    f.text(c.X(32) - 6, c.Y(7 / 39) + 18, "$p$ = 8，$m$ = 32：18%", 10.5, "end", RED)
    f.text(330, 256, "气泡比例 $(p-1)/(m+p-1)$；交错调度约为 $(p-1)/(vm+p-1)$。$m$ 至少要比 $p$ 大好几倍", 11.5, "middle", INK2)
    save(f)


def ch21_layout():
    f = Fig("ch21_layout", 660, 252)
    f.rect(10, 26, 520, 186, "#fbfcfd", NAVY, 1.6, 8)
    f.text(20, 44, "DP = 128 份（最外层，每步同步一次梯度，可以跨 pod）", 11.5, "start", NAVY, 700)
    f.rect(24, 56, 492, 140, BLUE_L, BLUE, 1.2, 6)
    f.text(34, 74, "一个模型副本：PP = 16 个阶段（点对点传激活值，可以跨机器）", 11, "start", BLUE, 700)
    for k in range(4):
        x = 36 + k * 120
        if k == 3:
            f.text(x + 50, 140, "……", 14, "middle", INK3)
            continue
        f.rect(x, 86, 106, 98, "#ffffff", ORANGE, 1.2, 4)
        f.text(x + 53, 102, f"阶段 {k + 1}：一台机器", 10.5, "middle", ORANGE, 700)
        f.text(x + 53, 118, "TP = 8（NVLink）", 10.5, "middle", INK2)
        for g in range(8):
            gx, gy = x + 9 + (g % 4) * 23, 128 + (g // 4) * 26
            f.rect(gx, gy, 19, 20, ORANGE, "none", 0, 2)
        if k < 2:
            f.arrow(x + 106, 135, x + 120, 135, INK3, 1.2)
    f.text(560, 40, "带宽", 11.5, "middle", INK, 700)
    f.arrow(560, 52, 560, 196, INK3, 1.4)
    f.text(568, 66, "高：TP", 11, "start", ORANGE)
    f.text(568, 118, "中：PP", 11, "start", BLUE)
    f.text(568, 190, "低：DP", 11, "start", NAVY)
    f.text(330, 230, "Llama 3 405B 的 8K 预训练阶段：8 × 16 × 128 = 16,384 张卡（CP = 1）。排列从内到外是 TP → CP → PP → DP，", 11, "middle", INK2)
    f.text(330, 246, "与带宽层级一一对应；128K 阶段改为 TP 8、CP 16、PP 16、DP 8", 11, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 22
def ch22_tiles():
    f = Fig("ch22_tiles", 660, 262)
    n, cs, x0, y0 = 8, 24, 70, 34
    f.text(x0 + n * cs / 2, 16, "K/V 块（每块 128 个位置）→", 11, "middle", INK2)
    f.text(x0 - 8, y0 - 6, "Q 块 ↓", 11, "end", INK2)
    for r in range(n):
        for c in range(n):
            x, y = x0 + c * cs, y0 + r * cs
            if c < r:
                f.rect(x, y, cs - 2, cs - 2, BLUE, "none", 0, 2)
            elif c == r:
                f.rect(x, y, cs - 2, cs - 2, BLUE_M, "none", 0, 2)
                f.line(x, y, x + cs - 2, y + cs - 2, "#ffffff", 1.2)
            else:
                f.rect(x, y, cs - 2, cs - 2, "#ffffff", IDLE_S, 0.8, 2, "2 2")
    hr = 5
    f.rect(x0 - 3, y0 + hr * cs - 3, n * cs + 4, cs + 4, "none", RED, 1.8, 3)
    f.text(x0 + n * cs + 10, y0 + hr * cs + 16, "← 一个线程块负责一行 Q 块", 11, "start", RED)
    f.text(x0 + n * cs + 10, 52, "深蓝：完整计算（28 块）", 11, "start", BLUE)
    f.text(x0 + n * cs + 10, 72, "浅蓝：对角线上的块，计算时加掩码（8 块）", 11, "start", INK2)
    f.text(x0 + n * cs + 10, 92, "虚线：整块都在“未来”，直接跳过（28 块）", 11, "start", INK2)
    f.text(x0 + n * cs + 10, 200, ["处理这一行时：Q 块常驻 SRAM，K/V 块从左到右", "依次流过；SRAM 里任何时刻只有一个", "128 × 128 的分数块"], 11, "start", INK2)
    f.text(330, 256, "$T$ = 1024、块大小 128 时的分块（22.2 节实验，实测）：64 个块对中实际计算 36 个", 11.5, "middle", INK2)
    save(f)


def ch22_online():
    f = Fig("ch22_online", 660, 238)
    x = [1, 3, 2, 5, 0, 4]
    f.text(10, 18, "某一行的 6 个分数，分 3 块依次到来：", 11.5, "start", INK, 700)
    for k, v in enumerate(x):
        bx = 248 + k * 38 + (k // 2) * 14
        f.box(bx, 6, 34, 22, str(v), ["blue", "orange", "green"][k // 2], 12)
    states = [("看完第 1 块 [1, 3]", "$m$ = 3", "$\\ell$ = $e^{-2}$ + $e^{0}$ = 1.135", None),
              ("看完第 2 块 [2, 5]", "$m$ = 5（变大了）", "$\\ell$ = 1.135 × $e^{3-5}$ + $e^{-3}$ + $e^{0}$ = 1.203", "旧的累加值先乘以 $e^{3-5}$ = 0.135，换算到新的最大值"),
              ("看完第 3 块 [0, 4]", "$m$ = 5（没变）", "$\\ell$ = 1.203 + $e^{-5}$ + $e^{-1}$ = 1.578", None)]
    for k, (t, a, b, note) in enumerate(states):
        y = 44 + k * 52
        f.rect(10, y, 640, 44, [BLUE_L, ORANGE_L, GREEN_L][k], "none", 0, 4)
        f.text(20, y + 18, t, 11.5, "start", INK, 700)
        f.text(170, y + 18, a, 11.5, "start", INK)
        f.text(300, y + 18, b, 11.5, "start", INK)
        if note:
            f.text(300, y + 36, note, 10.5, "start", RED)
    f.text(10, 214, "一次性计算：$\\sum e^{x-5}$ = $e^{-4}$ + $e^{-2}$ + $e^{-3}$ + 1 + $e^{-5}$ + $e^{-1}$ = 1.578，完全相同。输出 $o$ 的累加按同样的方式换算", 11.5, "start", INK2)
    f.text(10, 232, "（数字为手算示例）", 11, "start", INK3)
    save(f)


def ch22_profile():
    f = Fig("ch22_profile", 660, 236)
    u = 2.4
    def lane(y, label, segs):
        f.text(108, y + 13, label, 10.5, "end", INK2)
        f.line(114, y + 9, 650, y + 9, GRID, 1)
        for a, b, col in segs:
            f.rect(114 + a * u, y + 1, (b - a) * u - 1, 16, col, "none", 0, 2)
    f.text(10, 16, "有问题的时间线", 11.5, "start", RED, 700)
    rnd = random.Random(2)
    cpu = [(0, 12, GRAY), (40, 52, GRAY), (95, 110, GRAY), (150, 162, GRAY)]
    gpu = [(12, 40, BLUE), (52, 95, BLUE)] + [(110 + 2.5 * k, 111.8 + 2.5 * k, BLUE_M) for k in range(16)] + [(162, 190, BLUE)]
    lane(24, "CPU", cpu)
    lane(46, "GPU 计算", gpu)
    lane(68, "GPU 通信", [(190, 222, ORANGE)])
    f.text(114 + 41 * u, 102, "① 空隙：GPU 在等 CPU", 10.5, "middle", RED)
    f.text(114 + 125 * u, 102, "② 大量小内核", 10.5, "middle", RED)
    f.text(114 + 205 * u, 102, "③ 通信没有重叠", 10.5, "middle", RED)
    f.text(10, 132, "改进后", 11.5, "start", GREEN, 700)
    lane(140, "CPU", [(0, 10, GRAY), (30, 38, GRAY)])
    lane(162, "GPU 计算", [(10, 70, BLUE), (70, 110, BLUE), (110, 150, BLUE)])
    lane(184, "GPU 通信", [(60, 92, ORANGE), (100, 140, ORANGE)])
    f.text(114 + 150 * u + 6, 175, "更早结束", 11, "start", GREEN)
    f.text(330, 228, "在性能分析的时间线上找什么（示意）：融合小内核、去掉强制同步、让通信与计算重叠", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 23
def ch23_timeline():
    f = Fig("ch23_timeline", 660, 168)
    y, u, x0 = 56, 4.5, 14
    t = 0
    for k in range(4):
        f.rect(x0 + t * u, y, 20 * u, 28, BLUE, "none", 0, 0)
        f.rect(x0 + (t + 20) * u, y, 2 * u, 28, GRAY, "none", 0, 0)
        t += 22
    f.text(x0 + 10 * u, y + 18, "训练（间隔 $\\tau$）", 10.5, "middle", "#ffffff")
    f.text(x0 + 21 * u, y - 10, "保存检查点（停 $c$）", 10.5, "middle", INK2)
    f.line(x0 + 21 * u, y - 6, x0 + 21 * u, y, GRAY, 1.2)
    f.rect(x0 + t * u, y, 13 * u, 28, RED_L, RED, 1, 0)
    fail = t + 13
    f.text(x0 + fail * u, y - 10, "✗ 故障", 11, "middle", RED, 700)
    f.text(x0 + (t + 6.5) * u, y + 46, ["这段白算了"], 10.5, "middle", RED)
    f.rect(x0 + fail * u, y, 15 * u, 28, GRAY_L, "none", 0, 0)
    f.text(x0 + (fail + 7.5) * u, y + 18, "重启 $R$", 10.5, "middle", INK)
    r0 = fail + 15
    f.rect(x0 + r0 * u, y, 13 * u, 28, BLUE_M, "none", 0, 0)
    f.text(x0 + (r0 + 6.5) * u, y + 18, "重算", 10.5, "middle", INK)
    f.text(x0 + (r0 + 6.5) * u, y + 46, "从最近的检查点重新算", 10.5, "middle", INK2)
    f.rect(x0 + (r0 + 13) * u, y, 10 * u, 28, BLUE, "none", 0, 0)
    f.text(330, 146, "每次故障浪费两段时间：上一个检查点之后算的东西（平均 $\\tau/2$），加上重启的时间 $R$（示意）", 11.5, "middle", INK2)
    save(f)


def ch23_tau():
    f = Fig("ch23_tau", 660, 268)
    lam = 1 / 180
    cfgs = [("同步保存，重启慢（$c$ = 60 s，$R$ = 10 min）", 1.0, 10, RED),
            ("异步保存，重启慢（$c$ = 5 s，$R$ = 10 min）", 5 / 60, 10, ORANGE),
            ("异步保存，重启快（$c$ = 5 s，$R$ = 3 min）", 5 / 60, 3, GREEN)]
    c = Chart(f, 60, 26, 360, 180, (1, 100), (0, 0.4), xlog=True)
    c.axes([1, 3, 10, 30, 100], [0, 0.1, 0.2, 0.3, 0.4], xlabel="保存间隔 $\\tau$（分钟，对数坐标）", ylabel="损失的时间占比",
           xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0%}", size=11)
    xs = [10 ** (i / 40) for i in range(81)]
    for k, (lab, cc, R, col) in enumerate(cfgs):
        ys = [cc / t + lam * (t / 2 + R) for t in xs]
        clipped(c, xs, ys, col, 2)
        ts = math.sqrt(2 * cc / lam)
        v = cc / ts + lam * (ts / 2 + R)
        c.dots([ts], [v], col, 4.2)
        f.text(c.X(ts), c.Y(v) + (18 if k == 2 else -10), f"{v:.1%}（$\\tau^*$ = {ts:.1f} 分钟）" if k else f"{v:.0%}（$\\tau^*$ = {ts:.0f} 分钟）", 10.5, "middle", col)
    legend(f, 440, 60, [(lab, col, "line") for lab, _, _, col in cfgs], horizontal=False, size=10.5, gap=24)
    f.text(440, 150, ["$\\tau$ 太小：保存开销大；", "$\\tau$ 太大：故障时白算的多。", "最优间隔 $\\tau^*$ = $\\sqrt{2c/\\lambda}$"], 11, "start", INK2)
    f.text(330, 262, "故障率按每 3 小时一次计算（估算，数据同上表）", 11.5, "middle", INK2)
    save(f)


def ch23_restart():
    f = Fig("ch23_restart", 660, 152)
    steps = [["检测到", "故障"], ["定位并移除", "坏节点"], ["补上备用节点，", "重新调度"], ["拉镜像、起进程、", "初始化 NCCL"],
             ["加载检查点，恢复", "数据读取位置"], ["继续", "训练"]]
    w = [70, 92, 108, 116, 124, 60]
    x = 10
    for k, (a, b) in enumerate(steps):
        f.box(x, 40, w[k], 46, [a, b], "Green" if k == 5 else ("Red" if k == 0 else "blue"), 10.5)
        if k < 5:
            f.arrow(x + w[k] + 1, 63, x + w[k] + 11, 63, INK3, 1.2)
        x += w[k] + 12
    f.brace_h(10, x - 12 - 60 - 12, 92, None, INK3)
    f.text((10 + x - 84) / 2, 116, "这一整段就是重启时间 $R$：镜像预先分发、并行读取检查点、加快通信初始化", 11, "middle", INK2)
    f.text(10, 24, "作业的自动重启流程（23.7 节）", 11.5, "start", INK, 700)
    f.text(330, 144, "上万张卡的规模下，仅仅建立 NCCL 通信就可能要几分钟", 11, "middle", INK3)
    save(f)


def ch23_sdc():
    f = Fig("ch23_sdc", 660, 150)
    sums = ["3f9a c41e", "3f9a c41e", "7d02 9b6f", "3f9a c41e"]
    for k, s in enumerate(sums):
        x = 14 + k * 128
        bad = k == 2
        f.box(x, 30, 116, 34, f"数据并行副本 {k}", "red" if bad else "blue", 11)
        f.arrow(x + 58, 66, x + 58, 82, INK3, 1.1)
        f.box(x + 8, 84, 100, 26, s, "Red" if bad else "white", 11.5)
    f.text(14, 18, "同一步更新之后，各副本参数的校验和", 11.5, "start", INK, 700)
    f.text(530, 92, ["不一致：这个副本", "所在的硬件算错了"], 11, "start", RED)
    f.text(330, 140, "所有数据并行副本的参数本应逐位相同。定期比较校验和，代价很小，却能抓到静默数据损坏（示意）", 11, "middle", INK2)
    save(f)


if __name__ == "__main__":
    for fn in [ch18_bw, ch18_rail, ch18_fail,
               ch19_ops, ch19_ring, ch19_ab, ch19_hier, ch19_overlap,
               ch20_dp, ch20_zero, ch20_zero3, ch20_recompute,
               ch21_tp, ch21_cp, ch21_1f1b, ch21_bubble, ch21_layout,
               ch22_tiles, ch22_online, ch22_profile,
               ch23_timeline, ch23_tau, ch23_restart, ch23_sdc]:
        fn()
    print("ok")
