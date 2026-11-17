"""Insert <figure> blocks into chapter sources. Idempotent: a figure whose id is already present is skipped.

spec: (chapter_file, anchor, fig_id, svg_name, caption, ref) — the figure goes after the first line containing
`anchor`; if `ref` is given, the anchor line gets "（{{fig_id}}）" inserted right after the substring `ref`."""
import os, re
SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")


def insert(specs):
    for chf, anchor, fid, svg, caption, ref in specs:
        path = os.path.join(SRC, chf)
        s = open(path, encoding="utf-8").read()
        if f'id="{fid}"' in s:
            continue
        lines = s.split("\n")
        before = anchor.startswith("^")
        key = anchor[1:] if before else anchor
        hits = [i for i, l in enumerate(lines) if key in l]
        if len(hits) != 1:
            raise SystemExit(f"{chf}: anchor {anchor!r} matched {len(hits)} lines")
        i = hits[0]
        if ref:
            if ref not in lines[i]:
                raise SystemExit(f"{chf}: ref {ref!r} not in anchor line")
            lines[i] = lines[i].replace(ref, ref + "（{{" + fid + "}}）", 1)
        # skip to the end of a table / list block that the anchor line belongs to
        j = i
        while not before and j + 1 < len(lines) and lines[j + 1].strip() and (
                lines[j + 1].startswith("|") or lines[j].startswith("|") or re.match(r"(\s*[-*] |\s*\d+\. )", lines[j + 1])):
            j += 1
        if before:
            j = i - 1
        block = ["", f'<figure id="{fid}" data-svg="{svg}">', f"<figcaption>{caption}</figcaption>", "</figure>"]
        if before:
            block = block[1:] + [""] if not lines[i - 1].strip() else block + [""]
        lines[j + 1:j + 1] = block
        open(path, "w", encoding="utf-8").write("\n".join(lines))
        print("inserted", fid)


def addref(specs):
    """specs: (chapter_file, old, new). Replaces a unique substring once; skipped if `new` is already there."""
    for chf, old, new in specs:
        path = os.path.join(SRC, chf)
        s = open(path, encoding="utf-8").read()
        if new in s:
            continue
        if s.count(old) != 1:
            raise SystemExit(f"{chf}: {old!r} occurs {s.count(old)} times")
        open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))
