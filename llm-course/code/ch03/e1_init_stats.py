import sys, numpy as np
sys.path.insert(0, ".")
from nn import Data, Model
data = Data(sys.argv[1], K=8)
ctx, y = data.batch("train", np.random.default_rng(0).integers(0, len(data.train) - 8, 512))
configs = [("plain, std=1", dict(init="std1")), ("plain, std=1/sqrt(n)", dict(init="xavier")),
           ("plain, std=(5/3)/sqrt(n)", dict(init="tanh")), ("residual + RMSNorm", dict(init="tanh", residual=True))]
for name, kw in configs:
    m = Model(data.V, 8, D=16, H=128, depth=20, **kw)
    loss, cache = m.forward(ctx, y); m.backward(y, cache)
    if m.residual:
        acts = [(L[0] + L[3]) for L in cache["layers"]]; branch = [L[3] for L in cache["layers"]]
        sat = [np.mean(np.abs(b) > 0.97) for b in branch]
    else:
        acts = [L[1] for L in cache["layers"]]; sat = [np.mean(np.abs(a) > 0.97) for a in acts]
    std = [a.std() for a in acts]; gr = m.grad_act_rms
    print(f"\n{name}   initial loss {loss:.3f}")
    print("  layer:          " + "".join(f"{l:>8d}" for l in (1, 2, 5, 10, 15, 20)))
    print("  activation std: " + "".join(f"{std[l-1]:8.3f}" for l in (1, 2, 5, 10, 15, 20)))
    print("  saturated(>.97):" + "".join(f"{sat[l-1]:8.1%}" for l in (1, 2, 5, 10, 15, 20)))
    print("  grad RMS:       " + "".join(f"{gr[l-1]:8.1e}" for l in (1, 2, 5, 10, 15, 20)))
