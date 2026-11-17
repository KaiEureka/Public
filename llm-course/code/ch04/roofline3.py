import time, numpy as np
def bench(fn, reps=3):
    fn(); t0 = time.perf_counter()
    for _ in range(reps): fn()
    return (time.perf_counter() - t0) / reps
print("[1] bandwidth: y = x * 1.0001 on 256M float32 (1 GB in, 1 GB out; L3 cache is 260 MB)")
x = np.ones(256 * 2**20, dtype=np.float32); buf = np.empty_like(x)
t = bench(lambda: np.multiply(x, 1.0001, out=buf))
print(f"    {t*1e3:.0f} ms per pass -> {2*x.nbytes/t/1e9:.1f} GB/s")
print("\n[4] k unfused elementwise ops (each op reads + writes the whole 1 GB array)")
def chain(k):
    def f():
        np.multiply(x, 1.0001, out=buf)
        for _ in range(k - 1): np.multiply(buf, 1.0001, out=buf)
    return f
for k in (1, 2, 4, 8):
    t = bench(chain(k), 2)
    print(f"    k={k} ops: {t*1e3:6.0f} ms")
del x, buf
print("\n[3] (B x 16384) @ (16384 x 16384) float32, weight = 1 GB")
K = N = 16384
W = np.random.rand(K, N).astype(np.float32)
for Bt in (1, 8, 32, 128, 512):
    X = np.random.rand(Bt, K).astype(np.float32)
    t = bench(lambda: X @ W, 3 if Bt < 512 else 1)
    inten = 2 * Bt * K * N / ((Bt * K + K * N + Bt * N) * 4)
    print(f"    B={Bt:4d}  intensity={inten:6.1f} FLOP/B  {2*Bt*K*N/t/1e9:6.1f} GFLOP/s  {t*1e3:7.1f} ms total  {t*1e3/Bt:6.2f} ms per token")
