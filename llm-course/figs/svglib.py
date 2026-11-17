"""Tiny SVG toolkit for the book's figures: boxes, arrows, rich text and simple charts.

Every figure is drawn in a viewBox whose units map to 0.25 mm on the page (see Fig.svg), so text of size 13
prints at about 9 pt in every figure, whatever its width. Text uses the page fonts (BookSans for CJK and
labels, LatinSerif for math), because the SVG is inlined into the HTML.
"""
import math, re, html

INK, INK2, INK3, NAVY = "#1d2329", "#52606d", "#6b7785", "#0f2740"
BLUE, ORANGE, GREEN, PURPLE, RED = "#1c5d99", "#c77d12", "#2e7d4f", "#6b3fa0", "#b5443a"
BLUE_L, ORANGE_L, GREEN_L, PURPLE_L, RED_L = "#e8eff6", "#fff8ec", "#eef8f1", "#f5f0fb", "#fff4f2"
GRAY, GRAY_L, GRID, AXIS = "#9aa7b4", "#eef1f4", "#e3e7eb", "#9aa7b4"
BLUE_M, ORANGE_M, GREEN_M = "#9cbbd9", "#e6bf86", "#9cc9ad"
STYLE = {  # fill, stroke, text colour
    "blue": (BLUE_L, BLUE, INK), "navy": (BLUE_L, NAVY, INK), "orange": (ORANGE_L, ORANGE, INK),
    "green": (GREEN_L, GREEN, INK), "purple": (PURPLE_L, PURPLE, INK), "red": (RED_L, RED, INK),
    "gray": (GRAY_L, GRAY, INK), "white": ("#ffffff", GRAY, INK),
    "Blue": (BLUE, BLUE, "#ffffff"), "Orange": (ORANGE, ORANGE, "#ffffff"), "Green": (GREEN, GREEN, "#ffffff"),
    "Purple": (PURPLE, PURPLE, "#ffffff"), "Red": (RED, RED, "#ffffff"), "Navy": (NAVY, NAVY, "#ffffff"),
    "Gray": ("#7b8794", "#7b8794", "#ffffff"), "none": ("none", "none", INK),
}
MM_PER_UNIT = 0.25


def esc(s):
    return html.escape(str(s), quote=True)


def _is_cjk(ch):
    o = ord(ch)
    return o >= 0x2E80 or 0xFF00 <= o <= 0xFFEF or ch in "，。：；（）、“”‘’！？《》【】—…"


def text_width(s, size):
    """Rough rendered width of a (possibly marked-up) string."""
    s = re.sub(r"[$]", "", s)
    s = re.sub(r"\\(log|exp|max|min)", r"\1", s)
    s = re.sub(r"\\[A-Za-z]+|\\.", "x", s)
    s = re.sub(r"[_^]\{([^}]*)\}", lambda m: "\x01" * len(m.group(1)), s)
    s = re.sub(r"[_^](.)", "\x01", s)
    w = 0.0
    for ch in s:
        if ch == "\x01":
            w += 0.40
        elif _is_cjk(ch):
            w += 1.0
        elif ch == " ":
            w += 0.28
        elif ch in "il.,:;|'!()[]":
            w += 0.28
        elif ch in "mwMW":
            w += 0.82
        elif ch.isupper():
            w += 0.64
        else:
            w += 0.54
    return w * size


MATH_SYMS = {"times": "\u00d7", "approx": "\u2248", "cdot": "\u00b7", ",": "\u2009", "le": "\u2264", "ge": "\u2265",
             "infty": "\u221e", "sum": "\u03a3", "sqrt": "\u221a", "to": "\u2192", "propto": "\u221d", "pm": "\u00b1",
             "top": "\u22a4", "lvert": "|", "rvert": "|", "|": "\u2016", "ll": "\u226a", "gg": "\u226b", "prime": "\u2032", "lVert": "\u2016", "rVert": "\u2016", "langle": "\u27e8", "rangle": "\u27e9", "odot": "\u2299",
             "alpha": "\u03b1", "beta": "\u03b2", "gamma": "\u03b3", "theta": "\u03b8", "lambda": "\u03bb", "tau": "\u03c4",
             "sigma": "\u03c3", "pi": "\u03c0", "epsilon": "\u03b5", "Psi": "\u03a8", "Delta": "\u0394", "mu": "\u03bc",
             "rho": "\u03c1", "eta": "\u03b7", "nabla": "\u2207", "partial": "\u2202", "in": "\u2208", "neq": "\u2260", "ell": "\u2113", "Sigma": "\u03a3", "phi": "\u03c6", "omega": "\u03c9", "delta": "\u03b4", "varepsilon": "\u03b5", "kappa": "\u03ba", "xi": "\u03be", "zeta": "\u03b6", " ": " ", "{": "{", "}": "}"}


