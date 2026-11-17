"""Re-run code/ch35/mm_toys.py, then sample 1,500 more points from the trained DDPM, keeping snapshots for figure 35.x."""
import json, os, runpy, torch
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
g = runpy.run_path(os.path.join(ROOT, "code", "ch35", "mm_toys.py"))
net, T, beta, alpha, abar = g["net"], g["T"], g["beta"], g["alpha"], g["abar"]
snaps = {}
with torch.no_grad():
    x = torch.randn(1500, 2); snaps[T] = x.clone()
    for t in reversed(range(T)):
        e = net(torch.cat([x, torch.full((1500, 1), t / T)], 1))
        x = (x - beta[t] / (1 - abar[t]).sqrt() * e) / alpha[t].sqrt()
        if t > 0: x = x + beta[t].sqrt() * torch.randn_like(x)
        if t in (60, 30, 10, 0): snaps[t] = x.clone()
out = {str(k): [[round(a, 3), round(b, 3)] for a, b in v.tolist()] for k, v in snaps.items()}
out["data"] = [[round(a, 3), round(b, 3)] for a, b in g["data"](1500).tolist()]
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch35_diffusion.json"), "w"))
print("radius of final samples:", snaps[0].norm(dim=1).mean().item())
