"""A GPT-2-style character-level Transformer, written from scratch in PyTorch (CPU)."""
import math, sys, time
import torch, torch.nn as nn, torch.nn.functional as F

torch.manual_seed(0); torch.set_num_threads(4)
path, STEPS = sys.argv[1], int(sys.argv[2])
T, d, L, H, B = (int(a) for a in sys.argv[3:8])          # context, width, layers, heads, batch

text = open(path, encoding="utf-8").read()
chars = sorted(set(text)); V = len(chars); stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in text]); n = int(0.9 * len(data))
train, val = data[:n], data[n:]

class CausalSelfAttention(nn.Module):
    def __init__(self, d, H):
        super().__init__()
        self.H = H
        self.qkv = nn.Linear(d, 3 * d)       # W_q, W_k, W_v for all heads, fused into one matmul
        self.proj = nn.Linear(d, d)          # W_o
    def forward(self, x):
        Bn, Tn, dn = x.shape
        q, k, v = self.qkv(x).split(dn, dim=2)
        q, k, v = (t.view(Bn, Tn, self.H, dn // self.H).transpose(1, 2) for t in (q, k, v))  # (B, H, T, dh)
        att = q @ k.transpose(-2, -1) / math.sqrt(dn // self.H)                             # (B, H, T, T)
        mask = torch.triu(torch.ones(Tn, Tn, dtype=torch.bool), diagonal=1)                  # j > i is the future
        att = att.masked_fill(mask, float("-inf")).softmax(dim=-1)
        self.last_att = att.detach()
        y = (att @ v).transpose(1, 2).reshape(Bn, Tn, dn)                                    # concat heads
        return self.proj(y)

class Block(nn.Module):
    def __init__(self, d, H):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.attn = CausalSelfAttention(d, H)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
    def forward(self, x):
        x = x + self.attn(self.ln1(x))       # tokens exchange information
        x = x + self.mlp(self.ln2(x))        # each position computes on its own
        return x

class GPT(nn.Module):
    def __init__(self, V, T, d, L, H):
        super().__init__()
        self.tok = nn.Embedding(V, d)
        self.pos = nn.Embedding(T, d)        # learned absolute position embeddings (GPT-2)
        self.blocks = nn.ModuleList(Block(d, H) for _ in range(L))
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, V, bias=False)
        self.head.weight = self.tok.weight   # tied input/output embeddings
        for name, p in self.named_parameters():
            if p.dim() == 2:
                std = 0.02 / math.sqrt(2 * L) if name.endswith(("proj.weight", "mlp.2.weight")) else 0.02
                nn.init.normal_(p, 0.0, std)
            elif name.endswith("bias"):
                nn.init.zeros_(p)
    def forward(self, idx):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1]))
        for blk in self.blocks:
            x = blk(x)
        return self.head(self.ln_f(x))       # logits at every position: (B, T, V)

model = GPT(V, T, d, L, H)
print(f"params = {sum(p.numel() for p in model.parameters()):,}  (T={T} d={d} L={L} H={H} B={B})")

decay = [p for p in model.parameters() if p.dim() == 2]
no_decay = [p for p in model.parameters() if p.dim() < 2]
opt = torch.optim.AdamW([{"params": decay, "weight_decay": 0.1}, {"params": no_decay, "weight_decay": 0.0}],
                        lr=1e-3, betas=(0.9, 0.99))
def lr_at(step, peak=1e-3, warmup=100):
    if step < warmup: return peak * (step + 1) / warmup
    return peak * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * (step - warmup) / (STEPS - warmup))))

g = torch.Generator().manual_seed(1)
def batch(split, pos=None):
    src = train if split == "train" else val
    if pos is None: pos = torch.randint(0, len(src) - T - 1, (B,), generator=g)
    x = torch.stack([src[p:p + T] for p in pos]); y = torch.stack([src[p + 1:p + T + 1] for p in pos])
    return x, y

eval_pos = torch.linspace(0, len(val) - T - 2, 256).long()     # fixed validation windows
@torch.no_grad()
def evaluate():
    model.eval(); losses = []
    for i in range(0, len(eval_pos), 64):
        x, y = batch("val", eval_pos[i:i + 64])
        losses.append(F.cross_entropy(model(x).transpose(1, 2), y, reduction="none"))  # (b, T)
    model.train(); per_pos = torch.cat(losses).mean(0)
    return per_pos.mean().item(), per_pos

x, y = batch("train")
print(f"initial loss {F.cross_entropy(model(x).reshape(-1, V), y.reshape(-1)).item():.4f}  (ln V = {math.log(V):.4f})")
t0 = time.time()
for step in range(STEPS):
    for gr in opt.param_groups: gr["lr"] = lr_at(step)
    x, y = batch("train")
    loss = F.cross_entropy(model(x).reshape(-1, V), y.reshape(-1))
    opt.zero_grad(set_to_none=True); loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    if (step + 1) in (100, 500) or (step + 1) % 1000 == 0 or step + 1 == STEPS:
        vl, _ = evaluate()
        print(f"step {step+1:5d}  train(batch) {loss.item():.4f}  val {vl:.4f}  ({time.time()-t0:.0f}s)", flush=True)

vl, per_pos = evaluate()
print("\nval loss by position in the window (how many chars of context the prediction had):")
for p in (1, 2, 4, 8, 16, 32, 64, 128, 256):
    if p <= T: print(f"  {p:4d} chars of context: {per_pos[p-1]:.3f}")
if T > 8: print(f"  average over positions with >= 8 chars of context: {per_pos[7:].mean():.3f}")
torch.save(model.state_dict(), f"gpt_T{T}.pt")

# what do the heads look at? average attention distance per head on validation text
x, _ = batch("val", eval_pos[:64]); model(x)
idx = torch.arange(T)
dist = (idx[:, None] - idx[None, :]).clamp(min=0).float()
print("\naverage distance (in chars) each head looks back, per layer:")
for l, blk in enumerate(model.blocks):
    a = blk.attn.last_att                                     # (b, H, T, T)
    md = (a * dist).sum(-1)[:, :, 32:].mean((0, 2))           # positions with >= 32 chars of context
    print(f"  layer {l}: " + "  ".join(f"{v:5.1f}" for v in md.tolist()))

# one concrete example: the most-attended earlier characters for the last position
snippet = val[2000:2000 + T]
model(snippet[None]); s = "".join(chars[i] for i in snippet.tolist())
print(f"\nexample context (last 60 chars): {s[-60:]!r}")
for l, blk in enumerate(model.blocks):
    for h in range(H):
        w = blk.attn.last_att[0, h, -1]; top = torch.topk(w, 3).indices.tolist()
        desc = ", ".join(f"{s[j]!r}@-{T-1-j} ({w[j]:.2f})" for j in top)
        print(f"  L{l}H{h}: {desc}")

ctx = val[:T][None]; out = []
with torch.no_grad():
    for _ in range(400):
        logits = model(ctx[:, -T:])[0, -1] / 0.8
        nxt = torch.multinomial(logits.softmax(-1), 1, generator=g)
        ctx = torch.cat([ctx, nxt[None]], 1); out.append(chars[nxt.item()])
print("\nsample (temperature 0.8):\n" + "".join(out))
