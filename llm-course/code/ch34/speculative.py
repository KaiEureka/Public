"""Speculative sampling: (1) exactness on a toy distribution, (2) bigram draft + GPT target."""
import sys, torch
torch.set_num_threads(4); torch.manual_seed(0)
g = torch.Generator().manual_seed(0)

def accept_or_resample(p, q, x):
    """Draft proposed x ~ q. Return (accepted?, token) so that the final token is distributed exactly as p."""
    if torch.rand(1, generator=g).item() < min(1.0, (p[x] / q[x]).item()):
        return True, x
    resid = (p - q).clamp(min=0); resid /= resid.sum()          # sample from normalize(max(0, p - q))
    return False, torch.multinomial(resid, 1, generator=g).item()

# (1) exactness check on random 10-symbol distributions
p = torch.rand(10) ** 3; p /= p.sum(); q = torch.rand(10) ** 3; q /= q.sum()
N = 200000; counts = torch.zeros(10); acc = 0
xs = torch.multinomial(q, N, replacement=True, generator=g)
for x in xs.tolist():
    a, t = accept_or_resample(p, q, x); counts[t] += 1; acc += a
print("[1] toy check over", N, "draws")
print("    target p     :", [round(v, 3) for v in p.tolist()])
print("    output freq  :", [round(v, 3) for v in (counts / N).tolist()])
print(f"    acceptance rate {acc/N:.3f}  (theory: sum min(p,q) = {torch.minimum(p, q).sum():.3f})")

# (2) draft = character bigram (counting), target = lesson-6 GPT
L6 = sys.argv[1]
sys.argv = ["gpt.py", sys.argv[2], "0", "128", "128", "4", "4", "32"]
exec(open(f"{L6}/gpt.py").read().split("model = GPT(")[0])
tgt = GPT(V, T, d, L, H); tgt.load_state_dict(torch.load(f"{L6}/gpt_T128.pt")); tgt.eval()
C = torch.ones(V, V); C.index_put_((train[:-1], train[1:]), torch.ones(len(train) - 1), accumulate=True)
draft = C / C.sum(1, keepdim=True)                                  # q(next | prev char)

@torch.no_grad()
def target_probs(ctx):                                              # p for every position of ctx (one call)
    return tgt(ctx[None, -T:])[0].softmax(-1)

@torch.no_grad()
def generate_plain(n):
    ctx = val[:32].clone(); calls = 0
    while len(ctx) < 32 + n:
        p = target_probs(ctx)[-1]; calls += 1
        ctx = torch.cat([ctx, torch.multinomial(p, 1, generator=g)])
    return ctx[32:32 + n], calls

@torch.no_grad()
def generate_spec(n, gamma):
    ctx = val[:32].clone(); calls = proposed = accepted = 0
    while len(ctx) < 32 + n:
        guess, qs = [], []
        last = ctx[-1].item()
        for _ in range(gamma):                                      # cheap draft proposes gamma tokens
            qv = draft[last]; x = torch.multinomial(qv, 1, generator=g).item()
            guess.append(x); qs.append(qv); last = x
        full = torch.cat([ctx, torch.tensor(guess)])
        P = target_probs(full); calls += 1                          # ONE target call scores all of them
        off = P.shape[0] - gamma - 1                                # row of P that predicts guess[0]
        out = []
        for i, x in enumerate(guess):
            proposed += 1
            ok, t = accept_or_resample(P[off + i], qs[i], x)
            out.append(t); accepted += ok
            if not ok: break
        else:
            out.append(torch.multinomial(P[off + gamma], 1, generator=g).item())   # bonus token
        ctx = torch.cat([ctx, torch.tensor(out)])
    return ctx[32:32 + n], calls, accepted / proposed

n = 3000
a, ca = generate_plain(n)
print(f"\n[2] plain sampling: {n} chars with {ca} target calls ({n/ca:.2f} chars per call)")
fa = torch.bincount(a, minlength=V).float() / n
for gamma in (2, 4, 8):
    b, cb, rate = generate_spec(n, gamma)
    fb = torch.bincount(b, minlength=V).float() / n
    print(f"    speculative, gamma={gamma}: {cb} target calls ({n/cb:.2f} chars per call), "
          f"acceptance {rate:.2f}, char-frequency L1 distance to plain {(fa - fb).abs().sum():.3f}")
# noise floor: two independent plain runs
a2, _ = generate_plain(n)
print(f"    (two independent plain runs differ by L1 {(fa - torch.bincount(a2, minlength=V).float()/n).abs().sum():.3f})")
