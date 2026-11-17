import sys
import numpy as np

# [1] soft labels vs hard labels: distill a character bigram "teacher" into a student from M training positions
text = open(sys.argv[1], encoding="utf-8").read()
chars = sorted(set(text)); V = len(chars); stoi = {c: i for i, c in enumerate(chars)}
ids = np.array([stoi[c] for c in text]); n = int(0.9 * len(ids)); tr, va = ids[:n], ids[n:]
C = np.zeros((V, V)); np.add.at(C, (tr[:-1], tr[1:]), 1)
teacher = (C + 1) / (C + 1).sum(1, keepdims=True)                 # the "big model": full bigram
def val_loss(P): return -np.log(P[va[:-1], va[1:]]).mean()
print(f"[1] teacher val loss {val_loss(teacher):.3f}")
print("    M training positions | student on hard labels (sampled next char) | student on soft labels (teacher's full distribution)")
rng = np.random.default_rng(0)
for M in (300, 1000, 3000, 10000):
    pos = rng.integers(0, len(tr) - 1, M)
    a = tr[pos]
    nxt = np.array([rng.choice(V, p=teacher[x]) for x in a])       # what the teacher would actually write
    hard = np.full((V, V), 0.1); np.add.at(hard, (a, nxt), 1)
    soft = np.full((V, V), 0.1); np.add.at(soft, a, teacher[a])    # add the whole probability row
    hard /= hard.sum(1, keepdims=True); soft /= soft.sum(1, keepdims=True)
    print(f"    {M:6d}               |   {val_loss(hard):.3f}                                      |   {val_loss(soft):.3f}")

# [2] forward vs reverse KL: fit ONE Gaussian student to a TWO-peak teacher
x = np.linspace(-8, 8, 4001); dx = x[1] - x[0]
def gauss(m, s): return np.exp(-(x - m) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi))
p = 0.5 * gauss(-2, 0.5) + 0.5 * gauss(2, 0.5)
best = {}
for mu in np.linspace(-3, 3, 121):
    for s in np.linspace(0.2, 3.0, 141):
        q = gauss(mu, s) + 1e-300
        fwd = np.sum(p * np.log((p + 1e-300) / q)) * dx            # KL(teacher || student)
        rev = np.sum(q * np.log(q / (p + 1e-300))) * dx            # KL(student || teacher)
        for k, v in (("forward", fwd), ("reverse", rev)):
            if v < best.get(k, (np.inf,))[0]: best[k] = (v, mu, s)
print("\n[2] teacher = two peaks at -2 and +2 (std 0.5); student = one Gaussian")
for k in ("forward", "reverse"):
    v, mu, s = best[k]
    print(f"    minimize {k} KL: student mean {mu:+.2f}, std {s:.2f}")
