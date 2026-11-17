"""Per-dimension mean over tokens (the offset vector shared by all tokens), its size relative to a typical token vector,
and the average cosine similarity between unrelated tokens, at each layer of the ch. 6 GPT. Run from code/ch06."""
import sys, torch, torch.nn.functional as F
sys.argv = ["gpt.py", "../data/shakespeare.txt", "0", "128", "128", "4", "4", "32"]
exec(open("gpt.py").read().split("model = GPT(")[0])
def stats(name, x):
    x = x.reshape(-1, x.shape[-1])                       # (tokens, d)
    mu = x.mean(0)                                        # per-dimension mean over tokens: the shared offset vector
    rms = x.pow(2).mean().sqrt()
    xn = F.normalize(x[torch.randperm(len(x))[:2000]], dim=1)
    cos = (xn @ xn.T).fill_diagonal_(0).sum() / (len(xn) * (len(xn) - 1))
    top = mu.abs().topk(3)
    print(f"{name:<18}{x.mean().item():>9.4f}{(mu.norm() / x.norm(dim=1).mean()).item():>10.2f}{cos.item():>9.2f}"
          f"   最大偏移维度 {top.indices.tolist()} = {[round(v / rms.item(), 1) for v in mu[top.indices].tolist()]} 倍 RMS")
def run(model, title):
    pos = torch.linspace(0, len(val) - T - 2, 64).long(); idx = torch.stack([val[p:p + T] for p in pos])
    print(f"\n== {title} ==\n{'位置':<18}{'总均值':>9}{'偏移向量占比':>10}{'平均余弦':>9}")
    with torch.no_grad():
        x = model.tok(idx) + model.pos(torch.arange(T)); stats("嵌入", x)
        for i, b in enumerate(model.blocks, 1):
            x = x + b.attn(b.ln1(x)); x = x + b.mlp(b.ln2(x)); stats(f"第 {i} 层后残差流", x)
            h = F.gelu(b.mlp[0](b.ln2(x)))
        stats("最后一层 GELU 后", h)
torch.manual_seed(0); run(GPT(V, T, d, L, H), "初始化")
m = GPT(V, T, d, L, H); m.load_state_dict(torch.load("gpt_T128.pt")); run(m, "训练后")
