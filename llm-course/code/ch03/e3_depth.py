import sys, time, numpy as np
sys.path.insert(0, ".")
from nn import Data, Model, Optimizer, train
data = Data(sys.argv[1], K=8); lr = float(sys.argv[2]); steps = int(sys.argv[3])
configs = [("1 layer (reference)", dict(depth=1, init="tanh")),
           ("20 plain, std=1", dict(depth=20, init="std1")),
           ("20 plain, 1/sqrt(n)", dict(depth=20, init="xavier")),
           ("20 plain, (5/3)/sqrt(n)", dict(depth=20, init="tanh")),
           ("20 residual + RMSNorm", dict(depth=20, init="tanh", residual=True))]
for name, kw in configs:
    t0 = time.time()
    m = Model(data.V, 8, D=16, H=128, **kw)
    log = train(m, data, steps, lambda s: lr, Optimizer(m.p, "sgd"), log_at=(500, steps // 2, steps), quiet=True)
    print(f"{name:26s} " + "  ".join(f"step {k}: {v:.3f}" for k, v in log.items()) + f"   ({time.time()-t0:.0f}s)", flush=True)
