"""Toy GRPO: a policy only chooses how many 'thinking steps' k to use; longer thinking raises the chance
of a correct final answer. Reward = 1 if correct else 0 (outcome-only, no length penalty)."""
import numpy as np
rng = np.random.default_rng(0)
K = np.arange(31)                                       # 0..30 thinking steps
logits = -0.3 * K.astype(float)                         # "base model" rarely thinks long
def p_correct(k, d): return 1 - d * 0.9 ** k            # d = question difficulty in [0.3, 1.0]
G, Q, lr = 8, 32, 1.0
print("iter | mean thinking steps | accuracy | groups with zero signal (all right or all wrong)")
for it in range(1001):
    pi = np.exp(logits - logits.max()); pi /= pi.sum()
    d = rng.uniform(0.3, 1.0, Q)
    k = rng.choice(K, size=(Q, G), p=pi)                         # G samples per question
    r = (rng.random((Q, G)) < p_correct(k, d[:, None])).astype(float)
    std = r.std(1, keepdims=True)
    adv = (r - r.mean(1, keepdims=True)) / (std + 1e-6)          # GRPO: group-relative advantage
    zero = (std[:, 0] == 0).mean()
    grad = np.zeros_like(logits)                                  # policy gradient of sum A * log pi(k)
    for a, kk in zip(adv.ravel(), k.ravel()):
        g = -pi.copy(); g[kk] += 1; grad += a * g
    logits += lr * grad / (Q * G)
    if it in (0, 50, 100, 200, 400, 700, 1000):
        print(f"{it:4d} |        {(pi * K).sum():5.1f}        |  {r.mean():5.1%}  |   {zero:5.1%}")
