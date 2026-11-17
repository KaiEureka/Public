"""Mean and standard deviation at every point of the ch. 6 GPT (residual stream, LayerNorm outputs, branch outputs),
at initialization and after training. Answers a reader question; run from code/ch06: python3 layer_stats.py"""
import sys, torch
sys.argv = ["gpt.py", "../data/shakespeare.txt", "0", "128", "128", "4", "4", "32"]
exec(open("gpt.py").read().split("model = GPT(")[0])
def report(model, title):
    model.eval()
    pos = torch.linspace(0, len(val) - T - 2, 64).long()
    idx = torch.stack([val[p:p + T] for p in pos])
    rows = []
    def s(name, t): rows.append((name, t.mean().item(), t.std().item(), t.abs().max().item()))
    with torch.no_grad():
        x = model.tok(idx) + model.pos(torch.arange(T)); s("嵌入（残差流起点）", x)
        for i, b in enumerate(model.blocks, 1):
            a_in = b.ln1(x); s(f"L{i} LN1 输出（读的复印件）", a_in)
            a = b.attn(a_in); s(f"L{i} 注意力分支输出（便签）", a)
            x = x + a; s(f"L{i} 残差流（+注意力后）", x)
            m_in = b.ln2(x); s(f"L{i} LN2 输出", m_in)
            m = b.mlp(m_in); s(f"L{i} MLP 分支输出（便签）", m)
            x = x + m; s(f"L{i} 残差流（+MLP 后）", x)
        s("最终 LN 输出", model.ln_f(x))
        s("logits", model.head(model.ln_f(x)))
    print(f"\n== {title} ==\n{'位置':<26}{'均值':>9}{'标准差':>9}{'最大绝对值':>11}")
    for n, mu, sd, mx in rows: print(f"{n:<26}{mu:>9.3f}{sd:>9.3f}{mx:>11.2f}")
torch.manual_seed(0); init = GPT(V, T, d, L, H); report(init, "初始化（未训练）")
tr = GPT(V, T, d, L, H); tr.load_state_dict(torch.load("gpt_T128.pt")); report(tr, "训练 1000 步后（第 6 章的模型）")
