import sys, numpy as np
sys.path.insert(0, ".")
from nn import Data, Model
data = Data(sys.argv[1], K=8)
rng = np.random.default_rng(0)
for residual in (False, True):
    m = Model(data.V, 8, D=4, H=16, depth=3, residual=residual, dtype=np.float64, out_scale=0.5)
    ctx, y = data.batch("train", rng.integers(0, 10000, 6))
    loss, cache = m.forward(ctx, y); g = m.backward(y, cache)
    worst = 0
    for k, v in m.p.items():
        for _ in range(5):
            idx = tuple(rng.integers(0, s) for s in v.shape)
            if k == "E": idx = (ctx[0, 0], idx[1])
            old = v[idx]; v[idx] = old + 1e-6; lp, _ = m.forward(ctx, y)
            v[idx] = old - 1e-6; lm, _ = m.forward(ctx, y); v[idx] = old
            num = (lp - lm) / 2e-6
            worst = max(worst, abs(num - g[k][idx]) / max(1e-8, abs(num) + abs(g[k][idx])))
    print("residual" if residual else "plain", "max relative error:", f"{worst:.2e}")
