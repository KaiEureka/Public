"""Weight-only round-to-nearest quantization of the lesson-6 GPT's linear layers; effect on validation loss."""
import sys, copy, torch, torch.nn.functional as F
torch.set_num_threads(4)
L6 = sys.argv[1]
sys.argv = ["gpt.py", sys.argv[2], "0", "128", "128", "4", "4", "32"]
exec(open(f"{L6}/gpt.py").read().split("model = GPT(")[0])
base = GPT(V, T, d, L, H); base.load_state_dict(torch.load(f"{L6}/gpt_T128.pt")); base.eval()
pos = torch.linspace(0, len(val) - T - 2, 512).long()
@torch.no_grad()
def val_loss(m):
    x = torch.stack([val[p:p + T] for p in pos]); y = torch.stack([val[p + 1:p + T + 1] for p in pos])
    return F.cross_entropy(m(x).reshape(-1, V), y.reshape(-1)).item()

def quantize(w, bits, group=None):           # w: (out, in); symmetric, one scale per output row (or per group of inputs)
    qmax = 2 ** (bits - 1) - 1
    W = w if group is None else w.reshape(w.shape[0], -1, group)
    scale = W.abs().amax(-1, keepdim=True) / qmax
    Wq = (W / scale).round().clamp(-qmax - 1, qmax) * scale
    return Wq.reshape(w.shape)

print(f"FP32 baseline                       val loss {val_loss(base):.4f}")
for bits, group in [(8, None), (4, None), (4, 32), (3, None), (3, 32)]:
    m = copy.deepcopy(base)
    with torch.no_grad():
        for blk in m.blocks:
            for lin in (blk.attn.qkv, blk.attn.proj, blk.mlp[0], blk.mlp[2]):
                lin.weight.copy_(quantize(lin.weight, bits, group))
    tag = "per output channel" if group is None else f"groups of {group} inputs"
    print(f"INT{bits} weights, {tag:20s}   val loss {val_loss(m):.4f}")
