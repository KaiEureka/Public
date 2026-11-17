import sys
from collections import Counter
text = open(sys.argv[1], encoding="utf-8").read()
n = int(0.9 * len(text)); tr, va = text[:n], text[n:]
print("vocab:", repr("".join(sorted(set(text)))))
cnt = Counter(tr)
print("most common:", [(c, k) for c, k in cnt.most_common(6)])
print("rarest:", [(c, k) for c, k in cnt.most_common()[-6:]])
def nxt(ctx, top=6):
    c = Counter(tr[i + len(ctx)] for i in range(len(tr) - len(ctx)) if tr.startswith(ctx, i))
    tot = sum(c.values())
    return tot, [(ch, k, round(k / tot, 3)) for ch, k in c.most_common(top)]
for ctx in ["q", "t", "the k", " kin", " Kin", "KING"]:
    print(repr(ctx), nxt(ctx))
# a 6-char context from validation never seen in training
seen6 = set(tr[i:i+6] for i in range(len(tr) - 6))
for i in range(2000, len(va) - 7):
    ctx = va[i:i+6]
    if ctx not in seen6 and ctx.isascii() and "\n" not in ctx:
        print("unseen 6-char context in val:", repr(ctx), "-> next:", repr(va[i+6]), "| surrounding:", repr(va[i-20:i+20]))
        break
