"""Configurable character-level MLP LM (numpy, hand-written backward) for lesson 3 experiments.

Plain net:    x0 -> tanh(x0 W0) -> tanh(h W1) -> ... -> logits
Residual net: x0 -> h = x0 Win -> h = h + tanh(rms(h) W_l) (L times) -> rms(h) -> logits
"""
import numpy as np

class Data:
    def __init__(self, path, K):
        text = open(path, encoding="utf-8").read()
        self.chars = sorted(set(text)); self.V = len(self.chars)
        ids = np.array([{c: i for i, c in enumerate(self.chars)}[c] for c in text], dtype=np.int64)
        n = int(0.9 * len(ids)); self.train, self.val = ids[:n], ids[n:]; self.K = K

    def batch(self, split, pos):
        d = self.train if split == "train" else self.val
        return d[pos[:, None] + np.arange(self.K)], d[pos + self.K]

def rms(h, eps=1e-6):
    r = 1.0 / np.sqrt((h * h).mean(1, keepdims=True) + eps)
    return h * r, r

def rms_backward(dn, h, r):
    return r * dn - (r ** 3) * h * (dn * h).mean(1, keepdims=True)

class Model:
    def __init__(self, V, K, D=16, H=512, depth=1, residual=False, init="tanh",
                 out_scale=0.01, seed=0, dtype=np.float32):
        rng = np.random.default_rng(seed)
        self.K, self.D, self.H, self.depth, self.residual = K, D, H, depth, residual
        def w(fan_in, fan_out):
            s = {"std1": 1.0, "xavier": 1 / np.sqrt(fan_in), "tanh": (5 / 3) / np.sqrt(fan_in)}[init]
            return rng.normal(0, s, (fan_in, fan_out))
        p = {"E": rng.normal(0, 1, (V, D))}
        if residual:
            p["Win"] = rng.normal(0, 1 / np.sqrt(K * D), (K * D, H))
            for l in range(depth):
                p[f"W{l}"] = w(H, H); p[f"b{l}"] = np.zeros(H)
        else:
            for l in range(depth):
                p[f"W{l}"] = w(K * D if l == 0 else H, H); p[f"b{l}"] = np.zeros(H)
        p["Wout"] = rng.normal(0, out_scale, (H, V)); p["bout"] = np.zeros(V)
        self.p = {k: v.astype(dtype) for k, v in p.items()}

    def forward(self, ctx, y):
        p, B = self.p, len(ctx)
        x0 = p["E"][ctx].reshape(B, -1)
        cache = {"ctx": ctx, "x0": x0, "layers": []}
        if self.residual:
            h = x0 @ p["Win"]
            for l in range(self.depth):
                n, r = rms(h); t = np.tanh(n @ p[f"W{l}"] + p[f"b{l}"])
                cache["layers"].append((h, n, r, t)); h = h + t
            hf, rf = rms(h); cache["final"] = (h, hf, rf)
        else:
            h = x0
            for l in range(self.depth):
                hin = h; h = np.tanh(hin @ p[f"W{l}"] + p[f"b{l}"])
                cache["layers"].append((hin, h))
            hf = h
        logits = hf @ p["Wout"] + p["bout"]
        m = logits.max(1, keepdims=True)
        logp = logits - m - np.log(np.exp(logits - m).sum(1, keepdims=True))
        cache["hf"], cache["logp"] = hf, logp
        return -logp[np.arange(B), y].mean(), cache

    def backward(self, y, cache):
        p, B = self.p, len(y)
        g, dacts = {}, []
        dlogits = np.exp(cache["logp"]); dlogits[np.arange(B), y] -= 1; dlogits /= B
        g["Wout"] = cache["hf"].T @ dlogits; g["bout"] = dlogits.sum(0)
        dh = dlogits @ p["Wout"].T
        if self.residual:
            h, hf, rf = cache["final"]; dh = rms_backward(dh, h, rf)
            for l in reversed(range(self.depth)):
                hin, n, r, t = cache["layers"][l]
                dacts.append(np.sqrt((dh * dh).mean()))
                da = dh * (1 - t * t)
                g[f"W{l}"] = n.T @ da; g[f"b{l}"] = da.sum(0)
                dh = dh + rms_backward(da @ p[f"W{l}"].T, hin, r)
            g["Win"] = cache["x0"].T @ dh; dx0 = dh @ p["Win"].T
        else:
            for l in reversed(range(self.depth)):
                hin, h = cache["layers"][l]
                dacts.append(np.sqrt((dh * dh).mean()))
                da = dh * (1 - h * h)
                g[f"W{l}"] = hin.T @ da; g[f"b{l}"] = da.sum(0)
                dh = da @ p[f"W{l}"].T
            dx0 = dh
        dE = np.zeros_like(p["E"]); np.add.at(dE, cache["ctx"], dx0.reshape(B, self.K, self.D))
        g["E"] = dE
        self.grad_act_rms = dacts[::-1]          # RMS of dLoss/d(layer output), layer 0 first
        return g

class Optimizer:
    def __init__(self, params, kind="sgd", beta1=0.9, beta2=0.999, wd=0.0, clip=None):
        self.kind, self.b1, self.b2, self.wd, self.clip, self.t = kind, beta1, beta2, wd, clip, 0
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}

    def step(self, params, grads, lr):
        self.t += 1
        if self.clip is not None:
            norm = np.sqrt(sum((g * g).sum() for g in grads.values()))
            if norm > self.clip:
                grads = {k: g * (self.clip / norm) for k, g in grads.items()}
        for k in params:
            g = grads[k]
            if self.kind == "sgd":
                params[k] -= lr * g
            elif self.kind == "momentum":
                self.m[k] = self.b1 * self.m[k] + g
                params[k] -= lr * self.m[k]
            elif self.kind == "adam":
                self.m[k] = self.b1 * self.m[k] + (1 - self.b1) * g
                self.v[k] = self.b2 * self.v[k] + (1 - self.b2) * g * g
                mh = self.m[k] / (1 - self.b1 ** self.t); vh = self.v[k] / (1 - self.b2 ** self.t)
                params[k] -= lr * (mh / (np.sqrt(vh) + 1e-8) + self.wd * params[k])

def evaluate(model, data, split, limit=None):
    d = data.train if split == "train" else data.val
    pos = np.arange(len(d) - data.K)
    if limit: pos = pos[:limit]
    tot = 0.0
    for i in range(0, len(pos), 4096):
        c, t = data.batch(split, pos[i:i + 4096]); l, _ = model.forward(c, t); tot += l * len(t)
    return tot / len(pos)

def train(model, data, steps, lr_fn, opt, B=256, seed=1, log_at=(), quiet=False):
    rng = np.random.default_rng(seed); log = {}
    for step in range(1, steps + 1):
        ctx, y = data.batch("train", rng.integers(0, len(data.train) - data.K, B))
        loss, cache = model.forward(ctx, y)
        if not np.isfinite(loss):
            log[step] = float("nan"); break
        g = model.backward(y, cache)
        opt.step(model.p, g, lr_fn(step))
        if step in log_at:
            log[step] = evaluate(model, data, "val")
            if not quiet: print(f"    step {step:6d}  val {log[step]:.4f}", flush=True)
    return log

def cosine(peak, steps, warmup=0, final_frac=0.1):
    def f(step):
        if step <= warmup: return peak * step / warmup
        prog = (step - warmup) / max(1, steps - warmup)
        return peak * (final_frac + (1 - final_frac) * 0.5 * (1 + np.cos(np.pi * prog)))
    return f
