"""Per-character loss (bits) of the trained ch06 GPT on the validation set: how unevenly information is spread.
Run inside code/ch06:  python3 token_loss.py"""
import sys, math, torch, torch.nn.functional as F
sys.argv = ["gpt.py", "../data/shakespeare.txt", "0", "128", "128", "4", "4", "32"]
exec(open("gpt.py").read().split("model = GPT(")[0])
model = GPT(V, T, d, L, H); model.load_state_dict(torch.load("gpt_T128.pt")); model.eval()
itos = {i: c for c, i in stoi.items()}
losses, tgts, ctxs = [], [], []
with torch.no_grad():
    starts = list(range(0, len(val) - T - 1, 64))
    for i in range(0, len(starts), 256):
        ps = starts[i:i+256]
        x = torch.stack([val[p:p+T] for p in ps]); y = torch.stack([val[p+1:p+T+1] for p in ps])
        l = F.cross_entropy(model(x).transpose(1, 2), y, reduction="none")[:, 64:] / math.log(2)
        losses.append(l.reshape(-1)); tgts.append(y[:, 64:].reshape(-1))
        ctxs.append(x[:, 64:].reshape(-1))   # previous char
loss = torch.cat(losses); tgt = torch.cat(tgts); prev = torch.cat(ctxs)
n = len(loss); s = loss.sort(descending=True).values
print(f"chars={n}  mean={loss.mean():.3f} bits  median={loss.median():.3f}")
for th in [0.1, 0.5, 1, 3, 6]:
    print(f"  share of chars with loss < {th} bits: {(loss < th).float().mean():.1%}")
for q in [0.05, 0.1, 0.2, 0.5]:
    k = int(q * n); print(f"  top {q:.0%} hardest chars carry {s[:k].sum()/s.sum():.1%} of total loss")
sp = stoi[" "]; nl = stoi["\n"]
isalpha = torch.tensor([itos[int(t)].isalpha() for t in tgt]); prevalpha = torch.tensor([itos[int(t)].isalpha() for t in prev])
groups = {
 "word-initial letter (after space/newline)": isalpha & ((prev == sp) | (prev == nl)),
 "letter inside a word": isalpha & prevalpha,
 "space": tgt == sp,
 "newline": tgt == nl,
}
for k, m in groups.items():
    print(f"  {k:45s} n={int(m.sum()):6d}  mean={loss[m].mean():.2f} bits")
# example line with per-char bits
p = starts[40] ; x = val[p:p+T].unsqueeze(0); y = val[p+1:p+T+1]
with torch.no_grad(): l = F.cross_entropy(model(x)[0], y, reduction="none") / math.log(2)
seg = range(64, 128)
print("".join(itos[int(y[j])] for j in seg).replace("\n", "⏎"))
for j in seg: print(repr(itos[int(y[j])]), f"{l[j]:.2f}", end=" | ")
print()
