"""FlashAttention's math on CPU: tiled causal attention with online softmax == standard attention."""
import time, numpy as np
rng = np.random.default_rng(0)
N, d, Br, Bc = 1024, 64, 128, 128
Q, K, V = (rng.standard_normal((N, d)) for _ in range(3))
scale = 1 / np.sqrt(d)

def standard(Q, K, V):
    S = Q @ K.T * scale                                   # N x N scores (materialized)
    S[np.triu_indices(N, 1)] = -np.inf                    # causal mask
    P = np.exp(S - S.max(1, keepdims=True)); P /= P.sum(1, keepdims=True)
    return P @ V

def flash(Q, K, V):
    O = np.zeros_like(Q); L = np.zeros(N); tiles = skipped = 0
    for i in range(0, N, Br):                            # one Q tile = one GPU thread block
        q = Q[i:i+Br]
        m = np.full(len(q), -np.inf); l = np.zeros(len(q)); o = np.zeros_like(q)
        for j in range(0, N, Bc):                        # stream K/V tiles through "SRAM"
            if j > i + Br - 1: skipped += 1; continue    # tile entirely in the future: skip
            tiles += 1
            s = q @ K[j:j+Bc].T * scale                  # Br x Bc scores, never the full N x N
            qi, kj = np.arange(i, i+len(q))[:, None], np.arange(j, j+Bc)[None, :]
            s = np.where(kj > qi, -np.inf, s)
            m_new = np.maximum(m, s.max(1))
            p = np.exp(s - m_new[:, None])
            corr = np.exp(m - m_new)                     # rescale what was accumulated so far
            l = corr * l + p.sum(1)
            o = corr[:, None] * o + p @ V[j:j+Bc]
            m = m_new
        O[i:i+Br] = o / l[:, None]; L[i:i+Br] = m + np.log(l)   # keep logsumexp for the backward pass
    return O, L, tiles, skipped

ref = standard(Q.copy(), K, V)
out, L, tiles, skipped = flash(Q, K, V)
print(f"max |flash - standard| = {np.abs(out - ref).max():.2e}")
print(f"K/V tiles computed: {tiles}, skipped by causality: {skipped} (of {tiles + skipped})")
print(f"largest score block held at once: {Br}x{Bc} = {Br*Bc:,} numbers vs full matrix {N*N:,}")
for n, h in [(8192, 32), (32768, 32), (131072, 64)]:
    print(f"  materialized S+P in bf16 for N={n:,}, {h} heads, batch 1: {2 * n * n * h * 2 / 1e9:8.1f} GB per layer;"
          f"  FlashAttention keeps O + logsumexp: {(n * h * 128 * 2 + n * h * 4) / 1e6:6.1f} MB")
