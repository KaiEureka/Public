import math, torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0)

class RMSNorm(nn.Module):
    def __init__(self, d, eps=1e-6):
        super().__init__(); self.eps, self.weight = eps, nn.Parameter(torch.ones(d))
    def forward(self, x):
        return self.weight * x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)

def rope_cache(T, dh, base=10000.0):
    freqs = base ** (-torch.arange(0, dh, 2).float() / dh)        # one frequency per pair of dims
    ang = torch.arange(T).float()[:, None] * freqs[None, :]        # (T, dh/2): angle = position * freq
    return ang.cos(), ang.sin()

def apply_rope(x, cos, sin):                                       # x: (B, H, T, dh)
    x1, x2 = x[..., 0::2], x[..., 1::2]                            # pairs (x1, x2) = one 2-D plane each
    return torch.stack((x1 * cos - x2 * sin, x1 * sin + x2 * cos), dim=-1).flatten(-2)

class GQAttention(nn.Module):
    def __init__(self, d, n_heads, n_kv_heads):
        super().__init__()
        self.h, self.kv, self.dh = n_heads, n_kv_heads, d // n_heads
        self.wq = nn.Linear(d, n_heads * self.dh, bias=False)
        self.wk = nn.Linear(d, n_kv_heads * self.dh, bias=False)  # fewer K/V heads than Q heads
        self.wv = nn.Linear(d, n_kv_heads * self.dh, bias=False)
        self.wo = nn.Linear(n_heads * self.dh, d, bias=False)
    def forward(self, x, cos, sin):
        B, T, _ = x.shape
        q = self.wq(x).view(B, T, self.h, self.dh).transpose(1, 2)
        k = self.wk(x).view(B, T, self.kv, self.dh).transpose(1, 2)
        v = self.wv(x).view(B, T, self.kv, self.dh).transpose(1, 2)
        q, k = apply_rope(q, cos, sin), apply_rope(k, cos, sin)    # rotate q and k, not v
        g = self.h // self.kv
        k, v = k.repeat_interleave(g, dim=1), v.repeat_interleave(g, dim=1)  # each K/V head serves g Q heads
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.wo(y.transpose(1, 2).reshape(B, T, -1))

class SwiGLU(nn.Module):
    def __init__(self, d, hidden):
        super().__init__()
        self.w_gate = nn.Linear(d, hidden, bias=False)
        self.w_up = nn.Linear(d, hidden, bias=False)
        self.w_down = nn.Linear(hidden, d, bias=False)
    def forward(self, x):
        return self.w_down(F.silu(self.w_gate(x)) * self.w_up(x))

class ModernBlock(nn.Module):
    def __init__(self, d, n_heads, n_kv_heads, hidden):
        super().__init__()
        self.norm1, self.norm2 = RMSNorm(d), RMSNorm(d)
        self.attn, self.mlp = GQAttention(d, n_heads, n_kv_heads), SwiGLU(d, hidden)
    def forward(self, x, cos, sin):
        x = x + self.attn(self.norm1(x), cos, sin)
        return x + self.mlp(self.norm2(x))

# 1) RoPE: the q.k score depends only on the relative offset m - n
dh = 64; cos, sin = rope_cache(4096, dh)
q, k = torch.randn(dh), torch.randn(dh)
def score(m, n):
    qm = apply_rope(q.view(1, 1, 1, dh), cos[m:m+1], sin[m:m+1]).flatten()
    kn = apply_rope(k.view(1, 1, 1, dh), cos[n:n+1], sin[n:n+1]).flatten()
    return (qm @ kn).item()
print("RoPE scores:  (5,3) =", f"{score(5,3):.5f}", " (105,103) =", f"{score(105,103):.5f}",
      " (3005,3003) =", f"{score(3005,3003):.5f}", " | (5,1) =", f"{score(5,1):.5f}")

# 2) the block runs, and its parameter count matches 4d^2-ish attention budget accounting
blk = ModernBlock(d=256, n_heads=8, n_kv_heads=2, hidden=688)
x = torch.randn(2, 16, 256); c, s = rope_cache(16, 32)
print("block output shape:", tuple(blk(x, c, s).shape), " params:", sum(p.numel() for p in blk.parameters()))

# 3) Llama 3 8B parameter count from its config
d, L, H, KV, F_, V = 4096, 32, 32, 8, 14336, 128256
dh = d // H
attn = d * H * dh + 2 * d * KV * dh + H * dh * d
mlp = 3 * d * F_
total = L * (attn + mlp + 2 * d) + 2 * V * d + d
print(f"Llama 3 8B: attention/layer {attn/1e6:.1f}M, MLP/layer {mlp/1e6:.1f}M, total {total/1e9:.3f}B")
for name, kv in [("MHA (32 KV heads)", 32), ("GQA (8 KV heads)", 8), ("MQA (1 KV head)", 1)]:
    per_tok = 2 * L * kv * dh * 2
    print(f"  KV cache {name:18s}: {per_tok/1024:6.0f} KB per token, {per_tok*131072/2**30:5.1f} GB for a 128K-token sequence")
