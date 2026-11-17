import torch
torch.manual_seed(0)
f32, f16, bf16 = torch.float32, torch.float16, torch.bfloat16

print("[1] range")
for v in (70000.0, 1e-8):
    print(f"  {v:g}:  fp16 -> {torch.tensor(v, dtype=f16).item():g}   bf16 -> {torch.tensor(v, dtype=bf16).item():g}")
for dt in (f32, f16, bf16):
    fi = torch.finfo(dt)
    print(f"  {str(dt):15s} max={fi.max:.3g}  smallest normal={fi.tiny:.3g}  eps(spacing at 1.0)={fi.eps:.3g}")

print("\n[2] precision: 1 + 0.001")
for dt in (f32, f16, bf16):
    print(f"  {str(dt):15s} {(torch.tensor(1.0, dtype=dt) + torch.tensor(0.001, dtype=dt)).item():.7f}")

print("\n[3] sequential sum of 10,000 x 0.01 (should be 100)")
for dt in (f32, f16, bf16):
    s = torch.tensor(0.0, dtype=dt); x = torch.tensor(0.01, dtype=dt)
    for _ in range(10000): s = s + x
    print(f"  accumulate in {str(dt):15s}: {s.item():.4f}")

print("\n[4] 1000 optimizer updates of -1e-4 applied to a weight w=1.0 (should end at 0.9)")
def sr_bf16(x):                              # stochastic rounding fp32 -> bf16
    i = x.view(torch.int32)
    noise = torch.randint(0, 1 << 16, i.shape, dtype=torch.int32)
    return ((i + noise) & -65536).view(torch.float32).to(bf16)
w32 = torch.ones(10000); w16 = torch.ones(10000, dtype=bf16); wsr = torch.ones(10000, dtype=bf16)
for _ in range(1000):
    w32 -= 1e-4
    w16 = (w16.float() - 1e-4).to(bf16)        # round-to-nearest
    wsr = sr_bf16(wsr.float() - 1e-4)          # stochastic rounding
print(f"  fp32 master weight:            {w32.mean().item():.4f}")
print(f"  bf16 weight, round-to-nearest: {w16.float().mean().item():.4f}")
print(f"  bf16 weight, stochastic round: {wsr.float().mean().item():.4f}  (mean of 10,000 weights; one weight: {wsr[0].item():.4f})")

print("\n[5] fp16 gradient underflow and loss scaling")
g = torch.tensor([3e-8, 1e-6, 1e-4])
print("  true grads:            ", g.tolist())
print("  stored in fp16:        ", g.to(f16).float().tolist())
S = 2.0 ** 16
print("  scaled x2^16 in fp16, then unscaled in fp32:", (g * S).to(f16).float().div(S).tolist())

print("\n[6] FP8 (E4M3, max 448): relative error of quantize->dequantize, tensor with outliers")
x = torch.randn(1024, 1024)
x[torch.randint(0, 1024, (20,)), torch.randint(0, 1024, (20,))] = 2000.0   # a few large outliers
def q_per_tensor(t):
    s = 448.0 / t.abs().max(); return (t * s).to(torch.float8_e4m3fn).float() / s
def q_per_tile(t, tile=128):                  # DeepSeek-V3 style 1x128 tiles (per row, per 128 columns)
    r = t.view(t.shape[0], -1, tile); s = 448.0 / r.abs().amax(-1, keepdim=True)
    return ((r * s).to(torch.float8_e4m3fn).float() / s).view_as(t)
normal = x.abs() < 100
for name, fn in (("per-tensor scale", q_per_tensor), ("per-1x128-tile scale", q_per_tile)):
    y = fn(x); err = ((y - x)[normal].norm() / x[normal].norm()).item()
    print(f"  {name:22s}: relative error on the ordinary values = {err:.2%}")
print(f"  bf16 for comparison    : {((x.to(bf16).float() - x)[normal].norm() / x[normal].norm()).item():.2%}")
