"""Set (or clear) data-scale on every generated figure of the given chapters: python3 figs/scale.py 0.94 ch04 ch08"""
import os, re, sys
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
scale, chapters = sys.argv[1], sys.argv[2:]
for ch in chapters:
    path = os.path.join(SRC, ch + ".md")
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'(<figure id="[^"]+" data-svg="[^"]+")( data-scale="[0-9.]+")?>',
               lambda m: m.group(1) + ("" if scale == "1" else f' data-scale="{scale}"') + ">", s)
    open(path, "w", encoding="utf-8").write(s)
    print(ch, len(re.findall(r'data-scale=', s)), "figures scaled")
