"""Bengio-style MLP character language model, numpy only, hand-written backward pass."""
import sys, time
import numpy as np

text = open(sys.argv[1], encoding="utf-8").read()
STEPS = int(sys.argv[2]) if len(sys.argv) > 2 else 30000
chars = sorted(set(text)); V = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
ids = np.array([stoi[c] for c in text], dtype=np.int64)
n = int(0.9 * len(ids)); train, val = ids[:n], ids[n:]

K = int(sys.argv[3]) if len(sys.argv) > 3 else 8   # context length
D, H = 16, 512                # embedding dim, hidden units
B = 256                       # batch size
rng = np.random.default_rng(0)

def init(dtype):
    p = {
        "E":  rng.normal(0, 1, (V, D)),
        "W1": rng.normal(0, 1, (K * D, H)) * (5 / 3) / np.sqrt(K * D),
        "b1": np.zeros(H),
        "W2": rng.normal(0, 1, (H, V)) * 0.01,   # small output layer => initial loss ~ ln V
        "b2": np.zeros(V),
    }
    return {k: v.astype(dtype) for k, v in p.items()}

def batch(data, pos):
    ctx = data[pos[:, None] + np.arange(K)]       # (B, K) context chars
    return ctx, data[pos + K]                     # targets: the char right after the context

def forward(p, ctx, y):
    x = p["E"][ctx].reshape(len(ctx), K * D)      # embedding lookup + concatenate
    a = x @ p["W1"] + p["b1"]
    h = np.tanh(a)
    logits = h @ p["W2"] + p["b2"]
    m = logits.max(1, keepdims=True)
    logp = logits - m - np.log(np.exp(logits - m).sum(1, keepdims=True))
    loss = -logp[np.arange(len(y)), y].mean()
    return loss, (x, h, logp)

def backward(p, ctx, y, cache):
    x, h, logp = cache
    Bn = len(y)
    dlogits = np.exp(logp); dlogits[np.arange(Bn), y] -= 1; dlogits /= Bn   # softmax - onehot
    g = {"W2": h.T @ dlogits, "b2": dlogits.sum(0)}
    dh = dlogits @ p["W2"].T
    da = dh * (1 - h * h)                                                 # tanh'
    g["W1"] = x.T @ da; g["b1"] = da.sum(0)
    dx = (da @ p["W1"].T).reshape(Bn, K, D)
    dE = np.zeros_like(p["E"]); np.add.at(dE, ctx, dx)                    # scatter-add into rows used
    g["E"] = dE
    return g

# ---- gradient check (float64, tiny batch) ----
p64 = init(np.float64)
ctx, y = batch(train, rng.integers(0, len(train) - K, 8))
loss, cache = forward(p64, ctx, y); g = backward(p64, ctx, y, cache)
print("gradient check (analytic vs numerical):")
for name in ["E", "W1", "b1", "W2", "b2"]:
    idx = tuple(rng.integers(0, s) for s in p64[name].shape)
    if name == "E": idx = (ctx[0, 0], idx[1])
    old = p64[name][idx]; eps = 1e-5
    p64[name][idx] = old + eps; lp, _ = forward(p64, ctx, y)
    p64[name][idx] = old - eps; lm, _ = forward(p64, ctx, y)
    p64[name][idx] = old
    num = (lp - lm) / (2 * eps)
    print(f"  {name:2s}{str(idx):12s} analytic={g[name][idx]: .8f}  numerical={num: .8f}")

# ---- training: minibatch SGD ----
p = init(np.float32)
nparams = sum(v.size for v in p.values())
print(f"\nparams = {nparams:,}   context K={K}  emb D={D}  hidden H={H}")

def evaluate(data, limit=None):
    pos = np.arange(len(data) - K)
    if limit: pos = pos[:limit]
    tot = 0.0
    for i in range(0, len(pos), 4096):
        c, t = batch(data, pos[i:i + 4096]); l, _ = forward(p, c, t); tot += l * len(t)
    return tot / len(pos)

print(f"step     0  train {evaluate(train, 50000):.4f}  val {evaluate(val):.4f}   (ln V = {np.log(V):.4f})")
t0 = time.time()
for step in range(1, STEPS + 1):
    lr = 0.1 if step < STEPS * 0.6 else (0.03 if step < STEPS * 0.85 else 0.01)
    ctx, y = batch(train, rng.integers(0, len(train) - K, B))
    loss, cache = forward(p, ctx, y)
    g = backward(p, ctx, y, cache)
    for k in p: p[k] -= lr * g[k]
    if step in (100, 1000, 5000) or step % 10000 == 0:
        print(f"step {step:5d}  train {evaluate(train, 50000):.4f}  val {evaluate(val):.4f}   ({time.time() - t0:.0f}s)")
np.savez(f"mlp_params_K{K}.npz", **p)

# ---- what did it learn? ----
def predict(context):
    c = np.array([[stoi[ch] for ch in context[-K:]]])
    _, (_, _, logp) = forward(p, c, np.array([0]))
    pr = np.exp(logp[0]); top = np.argsort(-pr)[:4]
    return ", ".join(f"{chars[i]!r} {pr[i]:.2f}" for i in top)

print("\npredictions for the next char:")
for ctx_s in ["accept hi", "the King ", " the Kin", "Kin", " kin"]:
    s = ctx_s.rjust(K)[-K:]
    print(f"  {s!r:12s} -> {predict(s)}")

E = p["E"] / np.linalg.norm(p["E"], axis=1, keepdims=True)
sim = E @ E.T
print("\nnearest characters by embedding (cosine similarity):")
for ch in ["a", "e", "k", "K", "T", "t", ",", "!", "3"]:
    i = stoi[ch]; order = [j for j in np.argsort(-sim[i]) if j != i][:5]
    print(f"  {ch!r}: " + "  ".join(f"{chars[j]!r}" for j in order))

print("\nsample (temperature 0.8):")
c = list(train[:K]); out = []
for _ in range(400):
    _, (_, _, logp) = forward(p, np.array([c[-K:]]), np.array([0]))
    z = logp[0] / 0.8; pr = np.exp(z - z.max()); pr /= pr.sum()
    nxt = rng.choice(V, p=pr); c.append(nxt); out.append(chars[nxt])
print("".join(out))
