"""Induction heads from scratch: attention-only Transformers (1 vs 2 layers) on 'random segment repeated twice'.
The segment length k is random (6..24), so the copy offset cannot be read off the position alone.
Prints the loss on the 2nd copy during training, then which head attends where.  CPU, ~1-2 minutes.
Run inside code/ch32:  python3 induction_toy.py        (add "fine" to log the 2-layer loss every 20 steps for the first 400)"""
import math, sys, torch, torch.nn as nn, torch.nn.functional as F
torch.manual_seed(0); torch.set_num_threads(4)
V, T, d, H, B, STEPS = 32, 64, 64, 2, 64, 3000

def batch():
    x = torch.randint(0, V, (B, T)); m = torch.zeros(B, T, dtype=torch.bool); ks = torch.randint(6, 25, (B,))
    for b, k in enumerate(ks.tolist()):
        x[b, k:2 * k] = x[b, :k]                 # second copy of the segment
        m[b, k:2 * k - 1] = True                 # predict tokens k+1 .. 2k-1 (inputs at k .. 2k-2)
    return x, m, ks

class Attn(nn.Module):
    def __init__(s):
        super().__init__(); s.qkv = nn.Linear(d, 3 * d); s.o = nn.Linear(d, d)
    def forward(s, x):
        n, t, _ = x.shape; q, k, v = (z.view(n, t, H, d // H).transpose(1, 2) for z in s.qkv(x).split(d, 2))
        a = (q @ k.transpose(-1, -2) / math.sqrt(d // H)).masked_fill(torch.triu(torch.ones(t, t, dtype=torch.bool), 1), -1e9).softmax(-1)
        s.att = a.detach(); return s.o((a @ v).transpose(1, 2).reshape(n, t, d))

class Net(nn.Module):                            # attention only: no MLP, no LayerNorm
    def __init__(s, L):
        super().__init__(); s.tok = nn.Embedding(V, d); s.pos = nn.Embedding(T, d)
        s.layers = nn.ModuleList(Attn() for _ in range(L)); s.out = nn.Linear(d, V)
    def forward(s, x):
        h = s.tok(x) + s.pos(torch.arange(x.shape[1]))
        for a in s.layers: h = h + a(h)          # each layer ADDS its output to the residual stream
        return s.out(h)

def run(L, steps=STEPS, every=250):
    net = Net(L); opt = torch.optim.Adam(net.parameters(), 1e-3); curve = []
    for step in range(steps + 1):
        x, m, _ = batch(); logits = net(x[:, :-1])
        loss = F.cross_entropy(logits.transpose(1, 2), x[:, 1:], reduction="none")[m[:, :-1]].mean()
        if step % every == 0: curve.append((step, loss.item()))
        if step < steps: opt.zero_grad(); loss.backward(); opt.step()
    return net, curve

if sys.argv[1:] == ["fine"]:
    _, curve = run(2, 400, 20); print("2-layer, fine: " + "  ".join(f"{s}:{l:.2f}" for s, l in curve)); sys.exit()
print(f"chance level on the 2nd copy = ln {V} = {math.log(V):.2f} nats")
nets = {}
for L in (1, 2):
    nets[L], curve = run(L)
    print(f"{L}-layer: " + "  ".join(f"{s}:{l:.2f}" for s, l in curve))

net = nets[2]; x, m, ks = batch()
with torch.no_grad(): net(x)
for l, a in enumerate(net.layers):
    for h in range(H):
        prev, ind = [], []
        for b, k in enumerate(ks.tolist()):
            i = torch.arange(k, 2 * k - 1)       # query positions inside the 2nd copy
            prev.append(a.att[b, h, i, i - 1].mean()); ind.append(a.att[b, h, i, i - k + 1].mean())
        print(f"2-layer, layer {l} head {h}: attention to previous position {torch.stack(prev).mean():.2f}, "
              f"to 'token after the earlier copy' {torch.stack(ind).mean():.2f}")
