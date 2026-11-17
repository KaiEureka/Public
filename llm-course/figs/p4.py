"""Figures for Part 4 (chapters 14-17). Run: python3 figs/p4.py"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svglib import *

OUT = os.path.dirname(os.path.abspath(__file__))


def save(f):
    f.save(os.path.join(OUT, f.name + ".svg"))


def chip(f, x, y, s, style, size=11, h=20, pad=6):
    w = text_width(s, size) + 2 * pad
    f.box(x, y, w, h, s, style, size, rx=3, sw=1)
    return w


# ----------------------------------------------------------------- chapter 14
def ch14_mix():
    f = Fig("ch14_mix", 660, 132)
    parts = [("通用知识 50%", 50, BLUE), ("数学和推理 25%", 25, ORANGE), ("代码 17%", 17, GREEN), ("多语言 8%", 8, PURPLE)]
    f.text(10, 20, "Llama 3 预训练数据的配比（按 token 计）", 12.5, "start", INK, 700)
    x, w0 = 10, 640
    for k, (lab, v, col) in enumerate(parts):
        w = w0 * v / 100
        f.rect(x, 32, w - 2, 34, col, "none", 0, 2)
        if k < 3:
            f.text(x + w / 2, 54, lab, 12, "middle", "#ffffff")
        else:
            f.text(x + w - 2, 84, lab, 11.5, "end", PURPLE)
        x += w
    f.text(10, 106, "总量 15T token。英文平均约 4 个字节 1 个 token，15T token 相当于约 60 TB 干净文本；", 11.5, "start", INK2)
    f.text(10, 124, "过滤前的原始网页要多出好几十倍", 11.5, "start", INK2)
    save(f)


def ch14_formats():
    f = Fig("ch14_formats", 660, 254)
    # web page wireframe
    f.text(70, 18, "一个网页", 12, "middle", INK, 700)
    f.rect(10, 28, 120, 168, "#ffffff", GRAY, 1.2, 4)
    f.rect(16, 34, 108, 12, GRAY_L, "none", 0, 2)
    f.rect(16, 52, 72, 96, BLUE_L, BLUE, 0.8, 2)
    for k in range(6):
        f.line(22, 62 + k * 13, 82, 62 + k * 13, BLUE_M, 3)
    f.rect(94, 52, 30, 96, GRAY_L, "none", 0, 2)
    f.text(109, 104, "广告", 9.5, "middle", INK3)
    f.rect(16, 154, 108, 16, GRAY_L, "none", 0, 2)
    f.rect(16, 176, 108, 14, GRAY_L, "none", 0, 2)
    f.text(70, 214, ["正文只占一部分，其余是", "导航、广告、推荐、页脚"], 10.5, "middle", INK2)
    f.arrow(134, 112, 176, 112)
    f.text(155, 102, "抓取", 10.5, "middle", INK2)
    cards = [("WARC", ["原始 HTTP 响应，", "含完整 HTML"], "blue", 30),
             ("WAT", ["元数据（JSON）：", "HTTP 头、页面中的链接"], "gray", 94),
             ("WET", ["Common Crawl 自己", "提取的纯文本，较粗糙"], "gray", 158)]
    for name, desc, st, y in cards:
        f.box(180, y, 64, 52, name, st if st != "blue" else "Blue", 13, weight=700)
        f.text(252, y + 22, desc[0], 11, "start", INK2)
        f.text(252, y + 38, desc[1], 11, "start", INK2)
    f.poly([(392, 56), (440, 56), (440, 70)], INK3, 1.3, arrow=True)
    f.box(444, 72, 206, 52, ["自己提取正文（trafilatura 等）", "保留标题、列表、表格、公式"], "green", 11.5)
    f.text(547, 142, "FineWeb：效果比直接用 WET 更好", 11, "middle", GREEN)
    f.poly([(392, 184), (444, 184)], INK3, 1.2, "4 3", arrow=True)
    f.text(450, 188, "直接用 WET：省事，但质量差一些", 11, "start", INK2)
    f.text(330, 250, "Common Crawl 的三种文件。按网址、域名、语言筛选时可以先查索引，只下载需要的记录", 11.5, "middle", INK2)
    save(f)


def ch14_crawler():
    f = Fig("ch14_crawler", 660, 246)
    f.box(10, 40, 126, 56, ["待抓取队列", "按质量、语言、", "更新频率排优先级"], "blue", 11)
    f.arrow(138, 68, 166, 68)
    f.box(168, 34, 150, 68, ["调度器（礼貌规则）", "同一网站限并发和频率；", "查 robots.txt、DNS 缓存"], "orange", 11)
    f.arrow(320, 68, 348, 68)
    f.box(350, 40, 130, 56, ["大量异步下载器", "（必要时用无头", "浏览器渲染 JS）"], "blue", 11)
    f.arrow(482, 68, 510, 68)
    f.box(512, 40, 138, 56, ["原始响应存成 WARC", "内容哈希去重"], "gray", 11)
    f.arrow(415, 98, 415, 140)
    f.box(350, 142, 130, 44, ["解析页面中的", "新链接"], "blue", 11)
    f.arrow(348, 164, 320, 164)
    f.box(168, 142, 150, 44, ["网址规范化、去重；", "识别爬虫陷阱"], "orange", 11)
    f.poly([(166, 164), (73, 164), (73, 98)], INK3, 1.4, arrow=True)
    f.text(78, 186, "放回队列", 11, "start", INK2)
    f.text(330, 220, "一个大规模爬虫的工作循环（14.9 节）。抓取数十亿网页需要成千上万个并发下载器，存储达 PB 级；", 11.5, "middle", INK2)
    f.text(330, 238, "还要决定已抓过的页面隔多久重新抓一次", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 15
def ch15_pipeline():
    f = Fig("ch15_pipeline", 660, 190)
    steps = [["①", "网址", "过滤"], ["②", "正文", "提取"], ["③", "语言", "识别"], ["④", "Gopher", "规则"],
             ["⑤", "MinHash", "去重"], ["⑥", "C4 与自", "定义规则"], ["⑦", "个人信息", "匿名化"]]
    w, x0 = 90, 12
    cols = [BLUE_L] * 7
    for k, (n, a, b) in enumerate(steps):
        x = x0 + k * w
        pts = [(x, 40), (x + w - 12, 40), (x + w, 70), (x + w - 12, 100), (x, 100), (x + 12, 70)] if k else \
              [(x, 40), (x + w - 12, 40), (x + w, 70), (x + w - 12, 100), (x, 100)]
        shade = 0.15 + 0.85 * k / 6
        fill = f"rgb({int(255 - shade * (255 - 156))},{int(255 - shade * (255 - 187))},{int(255 - shade * (255 - 217))})"
        f.poly(pts + [pts[0]], "#ffffff", 1.5, fill=fill)
        tx = x + w / 2 + (4 if k else -2)
        f.text(tx, 60, n, 11, "middle", INK)
        f.text(tx, 76, a, 11, "middle", INK, 700)
        f.text(tx, 91, b, 11, "middle", INK, 700)
    f.arrow(20, 24, 640, 24, INK3, 1.2)
    f.text(20, 16, "便宜：几乎不花计算", 11, "start", INK2)
    f.text(640, 16, "昂贵：去重、分类器", 11, "end", INK2)
    # remaining data band (schematic)
    rem = [1.0, 0.72, 0.42, 0.33, 0.24, 0.17, 0.12, 0.11]
    top = []
    bot = []
    for k, r in enumerate(rem):
        x = x0 + k * w
        top.append((x, 140 - 26 * r))
        bot.append((x, 140 + 26 * r))
    f.poly(top + bot[::-1] + [top[0]], "none", 0, fill=BLUE_M)
    f.text(18, 144, "剩余的数据量（示意）", 11, "start", INK)
    f.text(330, 184, "FineWeb 的七步流水线。RefinedWeb 报告他们的流水线去掉了 Common Crawl 中近 90% 的文档", 11.5, "middle", INK2)
    save(f)


def ch15_extract():
    f = Fig("ch15_extract", 660, 208)
    f.rect(10, 14, 260, 172, "#ffffff", GRAY, 1.2, 4)
    blocks = [(16, 20, 248, 14, "导航栏", 0), (16, 38, 248, 13, "Cookie 提示", 0), (16, 55, 178, 16, "标题", 1),
              (16, 75, 178, 40, "正文段落", 1), (16, 119, 178, 18, "代码块 / 公式", 1), (198, 55, 66, 82, "广告", 0),
              (16, 141, 248, 14, "相关推荐", 0), (16, 159, 160, 11, "评论区", 0), (16, 174, 248, 8, "", 0)]
    for x, y, w, h, lab, body in blocks:
        f.rect(x, y, w, h, BLUE_L if body else GRAY_L, BLUE if body else "none", 0.8, 2)
        if lab:
            f.text(x + w / 2, y + h / 2 + 4, lab, 10.5, "middle", INK if body else INK3)
    f.text(140, 202, "灰色：模板内容（boilerplate）", 11, "middle", INK2)
    f.arrow(280, 100, 330, 100)
    f.text(305, 90, "提取", 11, "middle", INK2)
    f.rect(340, 24, 300, 140, BLUE_L, BLUE, 1.2, 4)
    f.text(354, 46, "# 标题", 12, "start", INK, 700)
    for k in range(4):
        f.line(354, 64 + k * 14, 620 - (60 if k == 3 else 0), 64 + k * 14, BLUE_M, 4)
    f.rect(354, 122, 200, 30, "#ffffff", BLUE_M, 1, 2)
    f.text(362, 141, "保留代码块和公式的结构", 10.5, "start", INK2)
    f.text(490, 182, ["工具：trafilatura、resiliparse、jusText，", "根据 HTML 结构和文本密度判断哪些是正文"], 11, "middle", INK2)
    save(f)


def ch15_minhash():
    f = Fig("ch15_minhash", 660, 244)
    A = ["to be or", "be or not", "or not to", "not to be", "to be that", "be that is", "that is the", "is the question"]
    B = ["to be or", "be or not", "or not to", "not to be", "to be this", "be this is", "this is the", "is the question"]
    common = [s for s in A if s in B]
    f.text(10, 18, "文档 A：to be or not to be that is the question", 11.5, "start", INK)
    f.text(340, 18, "文档 B：to be or not to be this is the question", 11.5, "start", INK)
    f.text(10, 40, "共有的 3 词片段（5 个）", 11, "start", PURPLE, 700)
    x = 10
    for s in common:
        x += chip(f, x, 46, s, "purple") + 4
    f.text(10, 84, "只在 A 中（3 个）", 11, "start", BLUE, 700)
    x = 10
    for s in A:
        if s not in common:
            x += chip(f, x, 90, s, "blue") + 4
    f.text(340, 84, "只在 B 中（3 个）", 11, "start", ORANGE, 700)
    x = 340
    for s in B:
        if s not in common:
            x += chip(f, x, 90, s, "orange") + 4
    f.text(10, 134, "Jaccard = 交集 ÷ 并集 = 5 ÷ 11 ≈ 0.45", 12, "start", INK, 700)
    rnd = random.Random(4)
    union = common + [s for s in A if s not in common] + [s for s in B if s not in common]
    order = union[:]
    rnd.shuffle(order)
    f.text(10, 162, "用一个随机哈希函数给并集里的 11 个片段排序，看排在第一位的是谁：", 11.5, "start", INK)
    x = 10
    for k, s in enumerate(order):
        st = "purple" if s in common else ("blue" if s in A else "orange")
        w = chip(f, x, 170, s, st, 9.5, 18, 3.5)
        if k == 0:
            f.rect(x - 3, 167, w + 6, 24, "none", RED, 1.6, 4)
        x += w + 2.5
    f.text(10, 210, "排第一的片段同时是 A 和 B 的最小值。它落在交集里的概率恰好是 5/11 = Jaccard。", 11.5, "start", INK2)
    f.text(10, 228, "换 $k$ 个哈希函数重复，两篇文档最小值相同的比例就是 Jaccard 的估计（示意：这里用 3 个词一组，实际用 5 个）", 11.5, "start", INK2)
    save(f)


def ch15_lsh():
    f = Fig("ch15_lsh", 660, 246)
    c = Chart(f, 60, 30, 360, 150, (0, 1), (0, 1))
    c.axes([0, 0.2, 0.4, 0.6, 0.8, 1.0], [0, 0.25, 0.5, 0.75, 1], xlabel="两篇文档的 Jaccard 相似度", ylabel="被列为候选对的概率",
           xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0%}")
    xs = [i / 200 for i in range(201)]
    c.series(xs, [1 - (1 - x ** 8) ** 14 for x in xs], BLUE, 2.2)
    c.vline((1 / 14) ** (1 / 8), INK3, "4 3", None)
    f.text(c.X(0.72) - 4, c.y0 + 12, "转折点约 0.72", 11, "end", INK2)
    meas = [(0.785, 0.90), (0.617, 0.22), (0.414, 0.0), (0.181, 0.0), (0.083, 0.0), (0.012, 0.0)]
    for j, p in meas:
        c.dots([j], [p], ORANGE, 4.2)
    f.text(c.X(0.785) + 8, c.Y(0.90) + 14, "实测：替换 2% 的词", 10.5, "start", ORANGE)
    f.text(c.X(0.617) + 8, c.Y(0.22) + 4, "替换 5%", 10.5, "start", ORANGE)
    # signature bands
    x0 = 450
    f.text(x0, 40, "签名：112 个最小哈希值", 11.5, "start", INK, 700)
    for b in range(14):
        f.rect(x0, 50 + b * 8, 120, 7, BLUE_M if b % 2 else BLUE_L, "none", 0, 1)
    f.text(x0 + 126, 82, ["切成 14 段，", "每段 8 个"], 11, "start", INK2)
    f.rect(x0 - 2, 50 + 5 * 8 - 1, 124, 9, "none", RED, 1.4, 1)
    f.text(x0, 176, ["两篇文档只要有任意一段", "完全相同，就列为候选对，", "再做精确比较"], 11, "start", INK2)
    legend(f, 60, 240, [("理论曲线 $1 - (1 - J^{8})^{14}$", BLUE, "line"), ("15.5 节实验的检出率（实测）", ORANGE, "dot")])
    save(f)


# ----------------------------------------------------------------- chapter 16
def ch16_edu():
    f = Fig("ch16_edu", 660, 220)
    f.box(10, 30, 120, 52, ["约 45 万篇", "FineWeb 网页"], "white", 11.5)
    f.arrow(132, 56, 156, 56)
    f.box(158, 24, 150, 64, ["Llama-3-70B-Instruct", "按“教育价值”打 0–5 分", "（累加制）"], "orange", 11)
    f.arrow(310, 56, 334, 56)
    f.box(336, 24, 150, 64, ["训练小分类器：", "文本嵌入 + 线性回归，", "学会预测这个分数"], "blue", 11)
    f.arrow(488, 56, 512, 56)
    f.box(514, 30, 136, 52, ["给全部 15T token", "打分"], "Blue", 11.5)
    f.arrow(582, 84, 582, 108)
    f.box(470, 110, 180, 34, "分数 ≥ 3：1.3T（FineWeb-Edu）", "Green", 11)
    f.box(470, 152, 180, 30, "分数 ≥ 2：5.4T", "green", 11)
    f.text(10, 126, "为什么不直接用 70B 模型给全部数据打分？", 11.5, "start", INK, 700)
    f.text(10, 146, ["读一遍 15T token 约需 $2\\times70\\times10^{9}\\times15\\times10^{12}$", "≈ $2\\times10^{24}$ FLOP，与训练一个大模型同一量级；", "小分类器的成本要低几个数量级"], 11, "start", INK2)
    f.text(330, 214, "代价：数据被推向“教科书风格”，知识和推理类基准大涨，常识和日常语言类基准提升不明显", 11.5, "middle", INK2)
    save(f)


def ch16_tiers():
    f = Fig("ch16_tiers", 660, 280)
    f.text(10, 18, "按质量分成 20 档（左低右高）", 12, "start", INK, 700)
    x0, w = 10, 30
    for k in range(20):
        t = k / 19
        f.rect(x0 + k * w + 10, 28, w - 3, 26, lerp(t), "none", 0, 2)
    f.brace_h(x0 + 18 * w + 10, x0 + 20 * w + 7, 58, None, RED)
    f.text(x0 + 19 * w + 8, 82, "DCLM 式：只留最高的 10%", 11, "end", RED)
    f.brace_h(x0 + 8 * w + 10, x0 + 20 * w + 7, 92, None, GREEN)
    f.text(x0 + 14 * w + 8, 116, "Nemotron-CC：保留多档，并用模型改写低质量文档、扩充高质量文档（档数示意）", 11, "middle", GREEN)
    c = Chart(f, 200, 158, 300, 72, (0, 9), (0, 2))
    rows = [("只用最好的 2T（正文的假设）", 7.5, RED), ("Nemotron-CC 的 6.3T", 15 / 6.3, GREEN)]
    for i, (lab, v, col) in enumerate(rows):
        yc = c.y0 + (i + 0.5) * c.h / 2
        f.text(c.x0 - 8, yc + 4, lab, 11.5, "end", INK)
        f.rect(c.x0, yc - 11, c.X(v) - c.x0, 22, col, "none", 0, 2)
        f.text(c.X(v) + 6, yc + 4, f"{v:.1f} 遍", 11.5, "start", INK)
    f.line(c.X(4), c.y0 - 4, c.X(4), c.y0 + c.h + 4, INK3, 1, "4 3")
    f.text(c.X(4) + 4, c.y0 - 6, "约 4 遍以上，收益迅速下降（第 10 章）", 10.5, "start", INK2)
    f.text(330, 254, "下：训练 15T token 时，每份数据要重复几遍。预算越大，越不能只盯着最高的那一档", 11.5, "middle", INK2)
    f.text(330, 272, "（Nemotron-CC：4.4T 原始数据 + 1.9T 合成数据）", 11, "middle", INK3)
    save(f)


def lerp(t):
    a, b = (0xee, 0xf1, 0xf4), (0x1c, 0x5d, 0x99)
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def ch16_anneal():
    f = Fig("ch16_anneal", 660, 274)
    ts = [i / 200 for i in range(201)]
    lr = [1.0 if t < 0.85 else max(0.0, 1 - (t - 0.85) / 0.15) for t in ts]
    c1 = Chart(f, 60, 24, 440, 54, (0, 1), (0, 1.1))
    c1.axes([], [0, 1], ylabel=None, yfmt=lambda v: "峰值" if v else "0", size=10.5)
    c1.series(ts, lr, NAVY, 2)
    f.text(c1.x0 + 6, c1.y0 + c1.h - 6, "学习率", 11, "start", INK2)
    c = Chart(f, 60, 94, 440, 120, (0, 1), (0, 1))
    c.axes([0, 0.25, 0.5, 0.75, 1], [0, 0.5, 1], xlabel="训练进度（示意）", ylabel=None, xfmt=lambda v: f"{v:.0%}", yfmt=lambda v: f"{v:.0%}", size=10.5)
    def mix(t):
        hq = 0.06 if t < 0.85 else 0.06 + 0.34 * min(1, (t - 0.85) / 0.03)
        code, math_ = 0.17, 0.12
        return [1 - hq - code - math_, code, math_, hq]
    layers = [("网页等通用数据", BLUE_M), ("代码", GREEN_M), ("数学", ORANGE_M), ("精选高质量数据", RED)]
    acc = [0.0] * len(ts)
    for k, (lab, col) in enumerate(layers):
        lo = acc[:]
        hi = [lo[i] + mix(t)[k] for i, t in enumerate(ts)]
        pts = [(c.X(t), c.Y(h)) for t, h in zip(ts, hi)] + [(c.X(t), c.Y(l)) for t, l in zip(ts[::-1], lo[::-1])]
        f.poly(pts + [pts[0]], "none", 0, fill=col)
        acc = hi
    legend(f, 518, 110, [(lab, col, "box") for lab, col in layers[::-1]], horizontal=False, size=11)
    f.text(518, 200, ["退火：学习率降下来的同时，", "提高最高质量数据的比例"], 11, "start", INK2)
    f.text(330, 268, "示意。Llama 3 在最后 4,000 万 token 上退火：8B 的 GSM8K 提升 24.0%，405B 几乎不受影响", 11.5, "middle", INK2)
    save(f)


# ----------------------------------------------------------------- chapter 17
def ch17_tail():
    f = Fig("ch17_tail", 660, 236)
    rnd = random.Random(11)
    V = 30
    p = [1 / (k + 1) ** 1.1 for k in range(V)]
    s = sum(p)
    p = [v / s for v in p]
    gens = [p]
    q = p
    for g in range(3):
        cnt = [0] * V
        for _ in range(120):
            r, acc = rnd.random(), 0
            for k in range(V):
                acc += q[k]
                if r < acc:
                    cnt[k] += 1
                    break
        q = [c / 120 for c in cnt]
        gens.append(q)
    shown = [(0, "第 0 代：真实分布"), (1, "第 1 代"), (3, "第 3 代")]
    for j, (g, title) in enumerate(shown):
        x0 = 20 + j * 215
        f.text(x0 + 95, 18, title, 12, "middle", INK, 700)
        q = gens[g]
        for k in range(V):
            h = 120 * q[k] / 0.3
            x = x0 + k * 6.3
            if q[k] > 0:
                f.rect(x, 150 - h, 5, h, BLUE if k < 8 else ORANGE, "none", 0, 1)
            elif p[k] > 0:
                f.line(x + 2.5, 150, x + 2.5, 146, RED, 1.5)
        f.line(x0, 150, x0 + V * 6.3, 150, AXIS, 1)
        nz = sum(1 for v in q if v > 0)
        f.text(x0 + 95, 168, f"还剩 {nz} 个词", 11, "middle", INK2)
        if j < 2:
            f.arrow(x0 + 194, 90, x0 + 212, 90)
    f.text(330, 196, "每一代只从上一代的模型里抽有限个样本，再用样本的频率作为下一代的模型。", 11.5, "middle", INK2)
    f.text(330, 214, "罕见词（橙色）一旦一次都没被抽到，概率就变成 0（红色短线），以后再也回不来", 11.5, "middle", INK2)
    f.text(330, 232, "示意：30 个词的 Zipf 分布，每代抽 120 个样本", 11, "middle", INK3)
    save(f)


def ch17_collapse():
    f = Fig("ch17_collapse", 660, 256)
    g = [0, 1, 2, 5, 10, 20, 30]
    vocab = [12631, 10200, 8811, 6605, 4980, 3553, 2801]
    rare = [100, 69.1, 53.3, 31.9, 19.9, 11.2, 7.5]
    c = Chart(f, 64, 34, 240, 160, (0, 30), (0, 14000))
    c.axes([0, 10, 20, 30], [0, 4000, 8000, 12000], xlabel="第几代", ylabel="词表大小", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:,.0f}", size=11)
    c.series(g, vocab, RED, 2, markers=True)
    c.series([0, 30], [12631, 12631], BLUE, 2)
    f.text(c.X(30), c.Y(12631) - 8, "累积：12,631", 11, "end", BLUE)
    f.text(c.X(30), c.Y(2801) - 10, "替换：2,801", 11, "end", RED)
    c2 = Chart(f, 400, 34, 240, 160, (0, 30), (0, 100))
    c2.axes([0, 10, 20, 30], [0, 25, 50, 75, 100], xlabel="第几代", ylabel="罕见词还剩多少", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}%", size=11)
    c2.series(g, rare, RED, 2, markers=True)
    c2.series([0, 30], [100, 100], BLUE, 2)
    f.text(c2.X(30), c2.Y(100) + 16, "累积：100%", 11, "end", BLUE)
    f.text(c2.X(1) + 8, c2.Y(69.1) + 4, "一代后只剩 69%", 11, "start", RED)
    f.text(c2.X(30), c2.Y(7.5) - 10, "替换：7.5%", 11, "end", RED)
    f.text(330, 250, "17.3 节的模拟（实测）：“替换”只用上一代生成的数据；“累积”始终保留原始真实数据", 11.5, "middle", INK2)
    save(f)


def ch17_verify():
    f = Fig("ch17_verify", 660, 214)
    f.text(160, 18, "可验证的合成：只留下通过检查的", 12, "middle", INK, 700)
    f.box(10, 36, 140, 60, ["强模型生成：", "题目、解答、", "单元测试"], "blue", 11)
    f.arrow(152, 66, 176, 66)
    f.box(178, 36, 132, 60, ["程序验证：", "运行测试 / 核对", "答案 / Lean 检查"], "orange", 11)
    f.poly([(244, 98), (244, 120), (180, 120)], INK3, 1.3, arrow=True)
    f.text(250, 114, "通过", 11, "start", GREEN, 700)
    f.box(30, 106, 148, 30, "加入训练数据", "Green", 11.5)
    f.poly([(244, 120), (244, 160), (200, 160)], RED, 1.2, "4 3", arrow=True)
    f.text(250, 154, "不通过", 11, "start", RED, 700)
    f.box(110, 146, 88, 28, "丢弃", "red", 11.5)
    f.text(490, 18, "自举（STaR）：用自己筛过的数据训练自己", 12, "middle", INK, 700)
    cx, cy, rx, ry = 482, 100, 96, 56
    nodes = [("模型", 0, -ry, "Blue"), ("为每道题生成推理过程", rx, 0, "white"), ("只保留答案正确的", 0, ry, "orange"), ("用它们微调", -rx, 0, "white")]
    boxes = []
    for lab, dx, dy, st in nodes:
        w = text_width(lab, 11) + 16
        x, y = cx + dx - w / 2, cy + dy - 13
        f.box(x, y, w, 26, lab, st, 11)
        boxes.append((x, y, w))
    (x0, y0, w0), (x1, y1, w1), (x2, y2, w2), (x3, y3, w3) = boxes
    f.poly([(x0 + w0, y0 + 13), (x1 + w1 / 2, y0 + 13), (x1 + w1 / 2, y1)], INK3, 1.4, arrow=True)
    f.poly([(x1 + w1 / 2, y1 + 26), (x1 + w1 / 2, y2 + 13), (x2 + w2, y2 + 13)], INK3, 1.4, arrow=True)
    f.poly([(x2, y2 + 13), (x3 + w3 / 2, y2 + 13), (x3 + w3 / 2, y3 + 26)], INK3, 1.4, arrow=True)
    f.poly([(x3 + w3 / 2, y3), (x3 + w3 / 2, y0 + 13), (x0, y0 + 13)], INK3, 1.4, arrow=True)
    f.text(330, 206, "两者的共同点：生成的数据要经过“对错”检查才能用。STaR 已经是强化学习的雏形（第 27 章）", 11.5, "middle", INK2)
    save(f)


def ch17_contam():
    f = Fig("ch17_contam", 660, 236)
    f.box(10, 86, 96, 50, ["基准测试", "的题目"], "Red", 12)
    paths = [(24, ["公开在网上：GitHub、", "论文、论坛、答案解析"], ["Common Crawl", "→ 预训练数据"]),
             (90, ["教师模型见过题目，", "生成时“复述”出来"], ["合成数据"]),
             (156, ["有意或无意混入"], ["后训练数据集"])]
    for y, mid, dst in paths:
        f.poly([(108, 111), (130, 111), (130, y + 20), (150, y + 20)], RED, 1.3, arrow=True)
        f.box(152, y, 170, 40, mid, "white", 10.5)
        f.arrow(324, y + 20, 348, y + 20, RED, 1.3)
        f.box(350, y, 132, 40, dst, "orange", 11)
        f.poly([(484, y + 20), (510, y + 20), (510, 111), (528, 111)], RED, 1.3, arrow=True)
    f.box(530, 86, 120, 50, ["训练出的模型：", "分数虚高"], "red", 11.5)
    f.text(416, 214, "检测：n-gram 重叠、语义相似度、Min-K% Prob、补全测试、金丝雀字符串", 11, "middle", INK2)
    f.rect(344, 16, 144, 186, "none", BLUE, 1.2, 6, "5 3")
    f.text(416, 230, "（在这一层建索引、扫描、删除并记录）", 11, "middle", BLUE)
    save(f)


if __name__ == "__main__":
    for fn in [ch14_mix, ch14_formats, ch14_crawler,
               ch15_pipeline, ch15_extract, ch15_minhash, ch15_lsh,
               ch16_edu, ch16_tiers, ch16_anneal,
               ch17_tail, ch17_collapse, ch17_verify, ch17_contam]:
        fn()
    print("ok")
