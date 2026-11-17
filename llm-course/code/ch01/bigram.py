import sys
import numpy as np
from collections import Counter

text = open(sys.argv[1], encoding="utf-8").read()
chars = sorted(set(text))
V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
ids = np.array([stoi[c] for c in text], dtype=np.int64)
n = int(0.9 * len(ids))
train, val = ids[:n], ids[n:]
print(f"chars={len(ids):,}  vocab V={V}  train={len(train):,}  val={len(val):,}")

# 1) uniform model
print(f"\n[uniform]  loss = ln V = {np.log(V):.4f} nats/char")

# 2) unigram counting
uni = np.bincount(train, minlength=V) + 1.0
p_uni = uni / uni.sum()
print(f"[unigram]  val loss = {-np.log(p_uni[val]).mean():.4f}")

# 3) bigram counting (MLE + add-1 smoothing)
C = np.zeros((V, V))
np.add.at(C, (train[:-1], train[1:]), 1)
P_count = (C + 1) / (C + 1).sum(1, keepdims=True)
bigram_val = -np.log(P_count[val[:-1], val[1:]]).mean()
bigram_train = -np.log(P_count[train[:-1], train[1:]]).mean()
print(f"[bigram counting]  train loss = {bigram_train:.4f}  val loss = {bigram_val:.4f}")

# 4) "neural" bigram: a V x V logit table trained by gradient descent on cross-entropy
W = np.zeros((V, V))  # all-zero logits => uniform => initial loss should equal ln V
N = C.sum()
row = C.sum(1, keepdims=True)
lr, b1, b2 = 0.1, 0.9, 0.999
m = np.zeros_like(W); v = np.zeros_like(W)
for step in range(1, 1001):
    Z = W - W.max(1, keepdims=True)
    P = np.exp(Z); P /= P.sum(1, keepdims=True)
    loss = -(C * np.log(P + 1e-12)).sum() / N
    if step in (1, 10, 50, 200, 1000):
        print(f"  step {step:4d}  train loss = {loss:.4f}")
    grad = (row * P - C) / N  # d loss / d logits = softmax - onehot, summed over counts
    m = b1 * m + (1 - b1) * grad; v = b2 * v + (1 - b2) * grad**2   # Adam
    W -= lr * (m / (1 - b1**step)) / (np.sqrt(v / (1 - b2**step)) + 1e-8)
Z = W - W.max(1, keepdims=True); P = np.exp(Z); P /= P.sum(1, keepdims=True)
print(f"[neural bigram]  val loss = {-np.log(P[val[:-1], val[1:]]).mean():.4f}")

# 5) sampling from the bigram model at different temperatures
rng = np.random.default_rng(0)
logP = np.log(P_count)
for T in (1.0, 0.5):
    cur, out = stoi["\n"], []
    for _ in range(200):
        z = logP[cur] / T
        p = np.exp(z - z.max()); p /= p.sum()
        cur = rng.choice(V, p=p)
        out.append(chars[cur])
    print(f"\n--- bigram sample, temperature {T} ---\n{''.join(out)}")

# 6) why counting doesn't scale: n-gram with add-k smoothing
print("\n[n-gram counting, add-0.01 smoothing]")
k = 0.01
for order in range(1, 8):
    ctx_len = order - 1
    tr = text[:n]; va = text[n:]
    ctx_counts, full_counts = Counter(), Counter()
    for i in range(ctx_len, len(tr)):
        ctx = tr[i - ctx_len:i]
        ctx_counts[ctx] += 1
        full_counts[ctx + tr[i]] += 1
    tot, unseen = 0.0, 0
    m = len(va) - ctx_len
    for i in range(ctx_len, len(va)):
        ctx = va[i - ctx_len:i]
        if ctx not in ctx_counts:
            unseen += 1
        p = (full_counts.get(ctx + va[i], 0) + k) / (ctx_counts.get(ctx, 0) + k * V)
        tot -= np.log(p)
    print(f"  {order}-gram: distinct contexts={len(ctx_counts):>8,}  "
          f"val contexts never seen in train={unseen / m:6.1%}  val loss={tot / m:.4f}")
