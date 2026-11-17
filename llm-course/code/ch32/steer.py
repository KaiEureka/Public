"""Steering: add an SAE feature's decoder direction to the layer-2 residual stream while generating."""
import sys, torch, torch.nn.functional as F
torch.set_num_threads(4)
L6 = sys.argv[1]
sys.argv = ["gpt.py", sys.argv[2], "0", "128", "128", "4", "4", "32"]
exec(open(f"{L6}/gpt.py").read().split("model = GPT(")[0])
model = GPT(V, T, d, L, H); model.load_state_dict(torch.load(f"{L6}/gpt_T128.pt")); model.eval()
ck = torch.load("sae.pt"); Wdec = ck["sae"]["dec.weight"]; sd = ck["sd"]
state = {"vec": None}
def hook(m, i, o):
    return o if state["vec"] is None else o + state["vec"]
model.blocks[2].register_forward_hook(hook)

def generate(seed, n=600):
    g = torch.Generator().manual_seed(seed); ctx = val[:T][None].clone(); out = []
    with torch.no_grad():
        for _ in range(n):
            p = (model(ctx[:, -T:])[0, -1] / 0.8).softmax(-1)
            nxt = torch.multinomial(p, 1, generator=g); ctx = torch.cat([ctx, nxt[None]], 1); out.append(chars[nxt.item()])
    return "".join(out)

def stats(s):
    letters = [c for c in s if c.isalpha()]
    return s.count("-"), sum(c.isupper() for c in letters) / max(1, len(letters))

for name, feat, alpha in [("baseline", None, 0), ("feature 148 ('-' dash)", 148, 4.0), ("feature 352 (inside SPEAKER NAME)", 352, 4.0)]:
    state["vec"] = None if feat is None else alpha * sd * Wdec[:, feat]
    dashes, upper = zip(*[stats(generate(s)) for s in range(5)])
    print(f"{name:36s}: dashes per 600 chars = {sum(dashes)/5:5.1f}, uppercase share of letters = {sum(upper)/5:5.1%}")
    if feat is not None: print("   sample:", repr(generate(0)[:160]))
