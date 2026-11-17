"""SP vs muP (Adam): does the best learning rate move when the hidden width grows?
Model: char-level MLP LM, 8 chars context -> W1 -> tanh -> W2 (H x H) -> tanh -> W_out -> logits."""
import sys, time, math, torch, torch.nn as nn, torch.nn.functional as F
torch.set_num_threads(4)
text = open(sys.argv[1], encoding="utf-8").read()
chars = sorted(set(text)); V = len(chars); stoi = {c: i for i, c in enumerate(chars)}
ids = torch.tensor([stoi[c] for c in text]); n = int(0.9 * len(ids)); tr, va = ids[:n], ids[n:]
K, D, BASE, STEPS, B = 8, 16, 64, 400, 256
vpos = torch.linspace(0, len(va) - K - 1, 20000).long()
vx = torch.stack([va[p:p + K] for p in vpos]); vy = va[vpos + K]

class Net(nn.Module):
    def __init__(self, H, mup):
        super().__init__()
        self.E = nn.Parameter(torch.randn(V, D))
        self.W1 = nn.Parameter(torch.randn(K * D, H) * (5 / 3) / math.sqrt(K * D)); self.b1 = nn.Parameter(torch.zeros(H))
        self.W2 = nn.Parameter(torch.randn(H, H) * (5 / 3) / math.sqrt(H)); self.b2 = nn.Parameter(torch.zeros(H))
        self.Wo = nn.Parameter(torch.randn(H, V) / math.sqrt(H))
        self.out_mult = BASE / H if mup else 1.0          # muP: readout multiplier 1/width
    def forward(self, x):
        h = torch.tanh(self.E[x].flatten(1) @ self.W1 + self.b1)
        h = torch.tanh(h @ self.W2 + self.b2)
        return (h @ self.Wo) * self.out_mult

def run(H, lr, mup, seed=0):
    torch.manual_seed(seed); net = Net(H, mup)
    hidden_lr = lr * BASE / H if mup else lr            # muP: hidden (H x H) matrix lr ~ 1/width
    groups = [{"params": [net.W2], "lr": hidden_lr},
              {"params": [net.E, net.W1, net.b1, net.b2, net.Wo], "lr": lr}]
    for gp in groups: gp["base"] = gp["lr"]
    opt = torch.optim.Adam(groups)
    g = torch.Generator().manual_seed(1)
    for step in range(STEPS):
        for gp in opt.param_groups: gp["lr"] = gp["base"] * min(1.0, (step + 1) / 50)
        pos = torch.randint(0, len(tr) - K - 1, (B,), generator=g)
        x = torch.stack([tr[p:p + K] for p in pos]); y = tr[pos + K]
        loss = F.cross_entropy(net(x), y)
        if not torch.isfinite(loss): return float("nan")
        opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad(): return F.cross_entropy(net(vx), vy).item()

lrs = [2.0 ** e for e in range(-12, -2)]
t0 = time.time()
for mup in (False, True):
    print(("muP" if mup else "SP (standard)") + "   val loss after 400 steps; columns = learning rate 2^-12 ... 2^-3")
    for H in (64, 256, 1024):
        res = [run(H, lr, mup) for lr in lrs]
        best = min(range(len(lrs)), key=lambda i: res[i] if res[i] == res[i] else 9)
        print(f"  H={H:5d}: " + " ".join(f"{r:5.2f}" for r in res) + f"   best lr = 2^{int(math.log2(lrs[best]))}  ({time.time()-t0:.0f}s)", flush=True)
