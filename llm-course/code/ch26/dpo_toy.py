"""Tabular DPO / IPO on 8 candidate responses. pi_ref is uniform, beta = 1, so the RLHF optimum is pi* ~ exp(r)."""
import torch, torch.nn.functional as F
torch.manual_seed(0)
K, beta = 8, 1.0
r = torch.linspace(-1.5, 1.5, K)                       # true rewards of the 8 responses
pi_star = torch.softmax(r / beta, 0)
i, j = torch.meshgrid(torch.arange(K), torch.arange(K), indexing="ij")
off = i != j                                            # all ordered pairs (i, j), sampled uniformly from pi_ref
p_bt = torch.sigmoid(r[i] - r[j])                       # Bradley-Terry: P(i preferred over j)
p_det = (r[i] > r[j]).float()                           # deterministic labels: better one always wins

def train(p_label, loss_kind, steps):
    theta = torch.zeros(K, requires_grad=True)          # policy logits; starts equal to pi_ref
    opt = torch.optim.Adam([theta], lr=0.05)
    for _ in range(steps):
        h = beta * (theta[i] - theta[j])                # implicit-reward margin; log pi_ref cancels (uniform)
        if loss_kind == "dpo":
            loss = -(p_label * F.logsigmoid(h))[off].mean()      # expected DPO loss over the preference data
        else:                                                    # IPO: regress the margin to 1/(2*beta)
            loss = (p_label * (theta[i] - theta[j] - 1 / (2 * beta)) ** 2)[off].mean()
        opt.zero_grad(); loss.backward(); opt.step()
    pi = torch.softmax(theta.detach(), 0)
    return pi, (pi * torch.log(pi * K)).sum().item()

kl_star = (pi_star * torch.log(pi_star * K)).sum().item()
print("pi* (closed form)          :", [round(x, 3) for x in pi_star.tolist()], f" KL={kl_star:.2f}")
for name, p, kind, steps in [("DPO, Bradley-Terry labels ", p_bt, "dpo", 3000),
                             ("DPO, deterministic, 1k st ", p_det, "dpo", 1000),
                             ("DPO, deterministic, 10k st", p_det, "dpo", 10000),
                             ("IPO, deterministic, 10k st", p_det, "ipo", 10000)]:
    pi, kl = train(p, kind, steps)
    print(f"{name}:", [round(x, 3) for x in pi.tolist()], f" KL={kl:.2f}")
