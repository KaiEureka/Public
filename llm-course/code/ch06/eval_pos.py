import sys, math, types, torch, torch.nn.functional as F
sys.argv = ["gpt.py", sys.argv[1], "0", "128", "128", "4", "4", "32"]
src = open("gpt.py").read().split("model = GPT(")[0]          # reuse the class definitions only
exec(src)
model = GPT(V, T, d, L, H); model.load_state_dict(torch.load("gpt_T128.pt")); model.eval()
pos = torch.linspace(0, len(val) - T - 2, 2048).long()
tot = torch.zeros(T)
with torch.no_grad():
    for i in range(0, len(pos), 128):
        x = torch.stack([val[p:p + T] for p in pos[i:i+128]]); y = torch.stack([val[p+1:p+T+1] for p in pos[i:i+128]])
        tot += F.cross_entropy(model(x).transpose(1, 2), y, reduction="none").sum(0)
per = tot / len(pos)
for a, b in [(1, 1), (2, 3), (4, 7), (8, 15), (16, 31), (32, 63), (64, 128)]:
    print(f"  context {a:3d}-{b:3d} chars: {per[a-1:b].mean():.3f}")