def rich(s, size):
    """Mini markup → tspans. $...$ is math: Latin letters italic in LatinSerif; _x / _{..} sub, ^x / ^{..} sup."""
    s = re.sub(r"\\sqrt\{([^{}]*)\}", "\u221a\\1", s)
    s = re.sub(r"\\mathrm\{([^{}]*)\}", lambda m: "\x02" + m.group(1) + "\x03", s)
    s = re.sub(r"\\hat\s*\{?([A-Za-z])\}?", "\\1\u0302", s)
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", "\\1/\\2", s)
    out, buf, math_on = [], [], False

    def flush(style):
        if buf:
            out.append((style, "".join(buf)))
            buf.clear()

    i, cur = 0, "text"
    while i < len(s):
        ch = s[i]
        if ch == "$":
            flush(cur)
            math_on = not math_on
            cur = "text"
            i += 1
            continue
        if math_on and ch == "\\":
            flush(cur)
            m = re.match(r"\\([A-Za-z]+|.)", s[i:])
            name = m.group(1)
            i += len(m.group(0))
            sym = MATH_SYMS.get(name, name)
            out.append(("mn", sym))
            cur = "text"
            continue
        if math_on and ch in "_^":
            flush(cur)
            if i + 1 < len(s) and s[i + 1] == "{":
                j = s.index("}", i + 2)
                grp, i = s[i + 2:j], j + 1
            else:
                grp, i = s[i + 1], i + 2
            grp = re.sub(r"\\([A-Za-z]+)", lambda m: MATH_SYMS.get(m.group(1), m.group(1)), grp).replace("-", "\u2212")
            out.append(("sub" if ch == "_" else "sup", grp))
            cur = "text"
            continue
        if math_on and ch == "\x02":
            flush(cur)
            j = s.index("\x03", i)
            out.append(("mn", s[i + 1:j]))
            i, cur = j + 1, "text"
            continue
        if math_on and ch == "-":
            ch = "\u2212"
        if math_on:
            st = "mi" if (ch.isascii() and ch.isalpha()) else "mn"
        else:
            st = "text"
        if st != cur:
            flush(cur)
            cur = st
        buf.append(ch)
        i += 1
    flush(cur)
    parts = []
    for st, t in out:
        t_e = esc(t)
        if st == "text":
            parts.append(f"<tspan>{t_e}</tspan>")
        elif st == "mi":
            parts.append(f'<tspan font-family="LatinSerif" font-style="italic">{t_e}</tspan>')
        elif st == "mn":
            parts.append(f'<tspan font-family="LatinSerif">{t_e}</tspan>')
        else:
            shift = "-0.25em" if st == "sub" else "0.42em"
            italic = ' font-style="italic"' if re.fullmatch(r"[A-Za-z]", t) else ""
            parts.append(f'<tspan font-family="LatinSerif"{italic} font-size="{size * 0.72:.1f}" '
                         f'baseline-shift="{shift}">{t_e}</tspan>')
    return "".join(parts)


