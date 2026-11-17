"""Train a sparse autoencoder on the residual stream of the lesson-6 char-level GPT (layer 2 output)."""
import sys, math, time, torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0); torch.set_num_threads(4)
L6 = sys.argv[1]
LAM = sys.argv[3] if len(sys.argv) > 3 else "3e-3"
sys.argv = ["gpt.py", sys.argv[2], "0", "128", "128", "4", "4", "32"]
exec(open(f"{L6}/gpt.py").read().split("model = GPT(")[0])          # class definitions + data
model = GPT(V, T, d, L, H); model.load_state_dict(torch.load(f"{L6}/gpt_T128.pt")); model.eval()
LAYER = 2
acts = {}
model.blocks[LAYER].register_forward_hook(lambda m, i, o: acts.__setitem__("x", o.detach()))

t0 = time.time()
pos = torch.arange(0, len(train) - T - 1, T)[:1600]                   # 1,600 windows x 128 chars ~ 205k tokens
X, CTX = [], []
with torch.no_grad():
    for k in range(0, len(pos), 100):
        x = torch.stack([train[p:p + T] for p in pos[k:k + 100]])
        model(x); X.append(acts["x"].reshape(-1, d)); CTX.append(x)
X = torch.cat(X); CTX = torch.cat(CTX)                                 # (N, d) activations, (n_win, T) chars
mu, sd = X.mean(0), X.std()
Xn = (X - mu) / sd
print(f"collected {len(X):,} activation vectors of dim {d} ({time.time()-t0:.0f}s)")

class SAE(nn.Module):
    def __init__(self, d, m):
        super().__init__()
        self.enc = nn.Linear(d, m); self.dec = nn.Linear(m, d, bias=False)
        with torch.no_grad():
            self.dec.weight.copy_(F.normalize(torch.randn(d, m), dim=0)); self.enc.weight.copy_(self.dec.weight.T)
            self.enc.bias.zero_()
    def forward(self, x):
        f = F.relu(self.enc(x)); return self.dec(f), f

M, lam = 1024, float(LAM)
sae = SAE(d, M); opt = torch.optim.Adam(sae.parameters(), lr=1e-3)
for step in range(3001):
    xb = Xn[torch.randint(0, len(Xn), (4096,))]
    xh, f = sae(xb)
    loss = (xh - xb).pow(2).sum(-1).mean() + lam * f.abs().sum(-1).mean() * d
    opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad(): sae.dec.weight.copy_(F.normalize(sae.dec.weight, dim=0))   # unit-norm dictionary
with torch.no_grad():
    xh, f = sae(Xn)
    fve = 1 - (xh - Xn).pow(2).sum() / (Xn - Xn.mean(0)).pow(2).sum()
    l0 = (f > 0).float().sum(-1).mean(); freq = (f > 0).float().mean(0)
print(f"SAE: {M} features | variance explained {fve:.1%} | avg active features per token (L0) {l0:.1f} | "
      f"dead features {(freq == 0).sum().item()} | ({time.time()-t0:.0f}s)")
torch.save({"sae": sae.state_dict(), "mu": mu, "sd": sd}, "sae.pt")

flat = CTX.reshape(-1)
def context(idx, width=24):
    w, t = divmod(idx, T); s = "".join(chars[c] for c in CTX[w, max(0, t - width):t + 1].tolist())
    return s.replace("\n", "⏎")
cand = [i for i in range(M) if 0.002 < freq[i] < 0.05]
cand = sorted(cand, key=lambda i: -f[:, i].max().item())[:20]
for i in cand:
    top = torch.topk(f[:, i], 6).indices.tolist()
    print(f"\nfeature {i:4d} (active on {freq[i]:.2%} of tokens):")
    for j in top: print(f"   {f[j, i]:5.2f}  …{context(j)!r}")
