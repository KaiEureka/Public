"""Toy model collapse: refit a word-frequency (unigram) model on its own samples, generation after generation."""
import sys, re
import numpy as np
rng = np.random.default_rng(0)
words = re.findall(r"[a-z']+", open(sys.argv[1], encoding="utf-8").read().lower())
vocab, counts0 = np.unique(words, return_counts=True)
N = len(words); p0 = counts0 / N
rare = counts0 <= 2                                   # words seen once or twice in the real corpus
def stats(c):
    p = c / c.sum(); nz = p[p > 0]
    return (p > 0).sum(), -(nz * np.log2(nz)).sum(), (c[rare] > 0).mean()
print(f"real corpus: {N:,} words, vocab {len(vocab):,}, rare words (count<=2): {rare.sum():,}")
print("gen |  REPLACE: vocab  entropy  rare-words-alive |  ACCUMULATE: vocab  entropy  rare-words-alive")
c_rep = counts0.astype(float); c_acc = counts0.astype(float)
for g in range(0, 31):
    if g in (0, 1, 2, 5, 10, 20, 30):
        v1, h1, r1 = stats(c_rep); v2, h2, r2 = stats(c_acc)
        print(f"{g:3d} |          {v1:6,d}   {h1:6.3f}      {r1:6.1%}       |             {v2:6,d}   {h2:6.3f}      {r2:6.1%}")
    s_rep = rng.multinomial(N, c_rep / c_rep.sum()).astype(float)   # train only on the last generation's samples
    s_acc = rng.multinomial(N, c_acc / c_acc.sum()).astype(float)
    c_rep = s_rep
    c_acc = c_acc + s_acc                                             # keep real data + all synthetic so far
