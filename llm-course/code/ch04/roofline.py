import time, numpy as np

def bench(fn, min_time=0.3):
    fn(); n, t0 = 0, time.perf_counter()
    while time.perf_counter() - t0 < min_time:
        fn(); n += 1
    return (time.perf_counter() - t0) / n

f32 = 4
print("[1] memory bandwidth: y = x + 1 on 64M float32 (256 MB in, 256 MB out)")
x = np.ones(64 * 2**20, dtype=np.float32); y = np.empty_like(x)
t = bench(lambda: np.add(x, 1.0, out=y))
bw = 2 * x.nbytes / t / 1e9
print(f"    {t*1e3:.1f} ms per pass -> {bw:.1f} GB/s, {x.size / t / 1e9:.2f} GFLOP/s (1 FLOP per element)")

print("\n[2] square matmul C = A @ B (float32): arithmetic intensity = 2n^3 / (3 n^2 * 4 bytes) = n/6")
peak = 0
for n in (32, 64, 128, 256, 512, 1024, 2048, 4096):
    A = np.random.rand(n, n).astype(np.float32); B = np.random.rand(n, n).astype(np.float32)
    t = bench(lambda: A @ B, 0.2 if n < 4096 else 1.0)
    g = 2 * n**3 / t / 1e9; peak = max(peak, g)
    print(f"    n={n:5d}  intensity={n/6:7.1f} FLOP/B  {g:8.1f} GFLOP/s")

print("\n[3] batch of B tokens through one 4096x4096 weight matrix: (B x 4096) @ (4096 x 4096)")
K = N = 4096
W = np.random.rand(K, N).astype(np.float32)
for Bt in (1, 4, 16, 64, 256, 1024):
    X = np.random.rand(Bt, K).astype(np.float32)
    t = bench(lambda: X @ W, 0.3)
    inten = 2 * Bt * K * N / ((Bt * K + K * N + Bt * N) * f32)
    print(f"    B={Bt:5d}  intensity={inten:7.1f} FLOP/B  {2*Bt*K*N/t/1e9:8.1f} GFLOP/s   {t*1e3:7.2f} ms  ({t*1e3/Bt:.3f} ms per token)")

print("\n[4] chain of k elementwise ops on 64M floats, unfused (each op = one full memory pass)")
def chain(k):
    def f():
        z = x
        for _ in range(k): z = z * 1.0001 + 0.5     # 2 ops (mul, add) per iteration in numpy
        return z
    return f
for k in (1, 2, 4, 8):
    t = bench(chain(k), 0.3)
    print(f"    k={k}: {t*1e3:7.1f} ms   ({2*k} numpy ops, {2*k*x.size/1e9:.2f} GFLOP total)")

print(f"\nmeasured peak ~{peak:.0f} GFLOP/s, bandwidth ~{bw:.0f} GB/s -> balance point ~{peak/bw:.0f} FLOP/byte")
