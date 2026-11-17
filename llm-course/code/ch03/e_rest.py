import sys, time, numpy as np
sys.path.insert(0, ".")
from nn import Data, Model, Optimizer, train, evaluate, cosine
data = Data(sys.argv[1], K=8); T0 = time.time()
def run(name, steps, lr_fn, kind, B=256, out_scale=0.01, log_at=None, **okw):
    t0 = time.time(); m = Model(data.V, 8, D=16, H=512, depth=1, init="tanh", out_scale=out_scale)
    init_loss = evaluate(m, data, "val", limit=20000)
    log = train(m, data, steps, lr_fn, Optimizer(m.p, kind, **okw), B=B, log_at=log_at or (steps,), quiet=True)
    print(f"  {name:34s} init {init_loss:6.3f}  " + "  ".join(f"step {k}: {v:.3f}" for k, v in log.items())
          + f"  ({time.time()-t0:.0f}s)", flush=True)

print("[E2] output-layer init scale (SGD lr 0.1)")
for s in (0.01, 1 / np.sqrt(512), 1.0):
    run(f"W_out std = {s:.3f}", 2000, lambda t: 0.1, "sgd", out_scale=s, log_at=(200, 2000))

print("[E4] optimizers, 5000 steps")
run("SGD lr=0.1", 5000, lambda t: 0.1, "sgd", log_at=(500, 5000))
run("SGD+momentum(0.9) lr=0.01", 5000, lambda t: 0.01, "momentum", log_at=(500, 5000))
run("Adam lr=3e-3", 5000, lambda t: 3e-3, "adam", log_at=(500, 5000))

print("[E5] learning-rate schedules with Adam, 5000 steps")
run("constant 3e-3", 5000, lambda t: 3e-3, "adam")
run("warmup 250 + cosine, peak 3e-3", 5000, cosine(3e-3, 5000, warmup=250), "adam")
run("constant 3e-2 (too high)", 5000, lambda t: 3e-2, "adam", log_at=(100, 5000))
run("warmup 250 + cosine, peak 3e-2", 5000, cosine(3e-2, 5000, warmup=250), "adam", log_at=(100, 5000))

print("[E6] batch size, same 640k training examples, Adam 3e-3")
for B in (32, 128, 512, 2048):
    run(f"B={B:4d}  steps={640000 // B}", 640000 // B, lambda t: 3e-3, "adam", B=B)
print(f"total {time.time()-T0:.0f}s")
