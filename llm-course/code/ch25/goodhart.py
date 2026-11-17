"""Reward over-optimization toy: the KL-regularized optimal policy pi_beta(y) ~ pi_ref(y) exp(r_proxy(y)/beta)."""
import numpy as np
rng = np.random.default_rng(0)
N = 10000
true = rng.standard_normal(N)                       # true quality of each candidate response
err = rng.normal(0, 0.3, N)                         # ordinary reward-model noise
hack = rng.random(N) < 0.01                         # 1% "exploit" responses (e.g. padded, flattering)
err[hack] += 3.0                                    # the RM badly over-scores them ...
true[hack] -= 1.0                                   # ... though they are actually worse
proxy = true + err
ref = np.full(N, 1 / N)                             # reference (SFT) policy: uniform over candidates
print("  beta   KL(pi||ref)   E[proxy reward]   E[true reward]   share of exploit responses")
for beta in (10, 2, 1, 0.5, 0.3, 0.2, 0.1, 0.05, 0.02):
    logits = np.log(ref) + proxy / beta
    pi = np.exp(logits - logits.max()); pi /= pi.sum()
    kl = (pi * np.log(pi / ref + 1e-300)).sum()
    print(f"  {beta:5.2f}   {kl:8.2f}       {pi @ proxy:8.3f}         {pi @ true:8.3f}            {pi[hack].sum():6.1%}")