class Fig:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.items, self.markers = [], {}

    # ---------- primitives ----------
    def raw(self, s):
        self.items.append(s)

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1, rx=0, dash=None, opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        self.raw(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')

    def circle(self, cx, cy, r, fill="none", stroke="none", sw=1):
        self.raw(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, size=13, anchor="start", fill=INK, weight=None, family=None, italic=False):
        """Single line, or a list of lines (line height 1.35 em). y is the baseline of the first line."""
        lines = s if isinstance(s, (list, tuple)) else [s]
        for k, line in enumerate(lines):
            attrs = f'x="{x:.1f}" y="{y + k * size * 1.35:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"'
            if weight:
                attrs += f' font-weight="{weight}"'
            if family:
                attrs += f' font-family="{family}"'
            if italic:
                attrs += ' font-style="italic"'
            self.raw(f"<text {attrs}>{rich(line, size)}</text>")

    def marker(self, color):
        mid = f"{self.name}-ah-{color.lstrip('#')}"
        if mid not in self.markers:
            self.markers[mid] = (f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
                                 f'markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')
        return mid

    def line(self, x1, y1, x2, y2, stroke=INK3, sw=1.4, dash=None, arrow=False, arrow_start=False, cap="butt"):
        self.poly([(x1, y1), (x2, y2)], stroke, sw, dash, arrow, arrow_start, cap)

    def poly(self, pts, stroke=INK3, sw=1.4, dash=None, arrow=False, arrow_start=False, cap="round", fill="none"):
        d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts))
        self.path(d, stroke, sw, dash, arrow, arrow_start, cap, fill)

    def path(self, d, stroke=INK3, sw=1.4, dash=None, arrow=False, arrow_start=False, cap="round", fill="none"):
        a = ""
        if arrow:
            a += f' marker-end="url(#{self.marker(stroke)})"'
        if arrow_start:
            a += f' marker-start="url(#{self.marker(stroke)})"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.raw(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" '
                 f'stroke-linejoin="round"{a}/>')

    def arrow(self, x1, y1, x2, y2, color=INK3, sw=1.4, dash=None, both=False):
        self.line(x1, y1, x2, y2, color, sw, dash, arrow=True, arrow_start=both)

    # ---------- composites ----------
    def box(self, x, y, w, h, label="", style="blue", size=13, sub=None, sub_size=11.5, rx=5, sw=1.2,
            weight=None, dash=None, align="middle"):
        fill, stroke, tc = STYLE[style]
        self.rect(x, y, w, h, fill, stroke, sw, rx, dash)
        lines = label if isinstance(label, (list, tuple)) else ([label] if label else [])
        subs = sub if isinstance(sub, (list, tuple)) else ([sub] if sub else [])
        total = len(lines) * size * 1.3 + len(subs) * sub_size * 1.3
        yy = y + h / 2 - total / 2 + size * 0.95
        tx = x + w / 2 if align == "middle" else x + 8
        for ln in lines:
            self.text(tx, yy, ln, size, align if align == "middle" else "start", tc, weight)
            yy += size * 1.3
        sc = tc if style[0].isupper() else INK2
        for ln in subs:
            self.text(tx, yy - size * 0.95 + sub_size * 0.95, ln, sub_size, align if align == "middle" else "start", sc)
            yy += sub_size * 1.3

    def label(self, x, y, s, size=12, anchor="middle", fill=INK2, weight=None):
        self.text(x, y, s, size, anchor, fill, weight)

    def brace_h(self, x1, x2, y, label=None, color=INK3, size=11.5, up=False):
        """Horizontal square bracket with a label below (or above)."""
        d = -6 if up else 6
        self.poly([(x1, y), (x1, y + d), (x2, y + d), (x2, y)], color, 1)
        if label:
            self.text((x1 + x2) / 2, y + d + (size + 3 if not up else -5), label, size, "middle", INK2)

    # ---------- output ----------
    def svg(self, width_mm=None):
        wmm = width_mm or self.w * MM_PER_UNIT
        defs = f"<defs>{''.join(self.markers.values())}</defs>" if self.markers else ""
        body = "\n".join(self.items)
        return (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" font-family="BookSans" '
                f'font-size="13" style="width:{wmm:.1f}mm;max-width:100%">\n{defs}\n{body}\n</svg>\n')

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.svg())


# ---------- charts ----------
def nice_num(v):
    if v == 0:
        return "0"
    if abs(v) >= 1e4 or abs(v) < 1e-3:
        e = int(math.floor(math.log10(abs(v))))
        m = v / 10 ** e
        if abs(m - 1) < 1e-9:
            return f"$10^{{{e}}}$"
        return f"${m:g}×10^{{{e}}}$"
    return f"{v:g}"


