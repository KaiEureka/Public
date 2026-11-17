import torch
torch.manual_seed(0)
def q_per_tensor(t):
    s = 448.0 / t.abs().max(); return (t * s).to(torch.float8_e4m3fn).float() / s
def q_per_tile(t, tile=128):
    r = t.view(t.shape[0], -1, tile); s = 448.0 / r.abs().amax(-1, keepdim=True)
    return ((r * s).to(torch.float8_e4m3fn).float() / s).view_as(t)
base = torch.randn(1024, 1024)
idx = (torch.randint(0, 1024, (20,)), torch.randint(0, 1024, (20,)))
print("outlier size | per-tensor error | per-1x128-tile error   (relative error on the ordinary values)")
for big in (1e2, 1e3, 1e4, 3e4, 1e5):
    x = base.clone(); x[idx] = big; normal = x.abs() < 50
    e = [((f(x) - x)[normal].norm() / x[normal].norm()).item() for f in (q_per_tensor, q_per_tile)]
    print(f"   {big:8.0e}  |     {e[0]:7.2%}      |     {e[1]:6.2%}")
