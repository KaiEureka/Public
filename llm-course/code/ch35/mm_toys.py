import math, time, torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0); torch.set_num_threads(4); t0 = time.time()

# [1] CLIP-style contrastive alignment of two "modalities" that share a hidden cause z
A1, B1 = torch.randn(8, 32), torch.randn(8, 48)
def pairs(n):
    z = torch.randn(n, 8)
    return torch.tanh(z @ A1) + 0.1 * torch.randn(n, 32), F.relu(z @ B1) + 0.1 * torch.randn(n, 48)
enc_a = nn.Sequential(nn.Linear(32, 128), nn.ReLU(), nn.Linear(128, 32))
enc_b = nn.Sequential(nn.Linear(48, 128), nn.ReLU(), nn.Linear(128, 32))
opt = torch.optim.Adam(list(enc_a.parameters()) + list(enc_b.parameters()), lr=1e-3)
xa_te, xb_te = pairs(1000)
def retrieval():
    with torch.no_grad():
        ea, eb = F.normalize(enc_a(xa_te), dim=-1), F.normalize(enc_b(xb_te), dim=-1)
        return ((ea @ eb.T).argmax(1) == torch.arange(1000)).float().mean().item()
print(f"[1] contrastive alignment: retrieval top-1 among 1000 candidates before training = {retrieval():.1%} (chance 0.1%)")
for step in range(2000):
    xa, xb = pairs(256)
    ea, eb = F.normalize(enc_a(xa), dim=-1), F.normalize(enc_b(xb), dim=-1)
    logits = ea @ eb.T / 0.07                                  # 256 x 256 similarity matrix, temperature 0.07
    labels = torch.arange(256)                                 # the matching pair is on the diagonal
    loss = (F.cross_entropy(logits, labels) + F.cross_entropy(logits.T, labels)) / 2   # symmetric InfoNCE
    opt.zero_grad(); loss.backward(); opt.step()
print(f"    after 2000 steps: retrieval top-1 = {retrieval():.1%}   ({time.time()-t0:.0f}s)")

# [2] DDPM on a 2-D toy distribution: points on a circle of radius 1
T = 100
beta = torch.linspace(1e-4, 0.02, T); alpha = 1 - beta; abar = torch.cumprod(alpha, 0)
def data(n):
    th = 2 * math.pi * torch.rand(n); return torch.stack([th.cos(), th.sin()], 1) * (1 + 0.05 * torch.randn(n, 1))
net = nn.Sequential(nn.Linear(3, 256), nn.SiLU(), nn.Linear(256, 256), nn.SiLU(), nn.Linear(256, 2))
opt = torch.optim.Adam(net.parameters(), lr=1e-3)
for step in range(4000):
    x0 = data(512); t = torch.randint(0, T, (512,)); eps = torch.randn_like(x0)
    xt = abar[t].sqrt()[:, None] * x0 + (1 - abar[t]).sqrt()[:, None] * eps     # forward: add noise in one shot
    pred = net(torch.cat([xt, (t.float() / T)[:, None]], 1))
    loss = F.mse_loss(pred, eps)                                                  # learn to predict the noise
    opt.zero_grad(); loss.backward(); opt.step()
@torch.no_grad()
def sample(n):
    x = torch.randn(n, 2)
    for t in reversed(range(T)):                                                  # reverse: denoise step by step
        e = net(torch.cat([x, torch.full((n, 1), t / T)], 1))
        x = (x - beta[t] / (1 - abar[t]).sqrt() * e) / alpha[t].sqrt()
        if t > 0: x = x + beta[t].sqrt() * torch.randn_like(x)
    return x
def describe(x):
    r = x.norm(dim=1); ang = torch.atan2(x[:, 1], x[:, 0])
    quad = torch.histc(ang, bins=4, min=-math.pi, max=math.pi) / len(x)
    return f"radius mean {r.mean():.3f}, std {r.std():.3f}; share per quadrant {[round(q, 2) for q in quad.tolist()]}"
print(f"\n[2] diffusion: data          {describe(data(4000))}")
print(f"    pure Gaussian noise       {describe(torch.randn(4000, 2))}")
print(f"    DDPM samples (100 steps)  {describe(sample(4000))}   ({time.time()-t0:.0f}s)")