class Chart:
    """An x/y plotting area inside a Fig. Data → pixel mapping with optional log axes."""

    def __init__(self, fig, x, y, w, h, xlim, ylim, xlog=False, ylog=False):
        self.f, self.x0, self.y0, self.w, self.h = fig, x, y, w, h
        self.xlim, self.ylim, self.xlog, self.ylog = xlim, ylim, xlog, ylog

    def _t(self, v, lim, log):
        a, b = lim
        if log:
            return (math.log10(v) - math.log10(a)) / (math.log10(b) - math.log10(a))
        return (v - a) / (b - a)

    def X(self, v):
        return self.x0 + self._t(v, self.xlim, self.xlog) * self.w

    def Y(self, v):
        return self.y0 + self.h - self._t(v, self.ylim, self.ylog) * self.h

    def axes(self, xticks, yticks, xlabel=None, ylabel=None, xfmt=nice_num, yfmt=nice_num, grid=True,
             size=11.5, ylabel_pos="top", xgrid=False):
        f = self.f
        for t in yticks:
            yy = self.Y(t)
            if grid:
                f.line(self.x0, yy, self.x0 + self.w, yy, GRID, 1)
            f.text(self.x0 - 6, yy + size * 0.35, yfmt(t), size, "end", INK2)
        for t in xticks:
            xx = self.X(t)
            if xgrid:
                f.line(xx, self.y0, xx, self.y0 + self.h, GRID, 1)
            f.line(xx, self.y0 + self.h, xx, self.y0 + self.h + 4, AXIS, 1)
            f.text(xx, self.y0 + self.h + 6 + size, xfmt(t), size, "middle", INK2)
        f.line(self.x0, self.y0 + self.h, self.x0 + self.w, self.y0 + self.h, AXIS, 1)
        f.line(self.x0, self.y0, self.x0, self.y0 + self.h, AXIS, 1)
        if xlabel:
            f.text(self.x0 + self.w / 2, self.y0 + self.h + 2 * size + 12, xlabel, size, "middle", INK2)
        if ylabel:
            if ylabel_pos == "top":
                f.text(self.x0 - 6, self.y0 - 10, ylabel, size, "start", INK2)
            else:
                cx, cy = self.x0 - 44, self.y0 + self.h / 2
                f.raw(f'<g transform="translate({cx:.1f},{cy:.1f}) rotate(-90)">')
                f.text(0, 0, ylabel, size, "middle", INK2)
                f.raw("</g>")

    def series(self, xs, ys, color, sw=2, dash=None, markers=False, r=3.6, end_label=None, label_dx=6,
               label_dy=4, label_size=11.5):
        pts = [(self.X(a), self.Y(b)) for a, b in zip(xs, ys)]
        self.f.poly(pts, color, sw, dash)
        if markers:
            for (px, py) in pts:
                self.f.circle(px, py, r, color, "#ffffff", 1.5)
        if end_label:
            px, py = pts[-1]
            self.f.text(px + label_dx, py + label_dy, end_label, label_size, "start", INK)
        return pts

    def dots(self, xs, ys, color, r=3.6, ring=True):
        for a, b in zip(xs, ys):
            self.f.circle(self.X(a), self.Y(b), r, color, "#ffffff" if ring else "none", 1.5 if ring else 0)

    def hline(self, v, color=INK3, dash="4 3", label=None, size=11, anchor="end", dy=-4, sw=1):
        yy = self.Y(v)
        self.f.line(self.x0, yy, self.x0 + self.w, yy, color, sw, dash)
        if label:
            x = self.x0 + self.w - 4 if anchor == "end" else self.x0 + 4
            self.f.text(x, yy + dy, label, size, anchor, INK2)

    def vline(self, v, color=INK3, dash="4 3", label=None, size=11, dy=12, sw=1, anchor="start", dx=4):
        xx = self.X(v)
        self.f.line(xx, self.y0, xx, self.y0 + self.h, color, sw, dash)
        if label:
            self.f.text(xx + dx, self.y0 + dy, label, size, anchor, INK2)

    def bar(self, xc, v, width, color, base=None):
        b = self.ylim[0] if base is None else base
        y1, y2 = self.Y(v), self.Y(b)
        top, hgt = min(y1, y2), abs(y2 - y1)
        self.f.rect(xc - width / 2, top, width, hgt, color, "none", 0, 1.5)


def legend(fig, x, y, items, size=11.5, gap=18, horizontal=True):
    """items: list of (label, colour, kind) with kind in {'line','dot','box','dash'}."""
    cx = x
    for k, (lab, col, kind) in enumerate(items):
        yy = y if horizontal else y + k * gap
        xx = cx if horizontal else x
        if kind == "line":
            fig.line(xx, yy - 4, xx + 18, yy - 4, col, 2.2)
        elif kind == "dash":
            fig.line(xx, yy - 4, xx + 18, yy - 4, col, 1.6, "4 3")
        elif kind == "dot":
            fig.circle(xx + 9, yy - 4, 4, col, "#ffffff", 1.5)
        else:
            fig.rect(xx + 2, yy - 10, 14, 11, col, "none", 0, 2)
        fig.text(xx + 23, yy, lab, size, "start", INK)
        if horizontal:
            cx += 23 + text_width(lab, size) + gap
