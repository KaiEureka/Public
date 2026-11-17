import numpy as np
from math import comb
rng = np.random.default_rng(0)
R = 100000                                                  # simulated evaluation runs

print("[1] how noisy is a benchmark score?  (model A true accuracy 50%, model B 55%)")
print("    questions | std of A's score | P(A scores >= B on the same benchmark)")
for n in (30, 200, 500, 2000):
    # each question has its own difficulty; both models see the same questions (paired), one sample each
    p_q = rng.beta(2, 2, size=(R, n))                       # per-question solve prob for A, mean 0.5
    pa = p_q; pb = np.clip(p_q + 0.05, 0, 1)
    a = (rng.random((R, n)) < pa).mean(1); b = (rng.random((R, n)) < pb).mean(1)
    print(f"    {n:5d}     |     {a.std()*100:5.1f} pts     |   {np.mean(a >= b):5.1%}")

print("\n[2] AIME-style: 30 questions, average over k independent samples per question")
p_q = rng.beta(2, 2, size=(20000, 30))
for k in (1, 4, 16, 64):
    s = rng.binomial(k, p_q) / k
    print(f"    k={k:3d} samples/question: std of score = {s.mean(1).std()*100:4.1f} pts")

print("\n[3] pass@k: unbiased estimator vs naive plug-in  (n=10 samples, c correct)")
def unbiased(n, c, k): return 1 - comb(n - c, k) / comb(n, k)
for c in (1, 2, 5):
    for k in (1, 5):
        print(f"    c={c}, k={k}: unbiased {unbiased(10, c, k):.3f}   naive 1-(1-c/n)^k {1 - (1 - c/10)**k:.3f}")
# check bias by simulation: true p = 0.2, k = 5
p, n, k = 0.2, 10, 5
cs = rng.binomial(n, p, 200000)
print(f"    simulation, true p=0.2, k=5: true pass@5 = {1-(1-p)**k:.3f}; mean unbiased = "
      f"{np.mean([unbiased(n, c, k) for c in cs]):.3f}; mean naive = {np.mean(1-(1-cs/n)**k):.3f}")
